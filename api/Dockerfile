# base image  
FROM python:3.8   

# setup environment variable for work directory  
ENV API_HOME=/home/app/webapp  

# make work directory  
RUN mkdir -p $API_HOME  

# set work directory  
WORKDIR $API_HOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# copy api directory to docker's work directory. 
COPY . $API_HOME  

# install dependencies  
RUN pip install --upgrade pip && pip install -r requirements.txt

# make migrations
RUN python manage.py makemigrations && python manage.py migrate

# port where the Django app runs  
EXPOSE 8000  

# start server  
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]

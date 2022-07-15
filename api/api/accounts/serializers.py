from rest_framework import serializers

from .models import Faculty, Staff, Student, User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['roll_no', 'batch', 'department', 'hostel_address', 'bio']


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['title', 'department', 'designation']


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['department', 'designation']


class UserSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False, allow_null=True, required=False)
    faculty = FacultySerializer(many=False, allow_null=True, required=False)
    staff = StaffSerializer(many=False, allow_null=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'gender',
                  'contact_no', 'user_type', 'picture_url', 'student', 'faculty', 'staff']

    def create(self, validated_data):
        student_data = validated_data.pop('student', None)
        faculty_data = validated_data.pop('faculty', None)
        staff_data = validated_data.pop('staff', None)

        user = User.objects.create(**validated_data)

        if student_data:
            Student.objects.create(user=user, **student_data)
        elif faculty_data:
            Faculty.objects.create(user=user, **faculty_data)
        elif staff_data:
            Staff.objects.create(user=user, **staff_data)

        return user

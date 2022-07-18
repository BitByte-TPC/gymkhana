from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import Faculty, Staff, Student

User = get_user_model()


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
    student = StudentSerializer(many=False, allow_null=True, required=False, read_only=False)
    faculty = FacultySerializer(many=False, allow_null=True, required=False, read_only=False)
    staff = StaffSerializer(many=False, allow_null=True, required=False, read_only=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'gender',
                  'contact_no', 'user_type', 'picture_url', 'student', 'faculty', 'staff']
        extra_kwargs = {'email': {'required': False}}

    def create(self, validated_data):
        student_data = validated_data.pop('student', None)
        faculty_data = validated_data.pop('faculty', None)
        staff_data = validated_data.pop('staff', None)

        # check for email
        if not validated_data.get('email'):
            raise serializers.ValidationError('Email field is required.')

        user = User.objects.create(**validated_data)
        user_type = user.user_type

        # Match data provided to user_type
        if user_type == 'Student' and student_data:
            Student.objects.create(user=user, **student_data)
        elif user_type == 'Faculty' and faculty_data:
            Faculty.objects.create(user=user, **faculty_data)
        elif user_type == 'Staff' and staff_data:
            Staff.objects.create(user=user, **staff_data)
        return user

    def update(self, instance, validated_data):
        # get new user_type data or set them to None
        student_data = validated_data.pop('student', None)
        faculty_data = validated_data.pop('faculty', None)
        staff_data = validated_data.pop('staff', None)

        self._update_base_user(instance, validated_data)

        # try to get user_type instances or set them to None
        try:
            student = instance.student
        except ObjectDoesNotExist:
            student = None

        try:
            faculty = instance.faculty
        except ObjectDoesNotExist:
            faculty = None

        try:
            staff = instance.staff
        except ObjectDoesNotExist:
            staff = None

        user_type = instance.user_type

        # create or update user type only if user_type and data match else ignore it
        if user_type == 'Student':
            if student and student_data:
                self._update_student(student, student_data)
            elif student_data:
                Student.objects.create(user=instance, **student_data)
        elif user_type == 'Faculty':
            if faculty and faculty_data:
                self._update_faculty(faculty, faculty_data)
            elif faculty_data:
                Faculty.objects.create(user=instance, **faculty_data)
        elif user_type == 'Staff':
            if staff and staff_data:
                self._update_staff(staff, staff_data)
            elif staff_data:
                Staff.objects.create(user=instance, **staff_data)

        return instance

    def _update_base_user(self, instance, validated_data):
        updatable_fields = ['first_name', 'last_name',
                            'gender', 'contact_no', 'picture_url']

        admin_only_editable_fields = ['email', 'user_type']

        request_user = self.context['request'].user

        if request_user.is_staff:
            updatable_fields += admin_only_editable_fields

        self._update_instance(instance, validated_data, updatable_fields)

    def _update_student(self, instance, validated_data):
        updatable_fields = ['hostel_address', 'bio']
        admin_only_editable_fields = ['roll_no', 'batch', 'department']

        request_user = self.context['request'].user

        if request_user.is_staff:
            updatable_fields += admin_only_editable_fields

        self._update_instance(instance, validated_data, updatable_fields)

    def _update_faculty(self, instance, validated_data):
        updatable_fields = ['title', 'department', 'designation']

        self._update_instance(instance, validated_data, updatable_fields)

    def _update_staff(self, instance, validated_data):
        updatable_fields = ['department', 'designation']

        self._update_instance(instance, validated_data, updatable_fields)

    def _update_instance(self, instance, validated_data, updatable_fields):

        for field in updatable_fields:
            field_stored_value = getattr(instance, field)
            field_new_value = validated_data.get(field, field_stored_value)
            setattr(instance, field, field_new_value)

        instance.save()

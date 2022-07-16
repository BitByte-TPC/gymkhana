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
        if not validated_data.get('email', None):
            raise serializers.ValidationError('Email field is required.')

        user = User.objects.create(**validated_data)
        user_type = user.user_type

        # create user type if user_type and data match else throw error
        if student_data:
            if user_type == 'Student':
                Student.objects.create(user=user, **student_data)
            else:
                raise serializers.ValidationError('Provided data doesn\'t match with user_type')
        elif faculty_data:
            if user_type == 'Faculty':
                Faculty.objects.create(user=user, **faculty_data)
            else:
                raise serializers.ValidationError('Provided data doesn\'t match with user_type')
        elif staff_data:
            if user_type == 'Staff':
                Staff.objects.create(user=user, **staff_data)
            else:
                raise serializers.ValidationError('Provided data doesn\'t match with user_type')
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

    # create or update user_type data based on instances
    # throw exception if data doesn't match with user type
        if user_type == 'Student':
            if student and student_data:
                self._update_student(student, student_data)
            elif student_data:
                Student.objects.create(user=instance, **student_data)
            elif staff_data or faculty_data:
                raise serializers.ValidationError('Provided data doesn\'t match with user type')
        elif user_type == 'Faculty':
            if faculty and faculty_data:
                self._update_faculty(faculty, faculty_data)
            elif faculty_data:
                Faculty.objects.create(user=instance, **faculty_data)
            elif staff_data or student_data:
                raise serializers.ValidationError('Provided data doesn\'t match with user type')
        elif user_type == 'Staff':
            if staff and staff_data:
                self._update_staff(staff, staff_data)
            elif staff_data:
                Staff.objects.create(user=instance, **staff_data)
            elif student_data or faculty_data:
                raise serializers.ValidationError('Provided data doesn\'t match with user type')

        return instance

    def _update_base_user(self, instance, validated_data):
        updatable_fields = ['first_name', 'last_name',
                            'gender', 'contact_no', 'picture_url']

        admin_only_editable_fields = ['email', 'user_type']

        updatable_fields = self._validate_permission_and_get_updatable_fields(
            instance,
            validated_data,
            updatable_fields,
            admin_only_editable_fields)

        self._update_instance(instance, validated_data, updatable_fields)

    def _update_student(self, instance, validated_data):
        updatable_fields = ['hostel_address', 'bio']
        admin_only_editable_fields = ['roll_no', 'batch', 'department']

        updatable_fields = self._validate_permission_and_get_updatable_fields(
            instance,
            validated_data,
            updatable_fields,
            admin_only_editable_fields)

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

    def _validate_permission_and_get_updatable_fields(self,
                                                      instance,
                                                      validated_data,
                                                      updatable_fields,
                                                      admin_only_editable_fields
                                                      ):
        request_user = self.context['request'].user

        if not request_user.is_staff:
            for field in admin_only_editable_fields:
                field_stored_value = getattr(instance, field)
                field_new_value = validated_data.get(field, None)

                if field_new_value and field_stored_value != field_new_value:
                    raise serializers.ValidationError(f'{field} field is not editable')
        else:
            updatable_fields += admin_only_editable_fields

        return updatable_fields

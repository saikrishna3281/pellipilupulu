# ['manage.py', 'inspectdb']
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


class Complexion(models.Model):
    complexion = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'complexion'


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.SmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         db_table = 'django_session'


class Gender(models.Model):
    gender = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'gender'


class Gothram(models.Model):
    gothram = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'gothram'


class Height(models.Model):
    height = models.CharField(unique=True, max_length=10)

    class Meta:
        db_table = 'height'


class IsPc(models.Model):
    is_pc = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'is_pc'


class MaritalStatus(models.Model):
    marital_status = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'marital_status'


class MatrimonyProfile(models.Model):
    reg_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    sect = models.IntegerField(blank=True, null=True)
    native_place = models.CharField(max_length=50, blank=True, null=True)
    gothram = models.IntegerField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=50, blank=True, null=True)
    time_of_birth = models.TimeField(blank=True, null=True)
    complexion = models.IntegerField(blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    sub_sect = models.IntegerField(blank=True, null=True)
    zodiac = models.IntegerField(blank=True, null=True)
    star = models.IntegerField(blank=True, null=True)
    padam = models.IntegerField(blank=True, null=True)
    qualification = models.CharField(max_length=50, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    fathers_name = models.CharField(max_length=50, blank=True, null=True)
    fathers_contact = models.CharField(max_length=50, blank=True, null=True)
    fathers_email = models.CharField(max_length=50, blank=True, null=True)
    num_brothers = models.IntegerField(blank=True, null=True)
    num_brothers_married = models.IntegerField(blank=True, null=True)
    num_brothers_unmarried = models.IntegerField(blank=True, null=True)
    num_sisters = models.IntegerField(blank=True, null=True)
    num_sisters_married = models.IntegerField(blank=True, null=True)
    num_sisters_unmarried = models.IntegerField(blank=True, null=True)
    designation = models.CharField(max_length=30, blank=True, null=True)
    org_name = models.CharField(max_length=30, blank=True, null=True)
    located_at = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    salary = models.BigIntegerField(blank=True, null=True)
    sect_bar = models.IntegerField(blank=True, null=True)
    sub_sect_bar = models.IntegerField(blank=True, null=True)
    minimum_age_gap = models.IntegerField(blank=True, null=True)
    maximum_age_gap = models.IntegerField(blank=True, null=True)
    minimum_height = models.IntegerField(blank=True, null=True)
    maximum_height = models.IntegerField(blank=True, null=True)
    job_requirement = models.IntegerField(blank=True, null=True)
    qualification_requirement = models.CharField(max_length=30, blank=True, null=True)
    is_pc = models.IntegerField(blank=True, null=True)
    pcdetails = models.CharField(max_length=500, blank=True, null=True)
    is_married = models.IntegerField(blank=True, null=True)
    num_kids = models.IntegerField(blank=True, null=True)
    candidate_mobile = models.CharField(max_length=20, blank=True, null=True)
    candidate_email = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'matrimony_profile'


class NumKids(models.Model):
    num_kids = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'num_kids'


class Padam(models.Model):
    padam = models.IntegerField(unique=True)

    class Meta:
        db_table = 'padam'


class RequirementBar(models.Model):
    requirement_bar = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'requirement_bar'


class Sect(models.Model):
    sect = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'sect'


class Star(models.Model):
    star = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'star'


class SubSect(models.Model):
    sub_sect = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'sub_sect'


class TestOrmTestTable(models.Model):
    col = models.CharField(max_length=30)
    col1 = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'test_orm_test_table'


class UserProfile(models.Model):
    reg_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    sector = models.CharField(max_length=50)
    native_place = models.CharField(max_length=50)
    gothram = models.CharField(max_length=50)
    dob = models.DateField()
    place_of_birth = models.CharField(max_length=50)
    time_of_birth = models.TimeField()
    complexion = models.IntegerField()
    surname = models.CharField(max_length=50)
    subsector = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    star = models.IntegerField()
    padam = models.IntegerField()
    qualification = models.CharField(max_length=50)
    gender = models.IntegerField()
    height = models.IntegerField()

    class Meta:
        db_table = 'user_profile'


class Users(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    mobile = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    last_updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_paid = models.BooleanField(blank=True, null=True)
    is_mobile_verified = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'users'


class Zodiac(models.Model):
    zodiac = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'zodiac'

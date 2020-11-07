import re
import os
import pyotp
import datetime
import requests
from django.forms import ValidationError
from django import forms
from .models_other import choices_attr, DBMatrimony
from .models import Users, MatrimonyProfile
from django.forms.models import model_to_dict
from django.forms.widgets import FileInput

VALID_IMAGE_EXTENSIONS = [
    "jpg",
    "jpeg",
    "png",
    "gif",
]

def validate_email(value):
    # Make a regular expression 
    # for validating an Email 
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if not re.search(regex, value):
        raise forms.ValidationError("Invalid email format")

class ProfilePicForm(forms.Form):
    profile_pic = forms.ImageField()
    reg_id = forms.IntegerField(label='reg_id' , required= False, widget=forms.NumberInput(attrs={'class':'form-control'}))

class UpdatePassword(forms.Form):
    password = forms.CharField(label='Current Password', widget=forms.PasswordInput(attrs={'placeholder': ' Current Password...', 'class':'form-control'}), max_length=30)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'placeholder': ' New Password...', 'class':'form-control'}), max_length=30)
    confirm_new_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password...', 'class':'form-control'}), max_length=30)

    def clean(self):
        cd = self.cleaned_data

        current_password_given = cd.get("password")
        password1 = cd.get("new_password")
        password2 = cd.get("confirm_new_password")

        if len(password1) < 6:
            self.add_error('new_password', "Password should be atleast 6 Characters")
            return cd

        if password1 != password2:
            self.add_error('confirm_new_password', "Password does not match")
            return cd

        with DBMatrimony() as db_matrimony:
            internal_user_id = self.initial['id']
            current_password = db_matrimony.get_user_password(internal_user_id)
            if current_password_given != current_password :
                self.add_error('password', "Incorrect Current Password!!")

        return cd

    def save(self):
        user_id = self.initial['id']
        new_password = self.cleaned_data.get("new_password")
        with DBMatrimony() as db_matrimony:
            return db_matrimony.update_user_password(user_id, new_password)


class Requirements(forms.Form):
    sect_bar = forms.ChoiceField(label='Sect' , required= False, choices=choices_attr['REQUIREMENT_BAR'], widget=forms.Select(attrs={'class':'form-control'}))
    minimum_age_gap = forms.IntegerField(label='Minimum Age Gap' , required= False, widget=forms.NumberInput(attrs={'class':'form-control', 'min':'0', 'max':'15'}))
    minimum_height = forms.ChoiceField(label='Minimum Height' , required= False, choices=choices_attr['HEIGHT'], widget=forms.Select(attrs={'class':'form-control'}))

    # sub_sect = forms.ChoiceField(label='Sub_Sect', choices=COLOR_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    sub_sect_bar = forms.ChoiceField(label='Sub_Sect' , required= False, choices=choices_attr['REQUIREMENT_BAR'], widget=forms.Select(attrs={'class':'form-control'}))
    maximum_age_gap = forms.IntegerField(label='Maximum Age Gap' , required= False, widget=forms.NumberInput(attrs={'class':'form-control', 'min':'1', 'max':'15'}))
    maximum_height = forms.ChoiceField(label='Maximum Height' , required= False, choices=choices_attr['HEIGHT'], widget=forms.Select(attrs={'class':'form-control'}))

    job_requirement = forms.ChoiceField(label='Job Requirement' , required= False, choices=choices_attr['REQUIREMENT_BAR'], widget=forms.Select(attrs={'class':'form-control'}))
    qualification_requirement = forms.CharField(label='Qualification Requirement' , required= False, widget=forms.TextInput(attrs={'class':'form-control'}), max_length=30)


class PersonalDetails(forms.Form):
    is_pc = forms.ChoiceField(label='Is He/She is Physically Challenged:' , required= False, choices=choices_attr['IS_PC'], widget=forms.Select(attrs={'class':'form-control'}))
    #pcdetails = forms.CharField(label = 'If Yes - Give Details:' , required= False, widget=forms.Textarea(attrs={'class':'form-control'} ))
    is_married = forms.ChoiceField(label='Marital Status' , required= False, choices=choices_attr['MARITAL_STATUS'], widget=forms.Select(attrs={'class':'form-control'}))
    num_kids = forms.ChoiceField(label='In case of Divorcee/ Widow/ Widower, Furnish the Details of Children:' , required= False, choices=choices_attr['NUM_KIDS'], widget=forms.Select(attrs={'class':'form-control'}))


class FamilyBackground(forms.Form):
    fathers_name = forms.CharField(label='Father\'s name', required= False, widget=forms.TextInput(attrs={'class':'form-control'}), max_length=30)
    num_brothers = forms.IntegerField(label='No. of brothers', required= False, widget=forms.NumberInput(attrs={'class':'form-control'}))
    num_sisters = forms.IntegerField(label='No. of sisters', required= False, widget=forms.NumberInput(attrs={'class':'form-control'}))

    fathers_contact = forms.IntegerField(label='Father\'s contact', required= False, widget=forms.NumberInput(attrs={'class':'form-control'}))
    num_brothers_married = forms.IntegerField(label='No. of Brothers Married', required= False, widget=forms.NumberInput(attrs={'class':'form-control'}))
    num_sisters_married = forms.IntegerField(label='No. of Sisters Married', required= False, widget=forms.NumberInput(attrs={'class':'form-control'}))

    fathers_email = forms.CharField(label='Father\'s Email' , required= False, widget=forms.TextInput(attrs={'class':'form-control'}))


class JobDetails(forms.Form):
    is_nri = forms.ChoiceField(label='Is NRI' , required= True, choices=choices_attr['IS_NRI'], widget=forms.Select(attrs={'class':'form-control'}))
    designation = forms.CharField(label='Designation' , required= False, widget=forms.TextInput(attrs={'class':'form-control'}), max_length=30)
    occupation = forms.ChoiceField(label='Occupation' , required= True, choices=choices_attr['OCCUPATION'], widget=forms.Select(attrs={'class':'form-control'}))
    org_name = forms.CharField(label='Organization\'s name' , required= False, widget=forms.TextInput(attrs={'class':'form-control'}), max_length=30)
    located_at = forms.CharField(label='Located at' , required= False, widget=forms.TextInput(attrs={'class':'form-control'}), max_length=30)
    state = forms.CharField(label='State' , required= False, widget=forms.TextInput(attrs={'class':'form-control'}), max_length=30)
    country = forms.CharField(label='Country' , required= False, widget=forms.TextInput(attrs={'class':'form-control'}), max_length=30)
    salary = forms.IntegerField(label='Salary (In rupees per annum)' , required= False, widget=forms.NumberInput(attrs={'class':'form-control'}))


class MatrimonyRegistration(forms.Form):
    name = forms.CharField(label='Name' , required= True, widget=forms.TextInput(attrs={'class':'form-control'}), max_length=30)
    sect = forms.ChoiceField(label='Sect' , required= True, choices=choices_attr['SECT'], widget=forms.Select(attrs={'class':'form-control'}))
    native_place = forms.CharField(label='Native place', required= True, widget=forms.TextInput(attrs={'class':'form-control'}), max_length=30)
    gothram = forms.ChoiceField(label='Gothram' , required= True, choices=choices_attr['GOTHRAM'], widget=forms.Select(attrs={'class':'form-control'}))
    dob = forms.DateField(label='DoB', required= True, widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    place_of_birth = forms.CharField(label='Place of Birth', required= True, widget=forms.TextInput(attrs={'class':'form-control'}), max_length=30)
    time_of_birth = forms.TimeField(label='Time of Birth', required= True, widget=forms.TimeInput(attrs={'class':'form-control', 'type':'time'}))
    complexion = forms.ChoiceField(label='Complexion', required= True, choices=choices_attr['COMPLEXION'], widget=forms.Select(attrs={'class':'form-control'}))
    candidate_mobile = forms.CharField(label='Mobile', required= True, widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'[5-9]{1}[0-9]{9}',
                                        'title':'Phone number should start with 5-9 and remaing 9 digits within 0-9'}),
                                       max_length=30)

    surname = forms.CharField(label='Surname', required= True, widget=forms.TextInput(attrs={'class':'form-control'}), max_length=30)
    sub_sect = forms.ChoiceField(label='Sub-Sect', required= True, choices=choices_attr['SUB_SECT'], widget=forms.Select(attrs={'class':'form-control'}))
    zodiac = forms.ChoiceField(label='Zodiac', required= True, choices=choices_attr['ZODIAC'], widget=forms.Select(attrs={'class':'form-control'}))
    star = forms.ChoiceField(label='Star', required= True, choices=choices_attr['STAR'], widget=forms.Select(attrs={'class':'form-control'}))
    padam = forms.ChoiceField(label='Padam', required= True, choices=choices_attr['PADAM'], widget=forms.Select(attrs={'class':'form-control'}))
    qualification = forms.CharField(label='Qualificiation', required= True, widget=forms.TextInput(attrs={'class':'form-control'}), max_length=30)
    gender = forms.ChoiceField(label='Gender', required= True, choices=choices_attr['GENDER'], widget=forms.Select(attrs={'class':'form-control'}))
    height = forms.ChoiceField(label='Height', required= True, choices=choices_attr['HEIGHT'], widget=forms.Select(attrs={'class':'form-control'}))
    candidate_email = forms.CharField(label='Email',  required= True, widget=forms.TextInput(attrs={'class':'form-control', 'type':'email'}), max_length=30)
    profile_pic = forms.ImageField(label='profile_pic', required=False, widget=FileInput)

    def upload_image(self, reg_id, old_file_name, file_name, img):
        try:
            img_size = img.size
            if img_size > 1000000:
                self.add_error('profile_pic', 'Image size should not be greater than 1MB')
                return False

            img_extension = file_name.split('.')[-1]
            if img_extension not in VALID_IMAGE_EXTENSIONS:
                self.add_error('profile_pic', 'Please upload a file with valid image extension')
                return False

            user_folder = 'matrimony/media/profile_images/' + str(reg_id)
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)

            img_save_path = f'{user_folder}/{file_name}'
            with open(img_save_path, 'wb+') as f:
                f.write(img.file.read())

            # Delete the old image path if exists
            if old_file_name:
                try:
                    old_image_path = f'{user_folder}/{old_file_name}'
                    os.remove(old_image_path)
                except:
                    print('Failed to delete old image {old_file_name}')
                    
        except Exception as ex:
            print(ex)
            self.add_error('profile_pic', 'Failed to upload the image')
            return False

        return True

    def save(self, id, avatar_name):
        data_modified = {}
        matrimony_model_fields = [field.name for field in MatrimonyProfile._meta.get_fields()]
        for field in matrimony_model_fields:
            if field in self.data:
                if not self.data[field]:
                    continue

                data_modified[field] = self.data[field]
            
        data_modified['reg_id'] = int(id)
        if avatar_name:
            data_modified['profile_pic'] = avatar_name

        # if not self.upload_image():
        #     return False

        try:
            profile_obj = MatrimonyProfile(**data_modified)
            profile_obj.save()
        except MatrimonyProfile.DoesNotExist:
            return False
        except Exception as ex:
            return False
        
        return True


    def clean(self):
        cd = self.cleaned_data

        mobile = cd.get("candidate_mobile")
        email = cd.get("candidate_email")

        if not mobile.isnumeric():
            self.add_error('candidate_mobile', 'Mobile number should be numeric!!')

        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not re.search(regex, email):
            self.add_error('candidate_email', 'Invalid email format')

        return cd



class RegistrationForm(forms.Form):
    error_css_class = 'error'
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name...', 'class':'form-control'}), max_length=30)
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name...', 'class':'form-control'}), max_length=30)
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password...', 'class':'form-control'}), max_length=30)
    confirm_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password...', 'class':'form-control'}), max_length=100)
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email...', 'class':'form-control', 'type':'email'}), max_length=30,
                            validators=[validate_email])
    mobile = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Mobile...', 'class':'form-control', 'pattern':'[5-9]{1}[0-9]{9}',
                                        'title':'Phone number should start with 5-9 and remaing 9 digits within 0-9'}), max_length=30)
        
    def clean(self):
        cd = self.cleaned_data

        password1 = cd.get("password")
        password2 = cd.get("confirm_password")

        if len(password1) < 6:
            self.add_error('password', "Password should be atleast 6 Characters")
            return cd

        if password1 != password2:
            self.add_error('confirm_password', "Password does not match")
            return cd

        email = cd.get("email")
        try:
            user_object = Users.objects.get(email = email)
        except Users.DoesNotExist:
            return cd

        if user_object.id:
            self.add_error(None, ValidationError("Email already exists. Try logging in"))

    def save(self, commit=True):
        # dict_details = dict(self.data.copy())
        data = self.cleaned_data.copy()
        del data['confirm_password']
        data['last_updated_at'] = datetime.datetime.now()
        data['created_at'] = datetime.datetime.now()
        data['is_paid'] = False
        data['is_mobile_verified'] = False

        try:
            user_obj = Users(**data)
            user_obj.save()
        except Exception as ex:
            return False

        return True



class LoginForm(forms.Form):
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email...'}), max_length=30,
                            validators=[validate_email])
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password...'}), max_length=30)

    def clean(self):
        cd = super(LoginForm, self).clean()
        # cd = self.cleaned_data
        email = cd.get("email")
        password = cd.get("password")
        try:
            user_object = Users.objects.get(email = email, password = password)
        except Users.DoesNotExist:
            self.add_error('email', "Invalid Credentials!")
            return

        self.cleaned_data['id'] = user_object.id
        self.cleaned_data['user_details'] = model_to_dict(user_object)
            

class SearchForm(forms.Form):
    choices_attr['SECT'].insert(0, (None, 'ALL'))
    choices_attr['OCCUPATION'].insert(0, (None, 'ALL'))
    choices_attr['IS_NRI'].insert(0, (None, 'ALL'))
    bsssid = forms.IntegerField(label='BSSS Id' , required= False, widget=forms.NumberInput(attrs={'class':'form-control', 'min':'3500'}))

    minimum_age_gap = forms.IntegerField(label='Minimum Age Gap' , required= False, widget=forms.NumberInput(attrs={'class':'form-control', 'min':'0', 'max':'15'}))
    maximum_age_gap = forms.IntegerField(label='Maximum Age Gap' , required= False, widget=forms.NumberInput(attrs={'class':'form-control', 'min':'1', 'max':'15'}))
    sect = forms.ChoiceField(label='Sect' , required= False, choices=choices_attr['SECT'], widget=forms.Select(attrs={'class':'form-control'}))
    occupation = forms.ChoiceField(label='Occupation' , required= False, choices=choices_attr['OCCUPATION'], widget=forms.Select(attrs={'class':'form-control'}))
    is_married = forms.ChoiceField(label='Marital Status' , required= False, choices=choices_attr['MARITAL_STATUS'], widget=forms.Select(attrs={'class':'form-control'}))
    is_nri = forms.ChoiceField(label='NRI Matches' , required= False, choices=choices_attr['IS_NRI'], widget=forms.Select(attrs={'class':'form-control'}))

    def clean(self):
        cd = super(SearchForm, self).clean()
        # cd = self.cleaned_data
        minimum_age_gap = cd.get("minimum_age_gap")
        maximum_age_gap = cd.get("maximum_age_gap")
        if not minimum_age_gap:
            minimum_age_gap = 0

        if not maximum_age_gap:
            maximum_age_gap = 15

        if minimum_age_gap > maximum_age_gap:
            self.add_error('minimum_age_gap', "Minimum age gap cannot be greater than maximum age gap")


class OTPForm(forms.Form):
    otp = forms.CharField(label='OTP' , required= False, widget=forms.TextInput(attrs={'placeholder': 'Enter OTP Received...'}), max_length=15)

    def generate_otp(self):
        totp = pyotp.TOTP('base32secret3232', interval = 10)
        otp_generated = totp.now()
        print(f'OTP GENERATED: {otp_generated}')
        return otp_generated

    def is_mobile_valid(self, mobile):
        return True

    def save_data(self, reg_id):
        try:
            user_obj = Users.objects.get(id = reg_id)
            user_obj.is_mobile_verified = True
            user_obj.save()
        except Exception as ex:
            print(ex)
            return False
        
        return True

    def send_otp(self, mobile_number, otp):
        message = f'Greetings from BSSS. Your OTP : {otp}'
        otp_url = f'https://sms.office24by7.com/API/sms.php?username=9000966999&password=Sridhar123&from=BSSSIN&to={mobile_number}&msg={message}&type=1'
        requests.post(otp_url)

    def verify_otp(self, otp_generated):
        cd = self.cleaned_data
        otp_user = cd.get("otp")
        if otp_generated != otp_user:
            self.add_error('otp', "Incorrect OTP given")
            return False

        return True

        


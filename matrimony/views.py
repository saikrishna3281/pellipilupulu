from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.db.models.fields.files import ImageFieldFile
import datetime
import pytz

from .models import Users, MatrimonyProfile

from .forms import (RegistrationForm, LoginForm, MatrimonyRegistration,
                    FamilyBackground, JobDetails, PersonalDetails, ProfilePicForm,
                    Requirements, UpdatePassword, SearchForm, OTPForm)


from .models_other import DBMatrimony, get_bsssid


def home(request):
    return login(request)


def register(request):
    if request.method == "POST":
        details = RegistrationForm(request.POST)
        if details.is_valid():
            if not details.save():
                return render(request, 'registration.html', {'form': details})
            else:
                request.session['user'] = details.cleaned_data['email']
                user_obj = Users.objects.get(email = details.cleaned_data['email'])
                request.session['id'] = user_obj.id

            register_dict = model_to_dict(user_obj)
            register_dict['is_subscribed'] = False
            for key, value in register_dict.items():
                if isinstance(value, datetime.date) or\
                    isinstance(value, datetime.time):
                    if key == 'subscribed_at':
                        # If subscribed already, check whem the user is subscribed
                        if value:
                            td = datetime.datetime.now(datetime.timezone.utc) - value
                            # Subscription is valied for 180 days
                            if td.days < 180:
                                register_dict['is_subscribed'] = True

                    register_dict[key] = str(value)
                else:
                    register_dict[key] = value

            request.session['user_details'] = register_dict
            return redirect(matrimony_registration)
        else:
            return render(request, 'registration.html', {'form': details})
    else:
        register = RegistrationForm()
        return render(request, 'registration.html', {'form': register})


def show_users(request):
    if 'user' not in request.session:
        return redirect(login)

    if 'user_details' not in request.session:
        return redirect(login)

    # if not request.session['user_details']['is_mobile_verified']:
    #     return redirect(otp_view)

    user_matrimony_details = request.session['user_matrimony_details']
    if not user_matrimony_details:
        return HttpResponse("<h1>You cannot view matches without filling your profile. Please complete your profile</h1>")

    users = None
    if request.method == "POST" or 'filter' in request.session:
        if request.POST:
            request.session['filter'] = request.POST

        search_filter = request.session.get('filter', None)
        search_form = SearchForm(search_filter)
        with DBMatrimony() as db_matrimony:
            if search_form.is_valid():
                users = db_matrimony.fetch_users_profiles(user_matrimony_details,
                                                          search_filter)
    else:
        if 'filter' in request.session:
            del request.session['filter']

        search_form = SearchForm()
        with DBMatrimony() as db_matrimony:
            users = db_matrimony.fetch_users_profiles(user_matrimony_details)

    if users:
        paginator = Paginator(users, 20) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj=[]

    return render(request, 'display.html', {'search_form': search_form, 'page_obj': page_obj})


def login(request):
    if request.method == "POST":
        if 'user' in request.session:
            del request.session['user']

        if 'filter' in request.session:
            del request.session['filter']

        login_details = LoginForm(request.POST)
        if login_details.is_valid():
            request.session['user'] = login_details.cleaned_data['email']
            request.session['id'] = login_details.cleaned_data['id']


            login_dict = login_details.cleaned_data['user_details']
            login_dict['is_subscribed'] = False
            for key, value in login_dict.items():
                if isinstance(value, datetime.date) or\
                    isinstance(value, datetime.time):
                    if key == 'subscribed_at':
                        # If subscribed already, check whem the user is subscribed
                        if value:
                            td = datetime.datetime.now(datetime.timezone.utc) - value
                            # Subscription is valied for 180 days
                            if td.days < 180:
                                login_dict['is_subscribed'] = True

                    login_dict[key] = str(value)
                else:
                    login_dict[key] = value

            request.session['user_details'] = login_dict
            return redirect(matrimony_registration)
        else:
            for field in login_details.errors:
                login_details[field].field.widget.attrs['class'] = 'error'

            return render(request, 'login.html', {'form': login_details})

    else:
        if 'user' in request.session:
            del request.session['user']

        login = LoginForm()
        return render(request, 'login.html', {'form': login})


def subscribe(request):
    reg_id = request.session['user_details']['id']
    bsssid = get_bsssid(reg_id)
    return render(request, 'subscription.html', {'bsssid': bsssid})


def view_profile_readonly(request, reg_id):
    if 'user' not in request.session:
        return redirect(login)

    if not request.session['user_details']['is_subscribed']:
        return subscribe(request)

    button_type = ''
    profile_obj = MatrimonyProfile.objects.get(reg_id=reg_id)
    profile = model_to_dict(profile_obj)

    bsssid = get_bsssid(reg_id)

    details = MatrimonyRegistration(initial=profile)
    family_reg = FamilyBackground(initial=profile)
    job_reg = JobDetails(initial=profile)
    personal_details = PersonalDetails(initial=profile)
    requirements = Requirements(initial=profile)

    for field in details.fields:
        details[field].field.widget.attrs['readonly'] = True

    for field in family_reg.fields:
        family_reg[field].field.widget.attrs['readonly'] = True


    for field in job_reg.fields:
        job_reg[field].field.widget.attrs['readonly'] = True


    for field in personal_details.fields:
        personal_details[field].field.widget.attrs['readonly'] = True


    for field in requirements.fields:
        requirements[field].field.widget.attrs['readonly'] = True


    context = {'form': details,
                'button_type': button_type,
                'family_background': family_reg,
                'job_details_form' : job_reg,
                'personal_details': personal_details,
                'requirements' : requirements,
                'bsssid' : bsssid,
                'reg_id' : str(reg_id),
                'alert_message': '',
                'is_readonly' : 'read_only'
                }
    return render(request, 'matrimony_registration.html', context)


def view_profile(request, reg_id=None, action=None, is_readonly=False, update=True, alert_message=''):
    if 'user' not in request.session:
        return redirect(login)

    if 'user_details' not in request.session:
        return redirect(login)

    # if not request.session['user_details']['is_mobile_verified']:
    #     return redirect(otp_view)

    try:
        profile_obj = MatrimonyProfile.objects.get(reg_id=reg_id)
        profile = model_to_dict(profile_obj)
    except MatrimonyProfile.DoesNotExist:
        profile = {}

    bsssid = get_bsssid(reg_id)
    if reg_id == request.session['id']:
        user_matrimony_details = {}
        for key, value in profile.items():
            if isinstance(value, ImageFieldFile):
                user_matrimony_details[key] = value.name

            elif isinstance(value, datetime.date) or\
                isinstance(value, datetime.time):
                user_matrimony_details[key] = str(value)
            else:
                user_matrimony_details[key] = value

        request.session['user_matrimony_details'] = user_matrimony_details

    if not profile:
        profile = {}
        button_type = 'submit'
        is_readonly = False
    else:
        button_type = 'update'

    if action:
        button_type = action

    # profile_pic = ProfilePicForm(initial=profile)
    details = MatrimonyRegistration(initial=profile)
    family_reg = FamilyBackground(initial=profile)
    job_reg = JobDetails(initial=profile)
    personal_details = PersonalDetails(initial=profile)
    requirements = Requirements(initial=profile)

    # for field in profile_pic.fields:
    #     profile_pic[field].field.widget.attrs['readonly'] = is_readonly

    for field in details.fields:
        details[field].field.widget.attrs['readonly'] = is_readonly

    for field in family_reg.fields:
        family_reg[field].field.widget.attrs['readonly'] = is_readonly
        family_reg[field].field.widget.required = False

    for field in job_reg.fields:
        job_reg[field].field.widget.attrs['readonly'] = is_readonly
        job_reg[field].field.widget.required = False

    for field in personal_details.fields:
        personal_details[field].field.widget.attrs['readonly'] = is_readonly
        personal_details[field].field.widget.required = False

    for field in requirements.fields:
        requirements[field].field.widget.attrs['readonly'] = is_readonly
        requirements[field].field.widget.required = False

    is_readonly_tag = 'read_only' if is_readonly else 'not_read_only'

    context = {'form': details,
                'button_type': button_type,
                'family_background': family_reg,
                # 'profile_pic': profile_pic,
                'job_details_form' : job_reg,
                'personal_details': personal_details,
                'requirements' : requirements,
                'bsssid' : bsssid,
                'alert_message': alert_message,
                'reg_id' : str(reg_id),
                'is_readonly' : is_readonly_tag
                }
    return render(request, 'matrimony_registration.html', context)


def show_validation_errors(request, reg_form_validated, reg_id):
    profile_obj = MatrimonyProfile.objects.get(reg_id=reg_id)
    profile = model_to_dict(profile_obj)

    bsssid = get_bsssid(reg_id)
    family_reg = FamilyBackground(initial=profile)
    job_reg = JobDetails(initial=profile)
    personal_details = PersonalDetails(initial=profile)
    requirements = Requirements(initial=profile)


    is_readonly = False
    for field in reg_form_validated.fields:
        reg_form_validated[field].field.widget.attrs['readonly'] = is_readonly

    for field in family_reg.fields:
        family_reg[field].field.widget.attrs['readonly'] = is_readonly
        family_reg[field].field.widget.required = False

    for field in job_reg.fields:
        job_reg[field].field.widget.attrs['readonly'] = is_readonly
        job_reg[field].field.widget.required = False

    for field in personal_details.fields:
        personal_details[field].field.widget.attrs['readonly'] = is_readonly
        personal_details[field].field.widget.required = False

    for field in requirements.fields:
        requirements[field].field.widget.attrs['readonly'] = is_readonly
        requirements[field].field.widget.required = False

    is_readonly_tag = 'read_only' if is_readonly else 'not_read_only'

    context = {'form': reg_form_validated,
                'button_type': 'submit',
                'family_background': family_reg,
                # 'profile_pic': profile_pic,
                'job_details_form' : job_reg,
                'personal_details': personal_details,
                'requirements' : requirements,
                'bsssid' : bsssid,
                'alert_message': 'Errors!! Please correct the validation errors',
                'reg_id' : str(reg_id),
                'is_readonly' : is_readonly_tag
                }
    return render(request, 'matrimony_registration.html', context)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def matrimony_registration(request):
    if 'user' not in request.session:
        return redirect(login)

    if 'user_details' not in request.session:
        return redirect(login)

    # if not request.session['user_details']['is_mobile_verified']:
    #     return redirect(otp_view)

    reg_id = request.session['id']
    if request.method == "POST" and 'submit' in request.POST: # For update
        details = MatrimonyRegistration(request.POST)
        old_avatar_name = None
        if details.is_valid():
            # details.save(reg_id)
            avatar_name = None
            if request.FILES:
                # It could be possible that user is trying to upload the pic
                # During the first time registration
                try:
                    old_avatar_name = request.session['user_matrimony_details']['profile_pic']
                except:
                    pass

                avatar_name = request.FILES['profile_pic'].name
                file = request.FILES['profile_pic']
                if not details.upload_image(reg_id, old_avatar_name, avatar_name, file):
                    return show_validation_errors(request, details, reg_id)

            if not avatar_name:
                avatar_name = old_avatar_name
            details.save(reg_id, avatar_name)

        return view_profile(request, reg_id, 'update', is_readonly=True,
                        alert_message="Congratulations! You Successfully saved your profile.")


    elif request.method == "POST" and 'update' in request.POST:
        details = MatrimonyRegistration(request.POST)
        # if details.is_valid():
        #     details.save(reg_id)

        return view_profile(request, reg_id, 'submit', is_readonly=False)


    else:
        return view_profile(request, reg_id, None, is_readonly=True)


def update_password(request):
    if 'user' not in request.session:
        return redirect(login)

    reg_id = request.session['id']
    bsssid = get_bsssid(reg_id)

    if request.method == "POST":
        password_details = UpdatePassword(request.POST, initial={'id':reg_id})
        if password_details.is_valid():
            if not password_details.save():
                return render(request, 'update_password.html', {'form': password_details, 'bsssid': bsssid, 'message':'fail'})
            else:
                return render(request, 'update_password.html', {'form': password_details, 'bsssid': bsssid, 'message':'success'})
        else:
            return render(request, 'update_password.html', {'form': password_details, 'bsssid': bsssid})
    else:
        password_details = UpdatePassword()
        return render(request, 'update_password.html', {'form': password_details, 'bsssid': bsssid})


def logout(request):
    try:
        if 'user' in request.session:
            del request.session['user']
        if 'user_details' in request.session:
            del request.session['user_details']
        if 'user_matrimony_details' in request.session:
            del request.session['user_matrimony_details']

        if 'filter' in request.session:
            del request.session['filter']

    except:
        pass

    return redirect(login)


def generate_otp(request, mobile_number):
    otp_form = OTPForm()
    otp_generated = otp_form.generate_otp()
    otp_form.send_otp(mobile_number, otp_generated)
    request.session['otp'] = otp_generated

    if otp_form.is_mobile_valid(mobile_number):
        time_now = str(datetime.datetime.now(pytz.timezone('Asia/Kolkata')))
        return render(request, 'otp.html', {'otp_form': otp_form, 'user_mobile_number':mobile_number, 'time_now' : time_now})
    else:
        error_message = f'OTP cannot be sent to invalid mobile number {mobile_number}. Please contact Helpline.'
        return render(request, 'otp.html', {'error_message': error_message})


def otp_view(request):
    mobile_number = request.session['user_details']['mobile']
    if request.method == "POST" and 'verify' in request.POST:
        otp_form = OTPForm(request.POST)
        reg_id = request.session['user_details']['id']
        otp_generated = request.session["otp"]
        if otp_form.is_valid() and otp_form.verify_otp(otp_generated):
            if otp_form.save_data(reg_id):
                request.session['user_details']['is_mobile_verified'] = True
                request.session.modified = True
                return redirect(matrimony_registration)
        else:
            time_now = str(datetime.datetime.now(pytz.timezone('Asia/Kolkata')))
            return render(request, 'otp.html', {'otp_form': otp_form, 'user_mobile_number':mobile_number, 'time_now' : time_now})
    else:
        return generate_otp(request, mobile_number)



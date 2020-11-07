import datetime
import psycopg2
import psycopg2.extras
from psycopg2 import IntegrityError

from django.db import models
from dateutil.relativedelta import relativedelta
#from django.core.validators import validate_email

# Contains data about the choice fields
choices_attr = {}
global attributes
attributes = {}
attribute_tables = ['COMPLEXION', 'GENDER', 'HEIGHT', 'PADAM', 'ZODIAC',
                    'STAR', 'GOTHRAM', 'SECT', 'SUB_SECT', 'MARITAL_STATUS',
                    'IS_PC', 'NUM_KIDS', 'REQUIREMENT_BAR', 'OCCUPATION', 'IS_NRI']

class DBMatrimony:
    def __init__(self):
        self.conn = None

    def __enter__(self):
        db_dict = self.get_db_parameters()
        self.conn = psycopg2.connect(**db_dict)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def get_db_parameters(self):
        db_dict = {'dbname' :'syhwraxk', 'user' :'syhwraxk', 'host' : 'ruby.db.elephantsql.com', 'password' :'VuZDTogPcvrGc_3olt1_lw3jcsc0E-8O'}
        return db_dict


    def get_user_password(self, user_id):
        command = f'SELECT password from public.users where  id={user_id}'
        try:
            cur = self.conn.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
            # command = f'SELECT id from public.users where email=\'{email}\' and password=\'{password}\''
            cur.execute(command)
            rows = cur.fetchall()
        except Exception as ex:
            print("Failed to fetch user details")
            print(ex)
            return None

        if len(rows) > 0:
            return rows[0].password
        
        return None


    def update_user_password(self, user_id, password):
        rows_updated = 0
        command = f'update public.users set password=\'{password}\' where id = {user_id}'
        try:
            cur = self.conn.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
            # command = f'SELECT id from public.users where email=\'{email}\' and password=\'{password}\''
            cur = self.conn.cursor()
            cur.execute(command)
            rows_updated = cur.rowcount
            self.conn.commit()
            cur.close()
        except Exception as ex:
            print("Failed to fetch user details")
            print(ex)
            return None

        return rows_updated > 0


    def fetch_users_profiles(self, user_matrimony_details, filters=None):
        # gender 1: Female, 2: Male
        user_gender = user_matrimony_details['gender']
        target_user_gender = 1 if user_gender == 2 else 2 
        filter_str = f'gender={target_user_gender}'

        dob_year = int(user_matrimony_details['dob'].split('-')[0])
        dob_datetime =  datetime.datetime(dob_year, 1, 1)
        try:
            if filters:
                min_age_gap = str(dob_datetime)
                if user_gender == 2:
                    max_age_gap = str(dob_datetime + relativedelta(years = 15))
                else:
                    max_age_gap = str(dob_datetime - relativedelta(years = 15))

                if filters['minimum_age_gap']:
                    if user_gender == 2:
                        min_age_gap = str(dob_datetime + relativedelta(years = int(filters['minimum_age_gap']) + 1))
                    else:
                        min_age_gap = str(dob_datetime - relativedelta(years = int(filters['minimum_age_gap']) - 1))


                if filters['maximum_age_gap']:
                    if user_gender == 2:
                        max_age_gap = str(dob_datetime + relativedelta(years = int(filters['maximum_age_gap']) + 1))
                    else:
                        max_age_gap = str(dob_datetime - relativedelta(years = int(filters['maximum_age_gap']) - 1))


                if user_gender == 2:
                    filter_str += f' and dob BETWEEN \'{min_age_gap}\' AND  \'{max_age_gap}\''
                else:
                    filter_str += f' and dob BETWEEN \'{max_age_gap}\' AND  \'{min_age_gap}\''
            

                if filters['sect']:
                    filter_str +=  " and "
                    sect = filters['sect']
                    filter_str += f'sect={sect}'

                if filters['occupation']:
                    filter_str +=  " and "
                    occupation = filters['occupation']
                    filter_str += f'occupation={occupation}'

                if filters['is_married']:
                    filter_str +=  " and "
                    is_married = filters['is_married']
                    filter_str += f'is_married={is_married}'

                if filters['is_nri']:
                    filter_str +=  " and "
                    is_nri = filters['is_nri']
                    filter_str += f'is_nri={is_nri}'

                # If BSSSID is given in input, always take this as priority
                if filters['bsssid']:
                    id = int(filters['bsssid']) - 3500
                    filter_str = f'reg_id={str(id)}'

            command = "SELECT name,surname,gothram,dob,reg_id from public.matrimony_profile"
            if filter_str:
                command = command + f' where {filter_str}'
            cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            cur.execute(command)
            rows = cur.fetchall()
        except Exception as ex:
            print("Failed to fetch user details")
            print(ex)
            return None

        gothram_choices = dict(choices_attr['GOTHRAM'])
        for row in rows:
            gothram_id = row['gothram']
            row['gothram'] = gothram_choices[gothram_id]
        return rows


    def fetch_attrs(self, table):
        try:
            cur = self.conn.cursor() # cursor_factory = psycopg2.extras.RealDictCursor
            cur.execute("SELECT * from public." + table)
            rows = cur.fetchall()
        except Exception as ex:
            print("Failed to fetch user details")
            print(ex)
            return None

        return rows


def get_attributes(name):
    global attributes
    if attributes:
        return attributes[name]
    
    with DBMatrimony() as db_matrimony:
        for attr_table in attribute_tables:
            attributes[attr_table] = db_matrimony.fetch_attrs(attr_table)

    return attributes[name]



def get_bsssid(id):
    """
    BSSS Id starts from 3500
    Any BSSSid should start from BM
    Any Id should contain six numbers
    For example if database id is 1
    Then BSSSId is "BM003501
    """
    
    #>>> a = 123
    #>>> a = str(a)
    #>>> a.zfill(6)
    #'000123'
    bsssid = int(id) + 3500
    bsssid =  str(bsssid).zfill(6)
    return "BM" + bsssid



for attr in attribute_tables:
    choices_attr[attr] = get_attributes(attr)
from util import dataframe_from_csv
from util import display
import os
import pandas as pd

mimic3_path = "mimic_data"

def create_stays(table1_name , table2_name):
    table1 = dataframe_from_csv(os.path.join(mimic3_path , table1_name))
    table2 = dataframe_from_csv(os.path.join(mimic3_path , table2_name))
    stays = table1.merge(table2 , how='inner', left_on=['subject_id'], right_on=['subject_id'])
    stays = stays[['subject_id', 'gender', 'dob', 'dod' , 'intime']]
    return stays

def process_stays_age(stays):
    stays['age'] = round(((stays['intime'].subtract(stays['dob'])).apply(lambda x: x.days)) / 365)
    stays.loc[stays.age < 0, 'age'] = 90
    return stays

# 合并patients和icustays表，计算age
stays = create_stays('PATIENTS.csv' , 'ICUSTAYS.csv')
stays['intime'] = pd.to_datetime(stays['intime'])
stays['dob'] = pd.to_datetime(stays['dob'])
stays = process_stays_age(stays)

display(stays)

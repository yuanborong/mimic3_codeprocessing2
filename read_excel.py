from util import dataframe_from_csv
from util import display
import os
import pandas as pd

mimic3_path = "mimic_data"

# 读取patients表，返回pats[['subject_id' , 'gender' , 'dob' , 'dod']]
def read_patients_table(mimic3_path):
    pats = dataframe_from_csv(os.path.join(mimic3_path, 'PATIENTS.csv'))
    pats = pats[['subject_id' , 'gender' , 'dob' , 'dod']]
    pats['dob'] = pd.to_datetime(pats['dob'])
    pats['dod'] = pd.to_datetime(pats['dod'])
    return pats

# 读取icustays表，
def read_icustays_table(mimic3_path):
    icustays = dataframe_from_csv(os.path.join(mimic3_path, 'ICUSTAYS.csv'))
    icustays['intime'] = pd.to_datetime(icustays['intime'])
    icustays['outtime'] = pd.to_datetime(icustays['outtime'])
    return icustays

# 读取admissions
def read_admissions_table(mimic3_path):
    admits = dataframe_from_csv(os.path.join(mimic3_path, 'ADMISSIONS.csv'))
    admits = admits[['subject_id', 'hadm_id', 'admittime', 'dischtime', 'deathtime', 'ethnicity', 'diagnosis']]
    admits['admittime'] = pd.to_datetime(admits['admittime'])
    admits['dischtime'] = pd.to_datetime(admits['dischtime'])
    admits['deathtime'] = pd.to_datetime(admits['deathtime'])
    return admits

# 合并patients,icustays和admissions表（整理ICU病人）
def create_stays(mimi3_path):
    pats = read_patients_table(mimic3_path)
    icustays = read_icustays_table(mimic3_path)
    admits = read_admissions_table(mimic3_path)
    stays = (pats.merge(icustays , how='inner', left_on=['subject_id'], right_on=['subject_id'])).merge(admits , how='inner' , left_on=['subject_id'], right_on=['subject_id'])
    stays = stays[['subject_id', 'gender', 'ethnicity' , 'dob', 'dod' , 'intime'  ]]
    return stays



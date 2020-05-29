import global_variable
from util import dataframe_from_csv
from util import display
import os
import pandas as pd
from global_variable import *

mimic3_path = global_variable.mimic3_path

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
    stays = (icustays.merge(admits , how='inner', left_on=['subject_id' , 'hadm_id'], right_on=['subject_id' , 'hadm_id'])).merge(pats , how='inner' , left_on=['subject_id'], right_on=['subject_id'])
    stays = stays[['subject_id', 'hadm_id' , 'gender', 'ethnicity' , 'dob', 'dod' , 'admittime' , 'dischtime' , 'deathtime' ,'intime' , 'outtime' ]]
    return stays

# 读取diagnose，并用字典表d_icd_diagnoses进行扩充解释
def create_diagnose(mimic3_path):
    diagnose = dataframe_from_csv(os.path.join(mimic3_path , "DIAGNOSES_ICD.csv"))
    d_diagnoses = dataframe_from_csv(os.path.join(mimic3_path , "D_ICD_DIAGNOSES.csv"))
    diagnose = diagnose.merge(d_diagnoses , how="inner" , left_on=['icd9_code'] , right_on=['icd9_code']).sort_values(by=['subject_id' , 'seq_num'] , ascending=True)
    diagnose = diagnose[['subject_id' , 'hadm_id' , 'icd9_code' , 'short_title' ]]
    return diagnose


from read_excel import *
from pre_processing import *
from global_variable import *

# 病人基本信息，涉及表：admission,patients,icu_stays
def test_stays():
    stays = create_stays(mimic3_path)
    stays = process_stays_age(stays)
    stays = process_stays_ethnicity(stays)
    stays = process_stays_gender(stays)
    stays = add_inhospital_mortality(stays)
    stays = add_inicu_mortality(stays)
    stays = stays.drop(['dob', 'dod', 'intime', 'outtime', 'admittime', 'dischtime', 'deathtime'], axis=1)
    display(stays)

def test_icd9():
    diagnose = create_diagnose(mimic3_path)
    display(diagnose)

# test_stays()
test_icd9()


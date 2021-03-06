from read_excel import *
from global_variable import global_variable


# 计算age
# 如果计算小于0（因为mimic为了脱敏的操作）全部年龄设置为90
def process_stays_age(stays):
    stays['age'] = (round(((stays['intime'].subtract(stays['dob'])).apply(lambda x: x.days)) / 365)).apply(lambda x : int(x))
    stays.loc[stays.age < 0, 'age'] = 90
    return stays

# 处理race
def process_stays_ethnicity(stays):
    e_map = global_variable.e_map
    ethnicity = stays['ethnicity'].apply(lambda str : str.replace(' OR ' , '/').split(' - ')[0].split('/')[0])
    stays['ethnicity'] = ethnicity.fillna('').apply(lambda str : e_map[str] if str in e_map else 0)
    return stays

# 处理gender
def process_stays_gender(stays):
    g_map = global_variable.g_map
    stays['gender'] = stays['gender'].fillna('').apply(lambda gender : g_map[gender] if gender in g_map else 0)
    return stays

# 统计入院mortality
def add_inhospital_mortality(stays):
    mortality = (stays.dod.notnull()) & (stays.admittime <= stays.dod) & (stays.dischtime >= stays.dod)
    mortality = mortality | ((stays.deathtime.notnull()) & (stays.admittime <= stays.deathtime) & (stays.dischtime >= stays.deathtime))
    stays['mortality_inhospital'] = mortality.astype(int)
    return stays

# 统计ICU重症室的mortality
def add_inicu_mortality(stays):
    mortality = (stays.dod.notnull()) & (stays.intime <= stays.dod) & (stays.outtime >= stays.dod)
    mortality = mortality | ((stays.deathtime.notnull()) & (stays.intime <= stays.deathtime) & (stays.outtime >= stays.deathtime))
    stays['mortality_inicu'] = mortality.astype(int)
    return stays






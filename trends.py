import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(
    '/Users/DavidAaronDeonarine/Desktop/MyCourses/COMP3610/Assignments/Project/credit_card_approval.csv')
df.head()
df = df.drop(columns=['ID'])

df['DAYS_BIRTH'] = (df['DAYS_BIRTH'] * -1) // 365
df.rename(columns={'DAYS_BIRTH': 'AGE'}, inplace=True)

df_1 = df.copy()
df_1 = df_1[df_1["TARGET"] > 0]

df_0 = df.copy()
df_0 = df_0[df_0["TARGET"] == 0]


def highRiskAge():
    plt.title("Age Distribution of High Risk Persons")
    sns.countplot(x='AGE', data=df_1)
    plt.show()


def lowRiskAge():
    plt.title("Age Distribution of Low Risk Persons")
    sns.countplot(x='AGE', data=df_0)
    plt.show()


def highRiskGender():
    plt.title("Gender Distribution of High Risk Persons")
    sns.countplot(x='CODE_GENDER', data=df_1)
    plt.show()


def lowRiskGender():
    plt.title("Gender Distribution of Low Risk Persons")
    sns.countplot(x='CODE_GENDER', data=df_0)
    plt.show()


def highRiskFamily():
    plt.title("Family Distribution of High Risk Persons")
    sns.countplot(y='NAME_FAMILY_STATUS', data=df_1)
    plt.show()


def lowRiskFamily():
    plt.title("Family Distribution of Low Risk Persons")
    sns.countplot(y='NAME_FAMILY_STATUS', data=df_0)
    plt.show()


def highRiskEducation():
    plt.title("Education Distribution of High Risk Persons")
    sns.countplot(y='NAME_EDUCATION_TYPE', data=df_1)
    plt.show()


def lowRiskEducation():
    plt.title("Education Distribution of Low Risk Persons")
    sns.countplot(y='NAME_EDUCATION_TYPE', data=df_0)
    plt.show()


def highRiskChildren():
    plt.title("Amount of Children of High Risk Persons")
    sns.countplot(x='CNT_CHILDREN', data=df_1)
    plt.show()


def lowRiskChildren():
    plt.title("Amount of Children of Low Risk Persons")
    sns.countplot(x='CNT_CHILDREN', data=df_0)
    plt.show()


def highRiskJob():
    plt.title("Job Distribution of Low Risk Persons")
    sns.countplot(y='JOB', data=df_1)
    plt.show()


def lowRiskJob():
    plt.title("Job Distribution of Low Risk Persons")
    sns.countplot(y='JOB', data=df_0)
    plt.show()

import PySimpleGUI as sg
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import date
import copy
import predict  # predict script
import trends

# GUI Layouts
header = [[sg.Text('Credit Card Qualifier', pad=(100, 0), background_color='#0c3578', justification='center',
                   size=(30, 1), font=("Helvetica", 25))],
          [sg.Text('Please complete all fields below!', pad=(200, 0), background_color='#0c3578',
                   justification='center', font=("Arial", 15))]]

# To collect person identifiers from user. Can be stored for future use.
personal_info = [
    [sg.Text('First Name', pad=(0, 10), font=("Arial", 12)), sg.InputText(key='fname', size=(20, 3), pad=((0, 99), 10)),
     sg.Text('Last Name', font=("Arial", 12)),
     sg.InputText(key='lname', size=(20, 3))],
    [sg.Text('Contact Number', font=("Arial", 12), pad=(0, 10)),
     sg.InputText(key='number', size=(10, 3), pad=((0, 160), 10)),
     sg.Text('Email', font=("Arial", 12)),
     sg.InputText(key='email_address', size=(20, 3))],
    [sg.Text('Gender', font=("Arial", 12), pad=(0, 10)),
     sg.InputCombo(['Female', 'Male'], enable_events=True, key='gender', pad=((0, 225), 10)),
     sg.Text('Age', font=("Arial", 12)),
     sg.InputText(key='dob', size=(5, 3))]]

# Enter 4 months of payment history for comprehensive prediction
payment_layout = [[sg.Text('Payment History', pad=(0, 0), font=("Arial", 15))],
                  [sg.Text('Payment Status for Current Month:', pad=(0, 10), font=("Arial", 12)),
                   sg.InputCombo(['0: 1-29 days past due', '1: 30-59 days past due', '2: 60-89 days overdue',
                                  '3: 90-119 days overdue', '4: 120-149 days overdue',
                                  '5: More than 150 days overdue', 'C: Paid off the month',
                                  'X: No loan for the month'], enable_events=True, key='payment1')],
                  [sg.Text('Payment Status for Prior Month:', font=("Arial", 12), pad=(0, 10)),
                   sg.InputCombo(['0: 1-29 days past due', '1: 30-59 days past due', '2: 60-89 days overdue',
                                  '3: 90-119 days overdue', '4: 120-149 days overdue',
                                  '5: More than 150 days overdue', 'C: Paid off the month',
                                  'X: No loan for the month'], enable_events=True, key='payment2')],
                  [sg.Text('Payment Status for 2 Months Ago:', font=("Arial", 12), pad=(0, 10)),
                   sg.InputCombo(['0: 1-29 days past due', '1: 30-59 days past due', '2: 60-89 days overdue',
                                  '3: 90-119 days overdue', '4: 120-149 days overdue',
                                  '5: More than 150 days overdue', 'C: Paid off the month',
                                  'X: No loan for the month'], enable_events=True, key='payment3')],
                  [sg.Text('Payment Status for 3 Months Ago:', font=("Arial", 12), pad=(0, 10)),
                   sg.InputCombo(['0: 1-29 days past due', '1: 30-59 days past due', '2: 60-89 days overdue',
                                  '3: 90-119 days overdue', '4: 120-149 days overdue',
                                  '5: More than 150 days overdue', 'C: Paid off the month',
                                  'X: No loan for the month'], enable_events=True, key='payment4')],
                  [sg.Button('Submit')]
                  ]
# To collect features for prediction
features = [[sg.Text('COMPLETE ALL FIELDS BELOW TO CALCULATE YOUR RISK', pad=(90, 0), background_color='#0c3578',
                     justification='center', font=("Arial", 15))],
            [sg.Text('Do you own a vehicle?', font=("Arial", 12), pad=((0, 20), 10)),
             sg.InputCombo(['Yes', 'No'], enable_events=True, key='vehicle'),
             sg.Text('\tDo you own property?', font=("Arial", 12)),
             sg.InputCombo(['Yes', 'No'], enable_events=True, key='realty')],
            [sg.Text('Do you have children?', font=("Arial", 12), pad=(0, 10)),
             sg.InputCombo(['No children', '1 children', '2+ children'], enable_events=True,
                           key='children'),
             sg.Text(' Highest Level of Education', font=("Arial", 12)),
             sg.InputCombo(['Secondary / secondary special', 'Higher education',
                            'Incomplete higher', 'Lower secondary', 'Academic degree'],
                           enable_events=True, key='education', size=(40, 3))],
            [sg.Text('Marital Status', font=("Arial", 12), pad=(0, 10)),
             sg.InputCombo(['Married', 'Single / not married', 'Civil marriage', 'Separated', 'Widow'],
                           enable_events=True, key='mstatus', pad=((0, 81), 10)),
             sg.Text(' Housing Type', font=("Arial", 12), pad=(0, 10)),
             sg.InputCombo(['With parents', 'House / apartment', 'Rented apartment', 'Municipal apartment',
                            'Co-op apartment', 'Office apartment'], enable_events=True, key='housing')],
            [sg.Text('Current Annual Income (USD)', font=("Arial", 12), pad=(0, 10)),
             sg.InputText(key='income', size=(10, 3), pad=((0, 58), 10)),
             sg.Text('Job Description', font=("Arial", 12)),
             sg.InputCombo(['Accountants', 'Cleaning staff', 'Cooking staff', 'Core staff', 'Drivers', 'HR staff',
                            'High skill tech staff', 'IT staff', 'Laborers', 'Low-skill Laborers', 'Managers',
                            'Medicine staff', 'Private service staff', 'Realty agents', 'Sales staff', 'Secretaries',
                            'Security staff', 'Waiters/barmen staff'], enable_events=True, key='job')],
            [sg.Text('Date of Employment (MM-DD-YYYY)', font=("Arial", 12), pad=(0, 10)),
             sg.InputText(key='start_date', size=(20, 3))],
            [sg.Text('Do you have a mobile phone?', font=("Arial", 12), pad=(0, 10)),
             sg.InputCombo(['Yes', 'No'], enable_events=True, key='mobile'),
             sg.Text('\tDo you have a work phone?', font=("Arial", 12)),
             sg.InputCombo(['Yes', 'No'], enable_events=True, key='workphone')],
            [sg.Text('Do you have a residential line?', font=("Arial", 12), pad=(0, 10)),
             sg.InputCombo(['Yes', 'No'], enable_events=True, key='residentialphone'),
             sg.Text('\tDo you have an email?', font=("Arial", 12)),
             sg.InputCombo(['Yes', 'No'], enable_events=True, key='email')],
            ]

trends_layout = [[sg.Button('High Risk Age', pad=((80, 80), 10), button_color='dark red'),
                  sg.Button('Low Risk Age', pad=((0, 80), 10), button_color='dark blue')],
                 [sg.Button('High Risk Gender', pad=((80, 64), 10), button_color='dark red'),
                  sg.Button('Low Risk Gender', pad=((0, 80), 10), button_color='dark blue')],
                 [sg.Button('High Risk Family', pad=((80, 68), 10), button_color='dark red'),
                  sg.Button('Low Risk Family', pad=((0, 80), 10), button_color='dark blue')],
                 [sg.Button('High Risk Education', pad=((80, 53), 10), button_color='dark red'),
                  sg.Button('Low Risk Education', pad=((0, 60), 10), button_color='dark blue')],
                 [sg.Button('High Risk Children', pad=((80, 60), 10), button_color='dark red'),
                  sg.Button('Low Risk Children', pad=((0, 80), 10), button_color='dark blue')],
                 [sg.Button('High Risk Job', pad=((80, 83), 10), button_color='dark red'),
                  sg.Button('Low Risk Job', pad=((0, 80), 10), button_color='dark blue')],
                 [sg.Exit()]
                 ]
# Combine layout for main window
data_layout = [
    [sg.Column(header, background_color='#0c3578', justification='center')],
    [sg.Text('Personal Information:', font=("Arial", 15), pad=((0, 0), (20, 0)))],
    [sg.Column(personal_info)],
    [sg.Text('_____________________________________________________________________________', justification='center',
             font=("Arial", 15))],
    [sg.Column(features)],
    [sg.Text('Enter payment history here: ', font=("Arial", 15)), sg.Button('Click Here',
                                                                            button_color='dark blue')],
    [sg.Text('_____________________________________________________________________________', justification='center',
             font=("Arial", 15))],
    [sg.Button('Check My Risk', pad=((80, 80), 20)), sg.Button('Investigate Database', pad=((70, 130), 20)), sg.Exit()]
]

# Mapping for GUI features to data set representation
gender_dict = {'Female': 0, 'Male': 1}
car_dict = {'Yes': 1, 'No': 0}
realty_dict = {'Yes': 1, 'No': 0}
children_dict = {'2+ children': 1, 'No children': 2, '1 children': 0}
education_dict = {'Secondary / secondary special': 4, 'Higher education': 1, 'Incomplete higher': 2,
                  'Lower secondary': 3, 'Academic degree': 0}
family_dict = {'Married': 1, 'Single / not married': 3, 'Civil marriage': 0, 'Separated': 2, 'Widow': 4}
housing_dict = {'With parents': 5, 'House / apartment': 1, 'Rented apartment': 4, 'Municipal apartment': 2,
                'Co-op apartment': 0, 'Office apartment': 3}
mobile_dict = {'Yes': 1, 'No': 0}
work_phone_dict = {'Yes': 1, 'No': 0}
phone_dict = {'Yes': 1, 'No': 0}
email_dict = {'Yes': 1, 'No': 0}
job_dict = {'Managers': 10, 'Private service staff': 12, 'Laborers': 8, 'Core staff': 3, 'Drivers': 4,
            'High skill tech staff': 6, 'Realty agents': 13, 'Secretaries': 15, 'Accountants': 0,
            'Sales staff': 14, 'Medicine staff': 11, 'Waiters/barmen staff': 17, 'Low-skill Laborers': 9,
            'Cleaning staff': 1, 'HR staff': 5, 'Cooking staff': 2, 'Security staff': 16, 'IT staff': 7}
status_dict = {'0: 1-29 days past due': 0, '1: 30-59 days past due': 1, '2: 60-89 days overdue': 2,
               '3: 90-119 days overdue': 3, '4: 120-149 days overdue': 4,
               '5: More than 150 days overdue': 5, 'C: Paid off the month': 6,
               'X: No loan for the month': 7}


def createPaymentWindow():
    layout = copy.deepcopy(payment_layout)  # Cannot reuse layouts in pysimplegui
    return sg.Window("Payment History", layout)


def createTrendWindow():
    layout = copy.deepcopy(trends_layout)  # Cannot reuse layouts in pysimplegui
    return sg.Window("Data Analytics", layout)


window = sg.Window('COMP3610 | Group 2', data_layout)

while True:
    event, values = window.Read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        window.Close()
        break

    if event == 'Click Here':
        # payment_window = sg.Window('Payment History', layout=payment_layout)
        payment_window = createPaymentWindow()

        while True:
            event1, values = payment_window.Read()
            if event1 == sg.WIN_CLOSED or event1 == 'Exit':
                payment_window.Close()
                break

            if event1 == 'Submit':
                status1 = values['payment1']
                status2 = values['payment2']
                status3 = values['payment3']
                status4 = values['payment4']
                payment_window.Close()

                if event1 == sg.WIN_CLOSED or event1 == 'Exit':
                    payment_window.Close()
                    break

    if event == 'Check My Risk':
        df = pd.DataFrame(
            columns=['CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'CNT_CHILDREN', 'AMT_INCOME_TOTAL',
                     'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 'AGE',
                     'FLAG_MOBIL', 'FLAG_WORK_PHONE', 'FLAG_PHONE', 'FLAG_EMAIL', 'JOB', 'BEGIN_MONTHS',
                     'STATUS'])

        fname = values['fname']
        lname = values['lname']
        number = values['number']
        email_address = values['email_address']

        doe = datetime.strptime(values['start_date'], '%m-%d-%Y').date()
        today = date.today()
        emp_days = today - doe
        emp_days = float(emp_days.days)

        new_row1 = [[gender_dict.get(values['gender']),
                     car_dict.get(values['vehicle']),
                     realty_dict.get(values['realty']),
                     children_dict.get(values['children']),
                     values['income'],
                     education_dict.get(values['education']),
                     family_dict.get(values['mstatus']),
                     housing_dict.get(values['housing']),
                     values['dob'],
                     emp_days,
                     mobile_dict.get(values['mobile']),
                     work_phone_dict.get(values['workphone']),
                     phone_dict.get(values['residentialphone']),
                     email_dict.get(values['email']),
                     job_dict.get(values['job']),
                     0,
                     status_dict.get(status1)]]

        new_row2 = [[gender_dict.get(values['gender']),
                     car_dict.get(values['vehicle']),
                     realty_dict.get(values['realty']),
                     children_dict.get(values['children']),
                     values['income'],
                     education_dict.get(values['education']),
                     family_dict.get(values['mstatus']),
                     housing_dict.get(values['housing']),
                     values['dob'],
                     emp_days,
                     mobile_dict.get(values['mobile']),
                     work_phone_dict.get(values['workphone']),
                     phone_dict.get(values['residentialphone']),
                     email_dict.get(values['email']),
                     job_dict.get(values['job']),
                     -1,
                     status_dict.get(status2)]]

        new_row3 = [[gender_dict.get(values['gender']),
                     car_dict.get(values['vehicle']),
                     realty_dict.get(values['realty']),
                     children_dict.get(values['children']),
                     values['income'],
                     education_dict.get(values['education']),
                     family_dict.get(values['mstatus']),
                     housing_dict.get(values['housing']),
                     values['dob'],
                     emp_days,
                     mobile_dict.get(values['mobile']),
                     work_phone_dict.get(values['workphone']),
                     phone_dict.get(values['residentialphone']),
                     email_dict.get(values['email']),
                     job_dict.get(values['job']),
                     -2,
                     status_dict.get(status3)]]

        new_row4 = [[gender_dict.get(values['gender']),
                     car_dict.get(values['vehicle']),
                     realty_dict.get(values['realty']),
                     children_dict.get(values['children']),
                     values['income'],
                     education_dict.get(values['education']),
                     family_dict.get(values['mstatus']),
                     housing_dict.get(values['housing']),
                     values['dob'],
                     emp_days,
                     mobile_dict.get(values['mobile']),
                     work_phone_dict.get(values['workphone']),
                     phone_dict.get(values['residentialphone']),
                     email_dict.get(values['email']),
                     job_dict.get(values['job']),
                     -3,
                     status_dict.get(status4)]]

        new_row11 = {'CODE_GENDER': gender_dict.get(values['gender']), 'AGE': values['dob'],
                     'FLAG_OWN_CAR': car_dict.get(values['vehicle']),
                     'FLAG_OWN_REALTY': realty_dict.get(values['realty']),
                     'CNT_CHILDREN': children_dict.get(values['children']),
                     'NAME_EDUCATION_TYPE': education_dict.get(values['education']),
                     'NAME_FAMILY_STATUS': family_dict.get(values['mstatus']),
                     'NAME_HOUSING_TYPE': housing_dict.get(values['housing']),
                     'JOB': job_dict.get(values['job']), 'BEGIN_MONTHS': emp_days,
                     'AMT_INCOME_TOTAL': values['income'], 'FLAG_MOBIL': mobile_dict.get(values['mobile']),
                     'FLAG_WORK_PHONE': work_phone_dict.get(values['workphone']),
                     'FLAG_PHONE': phone_dict.get(values['residentialphone']),
                     'FLAG_EMAIL': email_dict.get(values['email']), 'STATUS': status_dict.get(status1)}

        # df = df.append(new_row11, ignore_index=True) # Original implementation for dataframe

        row1 = np.array(new_row1)
        row2 = np.array(new_row2)
        row3 = np.array(new_row3)
        row4 = np.array(new_row4)

        pd.set_option('display.max_rows', None, 'display.max_columns', None)

        risk = predict.predict(row1, row2, row3, row4)

        report_layout = [
            [sg.Text('NAME: ' + fname + " " + lname, font=("Arial", 15))],
            [sg.Text('CONTACT: ' + number, font=("Arial", 15)), sg.Text('EMAIL: ' + email_address, font=("Arial", 15))],
            [sg.Text('RISK ASSESSMENT: ' + risk, font=("Arial", 16), background_color='#470505', pad=(0, 10))]]

        window2 = sg.Window('Risk Assessment', layout=report_layout).Read()

    if event == 'Investigate Database':  # for graphs/ analytics
        window3 = createTrendWindow()

        while True:
            event1, values = window3.Read()
            if event1 == sg.WIN_CLOSED or event1 == 'Exit':
                window3.Close()
                break

            if event1 == 'High Risk Age':
                trends.highRiskAge()

            if event1 == 'Low Risk Age':
                trends.lowRiskAge()

            if event1 == 'High Risk Gender':
                trends.highRiskGender()

            if event1 == 'Low Risk Gender':
                trends.lowRiskGender()

            if event1 == 'High Risk Family':
                trends.highRiskFamily()

            if event1 == 'Low Risk Family':
                trends.lowRiskFamily()

            if event1 == 'High Risk Education':
                trends.highRiskEducation()

            if event1 == 'Low Risk Education':
                trends.lowRiskEducation()

            if event1 == 'High Risk Children':
                trends.highRiskChildren()

            if event1 == 'Low Risk Children':
                trends.lowRiskChildren()

            if event1 == 'High Risk Job':
                trends.highRiskJob()

            if event1 == 'Low Risk Job':
                trends.lowRiskJob()

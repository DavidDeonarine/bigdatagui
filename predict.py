# Script to produce prediction
def predict(row1, row2, row3, row4):
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from imblearn.over_sampling import SMOTE
    from imblearn.under_sampling import RandomUnderSampler
    from sklearn.ensemble import RandomForestClassifier

    print("Prediction in Progress!")
    df = pd.read_csv('credit_card_approval.csv')
    df.head()
    df = df.drop(columns=['ID'])
    df.head()

    # print('\nModifiying Ages')
    df['DAYS_BIRTH'] = (df['DAYS_BIRTH'] * -1) // 365
    df.rename(columns={'DAYS_BIRTH': 'AGE'}, inplace=True)

    sm = SMOTE(sampling_strategy=0.25)
    under = RandomUnderSampler(sampling_strategy=0.7)

    X = df.drop(columns=['TARGET']).copy()
    X = np.array(X)
    y = df['TARGET']

    mappings = {}
    for col in df:
        if df[col].dtype == 'O':
            col_names = df[col].unique()
            encoder = LabelEncoder()
            df[col] = encoder.fit_transform(df[col])
            mappings[col] = (list(col_names), list(df[col].unique()))
    df.head()

    X = df.drop(columns=['TARGET']).copy()
    X = np.array(X)
    y = df['TARGET']

    x_train, x_test, y_train, y_test = train_test_split(X, y, stratify=y)

    # Over sampling and under sampling to balance data
    x_train_res, y_train_res = sm.fit_resample(x_train, y_train.ravel())
    x_train_res, y_train_res = under.fit_resample(x_train_res, y_train_res.ravel())

    # Random Forest Classifier
    clf_rf = RandomForestClassifier(n_estimators=50)
    clf_rf.fit(x_train_res, y_train_res)

    y_pred_rf1 = clf_rf.predict(row1)
    y_pred_rf2 = clf_rf.predict(row2)
    y_pred_rf3 = clf_rf.predict(row3)
    y_pred_rf4 = clf_rf.predict(row4)

    print(str(y_pred_rf1) + "\t" + str(y_pred_rf2) + "\t" + str(y_pred_rf3) + "\t" + str(y_pred_rf4))

    check = y_pred_rf1 + y_pred_rf2 + y_pred_rf3 + y_pred_rf4
    print("Check: " + str(check))
    print("Prediction Complete!\n")
    if check > 1:
        return "ATTENTION: You are currently high risk!"
    return "CONGRATULATIONS: You are currently low risk!"

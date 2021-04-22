# Script to find best classifier for the predictions. See Notebook for better information.
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import plot_confusion_matrix

df = pd.read_csv('credit_card_approval.csv')
df.head()
df = df.drop(columns=['ID'])
df.head()

print('\nModifiying Ages')
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

x_train_res, y_train_res = sm.fit_resample(x_train, y_train.ravel())
x_train_res, y_train_res = under.fit_resample(x_train_res, y_train_res.ravel())

print("Before OverSampling, counts of label '1': {}".format(sum(y_train == 1)))
print("Before OverSampling, counts of label '0': {} \n".format(sum(y_train == 0)))

print("After OverSampling, counts of label '1': {}".format(sum(y_train_res == 1)))
print("After OverSampling, counts of label '0': {}".format(sum(y_train_res == 0)))

print('\nOversampling and Undersampling with Logistic Regression')
clf_logreg = LogisticRegression(max_iter=500)
clf_logreg.fit(x_train_res, y_train_res)
y_pred_logreg = clf_logreg.predict(x_test)

plot_confusion_matrix(clf_logreg, x_test, y_test)
#plt.show()

print("Accuracy Score: ", accuracy_score(y_test, y_pred_logreg))
print("F1 Score: ", f1_score(y_test, y_pred_logreg))

print('\nOversampling and Undersampling with LinearSVC')
clf_svm = LinearSVC(max_iter=1000)
clf_svm.fit(x_train_res, y_train_res)
y_pred_svm = clf_svm.predict(x_test)

plot_confusion_matrix(clf_svm, x_test, y_test)
#plt.show()

print("Accuracy Score: ", accuracy_score(y_test, y_pred_svm))
print("F1 Score: ", f1_score(y_test, y_pred_svm))

print('\nOversampling and Undersampling with Gaussian Naive Bayes')
clf_gnb = GaussianNB()
clf_gnb.fit(x_train_res, y_train_res)
y_pred_gnb = clf_gnb.predict(x_test)

plot_confusion_matrix(clf_gnb, x_test, y_test)
#plt.show()

print("Accuracy Score: ", accuracy_score(y_test, y_pred_gnb))
print("F1 Score: ", f1_score(y_test, y_pred_gnb))

print('\nOversampling and Undersampling with Random Forest Classifier')
clf_rf = RandomForestClassifier(n_estimators=50)
clf_rf.fit(x_train_res, y_train_res)
y_pred_rf = clf_rf.predict(x_test)

plot_confusion_matrix(clf_rf, x_test, y_test)
#lt.show()

print("Accuracy Score: ", accuracy_score(y_test, y_pred_rf))
print("F1 Score: ", f1_score(y_test, y_pred_rf))

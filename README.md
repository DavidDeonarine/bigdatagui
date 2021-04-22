# Using a Machine Learning Model to Classify High-Risk and Low-Risk Credit Card Customers


## Pre-Requisites
Our GUI and Machine Learning model requires the following libraries to operate as intended.
1. pandas
2. PySimpleGUI
3. seaborn
4. sklearn
5. imblearn
 
## Overview
Studies involving the financial sector, such as credit cards and the risks associated with them have been prominent areas of investigation in recent times. Because of the high risk that is involved with lending money, banking institutions have utilized quantitative metrics such as credit score ratings to determine the customer’s credit risk. With the advancements in machine learning and artificial intelligence, it was hypothesized that a machine learning model can be developed and trained on previous risk assessments to predict a person’s credit risk.

To test this hypothesis, a comprehensive dataset with predetermined class labels was obtained as the training set for this model. Before selecting a single classifier, investigations were done to determine the best model based on the reported accuracy and F1 scores. For the purpose of this model, the Random Forest Classifier (RFC) with an accuracy score of 0.9999 and an F1 score of 0.9989 was implemented. 

In order to make this classifier accessible to users, a graphical user interface (GUI) was created backed by the PySimpleGUI library. This functional interface not only allowed for investigation of the dataset, but also requested seventeen main features from the user in addition to other personal identifiers. Backed by the trained RFC, four predictions were generated based on the user's supplied data and payment history for 4 consecutive months. If the user was determined to be high risk for two or more of these months, an overall ‘High Risk’ was assigned to the user and displayed via the GUI. Otherwise, a ‘Low Risk’ status was assigned and displayed respectively. The use of the average in this model prevents a person from being unfairly treated by not assigning a risk based on one bad month.

From testing, no false positives nor false negatives were predicted by the trained model which demonstrates that a machine learning model, facilitated by the random forest classifier can be used to classify high-risk and low-risk credit card customers. 

The full report of our project can be found at https://www.overleaf.com/read/tcgyqpfwfptv

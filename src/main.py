import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # setting the path of this project one level up (otherwise it can't find other files)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from Machine_Learning.prediction import average_classification_result
from streamlit_ui import create_student_form
from cloud.students_query import students_query, grade_query, absences_query, failure_query
from transformation.student_comparison import calc_student_comparison

project_id = 'bdt-2024'
dataset_id = 'Students_table_of_records'  
table_id = 'students_rec'
if os.path.exists(os.path.join("cloud", "bdt-2024-accesskey.json")):
    service_account_path = os.path.join("cloud", "bdt-2024-accesskey.json")
else:
    service_account_path = '../cloud/bdt-2024-accesskey.json'

def main():
    st.title("Welcome")
    st.subheader('Please provide your information below', divider='red')
    df_submit = create_student_form()
    
    if df_submit is not None:
        st.subheader('Your Report:', divider='green')
        pred_result = make_prediction(df_submit=df_submit)
        st.write(pred_result.loc[0])
        course_result, subject_result = get_KPIs(df_submit=df_submit)
        st.dataframe(data=course_result)
        st.dataframe(data=subject_result)
        build_graph(course_result, subject_result)
        

def make_prediction(df_submit):
    # for prediction
    student_id = df_submit.loc[0,'Student_P_ID']
    # print("student ID: " + student_id.astype(str))
    avg_grade = grade_query(project_id, dataset_id, table_id, service_account_path, student_id)
    total_absences = absences_query(project_id, dataset_id, table_id, service_account_path, student_id)
    total_failures = failure_query(project_id, dataset_id, table_id, service_account_path, student_id)
    print(avg_grade, total_absences, total_failures)

    df_pred = df_submit
    df_pred['absences'] = total_absences / 10
    df_pred['AVG_G'] = avg_grade / 30      # needs to be normalized
    df_pred['failures'] = total_failures
    df_pred = df_pred.drop(['Student_P_ID', 'DisplayName'], axis=1)

    pred_result = average_classification_result(df_submit=df_pred)           
    
    st.markdown("Prediction result if you have good chances to succeed with your studies:")
    pred_dict = {0: 'No', 1: 'Yes'}
    pred_result.replace(pred_dict, inplace=True)

    return pred_result

def get_KPIs(df_submit):
    student_id = df_submit.loc[0,'Student_P_ID']
    print("student ID KPI: " + student_id.astype(str))
    df_tor = students_query(project_id, dataset_id, table_id, service_account_path, student_id)
    course_result, subject_result = calc_student_comparison(df=df_tor, student_id=student_id)

    
    
    
    return course_result, subject_result
    
    


def build_graph(course_result, subject_result):
    student_coursegrade= float(course_result.loc[0,"own_grade"])
    course_distr= pd.DataFrame(course_result.at[0, "course_grade_dist"])
    print("here are the datsets:",course_distr, student_coursegrade)
    # Use Streamlit's built-in plotting
    fig = plt.figure(figsize=(10, 6))
    sns.histplot(data=course_distr, kde=True)
    plt.axvline(student_coursegrade, color='red', linestyle='dashed', linewidth=2, label='Your Grade')
    plt.title('Distribution of Final Grades')
    plt.xlabel('Final Grade')
    plt.ylabel('Count')
    plt.legend()
    
    # Display the plot using Streamlit
    st.pyplot(fig)
    
    
    return 
    


if __name__ == "__main__":
    main()
    

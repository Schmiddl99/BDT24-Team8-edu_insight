import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # setting the path of this project one level up (otherwise it can't find other files)

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Machine_Learning.prediction import average_classification_result
# from streamlit_ui import create_student_form
from cloud.students_query import students_query, grade_query, abseces_query, failure_query
from scipy.stats import percentileofscore

pd.options.display.max_columns = None       # type: ignore

project_id = 'bdt-2024'
dataset_id = 'Students_table_of_records'  
table_id = 'students_data'
service_account_path = '../cloud/bdt-2024-accesskey.json'


def calc_student_comparison(df, student_id):
    course_result = []
    subject_result = []
    course_grade_dist = []
    
    student_df = df[df['studentID'] == student_id] 
    course_names = student_df['course_name'].unique()
    subjects = student_df['subject'].unique()  

    ## course distribution
    own_course_grade = grade_query(project_id, dataset_id, table_id, service_account_path, student_id)

    course_comp = df[df['course_name'] == str(course_names[0])]
    unique_Student_IDs = course_comp['studentID'].unique()

    for ID in unique_Student_IDs:
        filtered_df = df[df['studentID'] == ID]
        grade_of_ID = (filtered_df['grade'] * filtered_df['credits']).sum() / filtered_df['credits'].sum()
        course_grade_dist.append(round(grade_of_ID, 1))
        # print(str(ID) + ": " + str(course_grade_dist))

    course_grade_dist = [0 if np.isnan(x) else x for x in course_grade_dist]
    # print(course_grade_dist)
    
    course_percentile = float(own_course_grade.loc[0, 'weighted_average_grade']) / max(course_grade_dist) * 100     # type:ignore
    # print(course_percentile)

    course_result.append({
                'course_name': course_names[0],
                'own_grade': own_course_grade.iloc[0,0],
                'subject_grade_dist': course_grade_dist,
                'percentile_course': round(course_percentile)
            })

    
    ## subject distribution
    for subject in subjects:
        subject_grade_dist = []

        own_subject_grade = student_df.query('subject == @subject')['grade']
        # print(own_subject_grade)

        subject_comp = df[df['subject'] == subject]
        unique_Student_IDs = subject_comp['studentID'].unique()

        for ID in unique_Student_IDs:
            filtered_df = df[(df['studentID'] == ID) & (df['subject'] == subject)]
            grade_of_ID = (filtered_df['grade'] * filtered_df['credits']).sum() / filtered_df['credits'].sum()
            subject_grade_dist.append(round(grade_of_ID, 1))
            # print(str(ID) + " -> " + str(subject) + ": " + str(subject_grade_dist))

        subject_grade_dist = [0 if np.isnan(x) else x for x in subject_grade_dist]
        subject_grade_dist.insert(0, own_subject_grade.iloc[0])
        
        subject_percentile = float(own_subject_grade.iloc[0]) / max(subject_grade_dist) * 100
        
        subject_result.append({
                'subject': subject,
                'own_grade': own_subject_grade.iloc[0],
                'subject_grade_dist': subject_grade_dist,
                'percentile_course': round(subject_percentile)
            })
        
        # print(pd.DataFrame(subject_result))

    print(pd.DataFrame(course_result))
    print(pd.DataFrame(subject_result))
    
    return pd.DataFrame(course_result), pd.DataFrame(subject_result) 
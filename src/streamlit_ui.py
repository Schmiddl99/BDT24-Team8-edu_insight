import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # setting the path of this project one level up (otherwise it can't find other files)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Machine_Learning.prediction import average_classification_result


def create_student_form():
    st.text("\t \t \t")
    with st.form("student_form"):
        st.subheader("Basic Information")
        name = st.text_input("How should we call you?")
        student_ID = st.number_input('Input Student ID', min_value=1000, max_value=9999, value="min", step=1)
        sex = st.radio("Gender", ["Female", "Male"])
        
        address = st.radio("Address Type", ["Urban", "Rural"])
        famsize = st.radio("Family Size", ["less or equal to 3", "greater then 3"])
        romantic = st.checkbox("Are you currently in a romantic relationship?")

        # Parents' Information
        st.subheader("Parents' Information")
        st.markdown("Provide your parents' education status")
        medu = st.selectbox("Mother's Education", ["None", "Primary education (4th grade)", "5th to 9th grade", "Secondary education", "Higher education"])   
        fedu = st.selectbox("Father's Education", ["None", "Primary education (4th grade)", "5th to 9th grade", "Secondary education", "Higher education"])
        pstatus = st.radio("Parents' Status", ["Living together", "Living apart"])

        # Education
        st.subheader("Education")
        
        st.markdown("From 1 to 4 indicate: (look for the '?' to get help)")        
        traveltime = st.slider("Average travel time to school", 1, 4, value=2, format="%d", help="1 - <15 min., 2 - 15 to 30 min., 3 - 30 min. to 1 hour, or 4 - >1 hour")
        studytime = st.slider("Weekly study time", 1, 4, value=2, format="%d", help="1 - <2 hours, 2 - 2 to 5 hours, 3 - 5 to 10 hours, or 4 - >10 hours")
        failures = st.number_input("Number of past class failures", 0, 3, value=0)
        schoolsup = st.checkbox("Extra educational support")
        famsup = st.checkbox("Family educational support")
        activities = st.checkbox("Extra-curricular activities")

        # Lifestyle
        st.subheader("Lifestyle")
        st.markdown("From 1 to 5 indicate how much you consider the following activities")

        famrel = st.slider("Spending quality time with your family", 1, 5, value=3, help="From 1 - very bad to 5 - excellent")
        freetime = st.slider("Free time after school", 1, 5, value=3, help="From 1 - very low to 5 - very high")
        goout = st.slider("Going out with friends", 1, 5, value=3, help="From 1 - very low to 5 - very high")
        dalc = st.slider("Workday alcohol consumption", 1, 5, value=1, help="From 1 - very low to 5 - very high")
        walc = st.slider("Weekend alcohol consumption", 1, 5, value=1, help="From 1 - very low to 5 - very high")
        health = st.slider("Current health status", 1, 5, value=3, help="From 1 - very bad to 5 - very good")
        

        submitted = st.form_submit_button("Submit")
        if submitted:
            data = {
                'Student_P_ID': [student_ID],  
                'DisplayName': [name],  
                'sex': [sex],
                'address': [address],
                'famsize': [famsize],
                'Pstatus': [pstatus],
                'Medu': [medu],
                'Fedu': [fedu],
                'traveltime': [traveltime],
                'studytime': [studytime],
                'failures': [failures],
                'schoolsup': [schoolsup],
                'famsup': [famsup],
                'activities': [activities],
                'romantic': [romantic],
                'famrel': [famrel],
                'freetime': [freetime],
                'goout': [goout],
                'Dalc': [dalc],
                'Walc': [walc],
                'health': [health]       
            }
            replace_dict = {'Female': 0, 'Male': 1, 'Urban': 0, 'Rural': 1, 'less or equal to 3': 0, 'greater then 3': 1, 
                            'Living together': 0, 'Living apart': 1, 'true': 1, 'false': 0,
                            'None': 0, 'Primary education (4th grade)': 1, '5th to 9th grade': 2, 'Secondary education': 3, 'Higher education': 4}
            df_submit = pd.DataFrame(data)
            df_submit.replace(replace_dict, inplace=True)
            
            st.success("Form submitted successfully!")

            return df_submit


def display_performance_graphs(data):
    st.header("Student Performance Graphs")

    # Overall Grade Distribution
    st.subheader("Overall Grade Distribution")
    fig, ax = plt.subplots()
    sns.histplot(data=data, x="G3", bins=20, ax=ax)
    ax.set_title("Distribution of Final Grades")
    ax.set_xlabel("Final Grade")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # Grade Distribution by School
    st.subheader("Grade Distribution by School")
    fig, ax = plt.subplots()
    sns.histplot(data=data, x="G3", hue="school", bins=20, ax=ax)
    ax.set_title("Final Grade Distribution by School")
    ax.set_xlabel("Final Grade")
    ax.set_ylabel("Count")
    ax.legend(title="School")
    st.pyplot(fig)

    # Grade Distribution by Sex
    st.subheader("Grade Distribution by Sex")
    fig, ax = plt.subplots()
    sns.histplot(data=data, x="G3", hue="sex", bins=20, ax=ax)
    ax.set_title("Final Grade Distribution by Sex")
    ax.set_xlabel("Final Grade")
    ax.set_ylabel("Count")
    ax.legend(title="Sex")
    st.pyplot(fig)
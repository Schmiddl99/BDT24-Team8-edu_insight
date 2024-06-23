import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests


if __name__ == "__main__":
    main()
    
def create_student_form():
    st.header("Student Information Form")
    with st.form("student_form"):
        # Basic Information
        col1, col2, col3 = st.columns(3)
        with col1:
            school = st.selectbox("School", ["GP - Gabriel Pereira", "MS - Mousinho da Silveira"])
            sex = st.radio("Sex", ["F - Female", "M - Male"])
            age = st.slider("Age", 15, 22, value=18)
        with col2:
            address = st.radio("Address Type", ["U - Urban", "R - Rural"])
            famsize = st.radio("Family Size", ["LE3 - ≤3", "GT3 - >3"])
            pstatus = st.radio("Parents' Status", ["T - Living together", "A - Apart"])
        with col3:
            guardian = st.selectbox("Guardian", ["Mother", "Father", "Other"])
            internet = st.checkbox("Internet access at home")
            romantic = st.checkbox("In a romantic relationship")

        # Parents' Information
        st.subheader("Parents' Information")
        col1, col2 = st.columns(2)
        with col1:
            medu = st.selectbox("Mother's Education", ["None", "Primary education (4th grade)", "5th to 9th grade", "Secondary education", "Higher education"])
            mjob = st.selectbox("Mother's Job", ["Teacher", "Health care related", "Civil Services", "At Home", "Other"])
        with col2:
            fedu = st.selectbox("Father's Education", ["None", "Primary education (4th grade)", "5th to 9th grade)", "Secondary education", "Higher education"])
            fjob = st.selectbox("Father's Job", ["Teacher", "Health care related", "Civil Services", "At Home", "Other"])

        # Education
        st.subheader("Education")
        reason = st.selectbox("Reason for choosing this school", ["Close to home", "School reputation", "Course preference", "Other"])
        traveltime = st.slider("Travel time to school (minutes)", 1, 4, value=2, format="%d", help="1 - <15 min., 2 - 15 to 30 min., 3 - 30 min. to 1 hour, or 4 - >1 hour")
        studytime = st.slider("Weekly study time (hours)", 1, 4, value=2, format="%d", help="1 - <2 hours, 2 - 2 to 5 hours, 3 - 5 to 10 hours, or 4 - >10 hours")
        failures = st.number_input("Number of past class failures", 0, 3, value=0)
        schoolsup = st.checkbox("Extra educational support")
        famsup = st.checkbox("Family educational support")
        paid = st.checkbox("Extra paid classes within the course subject")
        activities = st.checkbox("Extra-curricular activities")
        nursery = st.checkbox("Attended nursery school")
        higher = st.checkbox("Wants to take higher education")

        # Lifestyle
        st.subheader("Lifestyle")
        famrel = st.slider("Quality of family relationships", 1, 5, value=3, help="From 1 - very bad to 5 - excellent")
        freetime = st.slider("Free time after school", 1, 5, value=3, help="From 1 - very low to 5 - very high")
        goout = st.slider("Going out with friends", 1, 5, value=3, help="From 1 - very low to 5 - very high")
        dalc = st.slider("Workday alcohol consumption", 1, 5, value=1, help="From 1 - very low to 5 - very high")
        walc = st.slider("Weekend alcohol consumption", 1, 5, value=1, help="From 1 - very low to 5 - very high")
        health = st.slider("Current health status", 1, 5, value=3, help="From 1 - very bad to 5 - very good")
        absences = st.number_input("Number of school absences", 0, 93, value=0)

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Form submitted successfully!")
            # Here you would typically save the data or process it further

def main():
    st.title("Student Data Entry")
    create_student_form()

if __name__ == "__main__":
    main()

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

def main():
    st.title("Student Data Entry")
    create_student_form()

    # Load sample data (you can replace this with your actual data)
    data = pd.read_csv("/workspaces/BDT24-Team8/Data/Predict_student_performance/student.txt")

    # Display performance graphs
    display_performance_graphs(data)

if __name__ == "__main__":
    main()
    
    
    
    
    ###
#def main():
    #st.title("FastAPI Integration")

    # Call the root endpoint
    #response = requests.get("http://127.0.0.1:8000/")
    #root_message = response.json()["message"]
    #st.write(f"Root endpoint message: {root_message}")

    # Call the /hello endpoint
    #response = requests.get("http://127.0.0.1:8000/hello")
    #hello_message = response.json()["message"]
    #st.write(f"Hello endpoint message: {hello_message}")
###
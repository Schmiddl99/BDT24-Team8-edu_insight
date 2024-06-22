import pandas as pd
import joblib
import numpy as np
import os

def average_classification_result(df_submit):
    """
    Load models, test input data against them, aggregate the classification results,
    and return the average result.

    :param df_submit: DataFrame containing the input data.
    :param model_paths: List of paths to the saved models.
    :return: Series containing the average classification result for each instance.
    """

    # Paths to the saved models
    model_paths = [
        "best_DecisionTree_model_without_AVG_G.pkl",
        "best_GradientBoosting_model_without_AVG_G.pkl",
        "best_KNeighbors_model_without_AVG_G.pkl",
        "best_LogisticRegression_model_without_AVG_G.pkl",
        "best_MLPClassifier_model_without_AVG_G.pkl",
        "best_NaiveBayes_model_without_AVG_G.pkl",
        "best_RandomForest_model_without_AVG_G.pkl",
        "best_SVC_model_without_AVG_G.pkl"
    ]

    model_paths2 = [
        "best_KNeighbors_model_with_AVG_G.pkl",
        "best_LogisticRegression_model_with_AVG_G.pkl",
        "best_MLPClassifier_model_with_AVG_G.pkl",
        "best_NaiveBayes_model_with_AVG_G.pkl",
        "best_SVC_model_with_AVG_G.pkl"
    ]
    
    # Load models
    models = []
    for path in model_paths2:
        try:
            models.append(joblib.load(os.path.join(os.path.dirname(__file__),path)))
        except FileNotFoundError as e:
            print(f"Error loading {path}: {e}")
            continue

    if not models:
        raise ValueError("No models were successfully loaded. Please check the model paths.")

    # Ensure df_submit contains only the features expected by the models
    feature_columns = models[0].n_features_in_
    input_data = df_submit.iloc[:, :feature_columns]

    # Collect predictions from each model
    predictions = []

    for model in models:
        preds = model.predict(input_data)
        predictions.append(preds)

    # Convert list of arrays to a DataFrame for easier aggregation
    predictions_df = pd.DataFrame(predictions)
    print(predictions_df)

    # Calculate the average prediction for each instance
    # Average will be between 0 and 1; round to get binary classification
    average_predictions = predictions_df.mean(axis=0).round()

    return average_predictions


## uncomment for debugging purposes

# def main():
#     # Define the input data (example data)
#     data = {
#         'Student_P_ID': [1000],
#         'DisplayName': ['Alice'],
#         'sex': ['Female'],
#         'address': ['Urban'],
#         'famsize': ['less or equal to 3'],
#         'Pstatus': ['Living together'],
#         'Medu': ['Secondary education'],
#         'Fedu': ['Secondary education'],
#         'traveltime': [1],
#         'studytime': [2],
#         'failures': [0],
#         'schoolsup': [True],
#         'famsup': [True],
#         'activities': [False],
#         'romantic': [False],
#         'famrel': [4],
#         'freetime': [3],
#         'goout': [4],
#         'Dalc': [1],
#         'Walc': [1],
#         'health': [5]
#     }

#     # Create a DataFrame from the dictionary
#     df_submit = pd.DataFrame(data)
#     replace_dict = {'Female': 0, 'Male': 1, 'Urban': 0, 'Rural': 1, 'less or equal to 3': 0, 'greater then 3': 1, 
#                     'Living together': 0, 'Living apart': 1, 'true': 1, 'false': 0,
#                     'none': 0, 'Primary education (4th grade)': 1, '5th to 9th grade': 2, 'Secondary education': 3, 'Higher education': 4}
#     df_submit = pd.DataFrame(data)
#     df_submit.replace(replace_dict, inplace=True)

#     # for prediction testing
#     Grade = 23 / 30     # needs to be normalized
#     df_pred = df_submit
#     df_pred['absences'] = 5
#     df_pred['AVG_G'] = Grade
#     df_pred = df_pred.drop(['Student_P_ID', 'DisplayName'], axis=1)
#     print(df_pred)

#     # Get average classification result
#     try:
#         avg_result = average_classification_result(df_pred)
#         print("Average Classification Result:")
#         print(avg_result)
#     except ValueError as e:
#         print(e)

# if __name__ == "__main__":
#     main()
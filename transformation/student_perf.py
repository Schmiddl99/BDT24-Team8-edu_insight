import dask.dataframe as ddf
import pandas as pd

class StudentPerformance:
    def __init__(self, student_perf_raw, keep_columns, conv_columns, replace_dict, grades):
        self.student_perf_raw = student_perf_raw
        self.keep_columns = keep_columns
        self.conv_columns = conv_columns
        self.replace_dict = replace_dict
        self.grades = grades
        self.paths = self.load_paths()
        self.dataframes = self.load_dataframes()
        self.transformed_dfs = self.transform_dfs()
        self.student_perf = self.concat_and_normalize()
        
    def load_paths(self):
        paths = []
        for file in self.student_perf_raw:
            paths.append('Data/Predict_student_performance/' + file)
        return paths

    def load_dataframes(self):
        dfs = []
        for path in self.paths:
            df = ddf.read_csv(path=path, sep=';')
            dfs.append(df)
        return dfs

    def transform_dfs(self):
        transformed_dfs = []
        for df in self.dataframes:
            df = df[self.keep_columns]
            df = df.replace(self.replace_dict)
            df = df.dropna()

            for column in self.conv_columns:
                df[column] = df[column].astype('bool')

            transformed_dfs.append(df.compute())
        return transformed_dfs

    def concat_and_normalize(self):
        student_perf = ddf.concat(self.transformed_dfs)

        for grade in self.grades:
            student_perf[grade] = (student_perf[grade] - 0) / (20 - 0)

        student_perf['AVG_G'] = student_perf[self.grades].mean(axis=1)
        student_perf = student_perf.drop(self.grades, axis=1)
        student_perf['passed'] = student_perf['AVG_G'] >= 0.6
        
        return student_perf

    def get_student_performance(self):
        return self.student_perf
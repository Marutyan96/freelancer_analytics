import pandas as pd
import os

class Database:
    def __init__(self, data_path):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Файл {data_path} не найден")
        self.df = pd.read_csv(data_path)
        required_columns = ['Earnings_USD', 'Payment_Method', 'Client_Region', 'Experience_Level', 'Job_Completed']
        if not all(col in self.df.columns for col in required_columns):
            raise ValueError(f"CSV должен содержать столбцы: {required_columns}")
    
    def get_data(self):
        return self.df
    
    def filter_by_payment_method(self, method):
        return self.df[self.df['Payment_Method'] == method]
    
    def group_by_region(self):
        return self.df.groupby('Client_Region')['Earnings_USD'].agg(['mean', 'count']).reset_index()
    
    def expert_project_stats(self, threshold=100):
        experts = self.df[self.df['Experience_Level'] == 'Expert']
        below_threshold = experts[experts['Job_Completed'] < threshold]
        return len(below_threshold) / len(experts) * 100 if len(experts) > 0 else 0
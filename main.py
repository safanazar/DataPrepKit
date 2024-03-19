import pandas as pd
import numpy as np
import logging
from sklearn.preprocessing import LabelEncoder

class DataPrepKit:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.read_data()

    def read_data(self):
        try:
            file_extension = self.file_path.split('.')[-1]
            if file_extension == 'csv':
                df = pd.read_csv(self.file_path)
            elif file_extension == 'xlsx':
                df = pd.read_excel(self.file_path)
            elif file_extension == 'json':
                df = pd.read_json(self.file_path)
            else:
                raise ValueError("Unsupported file format. Please use CSV, Excel, or JSON.")
        except Exception as e:
            logging.error(f"Error reading data: {str(e)}")
            raise
        return df

    def data_summary(self, columns=None):
        if columns is None:
            columns = self.df.columns

        summary = {}
        for column in columns:
            try:
                data = pd.to_numeric(self.df[column], errors='coerce')
                summary[column] = {
                    'Mean': data.mean(),
                    'Median': data.median(),
                    'Mode': data.mode()[0],
                    'Standard Deviation': data.std(),
                    'Min': data.min(),
                    '25%': data.quantile(0.25),
                    '50%': data.quantile(0.50),
                    '75%': data.quantile(0.75),
                    'Max': data.max()
                }
            except ValueError:
                pass
        return summary

    def handle_missing_values(self, columns=None, strategy='remove'):
        if columns is None:
            columns = self.df.columns

        try:
            if strategy == 'remove':
                self.df = self.df.dropna(subset=columns)
            elif strategy in ['mean', 'median', 'mode']:
                fill_value = getattr(self.df[columns], strategy)()
                self.df[columns] = self.df[columns].fillna(fill_value)
        except Exception as e:
            logging.error(f"Error handling missing values: {str(e)}")
            raise

    def categorical_data_encoding(self, columns=None):
        if columns is None:
            columns = self.df.select_dtypes(include=['object']).columns

        try:
            encoder = LabelEncoder()
            self.df[columns] = self.df[columns].apply(encoder.fit_transform)
        except Exception as e:
            logging.error(f"Error encoding categorical data: {str(e)}")
            raise
        return self.df

    def deploy_package(self):
        # Add package deployment code here
        pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    try:
        file_path = 'data.csv'
        data_prepper = DataPrepKit(file_path)
        logging.info("Data read successfully.")

        logging.info("Original DataFrame:")
        print(data_prepper.df)

        data_prepper.handle_missing_values(strategy='mean')
        logging.info("DataFrame after handling missing values:")
        print(data_prepper.df)

        summary = data_prepper.data_summary()
        logging.info("Summary of DataFrame:")
        print(summary)

        encoding_df = data_prepper.categorical_data_encoding()
        logging.info("DataFrame after categorical data encoding:")
        print(encoding_df)
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
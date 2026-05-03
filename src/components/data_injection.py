import os
import sys
from src.exceptions import CustomerException
from src.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig


import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from dataclasses import dataclass


@dataclass  # this class is used to access the variable anywhere in other class by initilaze it in the __init__():
class DataInjectionConfig:
    
    train_data_path: str = os.path.join('artifacts','train.csv')
    test_data_path: str = os.path.join('artifacts','test.csv')
    raw_data_path: str = os.path.join('artifacts','raw_data.csv')


class DataInjection:
    def __init__(self):
        self.injection_config = DataInjectionConfig()

    def initiate_data_injection(self):
        logging.info("Data Injection method has started")
        try:
            # read dat acan be anywhere this is the line like database , api, website ...anywhere 
            df = pd.read_csv("data/stud.csv")  # type: ignore
            logging.info("Reading  the dataset as dataframe")

            #making folder for train data makedirs --> it will create the no of files because it is makedirs not makedir
            os.makedirs(os.path.dirname(self.injection_config.train_data_path),exist_ok=True)
            

            df.to_csv(self.injection_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.injection_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.injection_config.test_data_path,index=False,header=True)

            logging.info("Data Injection is C0mplete")

            return (
                self.injection_config.train_data_path,
                self.injection_config.test_data_path
            )
        except Exception as e:
            raise CustomerException(e,sys) # type: ignore

if __name__ == "__main__":
    logging.info("Data Injection has started")
    obj = DataInjection()
    train_data,test_data = obj.initiate_data_injection()

    data_transformation = DataTransformation()
    data_transformation.initiate_transformation(train_data,test_data)
    
    print("It is Working Fine")

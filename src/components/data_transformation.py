import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exceptions import CustomerException
from src.logger import logging
from src.utilis import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifacts','preprocessor.pkl')


class DataTransformation:
    '''
    This Function is responsile for data transformation.
    
    '''
    def __init__(self) -> None:
        self.transformation_config = DataTransformationConfig()

    def get_transformer_object(self):
        try:
            numerical_column = ["reading_score","writing_score"]
            categorical_column =["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )

            cat_pipeline =Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder(sparse_output=False)),
                    ("scaler",StandardScaler())
                ]
            )

            logging.info(f"Categorical columns :{categorical_column}")
            logging.info(f"Numerical columns :{numerical_column}")

            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline",num_pipeline,numerical_column),
                    ("categorical_pipeline",cat_pipeline,categorical_column)
                ]
            )

            return preprocessor


        except Exception as e:
            raise CustomerException(e,sys) #type: ignore
        
    def initiate_transformation(self,train_path,test_path):
        logging.info("Data Transformation has been Initiated ")
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading train and test data are Completed")

            logging.info("Obtaining Preprocessing objects")

            preprocessing_obj = self.get_transformer_object()
            target_column_name = "math_score"
            #numerical_columns = ["writing_score","reading_score"]

            input_feature_train_df = train_df.drop(columns=[target_column_name])
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name])
            target_feature_test_df = test_df[target_column_name]


            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)


            train_arr = np.c_[
                input_feature_train_arr ,np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr ,np.array(target_feature_test_df)
            ]

            logging.info("Saved preprocessing Object.")

            save_object(
                file_path = self.transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )


            return (
                train_arr,
                test_arr,
                self.transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomerException(e,sys) #type: ignore
import os
import numpy as np
import pandas as pd
import hsfs
import joblib


class Predict(object):

    def __init__(self):
        """ Initializes the serving state, reads a trained model"""        
        # get feature store handle
        fs_conn = hsfs.connection()
        self.fs = fs_conn.get_feature_store()
        
        # get feature view
        self.fv = self.fs.get_feature_view("electricity_feature_view", 1)
        
        # initialize serving
        self.fv.init_serving(1)

        # load the trained model
        self.model = joblib.load(os.environ["ARTIFACT_FILES_PATH"] + "/dk_electricity_model.pkl")
        print("Initialization Complete")

    
    def predict(self, timestamp_value, date_value):
        """ Serves a prediction request usign a trained model"""
        # Retrieve feature vectors
        feature_vector = self.fv.get_feature_vector(
            entry = {['timestamp','date']: [timestamp_value[0], date_value[0]]}
        )
        return self.model.predict(np.asarray(feature_vector[1:]).reshape(1, -1)).tolist()

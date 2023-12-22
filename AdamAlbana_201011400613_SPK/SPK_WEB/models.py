import numpy as np
import pandas as pd
from spk_model import WeightedProduct

class Motor():

    def __init__(self) -> None:
        self.motor = pd.read_csv('data/adam_motor.csv')
        self.motors = np.array(self.motor)

    @property
    def motor_data(self):
        data = []
        for motor in self.motors:
            data.append({'id': motor[0], 'nama': motor[1]})
        return data

    @property
    def motor_data_dict(self):
        data = {}
        for motor in self.motors:
            data[motor[0]] = motor[1] 
        return data

    def get_recs(self, kriteria:dict):
        wp = WeightedProduct(self.motor.to_dict(orient="records"), kriteria)
        return wp.calculate


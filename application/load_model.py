import pickle
import application.constants as const
from copy import deepcopy

def load_model():
    print("Loading Model")
    with open(const.model_path, 'rb') as buff:
        data = pickle.load(buff)
        return {
            "model": data['model'],
            "trace": data['trace'],
            "x_shared": data['X_New_shared'],
            "f_pred": data['f_pred'],
            "scaler": data['scaler'],
            "encoder": data['encoder'],
            "gp": data['gp'],
        }

model = load_model();

def get_model():
    return deepcopy(model)


import math
import numpy as np
import pandas as pd
import csv
import application.constants as const

import theano
import pymc3 as pm

import pickle

from application.response_formatter import formatter


seed = 42

np.random.seed(seed)

globalModel = None;
globalScaler = None;
globalEncoder = None;
f_pred = None;
X_New_shared = None;
globalTrace = None;
globalGp = None;

def load_model():
    with open(const.model_path, 'rb') as buff:
        data = pickle.load(buff)
        global globalModel
        global globalTrace
        global X_New_shared
        global f_pred
        global globalScaler
        global globalEncoder
        global globalGp
        globalModel = data['model']
        globalTrace = data['trace']
        X_New_shared = data['X_New_shared']
        f_pred = data['f_pred']
        globalScaler = data['scaler']
        globalEncoder = data['encoder']
        globalGp = data['gp']

    print("Model Loaded");


def predict(sample_count=const.DEFAULT_SAMPLE_COUNT):
    with globalModel:
        pred_samples = pm.sample_posterior_predictive(globalTrace, vars=[f_pred], samples=sample_count, random_seed=42)
        y_pred, uncer = pred_samples["f_pred"].mean(axis=0), pred_samples["f_pred"].std(axis=0)
        print(y_pred)
        return y_pred

def predict_gp():
    with globalModel:
        mu, var = globalGp.predict(Xnew=X_New_shared, point=globalTrace[0], diag=True)
        print(mu)
        return mu

def predict_list(method = None, sample_count=const.DEFAULT_SAMPLE_COUNT, file_name="custom.csv"):
    dataset = pd.read_csv(const.data_path+file_name);

    X_Custom = dataset.iloc[:, [0, 1, 2]].values;
    X_Custom[:, 0] = globalEncoder.transform(X_Custom[:, 0]);
    X_Custom = globalScaler.transform(X_Custom);

    X_New_shared.set_value(X_Custom)

    if method == "NS":
        predict_gp()
    else:
        predict(sample_count=sample_count)

def predict_point(data, method = None, sample_count=const.DEFAULT_SAMPLE_COUNT):

    X_Vals = data;

    X_Vals[0] = globalEncoder.transform([X_Vals[0]])[0]
    X_Vals = globalScaler.transform([X_Vals])

    global X_New_shared
    X_New_shared.set_value(X_Vals)

    if method == "NS":
        prediction = predict_gp()
        formatter(prediction[0])
        return prediction[0]
    else:
        prediction = predict(sample_count=sample_count)
        return prediction

    sys.exit(0)

def max_tps(data, method = None, sample_count=2000):
    print("In Max TPS")
    my_list = []
    individual_predictions = []
    scenario = data[0];
    message_size = data[1];

    for concurrency in range(50, 1000, 10):
        my_list.append([scenario, concurrency, message_size])

    data_array = np.array(my_list)
    data_array[:, 0] = globalEncoder.transform(data_array[:, 0]);
    data_array = globalScaler.transform(data_array);

    X_New_shared.set_value(data_array)

    if method == "NS":
        predictions = predict_gp()
        return max(predictions)

    else:
        predictions = predict(sample_count=sample_count)
        return max(predictions)

    sys.exit(0)
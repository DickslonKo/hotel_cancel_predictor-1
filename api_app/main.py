import numpy as np
import pickle
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def machine_learning_model():

    param_hotel = request.form.get("hotel_type")
    param_month = request.form.get("number_of_people")
    param_num = request.form.get("arrival_month")

    if param_hotel is None:
        return "Please provide hotel type."
    if param_month is None:
        return "Please provide arrival month."
    if param_num is None:
        return "Please provide number of resident."
    if not param_month.isdigit():
        return "Month must be integer."
    if not param_num.isdigit():
        return "Number must be integer."
    if param_hotel == "city":
        param_hotel = "City Hotel"
    elif param_hotel == "resort":
        param_hotel = "Resort Hotel"
    else:
        return "Hotel type must be [city, resort]"

    param_month = int(param_month)
    param_num = int(param_num)

    with open('exported_one_hot.pickle', 'rb') as fp:
        enc = pickle.load(fp)

    with open('exported_classifier.pickle', 'rb') as fp:
        classifier = pickle.load(fp)

    hotel_feature = enc.transform([[param_hotel]]).toarray()
    month_feature = (param_month >= 6) and (param_month <= 8)

    features = np.hstack([
        hotel_feature,
        np.array([[month_feature]]),
        np.array([[param_num]])
    ])

    if classifier.predict(features)[0]:
        return "will not cancel"
    else:
        return "will cancel"
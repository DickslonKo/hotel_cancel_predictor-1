from flask import Flask, request, jsonify

from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

@app.route('/',methods=["GET", "POST"])
def hello_world():
    import pickle
    import numpy as np

    print(request.form)

    param_hotel = request.form.get("hotel_type")
    param_month = request.form.get("arrival_month")
    param_num = request.form.get("number_of_people")

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

    with open("api_app/exported_one_hot.pickle", "rb") as fp:
        enc = pickle.load(fp)

    with open("api_app/exported_classifier.pickle", "rb") as fp:
        classifier = pickle.load(fp)

    param_hotel = "City Hotel"
    param_month = "2"
    param_num = 12

    hotel_feature = enc.transform([[param_hotel]]).toarray()
    month_feature = (int(param_month) >= 6) and (int(param_month) <=8)

    features = np.hstack([hotel_feature, np.array([[month_feature]]), np.array([[param_num]])])

    if classifier.predict(features)[0]:
        return "will not cancel"
    else:
        return "will cancel"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
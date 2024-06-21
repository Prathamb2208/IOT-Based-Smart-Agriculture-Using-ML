from markupsafe import Markup
import pandas as pd # type: ignore
from utils.fertilizer import fertilizer_dic

import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Home_1.html')

@app.route('/predict')
def prediction():
    return render_template('Index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/form1', methods=["POST"])  
def brain():
    if request.method == "POST":
        try:
            Nitrogen = float(request.form['Nitrogen'])
            Phosphorus = float(request.form['Phosphorus'])
            Potassium = float(request.form['Potassium'])
            Temperature = float(request.form['Temperature'])
            Humidity = float(request.form['Humidity'])
            Ph = float(request.form['ph'])
            Rainfall = float(request.form['Rainfall'])

            values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]

            if 0 < Ph <= 14 and Temperature < 100 and Humidity > 0:
                model = joblib.load('Models/crop decoded')
                arr = [values]
                acc = model.predict(arr)
                return render_template('prediction.html', prediction=str(acc[0]))
            else:
                return render_template('error.html')
        except Exception as e:
            return f"An error occurred: {str(e)}"
        else:
            return render_template('form1.html')  # Render the form page for GET requests
        
        
@app.route('/fertilizer')
def fertilizer_form():
    return render_template('fertilizer.html')

@app.route('/fertilizer-predict', methods=["POST"])
def fert_recommend():
    if request.method == "POST":
        crop_name = str(request.form["cropname"])
        N = int(request.form["nitrogen"])
        P = int(request.form["phosphorous"])
        K = int(request.form["pottasium"])

        df_fertilizer = pd.read_csv("crop_app/data/fertilizer.csv")

        nr = df_fertilizer[df_fertilizer["Crop"] == crop_name]["N"].iloc[0]
        pr = df_fertilizer[df_fertilizer["Crop"] == crop_name]["P"].iloc[0]
        kr = df_fertilizer[df_fertilizer["Crop"] == crop_name]["K"].iloc[0]

        n = nr - N
        p = pr - P
        k = kr - K

        temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
        max_value = temp[max(temp.keys())]

        if max_value == "N":
            key = "NHigh" if n < 0 else "Nlow"
        elif max_value == "P":
            key = "PHigh" if p < 0 else "Plow"
        else:
            key = "KHigh" if k < 0 else "Klow"

        response = Markup(fertilizer_dic[key])
        return render_template('fertilizer-result.html', recommendation=response)

#if __name__ == '__main__':
#    app.run(debug=True)

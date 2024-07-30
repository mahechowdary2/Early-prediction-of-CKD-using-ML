from flask import Flask, request, render_template
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

# Load your pre-trained model (make sure the path is correct)
model = pickle.load(open('mod.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/pre')
def pre():
    return render_template('pre.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        data = request.form
        
        # Create the DataFrame in the correct order
        input_data = [
            float(data['age']),
            1 if data['red_blood_cells']=='normal' else 0,
            1 if data['pus_cell'] == 'normal' else 0,
             float(data['blood_glucose_random']),
             float(data['blood_urea']),
             1 if data['pedal_edema'] == 'yes' else 0,
             1 if data['anemia'] == 'yes' else 0,
             2 if data['diabetesmellitus'] == 'yes' else 1,
            1 if data['coronary_disease'] == 'yes' else 0,
            float(data['blood_pressure'])
            ]
        # Predict the result using the model

        X = np.array(input_data).reshape(1,-1)
        print(X)
        prediction = model.predict(X)
        risk = "Your risk of developing Chronic Kidney Disease is low"
        if input_data[0] > 50 or input_data[3] > 200 or input_data[9] > 90:
            risk = "You have a high risk of developing Chronic Kidney Disease"

            return render_template('result.html', prediction=prediction, risk_factor=risk)

            


@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

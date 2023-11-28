from flask import Flask, request, jsonify
import numpy as np
import pickle
import pandas as pd
import flasgger
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

pickle_in = open("Diabetes.pkl","rb")
model = pickle.load(pickle_in)

scaler_pickle = open("scaler.pkl", "rb")
scaler = pickle.load(scaler_pickle)



@app.route('/predict', methods=['Get'])
def predict_class():

    """Predict if patient has diabetes or not.
    ---
    parameters:
        - name: pregnancies
          in: query
          type: number
          required: true

        - name: glucose
          in: query
          type: number
          required: true

        - name: Blood Pressure
          in: query
          type: number
          required: true

        - name: Skin Thickness
          in: query
          type: number
          required: true

        - name: Insulin
          in: query
          type: number
          required: true

        - name: BMI
          in: query
          type: number
          required: true

        - name: Diabetes Pedegree Function
          in: query
          type: number
          required: true

        - name: Age
          in: query
          type: number
          required: true

    responses:
        500:
            description: output
    """


    Pregnancies = request.args.get("pregnancies")
    Glucose = request.args.get('glucose')
    Blood_pressure = request.args.get('Blood Pressure')
    Skin_Thickness = request.args.get('Skin Thickness')
    Insulin = request.args.get('Insulin')
    BMI = request.args.get('BMI')
    DPF = request.args.get('Diabetes Pedegree Function')
    Age = request.args.get('Age')

    #processing all the input data
    input_list = [Pregnancies, Glucose, Blood_pressure, Skin_Thickness, Insulin, BMI, DPF, Age]
    input_array = np.asarray(input_list)
    input_reshape = input_array.reshape(1, -1)
    scaled_data = scaler.fit_transform(input_reshape)
    prediction = model.predict(scaled_data)   

    output = ""

    if prediction == 0:
        output = 'this patient does not have diabetes'
    else:
        output = "this Patient has diabetes"

    return 'This model predicts that'+ str(output)


@app.route('/predict_file', methods=['POST'])
def predict_file_func():

    """Predict if patient has diabetes or not.
    ---
    parameters:
        - name: file
          in: formData
          type: file
          required: true
    responses:
        500:
            description: output value
    """
    df_test = pd.read_csv(request.files.get('file'))
    print(df_test.head())
    predict = model.predict(df_test)
    return str(list(predict))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
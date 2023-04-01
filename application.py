from flask import Flask, request, jsonify
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import numpy as np

application=Flask(__name__)

app=application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') 

## Route for a prediction

@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON data from the request
    data = request.get_json()

    # Prepare the data for prediction
    input_data = np.array(data['input'])
    input_data = scaler.transform(input_data.reshape(-1, 1))
    input_data = input_data.reshape(1, -1, 1)

    # Make the prediction
    prediction = model.predict(input_data)

    # Inverse transform the prediction
    prediction = scaler.inverse_transform(prediction)[0][0]

    # Return the prediction as JSON
    return jsonify({'prediction': prediction})



if __name__ == '__main__':
    app.run(host='0.0.0.0')

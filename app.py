from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load model and scaler
model = pickle.load(open('concrete_model.pkl', 'rb'))
scaler = pickle.load(open('concrete_scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    
    features = np.array([[
        float(data['cement']),
        float(data['slag']),
        float(data['ash']),
        float(data['water']),
        float(data['superplastic']),
        float(data['coarseagg']),
        float(data['fineagg']),
        float(data['age'])
    ]])
    
    # Scale input
    features_scaled = scaler.transform(features)
    
    # Predict
    prediction = model.predict(features_scaled)
    
    return render_template('index.html', 
                         prediction=round(float(prediction[0]), 2))

if __name__ == '__main__':
    app.run(debug=True)
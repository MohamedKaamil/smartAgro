#!/usr/bin/env python3
"""Test model loading in Flask environment"""

import sys
import os

# Add backend to path like Flask does
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

import joblib
import pandas as pd

def test_model_in_flask_context():
    """Test model loading as Flask would do it"""
    print("Testing model loading in Flask context...")
    
    # This mimics the path calculation in main.py
    current_file = os.path.join(backend_path, 'app', 'routes', 'main.py')
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_file))), 'crop_recommendation_model.pkl')
    
    print(f"Model path: {model_path}")
    print(f"File exists: {os.path.exists(model_path)}")
    
    try:
        # Load model
        model_package = joblib.load(model_path)
        print("SUCCESS: Model loaded in Flask context!")
        
        model = model_package['model']
        encoders = model_package['encoders']
        
        # Test prediction
        input_data = pd.DataFrame({
            'N_cat': ['High'],
            'P_cat': ['Medium'],
            'K_cat': ['High'],
            'temperature_cat': ['Warm'],
            'humidity_cat': ['Humid'],
            'ph_cat': ['Neutral'],
            'rainfall_cat': ['High']
        })
        
        # Encode
        for col in input_data.columns:
            if col in encoders:
                input_data[col + '_encoded'] = encoders[col].transform(input_data[col])
        
        # Predict
        feature_cols = [col + '_encoded' for col in ['N_cat', 'P_cat', 'K_cat', 'temperature_cat', 'humidity_cat', 'ph_cat', 'rainfall_cat'] if col in encoders]
        X_test = input_data[feature_cols]
        
        prediction = model.predict(X_test)[0]
        print(f"Prediction: {prediction}")
        
        return True
        
    except Exception as e:
        print(f"FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_model_in_flask_context()
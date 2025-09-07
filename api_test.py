#!/usr/bin/env python3
"""
Direct API test for crop recommendation
"""
import os
import joblib
import pandas as pd

def test_model_directly():
    """Test the ML model directly with user's example data"""
    # Example data from user
    data = {
        'nitrogen_level': 'High',
        'phosphorous_level': 'Medium', 
        'potassium_level': 'Medium',
        'temperature_level': 'Warm',
        'humidity_level': 'Humid',
        'ph_level': 'Neutral',
        'rainfall_level': 'High'
    }
    
    # Load the ML model
    model_path = os.path.join('backend', 'app', 'routes', 'crop_recommendation_model.pkl')
    
    if not os.path.exists(model_path):
        print(f"ERROR: ML model not found at: {model_path}")
        return
    
    try:
        # Load model
        model_package = joblib.load(model_path)
        model = model_package['model'] 
        encoders = model_package['encoders']
        
        # Prepare input data
        input_data = pd.DataFrame({
            'N_cat': [data['nitrogen_level']],
            'P_cat': [data['phosphorous_level']],
            'K_cat': [data['potassium_level']],
            'temperature_cat': [data['temperature_level']],
            'humidity_cat': [data['humidity_level']],
            'ph_cat': [data['ph_level']],
            'rainfall_cat': [data['rainfall_level']]
        })
        
        # Encode features
        for col in input_data.columns:
            if col in encoders:
                input_data[col + '_encoded'] = encoders[col].transform(input_data[col])
        
        # Prepare features for prediction
        feature_cols = [col + '_encoded' for col in ['N_cat', 'P_cat', 'K_cat', 'temperature_cat', 'humidity_cat', 'ph_cat', 'rainfall_cat']]
        X_input = input_data[feature_cols]
        
        # Make prediction
        prediction = model.predict(X_input)[0]
        
        # Get confidence
        confidence = 0.0
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(X_input)[0]
            confidence = float(max(probabilities))
        
        print("="*60)
        print("CROP RECOMMENDATION RESULT")
        print("="*60)
        print(f"Input conditions:")
        print(f"  Nitrogen: {data['nitrogen_level']}")
        print(f"  Phosphorous: {data['phosphorous_level']}")
        print(f"  Potassium: {data['potassium_level']}")
        print(f"  Temperature: {data['temperature_level']}")
        print(f"  Humidity: {data['humidity_level']}")
        print(f"  pH: {data['ph_level']}")
        print(f"  Rainfall: {data['rainfall_level']}")
        print()
        print(f"PREDICTED CROP: {prediction}")
        print(f"CONFIDENCE: {confidence:.4f} ({confidence*100:.2f}%)")
        print("="*60)
        
        return {
            'crop': prediction,
            'confidence': confidence,
            'confidence_percentage': round(confidence * 100, 2)
        }
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    result = test_model_directly()
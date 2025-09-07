#!/usr/bin/env python3
"""Simple model test to verify the ML model works and produces output"""

import joblib
import pandas as pd

def test_model():
    """Test the crop recommendation model"""
    print("Testing crop recommendation model...")
    
    # Load the model
    model_path = 'crop_recommendation_model.pkl'
    print(f"Loading model from: {model_path}")
    
    try:
        model_package = joblib.load(model_path)
        print("Model loaded successfully!")
        
        # Get components
        model = model_package['model']
        encoders = model_package['encoders']
        model_type = model_package['model_type']
        
        print(f"Model type: {model_type}")
        print(f"Available encoders: {list(encoders.keys())}")
        
        # Test with sample data
        print("\nTesting with sample input...")
        
        # Create test input
        test_data = pd.DataFrame({
            'N_cat': ['High'],
            'P_cat': ['Medium'], 
            'K_cat': ['High'],
            'temperature_cat': ['Warm'],
            'humidity_cat': ['Humid'],
            'ph_cat': ['Neutral'],
            'rainfall_cat': ['High']
        })
        
        print(f"Input data: {test_data.iloc[0].to_dict()}")
        
        # Encode the features
        for col in test_data.columns:
            if col in encoders:
                test_data[col + '_encoded'] = encoders[col].transform(test_data[col])
        
        # Prepare features for prediction
        feature_cols = [col + '_encoded' for col in ['N_cat', 'P_cat', 'K_cat', 'temperature_cat', 'humidity_cat', 'ph_cat', 'rainfall_cat']]
        X_input = test_data[feature_cols]
        
        print(f"Encoded features shape: {X_input.shape}")
        
        # Make prediction
        prediction = model.predict(X_input)[0]
        print(f"Predicted crop: {prediction}")
        
        # Get confidence if available
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(X_input)[0]
            confidence = max(probabilities)
            print(f"Confidence: {confidence:.4f} ({confidence*100:.2f}%)")
        
        print("\nModel test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Model test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_model()
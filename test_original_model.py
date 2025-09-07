#!/usr/bin/env python3
"""Test the original crop_recommendation_model.pkl file"""

import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')

def test_original_model():
    """Test the original model file"""
    model_path = 'crop_recommendation_model.pkl'
    
    print("="*60)
    print("TESTING ORIGINAL MODEL FILE")
    print("="*60)
    
    # Test loading
    print("\n1. Testing model loading...")
    try:
        model_package = joblib.load(model_path)
        print("   SUCCESS: Original model loaded!")
        print("   Type:", type(model_package))
        
        if isinstance(model_package, dict):
            print("   Keys:", list(model_package.keys()))
            
            # Get components
            model = model_package.get('model')
            encoders = model_package.get('encoders', {})
            model_type = model_package.get('model_type')
            
            print(f"   Model type: {model_type}")
            print(f"   Model class: {model.__class__.__name__}")
            print(f"   Available encoders: {list(encoders.keys())}")
            
    except Exception as e:
        print(f"   FAILED: {str(e)}")
        return False
    
    # Test prediction
    print("\n2. Testing prediction...")
    try:
        # Create test input
        test_input = pd.DataFrame({
            'N_cat': ['High'],
            'P_cat': ['Medium'],
            'K_cat': ['High'],
            'temperature_cat': ['Warm'],
            'humidity_cat': ['Humid'],
            'ph_cat': ['Neutral'],
            'rainfall_cat': ['High']
        })
        
        print("   Test input created:", test_input.shape)
        
        # Encode features
        for col in test_input.columns:
            if col in encoders:
                test_input[col + '_encoded'] = encoders[col].transform(test_input[col])
        
        # Select encoded features
        feature_cols = [col + '_encoded' for col in ['N_cat', 'P_cat', 'K_cat', 'temperature_cat', 'humidity_cat', 'ph_cat', 'rainfall_cat'] if col in encoders]
        X_test = test_input[feature_cols]
        
        print("   Input for prediction:", X_test.shape)
        
        # Make prediction
        prediction = model.predict(X_test)[0]
        print("   PREDICTION SUCCESS!")
        print("   Predicted crop:", prediction)
        
        # Try confidence
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(X_test)[0]
            confidence = max(proba)
            print("   Confidence:", f"{confidence:.2%}")
        
        print("\n" + "="*60)
        print("RESULT: ORIGINAL MODEL IS WORKING!")
        print("The original pkl file works perfectly!")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"   Prediction FAILED: {str(e)}")
        print("\n" + "="*60)
        print("RESULT: MODEL LOADS BUT PREDICTION FAILS")
        print("="*60)
        return False

if __name__ == "__main__":
    test_original_model()
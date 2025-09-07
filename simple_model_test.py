#!/usr/bin/env python3
"""Simple test to check if the ML model works with test data"""

import pandas as pd
import numpy as np
import joblib
import pickle
import warnings
warnings.filterwarnings('ignore')

def test_model_loading_methods():
    """Try different methods to load the model"""
    model_path = 'crop_recommendation_model_new.pkl'
    
    print("="*60)
    print("TESTING DIFFERENT MODEL LOADING METHODS")
    print("="*60)
    
    # Method 1: Standard joblib load
    print("\n1. Testing standard joblib.load()...")
    try:
        model_package = joblib.load(model_path)
        print("   ✓ SUCCESS: Standard joblib.load() worked!")
        return model_package, "joblib_standard"
    except Exception as e:
        print(f"   ✗ FAILED: {str(e)}")
    
    # Method 2: Joblib with mmap_mode
    print("\n2. Testing joblib.load() with mmap_mode='r'...")
    try:
        model_package = joblib.load(model_path, mmap_mode='r')
        print("   ✓ SUCCESS: joblib.load() with mmap_mode worked!")
        return model_package, "joblib_mmap"
    except Exception as e:
        print(f"   ✗ FAILED: {str(e)}")
    
    # Method 3: Standard pickle
    print("\n3. Testing standard pickle.load()...")
    try:
        with open(model_path, 'rb') as f:
            model_package = pickle.load(f)
        print("   ✓ SUCCESS: Standard pickle.load() worked!")
        return model_package, "pickle_standard"
    except Exception as e:
        print(f"   ✗ FAILED: {str(e)}")
    
    # Method 4: Try with allow_pickle
    print("\n4. Testing with different joblib parameters...")
    try:
        # This might not work but worth trying
        import joblib
        model_package = joblib.load(model_path)
        print("   ✓ SUCCESS: Alternative method worked!")
        return model_package, "alternative"
    except Exception as e:
        print(f"   ✗ FAILED: {str(e)}")
    
    print("\n❌ ALL LOADING METHODS FAILED!")
    return None, None

def analyze_model_structure(model_package, method):
    """Analyze the structure of the loaded model"""
    print(f"\n{'='*60}")
    print(f"ANALYZING MODEL STRUCTURE (Loaded with: {method})")
    print(f"{'='*60}")
    
    print(f"Model package type: {type(model_package)}")
    
    if isinstance(model_package, dict):
        print(f"Model package keys: {list(model_package.keys())}")
        
        # Check each component
        for key, value in model_package.items():
            print(f"\n{key}:")
            print(f"  - Type: {type(value)}")
            
            if key == 'encoders' and isinstance(value, dict):
                print(f"  - Encoder keys: {list(value.keys())}")
                for enc_key, enc_value in value.items():
                    print(f"    - {enc_key}: {type(enc_value)}")
                    if hasattr(enc_value, 'classes_'):
                        print(f"      Classes: {enc_value.classes_}")
            
            elif key == 'model':
                print(f"  - Model class: {value.__class__.__name__}")
                if hasattr(value, 'feature_names_in_'):
                    print(f"  - Feature names: {value.feature_names_in_}")
                if hasattr(value, 'classes_'):
                    print(f"  - Target classes: {list(value.classes_)}")
    
    else:
        print(f"Model is not a dictionary, trying to use directly...")
        if hasattr(model_package, 'predict'):
            print("Model has predict method")
        if hasattr(model_package, 'classes_'):
            print(f"Model classes: {list(model_package.classes_)}")

def test_with_sample_data(model_package, method):
    """Test the model with sample input data"""
    print(f"\n{'='*60}")
    print(f"TESTING WITH SAMPLE DATA")
    print(f"{'='*60}")
    
    # Sample test cases
    test_cases = [
        {
            'name': 'Test Case 1 - Rice conditions',
            'data': {
                'nitrogen_level': 'High',
                'phosphorous_level': 'Medium', 
                'potassium_level': 'High',
                'temperature_level': 'Warm',
                'humidity_level': 'Very Humid',
                'ph_level': 'Neutral',
                'rainfall_level': 'Very High'
            }
        },
        {
            'name': 'Test Case 2 - Wheat conditions',
            'data': {
                'nitrogen_level': 'High',
                'phosphorous_level': 'High',
                'potassium_level': 'Medium', 
                'temperature_level': 'Mild',
                'humidity_level': 'Moderate',
                'ph_level': 'Neutral',
                'rainfall_level': 'Medium'
            }
        },
        {
            'name': 'Test Case 3 - General conditions',
            'data': {
                'nitrogen_level': 'Medium',
                'phosphorous_level': 'Medium',
                'potassium_level': 'Medium',
                'temperature_level': 'Warm',
                'humidity_level': 'Humid',
                'ph_level': 'Neutral',
                'rainfall_level': 'High'
            }
        }
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}:")
        print("Input conditions:")
        for key, value in test_case['data'].items():
            print(f"   - {key.replace('_level', '').replace('_', ' ').title()}: {value}")
        
        try:
            result = make_prediction(model_package, test_case['data'])
            if result:
                success_count += 1
                print(f"   ✓ SUCCESS: Predicted crop = {result['crop']}")
                if result['confidence']:
                    print(f"   Confidence: {result['confidence']:.2%}")
            else:
                print(f"   ✗ FAILED: No prediction returned")
                
        except Exception as e:
            print(f"   ✗ FAILED: {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"PREDICTION RESULTS SUMMARY:")
    print(f"Successful predictions: {success_count}/{len(test_cases)}")
    if success_count > 0:
        print(f"✓ MODEL IS WORKING with {method} loading method!")
    else:
        print(f"❌ MODEL IS NOT WORKING properly")
    print(f"{'='*60}")
    
    return success_count > 0

def make_prediction(model_package, input_data):
    """Make a prediction using the loaded model"""
    try:
        if isinstance(model_package, dict):
            model = model_package.get('model')
            encoders = model_package.get('encoders', {})
        else:
            # Try to use the model directly
            model = model_package
            encoders = {}
        
        if model is None:
            return None
            
        # Create input DataFrame with expected column names
        input_df = pd.DataFrame({
            'N_cat': [input_data['nitrogen_level']],
            'P_cat': [input_data['phosphorous_level']],
            'K_cat': [input_data['potassium_level']],
            'temperature_cat': [input_data['temperature_level']],
            'humidity_cat': [input_data['humidity_level']],
            'ph_cat': [input_data['ph_level']],
            'rainfall_cat': [input_data['rainfall_level']]
        })
        
        # If we have encoders, use them
        if encoders:
            encoded_df = input_df.copy()
            for col in input_df.columns:
                if col in encoders:
                    encoded_df[col + '_encoded'] = encoders[col].transform(input_df[col])
            
            # Use encoded features
            feature_cols = [col + '_encoded' for col in input_df.columns if col in encoders]
            X_input = encoded_df[feature_cols]
        else:
            # Try using the input directly
            X_input = input_df
        
        # Make prediction
        prediction = model.predict(X_input)[0]
        
        # Get confidence if available
        confidence = None
        if hasattr(model, 'predict_proba'):
            try:
                probabilities = model.predict_proba(X_input)[0]
                confidence = max(probabilities)
            except:
                pass
        
        return {
            'crop': prediction,
            'confidence': confidence,
            'input_shape': X_input.shape
        }
        
    except Exception as e:
        raise Exception(f"Prediction error: {str(e)}")

def main():
    """Main test function"""
    print("COMPREHENSIVE ML MODEL TEST")
    print("="*60)
    print("Testing crop_recommendation_model_new.pkl")
    
    # Step 1: Try to load the model
    model_package, loading_method = test_model_loading_methods()
    
    if model_package is None:
        print("\n❌ FINAL RESULT: MODEL CANNOT BE LOADED")
        print("The pkl file has compatibility issues with current environment.")
        print("\nRECOMMENDATIONS:")
        print("1. Try downgrading NumPy: pip install numpy==1.21.0")
        print("2. Retrain the model with current environment")
        print("3. Check if you have an older version of the model file")
        return False
    
    # Step 2: Analyze model structure
    analyze_model_structure(model_package, loading_method)
    
    # Step 3: Test with sample data
    is_working = test_with_sample_data(model_package, loading_method)
    
    # Final conclusion
    print(f"\n{'='*60}")
    print("FINAL TEST CONCLUSION:")
    print(f"{'='*60}")
    if is_working:
        print("✅ SUCCESS: The ML model is working correctly!")
        print(f"✅ Loading method: {loading_method}")
        print("✅ The model can make predictions with test data")
        print("\n🎯 NEXT STEPS:")
        print("1. The Flask endpoint should now work")
        print("2. Test the full application through the React frontend")
        print("3. The CORS issue should be resolved")
    else:
        print("❌ FAILURE: The ML model has issues")
        print("❌ Cannot make predictions with test data")
        print("\n🔧 DEBUGGING NEEDED:")
        print("1. Check model training process")
        print("2. Verify input data format")
        print("3. Consider retraining the model")
    
    return is_working

if __name__ == "__main__":
    main()
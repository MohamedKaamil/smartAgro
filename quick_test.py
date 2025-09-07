import joblib
import pandas as pd
import pickle

print("="*50)
print("QUICK ML MODEL TEST")
print("="*50)

model_path = 'crop_recommendation_model_new.pkl'

# Test 1: Try joblib
print("\n1. Testing joblib loading...")
try:
    pkg = joblib.load(model_path)
    print("SUCCESS: joblib loading worked!")
    print("Type:", type(pkg))
    if isinstance(pkg, dict):
        print("Keys:", list(pkg.keys()))
    joblib_success = True
except Exception as e:
    print("FAILED:", str(e)[:100])
    joblib_success = False

# Test 2: Try pickle
print("\n2. Testing pickle loading...")
try:
    with open(model_path, 'rb') as f:
        pkg = pickle.load(f)
    print("SUCCESS: pickle loading worked!")
    print("Type:", type(pkg))
    if isinstance(pkg, dict):
        print("Keys:", list(pkg.keys()))
    pickle_success = True
except Exception as e:
    print("FAILED:", str(e)[:100])
    pickle_success = False

# Test 3: If we got it loaded, try prediction
if joblib_success or pickle_success:
    print("\n3. Testing prediction...")
    try:
        if isinstance(pkg, dict):
            model = pkg.get('model')
            encoders = pkg.get('encoders', {})
        else:
            model = pkg
            encoders = {}
        
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
        
        print("Test input created:", test_input.shape)
        
        # Try encoding if encoders available
        if encoders:
            print("Found encoders:", list(encoders.keys()))
            for col in test_input.columns:
                if col in encoders:
                    test_input[col + '_encoded'] = encoders[col].transform(test_input[col])
            
            # Use encoded features
            feature_cols = [col + '_encoded' for col in ['N_cat', 'P_cat', 'K_cat', 'temperature_cat', 'humidity_cat', 'ph_cat', 'rainfall_cat'] if col in encoders]
            X_test = test_input[feature_cols]
        else:
            X_test = test_input
        
        print("Input for prediction:", X_test.shape)
        
        # Make prediction
        prediction = model.predict(X_test)
        print("PREDICTION SUCCESS!")
        print("Predicted crop:", prediction[0])
        
        # Try confidence
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(X_test)
            confidence = max(proba[0])
            print("Confidence:", f"{confidence:.2%}")
        
        print("\n" + "="*50)
        print("FINAL RESULT: ML MODEL IS WORKING!")
        print("The pkl file can load and make predictions.")
        print("="*50)
        
    except Exception as e:
        print("Prediction FAILED:", str(e)[:200])
        print("\n" + "="*50)
        print("FINAL RESULT: MODEL LOADS BUT PREDICTION FAILS")
        print("The pkl file has issues with prediction.")
        print("="*50)
        
else:
    print("\n" + "="*50)
    print("FINAL RESULT: MODEL CANNOT BE LOADED")
    print("The pkl file has compatibility issues.")
    print("="*50)
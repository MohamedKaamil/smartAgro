import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

def load_model():
    """Load the saved model and return all components"""
    try:
        model_package = joblib.load('crop_recommendation_model_new.pkl')
        model = model_package['model']
        encoders = model_package['encoders']
        model_type = model_package['model_type']
        
        print(f"Model loaded successfully!")
        print(f"Model Type: {model_type}")
        print(f"Available encoders: {list(encoders.keys())}")
        
        return model, encoders, model_type
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None, None, None

def categorize_features(n, p, k, temp, humidity, ph, rainfall):
    """Convert numerical values to categorical features"""
    
    # Nitrogen categorization
    if n <= 20:
        n_cat = 'Very Low'
    elif n <= 40:
        n_cat = 'Low'
    elif n <= 80:
        n_cat = 'Medium'
    elif n <= 120:
        n_cat = 'High'
    else:
        n_cat = 'Very High'
    
    # Phosphorous categorization
    if p <= 25:
        p_cat = 'Very Low'
    elif p <= 50:
        p_cat = 'Low'
    elif p <= 75:
        p_cat = 'Medium'
    elif p <= 100:
        p_cat = 'High'
    else:
        p_cat = 'Very High'
    
    # Potassium categorization
    if k <= 20:
        k_cat = 'Very Low'
    elif k <= 35:
        k_cat = 'Low'
    elif k <= 60:
        k_cat = 'Medium'
    elif k <= 100:
        k_cat = 'High'
    else:
        k_cat = 'Very High'
    
    # Temperature categorization
    if temp <= 18:
        temp_cat = 'Cool'
    elif temp <= 25:
        temp_cat = 'Mild'
    elif temp <= 32:
        temp_cat = 'Warm'
    else:
        temp_cat = 'Hot'
    
    # Humidity categorization
    if humidity <= 40:
        humidity_cat = 'Dry'
    elif humidity <= 70:
        humidity_cat = 'Moderate'
    elif humidity <= 90:
        humidity_cat = 'Humid'
    else:
        humidity_cat = 'Very Humid'
    
    # pH categorization
    if ph <= 6.0:
        ph_cat = 'Acidic'
    elif ph <= 7.0:
        ph_cat = 'Neutral'
    else:
        ph_cat = 'Alkaline'
    
    # Rainfall categorization
    if rainfall <= 60:
        rainfall_cat = 'Low'
    elif rainfall <= 120:
        rainfall_cat = 'Medium'
    elif rainfall <= 200:
        rainfall_cat = 'High'
    else:
        rainfall_cat = 'Very High'
    
    return n_cat, p_cat, k_cat, temp_cat, humidity_cat, ph_cat, rainfall_cat

def predict_crop_from_categorical(model, encoders, n_cat, p_cat, k_cat, temp_cat, humidity_cat, ph_cat, rainfall_cat):
    """Make prediction using categorical inputs"""
    try:
        # Create input dataframe
        input_data = pd.DataFrame({
            'N_cat': [n_cat],
            'P_cat': [p_cat],
            'K_cat': [k_cat],
            'temperature_cat': [temp_cat],
            'humidity_cat': [humidity_cat],
            'ph_cat': [ph_cat],
            'rainfall_cat': [rainfall_cat]
        })
        
        # Encode categorical features
        for col in input_data.columns:
            input_data[col + '_encoded'] = encoders[col].transform(input_data[col])
        
        # Select encoded features
        feature_columns = [col + '_encoded' for col in input_data.columns if not col.endswith('_encoded')]
        X_input = input_data[feature_columns]
        
        # Make prediction
        prediction = model.predict(X_input)[0]
        
        # Get prediction probability if available
        if hasattr(model, 'predict_proba'):
            prediction_proba = model.predict_proba(X_input)[0]
            confidence = max(prediction_proba)
            
            # Get top 3 predictions
            top_indices = np.argsort(prediction_proba)[-3:][::-1]
            top_predictions = [(model.classes_[i], prediction_proba[i]) for i in top_indices]
        else:
            confidence = None
            top_predictions = [(prediction, None)]
        
        return prediction, confidence, top_predictions
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return None, None, None

def test_with_original_data():
    """Test model with some original dataset samples"""
    print("\n" + "="*60)
    print("TESTING WITH ORIGINAL DATASET SAMPLES")
    print("="*60)
    
    # Load original dataset
    try:
        df = pd.read_csv(r"C:\Users\chan-shinan\Documents\icbt\final project\kamil\dataset\Crop_recommendation.csv")
        print(f"Original dataset loaded: {df.shape}")
        
        # Take a random sample of 10 records
        test_samples = df.sample(n=10, random_state=42)
        
        model, encoders, model_type = load_model()
        if model is None:
            return
        
        correct_predictions = 0
        total_predictions = len(test_samples)
        
        print(f"\nTesting {total_predictions} random samples from original dataset:")
        print("-" * 80)
        
        for idx, row in test_samples.iterrows():
            # Convert numerical values to categorical
            n_cat, p_cat, k_cat, temp_cat, humidity_cat, ph_cat, rainfall_cat = categorize_features(
                row['N'], row['P'], row['K'], row['temperature'], 
                row['humidity'], row['ph'], row['rainfall']
            )
            
            # Make prediction
            predicted_crop, confidence, top_predictions = predict_crop_from_categorical(
                model, encoders, n_cat, p_cat, k_cat, temp_cat, humidity_cat, ph_cat, rainfall_cat
            )
            
            actual_crop = row['label']
            is_correct = predicted_crop == actual_crop
            
            if is_correct:
                correct_predictions += 1
                status = "CORRECT"
            else:
                status = "INCORRECT"
            
            print(f"\nSample {idx}:")
            print(f"Input: N={n_cat}, P={p_cat}, K={k_cat}, T={temp_cat}, H={humidity_cat}, pH={ph_cat}, R={rainfall_cat}")
            print(f"Actual: {actual_crop}")
            print(f"Predicted: {predicted_crop}")
            if confidence:
                print(f"Confidence: {confidence:.4f} ({confidence*100:.2f}%)")
            print(f"Status: {status}")
        
        accuracy = correct_predictions / total_predictions
        print(f"\n" + "="*60)
        print(f"TEST RESULTS SUMMARY:")
        print(f"Correct Predictions: {correct_predictions}/{total_predictions}")
        print(f"Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Model Type: {model_type}")
        print(f"="*60)
        
        return accuracy
        
    except Exception as e:
        print(f"Error testing with original data: {str(e)}")
        return 0

def test_edge_cases():
    """Test model with edge cases and boundary conditions"""
    print("\n" + "="*60)
    print("TESTING EDGE CASES AND BOUNDARY CONDITIONS")
    print("="*60)
    
    model, encoders, model_type = load_model()
    if model is None:
        return
    
    edge_cases = [
        {
            'name': 'Very Low Everything',
            'inputs': ('Very Low', 'Very Low', 'Very Low', 'Cool', 'Dry', 'Acidic', 'Low'),
            'description': 'Testing with all minimum categorical values'
        },
        {
            'name': 'Very High Everything', 
            'inputs': ('Very High', 'Very High', 'Very High', 'Hot', 'Very Humid', 'Alkaline', 'Very High'),
            'description': 'Testing with all maximum categorical values'
        },
        {
            'name': 'Rice-like Conditions',
            'inputs': ('High', 'Medium', 'Medium', 'Warm', 'Very Humid', 'Neutral', 'Very High'),
            'description': 'Testing conditions typically favorable for rice'
        },
        {
            'name': 'Wheat-like Conditions',
            'inputs': ('High', 'High', 'Medium', 'Mild', 'Moderate', 'Neutral', 'Medium'),
            'description': 'Testing conditions typically favorable for wheat'
        },
        {
            'name': 'Desert-like Conditions',
            'inputs': ('Low', 'Low', 'Low', 'Hot', 'Dry', 'Alkaline', 'Low'),
            'description': 'Testing extreme dry conditions'
        }
    ]
    
    print(f"Testing {len(edge_cases)} edge cases:")
    print("-" * 80)
    
    for case in edge_cases:
        print(f"\n{case['name']}:")
        print(f"Description: {case['description']}")
        print(f"Inputs: N={case['inputs'][0]}, P={case['inputs'][1]}, K={case['inputs'][2]}")
        print(f"        T={case['inputs'][3]}, H={case['inputs'][4]}, pH={case['inputs'][5]}, R={case['inputs'][6]}")
        
        predicted_crop, confidence, top_predictions = predict_crop_from_categorical(
            model, encoders, *case['inputs']
        )
        
        if predicted_crop:
            print(f"Predicted: {predicted_crop}")
            if confidence:
                print(f"Confidence: {confidence:.4f} ({confidence*100:.2f}%)")
            
            if top_predictions and len(top_predictions) > 1:
                print("Top 3 predictions:")
                for i, (crop, prob) in enumerate(top_predictions[:3], 1):
                    if prob is not None:
                        print(f"  {i}. {crop}: {prob:.4f} ({prob*100:.2f}%)")
                    else:
                        print(f"  {i}. {crop}")
        else:
            print("Prediction failed")

def test_invalid_inputs():
    """Test model behavior with invalid inputs"""
    print("\n" + "="*60)
    print("TESTING INVALID INPUT HANDLING")
    print("="*60)
    
    model, encoders, model_type = load_model()
    if model is None:
        return
    
    invalid_cases = [
        {
            'name': 'Invalid Nitrogen Level',
            'inputs': ('Invalid', 'Medium', 'Medium', 'Warm', 'Humid', 'Neutral', 'High'),
            'expected': 'Should handle gracefully or show error'
        },
        {
            'name': 'Invalid Temperature Level',
            'inputs': ('Medium', 'Medium', 'Medium', 'Invalid', 'Humid', 'Neutral', 'High'),
            'expected': 'Should handle gracefully or show error'
        }
    ]
    
    print("Testing invalid input handling:")
    print("-" * 50)
    
    for case in invalid_cases:
        print(f"\n{case['name']}:")
        print(f"Expected: {case['expected']}")
        
        try:
            predicted_crop, confidence, top_predictions = predict_crop_from_categorical(
                model, encoders, *case['inputs']
            )
            if predicted_crop:
                print(f"Result: Model still made prediction: {predicted_crop}")
            else:
                print("Result: Model correctly handled invalid input")
        except Exception as e:
            print(f"Result: Model correctly raised error: {str(e)}")

def comprehensive_test():
    """Run comprehensive test suite"""
    print("COMPREHENSIVE MODEL TESTING")
    print("="*60)
    
    # Test 1: Load model
    print("\n1. TESTING MODEL LOADING")
    model, encoders, model_type = load_model()
    if model is None:
        print("Cannot proceed - model loading failed")
        return
    
    # Test 2: Original data accuracy
    print("\n2. TESTING ACCURACY WITH ORIGINAL DATA")
    accuracy = test_with_original_data()
    
    # Test 3: Edge cases
    test_edge_cases()
    
    # Test 4: Invalid inputs
    test_invalid_inputs()
    
    # Final summary
    print("\n" + "="*60)
    print("FINAL TEST SUMMARY")
    print("="*60)
    print(f"Model loaded successfully: {model_type}")
    print(f"Model encoders working: {len(encoders)} encoders")
    if accuracy > 0:
        print(f"Sample accuracy test: {accuracy:.2%}")
    print(f"Edge case testing: Completed")
    print(f"Invalid input handling: Completed")
    
    if accuracy >= 0.8:
        print(f"\nMODEL PERFORMANCE: EXCELLENT (>= 80%)")
    elif accuracy >= 0.6:
        print(f"\nMODEL PERFORMANCE: GOOD (>= 60%)")
    elif accuracy >= 0.4:
        print(f"\nMODEL PERFORMANCE: FAIR (>= 40%)")
    else:
        print(f"\nMODEL PERFORMANCE: NEEDS IMPROVEMENT (< 40%)")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    comprehensive_test()
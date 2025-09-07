from flask import Blueprint, jsonify, request
import joblib
import pandas as pd
import os

main_test_bp = Blueprint('main_test', __name__)

@main_test_bp.route('/test-simple', methods=['GET'])
def test_simple():
    """Simple test"""
    return jsonify({'success': True, 'message': 'Test working!'})

@main_test_bp.route('/buyer/recommend-crop-test', methods=['POST'])
def recommend_crop_test():
    """Test crop recommendation endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'nitrogen_level', 'phosphorous_level', 'potassium_level',
            'temperature_level', 'humidity_level', 'ph_level', 'rainfall_level'
        ]
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        # Load the ML model
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'crop_recommendation_model.pkl')
        
        if not os.path.exists(model_path):
            return jsonify({
                'success': False,
                'message': f'ML model not found at: {model_path}'
            }), 500

        # Load model and make prediction
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
        
        return jsonify({
            'success': True,
            'message': 'Crop recommendation generated successfully!',
            'recommendation': {
                'crop': prediction,
                'confidence': confidence
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating recommendation: {str(e)}'
        }), 500
#!/usr/bin/env python3
"""
Enhanced API server for crop recommendation with seller lookup
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import joblib
import pandas as pd
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

def get_database_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='crop_recommendation',
            port=3306
        )
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def find_sellers_for_crop(crop_name):
    """Find sellers who have the predicted crop available"""
    connection = get_database_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Query to find sellers with the predicted crop
        query = """
            SELECT 
                sc.id as seller_crop_id,
                sc.crop_name,
                sc.crop_variety,
                sc.is_available,
                sc.price_per_kg,
                sc.price_per_unit,
                sc.unit_type,
                sc.quantity_available,
                sc.minimum_order,
                sc.harvest_season,
                sc.best_quality_months,
                sc.quality_grade,
                sc.organic_certified,
                sc.pesticide_free,
                s.id as seller_id,
                s.business_name,
                s.business_type,
                s.contact_number,
                s.secondary_contact,
                s.business_email,
                s.website,
                s.address_line_1,
                s.address_line_2,
                s.postal_code,
                s.shop_name,
                s.shop_type,
                s.establishment_year,
                s.is_verified,
                s.is_active,
                s.description,
                p.name as province_name,
                d.name as district_name,
                c.name as city_name
            FROM seller_crops sc
            JOIN sellers s ON sc.seller_id = s.id
            LEFT JOIN provinces p ON s.province_id = p.id
            LEFT JOIN districts d ON s.district_id = d.id
            LEFT JOIN cities c ON s.city_id = c.id
            WHERE LOWER(sc.crop_name) = LOWER(%s)
            AND sc.is_available = true
            AND s.is_active = true
            ORDER BY s.is_verified DESC, sc.price_per_kg ASC
        """
        
        cursor.execute(query, (crop_name,))
        sellers = cursor.fetchall()
        
        # Get cultivation details for each seller crop
        for seller in sellers:
            cultivation_query = """
                SELECT * FROM crop_cultivations 
                WHERE seller_crop_id = %s
            """
            cursor.execute(cultivation_query, (seller['seller_crop_id'],))
            cultivation_info = cursor.fetchone()
            seller['cultivation_info'] = cultivation_info
        
        cursor.close()
        return sellers
        
    except Error as e:
        print(f"Database query error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()

@app.route('/predict', methods=['POST'])
def predict_crop():
    """Crop recommendation endpoint"""
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
        model_path = os.path.join('backend', 'app', 'routes', 'crop_recommendation_model.pkl')
        
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
        
        # Find sellers for the predicted crop
        sellers = find_sellers_for_crop(prediction)
        
        response_data = {
            'success': True,
            'message': 'Crop recommendation generated successfully!',
            'recommendation': {
                'crop': prediction,
                'confidence': confidence,
                'confidence_percentage': round(confidence * 100, 2)
            },
            'input_conditions': {
                'nitrogen': data['nitrogen_level'],
                'phosphorous': data['phosphorous_level'],
                'potassium': data['potassium_level'],
                'temperature': data['temperature_level'],
                'humidity': data['humidity_level'],
                'ph': data['ph_level'],
                'rainfall': data['rainfall_level']
            },
            'sellers': {
                'available': len(sellers) > 0,
                'count': len(sellers),
                'message': f"Found {len(sellers)} seller(s) offering {prediction}" if len(sellers) > 0 
                          else f"Currently no sellers available for {prediction}. You will find sellers for this crop in the near future.",
                'data': sellers if len(sellers) > 0 else []
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating recommendation: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Crop recommendation API is running'})

if __name__ == '__main__':
    print("="*60)
    print("CROP RECOMMENDATION API SERVER")
    print("="*60)
    print("Starting server on http://localhost:5001")
    print("Endpoint: POST /predict")
    print("Health check: GET /health")
    print("="*60)
    app.run(host='0.0.0.0', port=5001, debug=True)
from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.models import SellerCrop, Seller, Province, District, City
import joblib
import pandas as pd
import os

buyer_bp = Blueprint('buyer', __name__)

def get_db():
    from app import db
    return db

@buyer_bp.route('/recommend-crop', methods=['POST'])
def recommend_crop():
    """Get crop recommendation based on soil and environmental conditions"""
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
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'crop_recommendation_model_new.pkl')
        
        if not os.path.exists(model_path):
            return jsonify({
                'success': False,
                'message': 'ML model not found. Please ensure the model file exists.'
            }), 500
        
        try:
            model_package = joblib.load(model_path)
            model = model_package['model']
            encoders = model_package['encoders']
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error loading ML model: {str(e)}'
            }), 500
        
        # Create input dataframe with the exact column names expected by the model
        input_data = pd.DataFrame({
            'N_cat': [data['nitrogen_level']],
            'P_cat': [data['phosphorous_level']],
            'K_cat': [data['potassium_level']],
            'temperature_cat': [data['temperature_level']],
            'humidity_cat': [data['humidity_level']],
            'ph_cat': [data['ph_level']],
            'rainfall_cat': [data['rainfall_level']]
        })
        
        # Encode categorical features
        try:
            for col in input_data.columns:
                if col in encoders:
                    input_data[col + '_encoded'] = encoders[col].transform(input_data[col])
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': f'Invalid input values. Please check your selections: {str(e)}'
            }), 400
        
        # Select encoded features for prediction
        feature_columns = [col + '_encoded' for col in input_data.columns if not col.endswith('_encoded')]
        X_input = input_data[feature_columns]
        
        # Make prediction
        prediction = model.predict(X_input)[0]
        
        # Get prediction confidence if available
        confidence = None
        if hasattr(model, 'predict_proba'):
            prediction_proba = model.predict_proba(X_input)[0]
            confidence = max(prediction_proba)
        
        # Find sellers who have this recommended crop
        sellers_with_crop = get_db().session.query(
            SellerCrop, Seller, Province, District, City
        ).join(
            Seller, SellerCrop.seller_id == Seller.id
        ).join(
            Province, Seller.province_id == Province.id
        ).join(
            District, Seller.district_id == District.id
        ).join(
            City, Seller.city_id == City.id
        ).filter(
            SellerCrop.crop_name.ilike(f'%{prediction}%'),
            SellerCrop.is_available == True,
            Seller.is_active == True
        ).all()
        
        # Format seller information
        available_sellers = []
        for crop, seller, province, district, city in sellers_with_crop:
            seller_info = {
                'seller_id': seller.id,
                'business_name': seller.business_name,
                'contact_number': seller.contact_number,
                'location': {
                    'address': seller.address_line_1,
                    'city': city.name,
                    'district': district.name,
                    'province': province.name,
                    'full_address': f"{seller.address_line_1}, {city.name}, {district.name}, {province.name}"
                },
                'crop_details': {
                    'crop_id': crop.id,
                    'crop_name': crop.crop_name,
                    'crop_variety': crop.crop_variety,
                    'price_per_kg': crop.price_per_kg,
                    'price_per_unit': crop.price_per_unit,
                    'unit_type': crop.unit_type,
                    'quantity_available': crop.quantity_available,
                    'minimum_order': crop.minimum_order,
                    'quality_grade': crop.quality_grade,
                    'organic_certified': crop.organic_certified,
                    'pesticide_free': crop.pesticide_free,
                    'harvest_season': crop.harvest_season
                },
                'seller_services': {
                    'delivery_available': seller.delivery_available,
                    'home_delivery': seller.home_delivery,
                    'pickup_available': seller.pickup_available
                }
            }
            available_sellers.append(seller_info)
        
        return jsonify({
            'success': True,
            'recommendation': {
                'crop_name': prediction,
                'confidence': round(confidence, 4) if confidence else None,
                'confidence_percentage': round(confidence * 100, 2) if confidence else None,
                'input_conditions': {
                    'nitrogen': data['nitrogen_level'],
                    'phosphorous': data['phosphorous_level'],
                    'potassium': data['potassium_level'],
                    'temperature': data['temperature_level'],
                    'humidity': data['humidity_level'],
                    'ph': data['ph_level'],
                    'rainfall': data['rainfall_level']
                }
            },
            'available_sellers': available_sellers,
            'sellers_count': len(available_sellers)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Recommendation failed: {str(e)}'
        }), 500

@buyer_bp.route('/crop-details/<crop_id>', methods=['GET'])
def get_crop_details(crop_id):
    """Get detailed information about a specific crop including cultivation methods"""
    try:
        # Get crop with cultivation information
        crop = SellerCrop.query.get(crop_id)
        
        if not crop:
            return jsonify({
                'success': False,
                'message': 'Crop not found'
            }), 404
        
        # Get seller information
        seller = Seller.query.get(crop.seller_id)
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Seller information not found'
            }), 404
        
        # Get location information
        province = Province.query.get(seller.province_id)
        district = District.query.get(seller.district_id)
        city = City.query.get(seller.city_id)
        
        crop_details = {
            'crop_info': crop.to_dict(include_cultivation=True),
            'seller_info': {
                'id': seller.id,
                'business_name': seller.business_name,
                'shop_name': seller.shop_name,
                'contact_number': seller.contact_number,
                'secondary_contact': seller.secondary_contact,
                'business_email': seller.business_email,
                'description': seller.description,
                'location': {
                    'address': seller.address_line_1,
                    'city': city.name if city else None,
                    'district': district.name if district else None,
                    'province': province.name if province else None,
                    'full_address': seller.get_full_address()
                },
                'services': {
                    'delivery_available': seller.delivery_available,
                    'home_delivery': seller.home_delivery,
                    'pickup_available': seller.pickup_available,
                    'operating_days': seller.operating_days
                },
                'verification': {
                    'is_verified': seller.is_verified,
                    'is_active': seller.is_active
                }
            }
        }
        
        return jsonify({
            'success': True,
            'crop_details': crop_details
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching crop details: {str(e)}'
        }), 500

@buyer_bp.route('/dashboard-stats', methods=['GET'])
def get_buyer_dashboard_stats():
    """Get statistics for buyer dashboard"""
    try:
        # Get total number of active sellers
        total_sellers = Seller.query.filter_by(is_active=True).count()
        
        # Get total number of available crops
        total_crops = SellerCrop.query.filter_by(is_available=True).count()
        
        # Get unique crop types
        unique_crop_types = get_db().session.query(SellerCrop.crop_name).filter_by(is_available=True).distinct().count()
        
        # Get verified sellers count
        verified_sellers = Seller.query.filter_by(is_active=True, is_verified=True).count()
        
        # Get crop distribution (top 10 most available crops)
        crop_distribution = get_db().session.query(
            SellerCrop.crop_name,
            get_db().func.count(SellerCrop.id).label('count')
        ).filter_by(is_available=True).group_by(
            SellerCrop.crop_name
        ).order_by(
            get_db().func.count(SellerCrop.id).desc()
        ).limit(10).all()
        
        crop_stats = [{'crop_name': crop[0], 'availability_count': crop[1]} for crop in crop_distribution]
        
        # Get province-wise seller distribution
        province_distribution = get_db().session.query(
            Province.name,
            get_db().func.count(Seller.id).label('seller_count')
        ).join(
            Seller, Province.id == Seller.province_id
        ).filter(
            Seller.is_active == True
        ).group_by(
            Province.name
        ).order_by(
            get_db().func.count(Seller.id).desc()
        ).limit(10).all()
        
        province_stats = [{'province': prov[0], 'seller_count': prov[1]} for prov in province_distribution]
        
        return jsonify({
            'success': True,
            'dashboard_stats': {
                'overview': {
                    'total_sellers': total_sellers,
                    'total_crops': total_crops,
                    'unique_crop_types': unique_crop_types,
                    'verified_sellers': verified_sellers
                },
                'crop_distribution': crop_stats,
                'province_distribution': province_stats
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching dashboard stats: {str(e)}'
        }), 500

@buyer_bp.route('/search-crops', methods=['GET'])
def search_crops():
    """Search for crops with optional filters"""
    try:
        # Get query parameters
        crop_name = request.args.get('crop_name', '')
        province_id = request.args.get('province_id', type=int)
        district_id = request.args.get('district_id', type=int)
        organic_only = request.args.get('organic_only', type=bool)
        min_quantity = request.args.get('min_quantity', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Build query
        query = get_db().session.query(
            SellerCrop, Seller, Province, District, City
        ).join(
            Seller, SellerCrop.seller_id == Seller.id
        ).join(
            Province, Seller.province_id == Province.id
        ).join(
            District, Seller.district_id == District.id
        ).join(
            City, Seller.city_id == City.id
        ).filter(
            SellerCrop.is_available == True,
            Seller.is_active == True
        )
        
        # Apply filters
        if crop_name:
            query = query.filter(SellerCrop.crop_name.ilike(f'%{crop_name}%'))
        
        if province_id:
            query = query.filter(Seller.province_id == province_id)
        
        if district_id:
            query = query.filter(Seller.district_id == district_id)
        
        if organic_only:
            query = query.filter(SellerCrop.organic_certified == True)
        
        if min_quantity:
            query = query.filter(SellerCrop.quantity_available >= min_quantity)
        
        if max_price:
            query = query.filter(SellerCrop.price_per_kg <= max_price)
        
        # Execute query
        results = query.all()
        
        # Format results
        crops = []
        for crop, seller, province, district, city in results:
            crop_info = {
                'crop_id': crop.id,
                'crop_name': crop.crop_name,
                'crop_variety': crop.crop_variety,
                'price_per_kg': crop.price_per_kg,
                'quantity_available': crop.quantity_available,
                'quality_grade': crop.quality_grade,
                'organic_certified': crop.organic_certified,
                'seller_info': {
                    'seller_id': seller.id,
                    'business_name': seller.business_name,
                    'contact_number': seller.contact_number,
                    'location': f"{city.name}, {district.name}, {province.name}"
                }
            }
            crops.append(crop_info)
        
        return jsonify({
            'success': True,
            'crops': crops,
            'total_results': len(crops)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Search failed: {str(e)}'
        }), 500
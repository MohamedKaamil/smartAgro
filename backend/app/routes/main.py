from flask import Blueprint, jsonify, request
from app import db
from app.models import Province, District, City, Seller, SellerCrop, CropCultivation
from sqlalchemy import func
import joblib
import pandas as pd
import os

main_bp = Blueprint('main', __name__)

# List of all 122 crop types from ML model
ML_CROP_TYPES = [
    "almond", "amaranth", "apple", "apricot", "artichoke", "asparagus", "avocado", "bamboo", "banana", "barley",
    "basil", "beetroot", "betel", "bilberry", "blackberry", "blackgram", "blueberry", "breadfruit", "broccoli", "buckwheat",
    "cabbage", "carambola", "carrot", "cashew", "cassava", "cauliflower", "celery", "chard", "cherry", "chia",
    "chickpea", "clementine", "coconut", "coffee", "cotton", "cranberry", "cucumber", "currant", "date", "dragonfruit",
    "durian", "eggplant", "fig", "garlic", "ginger", "gooseberry", "grapes", "guava", "hazelnut", "hemp",
    "jackfruit", "jambul", "jute", "kidneybeans", "kiwi", "leek", "lemongrass", "lentil", "lettuce", "longan",
    "lychee", "macadamia", "maize", "mandarin", "mango", "mangosteen", "melon", "millet", "mint", "mothbeans",
    "mulberry", "mungbean", "muskmelon", "nectarine", "oats", "okra", "olive", "onion", "orange", "papaya",
    "parsley", "passionfruit", "peach", "pear", "peas", "pecan", "persimmon", "pigeonpeas", "pistachio", "plantain",
    "plum", "pomegranate", "pomelo", "pumpkin", "quince", "radish", "rambutan", "raspberry", "rice", "rye",
    "salak", "sapodilla", "sorghum", "soursop", "soybean", "spinach", "starfruit", "strawberry", "sunflower", "sweetpotato",
    "tamarind", "tangelo", "taro", "teff", "tomato", "turmeric", "turnip", "walnut", "watermelon", "wheat", "yam", "zucchini"
]

@main_bp.route('/test-crop', methods=['POST'])
def test_crop_endpoint():
    """Working crop recommendation endpoint"""
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
        model_path = os.path.join(os.path.dirname(__file__), 'crop_recommendation_model.pkl')
        
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
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating recommendation: {str(e)}'
        }), 500

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check database connectivity
        total_provinces = Province.query.count()
        total_districts = District.query.count()
        total_cities = City.query.count()
        total_sellers = Seller.query.count()
        total_crops = SellerCrop.query.count()
        
        return jsonify({
            'status': 'healthy',
            'message': 'API is running properly',
            'database': {
                'connected': True,
                'total_provinces': total_provinces,
                'total_districts': total_districts,
                'total_cities': total_cities,
                'total_sellers': total_sellers,
                'total_crops': total_crops
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'Database connection failed: {str(e)}',
            'database': {
                'connected': False
            }
        }), 500

@main_bp.route('/find-sellers/<crop_name>', methods=['GET'])
def find_sellers(crop_name):
    """Find sellers for a specific crop"""
    try:
        # Get filter parameters
        province_id = request.args.get('province_id', type=int)
        district_id = request.args.get('district_id', type=int)
        city_id = request.args.get('city_id', type=int)
        organic_only = request.args.get('organic_only', 'false').lower() == 'true'
        verified_only = request.args.get('verified_only', 'true').lower() == 'true'
        
        # Build base query
        query = db.session.query(Seller, SellerCrop, CropCultivation) \
            .join(SellerCrop, Seller.id == SellerCrop.seller_id) \
            .outerjoin(CropCultivation, SellerCrop.id == CropCultivation.seller_crop_id) \
            .filter(SellerCrop.crop_name.ilike(f'%{crop_name}%')) \
            .filter(SellerCrop.is_available == True) \
            .filter(Seller.is_active == True)
        
        # Apply filters
        if verified_only:
            query = query.filter(Seller.is_verified == True)
        
        if organic_only:
            query = query.filter(SellerCrop.organic_certified == True)
        
        if province_id:
            query = query.filter(Seller.province_id == province_id)
        
        if district_id:
            query = query.filter(Seller.district_id == district_id)
        
        if city_id:
            query = query.filter(Seller.city_id == city_id)
        
        results = query.all()
        
        if not results:
            return jsonify({
                'success': True,
                'message': 'No sellers found for the specified criteria',
                'sellers': []
            })
        
        # Format results
        sellers_list = []
        for seller, crop, cultivation in results:
            seller_data = seller.to_dict()
            seller_data['crop'] = crop.to_dict()
            if cultivation:
                seller_data['crop']['cultivation'] = cultivation.to_dict()
            sellers_list.append(seller_data)
        
        return jsonify({
            'success': True,
            'sellers': sellers_list,
            'total_found': len(sellers_list)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error finding sellers: {str(e)}'
        }), 500

@main_bp.route('/crops/search', methods=['GET'])
def search_crops():
    """Search for crops across all sellers"""
    try:
        # Get search parameters
        search_term = request.args.get('q', '').strip()
        province_id = request.args.get('province_id', type=int)
        district_id = request.args.get('district_id', type=int)
        organic_only = request.args.get('organic_only', 'false').lower() == 'true'
        available_only = request.args.get('available_only', 'true').lower() == 'true'
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        if not search_term:
            return jsonify({
                'success': False,
                'message': 'Search term is required'
            }), 400
        
        # Build query
        query = db.session.query(SellerCrop, Seller) \
            .join(Seller, SellerCrop.seller_id == Seller.id) \
            .filter(SellerCrop.crop_name.ilike(f'%{search_term}%')) \
            .filter(Seller.is_active == True)
        
        if available_only:
            query = query.filter(SellerCrop.is_available == True)
        
        if organic_only:
            query = query.filter(SellerCrop.organic_certified == True)
        
        if province_id:
            query = query.filter(Seller.province_id == province_id)
        
        if district_id:
            query = query.filter(Seller.district_id == district_id)
        
        # Apply pagination
        paginated_results = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Format results
        crops = []
        for crop, seller in paginated_results.items:
            crop_data = crop.to_dict()
            crop_data['seller'] = {
                'id': seller.id,
                'business_name': seller.business_name,
                'shop_name': seller.shop_name,
                'location': {
                    'province': seller.province.name,
                    'district': seller.district.name,
                    'city': seller.city.name
                },
                'contact_number': seller.contact_number,
                'is_verified': seller.is_verified
            }
            crops.append(crop_data)
        
        return jsonify({
            'success': True,
            'crops': crops,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_pages': paginated_results.pages,
                'total_items': paginated_results.total,
                'has_next': paginated_results.has_next,
                'has_prev': paginated_results.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error searching crops: {str(e)}'
        }), 500

@main_bp.route('/crops/types', methods=['GET'])
def get_crop_types():
    """Get all available crop types from ML model"""
    try:
        # Format crops with proper capitalization for display
        formatted_crops = []
        for crop in ML_CROP_TYPES:
            formatted_crops.append({
                'key': crop,
                'name': crop.replace('_', ' ').title(),
                'value': crop
            })
        
        # Sort alphabetically by name
        formatted_crops.sort(key=lambda x: x['name'])
        
        return jsonify({
            'success': True,
            'crops': formatted_crops,
            'total': len(formatted_crops)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching crop types: {str(e)}'
        }), 500

@main_bp.route('/recommend-crop', methods=['POST'])
def recommend_crop_direct():
    """Direct crop recommendation endpoint"""
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
        model_path = os.path.join(os.path.dirname(__file__), 'crop_recommendation_model.pkl')
        
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
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating recommendation: {str(e)}'
        }), 500

@main_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    try:
        stats = {
            'provinces': Province.query.count(),
            'districts': District.query.count(),
            'cities': City.query.count(),
            'sellers': {
                'total': Seller.query.count(),
                'verified': Seller.query.filter_by(is_verified=True).count(),
                'active': Seller.query.filter_by(is_active=True).count()
            },
            'crops': {
                'total': SellerCrop.query.count(),
                'available': SellerCrop.query.filter_by(is_available=True).count(),
                'organic': SellerCrop.query.filter_by(organic_certified=True).count(),
                'ml_types_available': len(ML_CROP_TYPES)
            }
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching stats: {str(e)}'
        }), 500

# BUYER ROUTES - Temporary addition to main blueprint
@main_bp.route('/buyer/dashboard-stats', methods=['GET'])
def get_buyer_dashboard_stats():
    """Get statistics for buyer dashboard"""
    try:
        # Get total number of active sellers
        total_sellers = Seller.query.filter_by(is_active=True).count()
        
        # Get total number of available crops
        total_crops = SellerCrop.query.filter_by(is_available=True).count()
        
        # Get unique crop types
        unique_crop_types = db.session.query(SellerCrop.crop_name).filter_by(is_available=True).distinct().count()
        
        # Get verified sellers count
        verified_sellers = Seller.query.filter_by(is_active=True, is_verified=True).count()
        
        # Get crop distribution (top 10 most available crops)
        crop_distribution = db.session.query(
            SellerCrop.crop_name,
            func.count(SellerCrop.id).label('count')
        ).filter_by(is_available=True).group_by(
            SellerCrop.crop_name
        ).order_by(
            func.count(SellerCrop.id).desc()
        ).limit(10).all()
        
        crop_stats = [{'crop_name': crop[0], 'availability_count': crop[1]} for crop in crop_distribution]
        
        # Get province-wise seller distribution
        province_distribution = db.session.query(
            Province.name,
            func.count(Seller.id).label('seller_count')
        ).join(
            Seller, Province.id == Seller.province_id
        ).filter(
            Seller.is_active == True
        ).group_by(
            Province.name
        ).order_by(
            func.count(Seller.id).desc()
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

@main_bp.route('/buyer/test-endpoint', methods=['GET', 'POST'])
def buyer_test_endpoint():
    """Simple test endpoint for buyer functionality"""
    return jsonify({
        'success': True,
        'message': 'Buyer test endpoint is working!',
        'method': request.method
    })

@main_bp.route('/buyer/recommend-crop', methods=['POST'])
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
        model_path = os.path.join(os.path.dirname(__file__), 'crop_recommendation_model.pkl')
        
        if not os.path.exists(model_path):
            return jsonify({
                'success': False,
                'message': 'ML model not found. Please ensure the model file exists.'
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

@main_bp.route('/buyer/recommend-crop-full', methods=['POST'])
def recommend_crop_full():
    """Full crop recommendation with ML model - backup version"""
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
        model_path = os.path.join(os.path.dirname(__file__), 'crop_recommendation_model.pkl')
        
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
        sellers_with_crop = db.session.query(
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

@main_bp.route('/buyer/crop-details/<crop_id>', methods=['GET'])
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
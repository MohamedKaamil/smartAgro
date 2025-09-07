from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Seller, SellerCrop, CropCultivation, Province, District, City
import json

seller_bp = Blueprint('seller', __name__)

@seller_bp.route('/dashboard/<seller_id>', methods=['GET'])
def get_seller_dashboard(seller_id):
    try:
        # Get seller info
        seller_info = Seller.query.get(seller_id)
        
        if not seller_info:
            return jsonify({'success': False, 'message': 'Seller not found'}), 404
        
        # Get crop statistics
        total_crops = SellerCrop.query.filter_by(seller_id=seller_id).count()
        available_crops = SellerCrop.query.filter_by(seller_id=seller_id, is_available=True).count()
        # Calculate total quantity manually to avoid query issues
        available_crop_objects = SellerCrop.query.filter_by(seller_id=seller_id, is_available=True).all()
        total_quantity = sum(crop.quantity_available or 0 for crop in available_crop_objects)
        
        # Get recent crops
        recent_crops = SellerCrop.query.filter_by(seller_id=seller_id).order_by(
            SellerCrop.created_at.desc()
        ).limit(5).all()
        
        recent_crops_data = []
        for crop in recent_crops:
            recent_crops_data.append({
                'id': crop.id,
                'crop_name': crop.crop_name,
                'price_per_kg': crop.price_per_kg,
                'quantity_available': crop.quantity_available,
                'is_available': crop.is_available,
                'created_at': crop.created_at.isoformat() if crop.created_at else None
            })
        
        dashboard_data = {
            'seller_info': {
                'id': seller_info.id,
                'business_name': seller_info.business_name,
                'contact_number': seller_info.contact_number,
                'address': seller_info.address_line_1,
                'location': {
                    'province': seller_info.province.name if seller_info.province else None,
                    'district': seller_info.district.name if seller_info.district else None,
                    'city': seller_info.city.name if seller_info.city else None
                }
            },
            'statistics': {
                'total_crops': total_crops,
                'available_crops': available_crops,
                'total_quantity': total_quantity
            },
            'recent_crops': recent_crops_data
        }
        
        return jsonify({
            'success': True,
            'dashboard': dashboard_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@seller_bp.route('/register-business', methods=['POST'])
def register_business():
    """Register seller with user account and business details in one step"""
    try:
        data = request.get_json()
        
        # Validate required fields - now including email and password
        required_fields = [
            'email', 'password', 'business_name', 'contact_number', 'address_line_1',
            'province_id', 'district_id', 'city_id'
        ]
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Check if email already exists
        email = data['email'].lower().strip()
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Email address already registered'
            }), 409
        
        # Validate location IDs
        province = Province.query.get(data['province_id'])
        district = District.query.get(data['district_id'])
        city = City.query.get(data['city_id'])
        
        if not province or not district or not city:
            return jsonify({
                'success': False,
                'message': 'Invalid location IDs provided'
            }), 400
        
        # Validate location hierarchy
        if district.province_id != province.id or city.district_id != district.id:
            return jsonify({
                'success': False,
                'message': 'Location hierarchy mismatch'
            }), 400
        
        # Create user account first
        user = User(
            email=email,
            user_type='seller'
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.flush()  # Get the user ID
        
        # Create seller profile
        seller = Seller(
            user_id=user.id,
            
            # Basic Business Information
            business_name=data['business_name'],
            business_registration_number=data.get('business_registration_number'),
            business_type=data.get('business_type'),
            
            # Contact Information
            contact_number=data['contact_number'],
            secondary_contact=data.get('secondary_contact'),
            business_email=data.get('business_email'),
            website=data.get('website'),
            
            # Address Information
            address_line_1=data['address_line_1'],
            address_line_2=data.get('address_line_2'),
            postal_code=data.get('postal_code'),
            
            # Location
            province_id=data['province_id'],
            district_id=data['district_id'],
            city_id=data['city_id'],
            
            # Shop/Farm Details
            shop_name=data.get('shop_name'),
            shop_type=data.get('shop_type'),
            establishment_year=data.get('establishment_year'),
            shop_size_sqft=data.get('shop_size_sqft'),
            
            # Business Hours
            opening_hours=json.dumps(data.get('opening_hours')) if data.get('opening_hours') else None,
            operating_days=data.get('operating_days'),
            
            # Services
            services_offered=json.dumps(data.get('services_offered')) if data.get('services_offered') else None,
            delivery_available=data.get('delivery_available', False),
            home_delivery=data.get('home_delivery', False),
            pickup_available=data.get('pickup_available', True),
            
            # Additional Information
            description=data.get('description'),
            specialties=json.dumps(data.get('specialties')) if data.get('specialties') else None,
            certifications=json.dumps(data.get('certifications')) if data.get('certifications') else None
        )
        
        db.session.add(seller)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Business registered successfully',
            'seller': seller.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Business registration failed: {str(e)}'
        }), 500

@seller_bp.route('/profile/<user_id>', methods=['GET'])
def get_seller_profile(user_id):
    """Get seller profile"""
    try:
        seller = Seller.query.filter_by(user_id=user_id).first()
        
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Seller profile not found'
            }), 404
        
        return jsonify({
            'success': True,
            'seller': seller.to_dict(include_crops=True)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching seller profile: {str(e)}'
        }), 500

@seller_bp.route('/profile/<user_id>', methods=['PUT'])
def update_seller_profile(user_id):
    """Update seller profile"""
    try:
        seller = Seller.query.filter_by(user_id=user_id).first()
        
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Seller profile not found'
            }), 404
        
        data = request.get_json()
        
        # Update allowed fields
        updatable_fields = [
            'business_name', 'business_registration_number', 'business_type',
            'contact_number', 'secondary_contact', 'business_email', 'website',
            'address_line_1', 'address_line_2', 'postal_code',
            'shop_name', 'shop_type', 'establishment_year', 'shop_size_sqft',
            'operating_days', 'delivery_available', 'home_delivery', 'pickup_available',
            'description'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(seller, field, data[field])
        
        # Handle JSON fields
        json_fields = ['opening_hours', 'services_offered', 'specialties', 'certifications']
        for field in json_fields:
            if field in data:
                setattr(seller, field, json.dumps(data[field]) if data[field] else None)
        
        # Handle location updates
        if any(field in data for field in ['province_id', 'district_id', 'city_id']):
            province_id = data.get('province_id', seller.province_id)
            district_id = data.get('district_id', seller.district_id)
            city_id = data.get('city_id', seller.city_id)
            
            # Validate location hierarchy
            province = Province.query.get(province_id)
            district = District.query.get(district_id)
            city = City.query.get(city_id)
            
            if not province or not district or not city:
                return jsonify({
                    'success': False,
                    'message': 'Invalid location IDs provided'
                }), 400
            
            if district.province_id != province.id or city.district_id != district.id:
                return jsonify({
                    'success': False,
                    'message': 'Location hierarchy mismatch'
                }), 400
            
            seller.province_id = province_id
            seller.district_id = district_id
            seller.city_id = city_id
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Seller profile updated successfully',
            'seller': seller.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Profile update failed: {str(e)}'
        }), 500

@seller_bp.route('/crops', methods=['POST'])
def add_crop():
    """Add crop to seller's offerings"""
    try:
        data = request.get_json()
        
        required_fields = ['seller_id', 'crop_name']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields: seller_id, crop_name'
            }), 400
        
        # Validate seller exists
        seller = Seller.query.get(data['seller_id'])
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Seller not found'
            }), 404
        
        # Create crop entry
        crop = SellerCrop(
            seller_id=data['seller_id'],
            crop_name=data['crop_name'],
            crop_variety=data.get('crop_variety'),
            
            # Availability and Pricing
            is_available=data.get('is_available', True),
            price_per_kg=data.get('price_per_kg'),
            price_per_unit=data.get('price_per_unit'),
            unit_type=data.get('unit_type'),
            quantity_available=data.get('quantity_available'),
            minimum_order=data.get('minimum_order'),
            
            # Seasonal Information
            harvest_season=data.get('harvest_season'),
            best_quality_months=data.get('best_quality_months'),
            
            # Quality Information
            quality_grade=data.get('quality_grade'),
            organic_certified=data.get('organic_certified', False),
            pesticide_free=data.get('pesticide_free', False)
        )
        
        db.session.add(crop)
        db.session.flush()  # Get the crop ID
        
        # Add cultivation information if provided
        cultivation_data = data.get('cultivation')
        if cultivation_data:
            cultivation = CropCultivation(
                seller_crop_id=crop.id,
                seed_nursery=cultivation_data.get('seed_nursery'),
                land_preparation=cultivation_data.get('land_preparation'),
                planting=cultivation_data.get('planting'),
                crop_management=cultivation_data.get('crop_management'),
                seed_requirements=cultivation_data.get('seed_requirements'),
                cultivation_steps=cultivation_data.get('cultivation_steps'),
                
                # Additional cultivation info
                irrigation_method=cultivation_data.get('irrigation_method'),
                fertilizer_used=json.dumps(cultivation_data.get('fertilizer_used')) if cultivation_data.get('fertilizer_used') else None,
                pest_control_methods=json.dumps(cultivation_data.get('pest_control_methods')) if cultivation_data.get('pest_control_methods') else None,
                harvesting_method=cultivation_data.get('harvesting_method'),
                post_harvest_handling=cultivation_data.get('post_harvest_handling'),
                
                # Growing conditions
                soil_type=cultivation_data.get('soil_type'),
                water_requirements=cultivation_data.get('water_requirements'),
                sunlight_requirements=cultivation_data.get('sunlight_requirements'),
                temperature_range=cultivation_data.get('temperature_range'),
                
                # Timeline
                planting_season=cultivation_data.get('planting_season'),
                growing_duration_days=cultivation_data.get('growing_duration_days')
            )
            db.session.add(cultivation)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Crop added successfully',
            'crop': crop.to_dict(include_cultivation=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to add crop: {str(e)}'
        }), 500

@seller_bp.route('/crops/<seller_id>', methods=['GET'])
def get_seller_crops(seller_id):
    """Get all crops for a seller"""
    try:
        seller = Seller.query.get(seller_id)
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Seller not found'
            }), 404
        
        crops = SellerCrop.query.filter_by(seller_id=seller_id).all()
        
        return jsonify({
            'success': True,
            'crops': [crop.to_dict(include_cultivation=True) for crop in crops]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching crops: {str(e)}'
        }), 500

@seller_bp.route('/crops/<crop_id>', methods=['PUT'])
def update_crop(crop_id):
    """Update crop information"""
    try:
        crop = SellerCrop.query.get(crop_id)
        if not crop:
            return jsonify({
                'success': False,
                'message': 'Crop not found'
            }), 404
        
        data = request.get_json()
        
        # Update crop fields
        updatable_fields = [
            'crop_name', 'crop_variety', 'is_available', 'price_per_kg', 
            'price_per_unit', 'unit_type', 'quantity_available', 'minimum_order',
            'harvest_season', 'best_quality_months', 'quality_grade',
            'organic_certified', 'pesticide_free'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(crop, field, data[field])
        
        # Update cultivation information if provided
        cultivation_data = data.get('cultivation')
        if cultivation_data:
            cultivation = crop.cultivation_info
            if not cultivation:
                cultivation = CropCultivation(seller_crop_id=crop.id)
                db.session.add(cultivation)
            
            cultivation_fields = [
                'seed_nursery', 'land_preparation', 'planting', 'crop_management',
                'seed_requirements', 'cultivation_steps', 'irrigation_method',
                'harvesting_method', 'post_harvest_handling', 'soil_type',
                'water_requirements', 'sunlight_requirements', 'temperature_range',
                'planting_season', 'growing_duration_days'
            ]
            
            for field in cultivation_fields:
                if field in cultivation_data:
                    setattr(cultivation, field, cultivation_data[field])
            
            # Handle JSON fields
            json_cultivation_fields = ['fertilizer_used', 'pest_control_methods']
            for field in json_cultivation_fields:
                if field in cultivation_data:
                    setattr(cultivation, field, json.dumps(cultivation_data[field]) if cultivation_data[field] else None)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Crop updated successfully',
            'crop': crop.to_dict(include_cultivation=True)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to update crop: {str(e)}'
        }), 500

@seller_bp.route('/crops/<crop_id>', methods=['DELETE'])
def delete_crop(crop_id):
    """Delete crop"""
    try:
        crop = SellerCrop.query.get(crop_id)
        if not crop:
            return jsonify({
                'success': False,
                'message': 'Crop not found'
            }), 404
        
        db.session.delete(crop)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Crop deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to delete crop: {str(e)}'
        }), 500

@seller_bp.route('/cultivation', methods=['POST'])
def add_cultivation():
    """Add cultivation information for a crop"""
    try:
        data = request.get_json()
        
        required_fields = ['seller_crop_id']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required field: seller_crop_id'
            }), 400
        
        # Check if crop exists
        crop = SellerCrop.query.get(data['seller_crop_id'])
        if not crop:
            return jsonify({
                'success': False,
                'message': 'Crop not found'
            }), 404
        
        # Check if cultivation already exists
        existing_cultivation = CropCultivation.query.filter_by(seller_crop_id=data['seller_crop_id']).first()
        if existing_cultivation:
            return jsonify({
                'success': False,
                'message': 'Cultivation information already exists for this crop'
            }), 409
        
        # Create cultivation entry
        cultivation = CropCultivation(
            seller_crop_id=data['seller_crop_id'],
            seed_nursery=data.get('seed_nursery'),
            land_preparation=data.get('land_preparation'),
            planting=data.get('planting'),
            crop_management=data.get('crop_management'),
            seed_requirements=data.get('seed_requirements'),
            cultivation_steps=data.get('cultivation_steps'),
            irrigation_method=data.get('irrigation_method'),
            fertilizer_used=data.get('fertilizer_used'),
            pest_control_methods=data.get('pest_control_methods'),
            harvesting_method=data.get('harvesting_method'),
            post_harvest_handling=data.get('post_harvest_handling'),
            soil_type=data.get('soil_type'),
            water_requirements=data.get('water_requirements'),
            sunlight_requirements=data.get('sunlight_requirements'),
            temperature_range=data.get('temperature_range'),
            planting_season=data.get('planting_season'),
            growing_duration_days=data.get('growing_duration_days')
        )
        
        db.session.add(cultivation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cultivation information added successfully',
            'cultivation': cultivation.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to add cultivation: {str(e)}'
        }), 500

@seller_bp.route('/cultivation/crop/<crop_id>', methods=['GET'])
def get_cultivation_by_crop(crop_id):
    """Get cultivation information by crop ID"""
    try:
        cultivation = CropCultivation.query.filter_by(seller_crop_id=crop_id).first()
        
        return jsonify({
            'success': True,
            'cultivation': cultivation.to_dict() if cultivation else None
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching cultivation: {str(e)}'
        }), 500

@seller_bp.route('/cultivation/<cultivation_id>', methods=['PUT'])
def update_cultivation(cultivation_id):
    """Update cultivation information"""
    try:
        cultivation = CropCultivation.query.get(cultivation_id)
        if not cultivation:
            return jsonify({
                'success': False,
                'message': 'Cultivation not found'
            }), 404
        
        data = request.get_json()
        
        # Update cultivation fields
        updatable_fields = [
            'seed_nursery', 'land_preparation', 'planting', 'crop_management',
            'seed_requirements', 'cultivation_steps', 'irrigation_method',
            'fertilizer_used', 'pest_control_methods', 'harvesting_method',
            'post_harvest_handling', 'soil_type', 'water_requirements',
            'sunlight_requirements', 'temperature_range', 'planting_season',
            'growing_duration_days'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(cultivation, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cultivation updated successfully',
            'cultivation': cultivation.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to update cultivation: {str(e)}'
        }), 500

@seller_bp.route('/cultivation/<cultivation_id>', methods=['DELETE'])
def delete_cultivation(cultivation_id):
    """Delete cultivation information"""
    try:
        cultivation = CropCultivation.query.get(cultivation_id)
        if not cultivation:
            return jsonify({
                'success': False,
                'message': 'Cultivation not found'
            }), 404
        
        db.session.delete(cultivation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cultivation deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to delete cultivation: {str(e)}'
        }), 500
from flask import Blueprint, jsonify
from app.models import Province, District, City

locations_bp = Blueprint('locations', __name__)

@locations_bp.route('/provinces', methods=['GET'])
def get_provinces():
    """Get all provinces"""
    try:
        provinces = Province.query.order_by(Province.name).all()
        return jsonify({
            'success': True,
            'provinces': [province.to_dict() for province in provinces]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching provinces: {str(e)}'
        }), 500

@locations_bp.route('/districts/<int:province_id>', methods=['GET'])
def get_districts(province_id):
    """Get districts by province"""
    try:
        province = Province.query.get(province_id)
        if not province:
            return jsonify({
                'success': False,
                'message': 'Province not found'
            }), 404
        
        districts = District.query.filter_by(province_id=province_id).order_by(District.name).all()
        return jsonify({
            'success': True,
            'districts': [district.to_dict() for district in districts]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching districts: {str(e)}'
        }), 500

@locations_bp.route('/cities/<int:district_id>', methods=['GET'])
def get_cities(district_id):
    """Get cities by district"""
    try:
        district = District.query.get(district_id)
        if not district:
            return jsonify({
                'success': False,
                'message': 'District not found'
            }), 404
        
        cities = City.query.filter_by(district_id=district_id).order_by(City.name).all()
        return jsonify({
            'success': True,
            'cities': [city.to_dict() for city in cities]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching cities: {str(e)}'
        }), 500

@locations_bp.route('/location-info/<int:city_id>', methods=['GET'])
def get_location_info(city_id):
    """Get complete location information (city, district, province)"""
    try:
        city = City.query.get(city_id)
        if not city:
            return jsonify({
                'success': False,
                'message': 'City not found'
            }), 404
        
        return jsonify({
            'success': True,
            'location': {
                'city': city.to_dict(),
                'district': city.district.to_dict(),
                'province': city.district.province.to_dict()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching location info: {str(e)}'
        }), 500
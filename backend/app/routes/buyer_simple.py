from flask import Blueprint, jsonify

buyer_bp = Blueprint('buyer_new', __name__)

@buyer_bp.route('/test', methods=['GET'])
def test():
    """Simple test endpoint"""
    return jsonify({
        'success': True,
        'message': 'Buyer API is working!'
    })

@buyer_bp.route('/dashboard-stats', methods=['GET'])
def get_buyer_dashboard_stats():
    """Get statistics for buyer dashboard - simple version"""
    return jsonify({
        'success': True,
        'dashboard_stats': {
            'overview': {
                'total_sellers': 1,
                'total_crops': 4,
                'unique_crop_types': 4,
                'verified_sellers': 1
            },
            'crop_distribution': [
                {'crop_name': 'rice', 'availability_count': 1},
                {'crop_name': 'wheat', 'availability_count': 1}
            ],
            'province_distribution': [
                {'province': 'Western Province', 'seller_count': 1}
            ]
        }
    })
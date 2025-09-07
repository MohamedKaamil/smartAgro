from flask import Blueprint, jsonify

buyer_test_bp = Blueprint('buyer_test', __name__)

@buyer_test_bp.route('/test', methods=['GET'])
def test_route():
    return jsonify({'message': 'Buyer test route works!'})
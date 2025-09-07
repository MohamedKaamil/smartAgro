from flask import Blueprint, request, jsonify
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'user_type']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False, 
                'message': 'Missing required fields: email, password, user_type'
            }), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        user_type = data['user_type']
        
        # Validate user type
        if user_type not in ['buyer', 'seller']:
            return jsonify({
                'success': False, 
                'message': 'Invalid user type. Must be "buyer" or "seller"'
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False, 
                'message': 'Email address already registered'
            }), 409
        
        # Create new user
        user = User(
            email=email,
            user_type=user_type
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False, 
            'message': f'Registration failed: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(field in data for field in ['email', 'password']):
            return jsonify({
                'success': False, 
                'message': 'Email and password required'
            }), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({
                'success': False, 
                'message': 'Invalid email or password'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False, 
                'message': 'Account is deactivated. Please contact support.'
            }), 401
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Login failed: {str(e)}'
        }), 500

@auth_bp.route('/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    """Get user profile"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False, 
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error fetching profile: {str(e)}'
        }), 500

@auth_bp.route('/profile/<user_id>', methods=['PUT'])
def update_profile(user_id):
    """Update user profile"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False, 
                'message': 'User not found'
            }), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'email' in data:
            new_email = data['email'].lower().strip()
            # Check if email is already taken by another user
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({
                    'success': False, 
                    'message': 'Email already taken by another user'
                }), 409
            user.email = new_email
        
        if 'password' in data:
            user.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False, 
            'message': f'Profile update failed: {str(e)}'
        }), 500
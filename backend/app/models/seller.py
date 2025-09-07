from app import db
from datetime import datetime
import uuid

class Seller(db.Model):
    """Enhanced Seller model with comprehensive business details"""
    __tablename__ = 'sellers'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Basic Business Information
    business_name = db.Column(db.String(200), nullable=False)
    business_registration_number = db.Column(db.String(50), unique=True, nullable=True)  # BR number
    business_type = db.Column(db.String(50), nullable=True)  # e.g., 'sole_proprietorship', 'partnership', 'company'
    
    # Contact Information
    contact_number = db.Column(db.String(20), nullable=False)
    secondary_contact = db.Column(db.String(20), nullable=True)
    business_email = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    
    # Address Information
    address_line_1 = db.Column(db.String(255), nullable=False)
    address_line_2 = db.Column(db.String(255), nullable=True)
    postal_code = db.Column(db.String(10), nullable=True)
    
    # Location (Foreign Keys)
    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    
    # Shop/Farm Details
    shop_name = db.Column(db.String(200), nullable=True)  # Display name for the shop
    shop_type = db.Column(db.String(50), nullable=True)  # e.g., 'retail', 'wholesale', 'farm', 'nursery'
    establishment_year = db.Column(db.Integer, nullable=True)
    shop_size_sqft = db.Column(db.Float, nullable=True)  # Shop/farm size in square feet
    
    # Business Hours
    opening_hours = db.Column(db.Text, nullable=True)  # JSON string for business hours
    operating_days = db.Column(db.String(100), nullable=True)  # e.g., 'Monday-Saturday'
    
    # Services Offered
    services_offered = db.Column(db.Text, nullable=True)  # JSON array of services
    delivery_available = db.Column(db.Boolean, default=False)
    home_delivery = db.Column(db.Boolean, default=False)
    pickup_available = db.Column(db.Boolean, default=True)
    
    # Business Status
    is_verified = db.Column(db.Boolean, default=False)
    verification_documents = db.Column(db.Text, nullable=True)  # JSON array of document paths
    is_active = db.Column(db.Boolean, default=True)
    
    # Additional Information
    description = db.Column(db.Text, nullable=True)  # Business description
    specialties = db.Column(db.Text, nullable=True)  # JSON array of specialties
    certifications = db.Column(db.Text, nullable=True)  # JSON array of certifications
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    verified_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    crops = db.relationship('SellerCrop', backref='seller', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_full_address(self):
        """Get formatted full address"""
        address_parts = [self.address_line_1]
        if self.address_line_2:
            address_parts.append(self.address_line_2)
        if self.city:
            address_parts.append(self.city.name)
        if self.district:
            address_parts.append(self.district.name)
        if self.province:
            address_parts.append(self.province.name)
        if self.postal_code:
            address_parts.append(self.postal_code)
        return ', '.join(address_parts)
    
    def to_dict(self, include_crops=False):
        """Convert seller to dictionary"""
        seller_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'business_name': self.business_name,
            'business_registration_number': self.business_registration_number,
            'business_type': self.business_type,
            'contact_number': self.contact_number,
            'secondary_contact': self.secondary_contact,
            'business_email': self.business_email,
            'website': self.website,
            'address': {
                'line_1': self.address_line_1,
                'line_2': self.address_line_2,
                'postal_code': self.postal_code,
                'full_address': self.get_full_address()
            },
            'location': {
                'province_id': self.province_id,
                'district_id': self.district_id,
                'city_id': self.city_id,
                'province': self.province.name if self.province else None,
                'district': self.district.name if self.district else None,
                'city': self.city.name if self.city else None
            },
            'shop_details': {
                'shop_name': self.shop_name,
                'shop_type': self.shop_type,
                'establishment_year': self.establishment_year,
                'shop_size_sqft': self.shop_size_sqft,
                'opening_hours': self.opening_hours,
                'operating_days': self.operating_days
            },
            'services': {
                'services_offered': self.services_offered,
                'delivery_available': self.delivery_available,
                'home_delivery': self.home_delivery,
                'pickup_available': self.pickup_available
            },
            'verification': {
                'is_verified': self.is_verified,
                'is_active': self.is_active,
                'verified_at': self.verified_at.isoformat() if self.verified_at else None
            },
            'additional_info': {
                'description': self.description,
                'specialties': self.specialties,
                'certifications': self.certifications
            },
            'timestamps': {
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None
            }
        }
        
        if include_crops:
            seller_dict['crops'] = [crop.to_dict() for crop in self.crops]
        
        return seller_dict
    
    def __repr__(self):
        return f'<Seller {self.business_name}>'

class SellerCrop(db.Model):
    """Crops offered by sellers"""
    __tablename__ = 'seller_crops'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    seller_id = db.Column(db.String(36), db.ForeignKey('sellers.id'), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False, index=True)
    crop_variety = db.Column(db.String(100), nullable=True)  # e.g., 'Basmati', 'Jasmine'
    
    # Availability and Pricing
    is_available = db.Column(db.Boolean, default=True)
    price_per_kg = db.Column(db.Float, nullable=True)
    price_per_unit = db.Column(db.Float, nullable=True)  # Alternative pricing
    unit_type = db.Column(db.String(20), nullable=True)  # e.g., 'bunch', 'piece', 'packet'
    quantity_available = db.Column(db.Float, nullable=True)
    minimum_order = db.Column(db.Float, nullable=True)
    
    # Seasonal Information
    harvest_season = db.Column(db.String(100), nullable=True)  # e.g., 'March-May, September-November'
    best_quality_months = db.Column(db.String(100), nullable=True)
    
    # Quality Information
    quality_grade = db.Column(db.String(20), nullable=True)  # e.g., 'Premium', 'Grade A', 'Grade B'
    organic_certified = db.Column(db.Boolean, default=False)
    pesticide_free = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cultivation_info = db.relationship('CropCultivation', backref='crop', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self, include_cultivation=False):
        """Convert crop to dictionary"""
        crop_dict = {
            'id': self.id,
            'seller_id': self.seller_id,
            'crop_name': self.crop_name,
            'crop_variety': self.crop_variety,
            'availability': {
                'is_available': self.is_available,
                'quantity_available': self.quantity_available,
                'minimum_order': self.minimum_order
            },
            'pricing': {
                'price_per_kg': self.price_per_kg,
                'price_per_unit': self.price_per_unit,
                'unit_type': self.unit_type
            },
            'seasonal_info': {
                'harvest_season': self.harvest_season,
                'best_quality_months': self.best_quality_months
            },
            'quality': {
                'quality_grade': self.quality_grade,
                'organic_certified': self.organic_certified,
                'pesticide_free': self.pesticide_free
            },
            'timestamps': {
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None
            }
        }
        
        if include_cultivation and self.cultivation_info:
            crop_dict['cultivation'] = self.cultivation_info.to_dict()
        
        return crop_dict
    
    def __repr__(self):
        return f'<SellerCrop {self.crop_name}>'

class CropCultivation(db.Model):
    """Cultivation information for crops"""
    __tablename__ = 'crop_cultivations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    seller_crop_id = db.Column(db.String(36), db.ForeignKey('seller_crops.id'), nullable=False, unique=True)
    
    # Cultivation Steps and Information
    seed_nursery = db.Column(db.Text, nullable=True)
    land_preparation = db.Column(db.Text, nullable=True)
    planting = db.Column(db.Text, nullable=True)
    crop_management = db.Column(db.Text, nullable=True)
    seed_requirements = db.Column(db.Text, nullable=True)
    cultivation_steps = db.Column(db.Text, nullable=True)
    
    # Additional Cultivation Info
    irrigation_method = db.Column(db.String(100), nullable=True)
    fertilizer_used = db.Column(db.Text, nullable=True)  # JSON array
    pest_control_methods = db.Column(db.Text, nullable=True)  # JSON array
    harvesting_method = db.Column(db.Text, nullable=True)
    post_harvest_handling = db.Column(db.Text, nullable=True)
    
    # Growing Conditions
    soil_type = db.Column(db.String(100), nullable=True)
    water_requirements = db.Column(db.String(100), nullable=True)
    sunlight_requirements = db.Column(db.String(100), nullable=True)
    temperature_range = db.Column(db.String(50), nullable=True)
    
    # Timeline
    planting_season = db.Column(db.String(100), nullable=True)
    growing_duration_days = db.Column(db.Integer, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert cultivation info to dictionary"""
        return {
            'id': self.id,
            'seller_crop_id': self.seller_crop_id,
            'seed_nursery': self.seed_nursery,
            'land_preparation': self.land_preparation,
            'planting': self.planting,
            'crop_management': self.crop_management,
            'seed_requirements': self.seed_requirements,
            'cultivation_steps': self.cultivation_steps,
            'irrigation_method': self.irrigation_method,
            'fertilizer_used': self.fertilizer_used,
            'pest_control_methods': self.pest_control_methods,
            'harvesting_method': self.harvesting_method,
            'post_harvest_handling': self.post_harvest_handling,
            'soil_type': self.soil_type,
            'water_requirements': self.water_requirements,
            'sunlight_requirements': self.sunlight_requirements,
            'temperature_range': self.temperature_range,
            'planting_season': self.planting_season,
            'growing_duration_days': self.growing_duration_days,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<CropCultivation {self.id}>'
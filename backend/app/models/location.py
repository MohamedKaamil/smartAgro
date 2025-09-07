from app import db
from datetime import datetime

class Province(db.Model):
    """Province model for Sri Lankan provinces"""
    __tablename__ = 'provinces'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    districts = db.relationship('District', backref='province', lazy='dynamic', cascade='all, delete-orphan')
    sellers = db.relationship('Seller', backref='province', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return f'<Province {self.name}>'

class District(db.Model):
    """District model for Sri Lankan districts"""
    __tablename__ = 'districts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    cities = db.relationship('City', backref='district', lazy='dynamic', cascade='all, delete-orphan')
    sellers = db.relationship('Seller', backref='district', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'province_id': self.province_id
        }
    
    def __repr__(self):
        return f'<District {self.name}>'

class City(db.Model):
    """City model for Sri Lankan cities"""
    __tablename__ = 'cities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sellers = db.relationship('Seller', backref='city', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'district_id': self.district_id
        }
    
    def __repr__(self):
        return f'<City {self.name}>'
# Structured Flask Backend - Directory Overview

## 📁 Directory Structure

```
backend/
├── run.py                          # Main entry point
├── requirements_structured.txt     # Dependencies
├── app.py                          # Old monolithic file (keep as reference)
├── config/
│   ├── __init__.py
│   └── config.py                   # Configuration settings
├── app/
│   ├── __init__.py                 # Application factory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                 # User model
│   │   ├── location.py             # Province, District, City models
│   │   └── seller.py               # Seller, SellerCrop, CropCultivation models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                 # Authentication routes
│   │   ├── locations.py            # Location-related routes
│   │   ├── seller.py               # Seller business registration
│   │   └── main.py                 # Health, search, stats
│   └── utils/
│       ├── __init__.py
│       └── database.py             # Database utilities
```

## 🚀 API Endpoints

### Authentication (`/api/auth/`)
- `POST /register` - Register new user (buyer/seller)
- `POST /login` - User login
- `GET /profile/<user_id>` - Get user profile
- `PUT /profile/<user_id>` - Update user profile

### Locations (`/api/locations/`)
- `GET /provinces` - Get all provinces
- `GET /districts/<province_id>` - Get districts by province
- `GET /cities/<district_id>` - Get cities by district
- `GET /location-info/<city_id>` - Get complete location info

### Seller Business (`/api/seller/`)
- `POST /register-business` - **Enhanced** business registration
- `GET /profile/<user_id>` - Get seller profile
- `PUT /profile/<user_id>` - Update seller profile
- `POST /crops` - Add crop to seller
- `GET /crops/<seller_id>` - Get seller's crops
- `PUT /crops/<crop_id>` - Update crop
- `DELETE /crops/<crop_id>` - Delete crop

### General (`/api/`)
- `GET /health` - Health check with stats
- `GET /find-sellers/<crop_name>` - Find sellers by crop
- `GET /crops/search` - Search crops with pagination
- `GET /stats` - Application statistics

## 🏢 Enhanced Business Registration Fields

### Basic Business Information
- `business_name` ✅ **Required**
- `business_registration_number` (BR number)
- `business_type` (sole_proprietorship, partnership, company)

### Contact Information
- `contact_number` ✅ **Required**
- `secondary_contact`
- `business_email`
- `website`

### Address Information
- `address_line_1` ✅ **Required**
- `address_line_2`
- `postal_code`
- `province_id` ✅ **Required**
- `district_id` ✅ **Required**
- `city_id` ✅ **Required**

### Shop/Farm Details
- `shop_name` (Display name)
- `shop_type` (retail, wholesale, farm, nursery)
- `establishment_year`
- `shop_size_sqft`

### Business Operations
- `opening_hours` (JSON)
- `operating_days`
- `services_offered` (JSON)
- `delivery_available`
- `home_delivery`
- `pickup_available`

### Additional Information
- `description`
- `specialties` (JSON)
- `certifications` (JSON)

## 🗄️ Database Models

### User
- Enhanced with email verification
- Account status management
- Relationships with seller profile

### Seller (Enhanced)
- Comprehensive business details
- Location hierarchy validation
- Service offerings
- Verification status

### SellerCrop (Enhanced)
- Pricing options (per kg, per unit)
- Quality information
- Seasonal data
- Organic certification

### CropCultivation (Enhanced)
- Detailed cultivation steps
- Growing conditions
- Timeline information
- Methods and techniques

## 🔧 Features

### ✅ Completed Features
- Structured Flask application with blueprints
- Enhanced database models with comprehensive fields
- Location hierarchy validation
- Business registration with detailed information
- Crop management with cultivation details
- Search and filtering capabilities
- Health monitoring and statistics
- CORS enabled for frontend integration

### 🚀 Ready for Frontend Integration
- All API endpoints are functional
- Database is populated with Sri Lankan locations
- Enhanced business registration form support
- Modern JSON responses with proper error handling

## 💡 Usage Examples

### Register Business (Enhanced)
```json
POST /api/seller/register-business
{
  "user_id": "user-uuid",
  "business_name": "Green Valley Farm",
  "business_registration_number": "BR123456789",
  "business_type": "sole_proprietorship",
  "contact_number": "+94771234567",
  "secondary_contact": "+94112345678",
  "business_email": "info@greenvalley.lk",
  "website": "https://greenvalley.lk",
  "address_line_1": "123 Farm Road",
  "address_line_2": "Near Central Market",
  "postal_code": "10100",
  "province_id": 1,
  "district_id": 1,
  "city_id": 1,
  "shop_name": "Green Valley Store",
  "shop_type": "farm",
  "establishment_year": 2020,
  "shop_size_sqft": 5000,
  "operating_days": "Monday-Saturday",
  "opening_hours": {"mon_fri": "8:00-17:00", "sat": "8:00-15:00"},
  "services_offered": ["fresh_produce", "organic_vegetables", "delivery"],
  "delivery_available": true,
  "home_delivery": true,
  "pickup_available": true,
  "description": "Fresh organic vegetables and fruits",
  "specialties": ["organic", "pesticide_free", "local_varieties"],
  "certifications": ["organic_certified", "good_agricultural_practices"]
}
```
#!/usr/bin/env python3
"""
Script to add a comprehensive test seller with all crop varieties for testing
"""
import mysql.connector
from mysql.connector import Error
import uuid
from datetime import datetime
import random

# All crops from the ML model
ALL_CROPS = [
    'almond', 'amaranth', 'apple', 'apricot', 'artichoke', 'asparagus', 'avocado', 
    'bamboo', 'banana', 'barley', 'basil', 'beetroot', 'betel', 'bilberry', 
    'blackberry', 'blackgram', 'blueberry', 'breadfruit', 'broccoli', 'buckwheat', 
    'cabbage', 'carambola', 'carrot', 'cashew', 'cassava', 'cauliflower', 'celery', 
    'chard', 'cherry', 'chia', 'chickpea', 'clementine', 'coconut', 'coffee', 
    'cotton', 'cranberry', 'cucumber', 'currant', 'date', 'dragonfruit', 'durian', 
    'eggplant', 'fig', 'garlic', 'ginger', 'gooseberry', 'grapes', 'guava', 
    'hazelnut', 'hemp', 'jackfruit', 'jambul', 'jute', 'kidneybeans', 'kiwi', 
    'leek', 'lemongrass', 'lentil', 'lettuce', 'longan', 'lychee', 'macadamia', 
    'maize', 'mandarin', 'mango', 'mangosteen', 'melon', 'millet', 'mint', 
    'mothbeans', 'mulberry', 'mungbean', 'muskmelon', 'nectarine', 'oats', 'okra', 
    'olive', 'onion', 'orange', 'papaya', 'parsley', 'passionfruit', 'peach', 
    'pear', 'peas', 'pecan', 'persimmon', 'pigeonpeas', 'pistachio', 'plantain', 
    'plum', 'pomegranate', 'pomelo', 'pumpkin', 'quince', 'radish', 'rambutan', 
    'raspberry', 'rice', 'rye', 'salak', 'sapodilla', 'sorghum', 'soursop', 
    'soybean', 'spinach', 'starfruit', 'strawberry', 'sunflower', 'sweetpotato', 
    'tamarind', 'tangelo', 'taro', 'teff', 'tomato', 'turmeric', 'turnip', 
    'walnut', 'watermelon', 'wheat', 'yam', 'zucchini'
]

def get_database_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='crop_recommendation',
            port=3306
        )
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def create_test_user():
    """Create a test user account"""
    connection = get_database_connection()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor()
        user_id = str(uuid.uuid4())
        
        # Insert test user
        user_query = """
            INSERT INTO users (id, email, password_hash, user_type, is_verified, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(user_query, (
            user_id,
            'test_seller@agriconnect.lk',
            'hashed_password_placeholder',  # In real app, this would be properly hashed
            'seller',
            True,
            datetime.utcnow()
        ))
        
        connection.commit()
        cursor.close()
        print(f"[OK] Created test user: {user_id}")
        return user_id
        
    except Error as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

def get_or_create_location_ids():
    """Get or create location IDs for testing"""
    connection = get_database_connection()
    if not connection:
        return None, None, None
        
    try:
        cursor = connection.cursor()
        
        # Check if Western Province exists, create if not
        cursor.execute("SELECT id FROM provinces WHERE name = 'Western Province'")
        province_result = cursor.fetchone()
        
        if province_result:
            province_id = province_result[0]
        else:
            cursor.execute("INSERT INTO provinces (name, created_at) VALUES ('Western Province', %s)", (datetime.utcnow(),))
            province_id = cursor.lastrowid
            print("[OK] Created Western Province")
        
        # Check if Colombo District exists, create if not
        cursor.execute("SELECT id FROM districts WHERE name = 'Colombo' AND province_id = %s", (province_id,))
        district_result = cursor.fetchone()
        
        if district_result:
            district_id = district_result[0]
        else:
            cursor.execute("INSERT INTO districts (name, province_id, created_at) VALUES ('Colombo', %s, %s)", (province_id, datetime.utcnow()))
            district_id = cursor.lastrowid
            print("[OK] Created Colombo District")
        
        # Check if Colombo City exists, create if not
        cursor.execute("SELECT id FROM cities WHERE name = 'Colombo' AND district_id = %s", (district_id,))
        city_result = cursor.fetchone()
        
        if city_result:
            city_id = city_result[0]
        else:
            cursor.execute("INSERT INTO cities (name, district_id, created_at) VALUES ('Colombo', %s, %s)", (district_id, datetime.utcnow()))
            city_id = cursor.lastrowid
            print("[OK] Created Colombo City")
        
        connection.commit()
        cursor.close()
        return province_id, district_id, city_id
        
    except Error as e:
        print(f"Error with locations: {e}")
        return None, None, None
    finally:
        if connection.is_connected():
            connection.close()

def create_test_seller(user_id, province_id, district_id, city_id):
    """Create a comprehensive test seller"""
    connection = get_database_connection()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor()
        seller_id = str(uuid.uuid4())
        
        # Insert comprehensive seller information
        seller_query = """
            INSERT INTO sellers (
                id, user_id, business_name, business_registration_number, business_type,
                contact_number, secondary_contact, business_email, website,
                address_line_1, address_line_2, postal_code,
                province_id, district_id, city_id,
                shop_name, shop_type, establishment_year, shop_size_sqft,
                opening_hours, operating_days, services_offered,
                delivery_available, home_delivery, pickup_available,
                is_verified, is_active, description, specialties, certifications,
                created_at, updated_at, verified_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        
        now = datetime.utcnow()
        
        cursor.execute(seller_query, (
            seller_id,
            user_id,
            'AgriConnect Test Farm & Nursery',
            'BR2024001',
            'agricultural_cooperative',
            '+94771234567',
            '+94112345678',
            'contact@agriconnectfarm.lk',
            'https://www.agriconnectfarm.lk',
            '123 Agricultural Avenue',
            'Near Central Market',
            '10100',
            province_id,
            district_id,
            city_id,
            'AgriConnect Central Hub',
            'wholesale',
            2015,
            50000.0,
            '{"monday": "6:00-18:00", "tuesday": "6:00-18:00", "wednesday": "6:00-18:00", "thursday": "6:00-18:00", "friday": "6:00-18:00", "saturday": "6:00-16:00", "sunday": "closed"}',
            'Monday to Saturday',
            '["wholesale", "retail", "organic_produce", "seeds_supply", "farming_consultation", "crop_planning"]',
            True,  # delivery_available
            True,  # home_delivery  
            True,  # pickup_available
            True,  # is_verified
            True,  # is_active
            'Premium agricultural supplier specializing in organic and conventional crops. We provide high-quality seeds, fresh produce, and comprehensive farming solutions for agricultural communities across Sri Lanka.',
            '["organic_farming", "seed_production", "sustainable_agriculture", "crop_rotation", "integrated_pest_management", "precision_farming"]',
            '["organic_certification", "good_agricultural_practices", "iso_9001", "haccp", "global_gap"]',
            now,
            now,
            now
        ))
        
        connection.commit()
        cursor.close()
        print(f"✅ Created comprehensive test seller: {seller_id}")
        return seller_id
        
    except Error as e:
        print(f"Error creating seller: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

def get_crop_varieties_and_info(crop_name):
    """Get realistic crop varieties and information based on crop type"""
    crop_info = {
        # Fruits
        'apple': {'varieties': ['Red Delicious', 'Granny Smith', 'Gala', 'Fuji'], 'season': 'March-May', 'price_range': (350, 800)},
        'banana': {'varieties': ['Cavendish', 'Red Banana', 'Lady Finger', 'Plantain'], 'season': 'Year-round', 'price_range': (120, 250)},
        'mango': {'varieties': ['Alphonso', 'Kesar', 'Totapuri', 'Banganapalli'], 'season': 'April-July', 'price_range': (200, 600)},
        'orange': {'varieties': ['Valencia', 'Navel', 'Blood Orange', 'Mandarin'], 'season': 'December-May', 'price_range': (180, 350)},
        'grapes': {'varieties': ['Thompson Seedless', 'Red Globe', 'Black Beauty'], 'season': 'January-April', 'price_range': (400, 800)},
        
        # Vegetables
        'tomato': {'varieties': ['Roma', 'Cherry', 'Beefsteak', 'Heirloom'], 'season': 'Year-round', 'price_range': (80, 200)},
        'onion': {'varieties': ['Red Onion', 'White Onion', 'Yellow Onion'], 'season': 'Year-round', 'price_range': (60, 150)},
        'carrot': {'varieties': ['Nantes', 'Chantenay', 'Imperator'], 'season': 'Year-round', 'price_range': (100, 200)},
        'cabbage': {'varieties': ['Green Cabbage', 'Red Cabbage', 'Savoy'], 'season': 'November-March', 'price_range': (40, 100)},
        'cauliflower': {'varieties': ['Snowball', 'Purple Head', 'Romanesco'], 'season': 'November-March', 'price_range': (80, 180)},
        
        # Grains & Cereals  
        'rice': {'varieties': ['Basmati', 'Jasmine', 'Samba', 'Red Rice'], 'season': 'Maha: October-March, Yala: May-August', 'price_range': (120, 250)},
        'wheat': {'varieties': ['Durum', 'Hard Red', 'Soft White'], 'season': 'December-April', 'price_range': (80, 150)},
        'maize': {'varieties': ['Sweet Corn', 'Field Corn', 'Baby Corn'], 'season': 'Year-round', 'price_range': (60, 120)},
        'barley': {'varieties': ['Two-row', 'Six-row', 'Hull-less'], 'season': 'November-March', 'price_range': (70, 130)},
        
        # Legumes
        'kidneybeans': {'varieties': ['Dark Red', 'Light Red', 'White Kidney'], 'season': 'October-February', 'price_range': (200, 350)},
        'chickpea': {'varieties': ['Kabuli', 'Desi', 'Green Chickpea'], 'season': 'November-March', 'price_range': (150, 300)},
        'lentil': {'varieties': ['Red Lentil', 'Green Lentil', 'Black Lentil'], 'season': 'October-February', 'price_range': (180, 320)},
        'soybean': {'varieties': ['Yellow Soybean', 'Black Soybean', 'Edamame'], 'season': 'June-October', 'price_range': (150, 250)},
        
        # Spices & Herbs
        'turmeric': {'varieties': ['Curcuma Longa', 'Lakadong', 'Erode'], 'season': 'March-May', 'price_range': (300, 600)},
        'ginger': {'varieties': ['Fresh Ginger', 'Dry Ginger', 'Young Ginger'], 'season': 'Year-round', 'price_range': (200, 400)},
        'garlic': {'varieties': ['White Garlic', 'Purple Garlic', 'Elephant Garlic'], 'season': 'April-June', 'price_range': (250, 500)},
        
        # Cash Crops
        'cotton': {'varieties': ['Bt Cotton', 'Hybrid Cotton', 'Desi Cotton'], 'season': 'June-October', 'price_range': (100, 200)},
        'coffee': {'varieties': ['Arabica', 'Robusta', 'Liberica'], 'season': 'November-February', 'price_range': (800, 1500)},
        'coconut': {'varieties': ['Tall Variety', 'Dwarf Variety', 'Hybrid'], 'season': 'Year-round', 'price_range': (30, 80)},
    }
    
    # Default values for crops not specifically defined
    default_info = {
        'varieties': ['Premium Grade', 'Standard Grade', 'Organic'],
        'season': 'Seasonal',
        'price_range': (100, 300)
    }
    
    return crop_info.get(crop_name, default_info)

def get_cultivation_info(crop_name):
    """Get realistic cultivation information for each crop"""
    cultivation_data = {
        'rice': {
            'seed_nursery': 'Prepare seedbed with well-decomposed organic matter. Soak seeds for 24 hours before sowing.',
            'land_preparation': 'Plow the field 2-3 times. Level the field and prepare bunds for water management.',
            'planting': 'Transplant 25-30 day old seedlings with 20x15 cm spacing. Plant 2-3 seedlings per hill.',
            'crop_management': 'Maintain 2-5cm water level. Apply fertilizer in splits. Control weeds and pests regularly.',
            'irrigation_method': 'Flood irrigation with controlled water levels',
            'fertilizer_used': 'NPK 20:10:10 at planting, Urea top dressing',
            'soil_type': 'Clay loam with good water retention',
            'water_requirements': 'High - 1200-1800mm annually',
            'growing_duration_days': 120
        },
        'tomato': {
            'seed_nursery': 'Sow seeds in seedbeds or trays. Maintain temperature 20-25°C for germination.',
            'land_preparation': 'Prepare raised beds with good drainage. Add compost and organic matter.',
            'planting': 'Transplant 4-5 week old seedlings with 60x45 cm spacing.',
            'crop_management': 'Support with stakes or cages. Prune suckers regularly. Monitor for diseases.',
            'irrigation_method': 'Drip irrigation or furrow irrigation',
            'fertilizer_used': 'NPK 19:19:19, Calcium nitrate, Micronutrients',
            'soil_type': 'Well-drained loamy soil with pH 6.0-7.0',
            'water_requirements': 'Medium - 600-800mm',
            'growing_duration_days': 90
        },
        'wheat': {
            'seed_nursery': 'Direct seeding in the field. No nursery required.',
            'land_preparation': 'Deep plowing followed by harrowing. Prepare a fine seedbed.',
            'planting': 'Sow seeds in rows 20-25 cm apart at 2-3 cm depth.',
            'crop_management': 'Control weeds at tillering stage. Monitor for rust diseases.',
            'irrigation_method': 'Furrow irrigation or sprinkler irrigation',
            'fertilizer_used': 'NPK 12:32:16 at planting, Urea at tillering',
            'soil_type': 'Well-drained clay loam soil',
            'water_requirements': 'Medium - 450-650mm',
            'growing_duration_days': 120
        }
    }
    
    # Default cultivation info for crops not specifically defined
    default_cultivation = {
        'seed_nursery': f'Prepare quality seeds for {crop_name}. Use certified seeds from reliable sources.',
        'land_preparation': f'Prepare soil according to {crop_name} requirements. Ensure proper drainage and soil fertility.',
        'planting': f'Plant {crop_name} at optimal spacing and depth for maximum yield.',
        'crop_management': f'Monitor {crop_name} growth regularly. Apply appropriate nutrients and pest control measures.',
        'irrigation_method': 'Appropriate irrigation based on crop requirements',
        'fertilizer_used': 'Balanced NPK fertilizers and organic amendments',
        'soil_type': 'Well-drained fertile soil suitable for cultivation',
        'water_requirements': 'Moderate water requirements',
        'growing_duration_days': 90
    }
    
    return cultivation_data.get(crop_name, default_cultivation)

def add_crops_for_seller(seller_id):
    """Add all crops for the test seller with realistic information"""
    connection = get_database_connection()
    if not connection:
        return False
        
    try:
        cursor = connection.cursor()
        crops_added = 0
        
        print(f"Adding {len(ALL_CROPS)} crops for seller...")
        
        for crop_name in ALL_CROPS:
            # Get crop-specific information
            crop_info = get_crop_varieties_and_info(crop_name)
            cultivation_info = get_cultivation_info(crop_name)
            
            # Random variety selection
            variety = random.choice(crop_info['varieties'])
            price_min, price_max = crop_info['price_range']
            price = random.randint(price_min, price_max)
            
            # Generate realistic quantities
            quantity = random.randint(100, 1000)
            min_order = random.randint(5, 20)
            
            # Random quality and certification
            organic = random.choice([True, False])
            pesticide_free = random.choice([True, False]) if not organic else True
            quality_grades = ['Premium', 'Grade A', 'Grade B', 'Standard']
            quality = random.choice(quality_grades)
            
            # Insert seller crop
            seller_crop_id = str(uuid.uuid4())
            
            crop_query = """
                INSERT INTO seller_crops (
                    id, seller_id, crop_name, crop_variety, is_available,
                    price_per_kg, quantity_available, minimum_order,
                    harvest_season, best_quality_months, quality_grade,
                    organic_certified, pesticide_free, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            cursor.execute(crop_query, (
                seller_crop_id,
                seller_id,
                crop_name,
                variety,
                True,  # is_available
                float(price),
                float(quantity),
                float(min_order),
                crop_info['season'],
                crop_info['season'],
                quality,
                organic,
                pesticide_free,
                datetime.utcnow(),
                datetime.utcnow()
            ))
            
            # Insert cultivation information
            cultivation_query = """
                INSERT INTO crop_cultivations (
                    id, seller_crop_id, seed_nursery, land_preparation, planting,
                    crop_management, seed_requirements, cultivation_steps,
                    irrigation_method, fertilizer_used, pest_control_methods,
                    harvesting_method, post_harvest_handling, soil_type,
                    water_requirements, sunlight_requirements, temperature_range,
                    planting_season, growing_duration_days, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            cultivation_id = str(uuid.uuid4())
            
            cursor.execute(cultivation_query, (
                cultivation_id,
                seller_crop_id,
                cultivation_info['seed_nursery'],
                cultivation_info['land_preparation'],
                cultivation_info['planting'],
                cultivation_info['crop_management'],
                f'Quality {crop_name} seeds, certified variety',
                f'Step-by-step cultivation guide for {crop_name}',
                cultivation_info['irrigation_method'],
                cultivation_info['fertilizer_used'],
                f'Integrated pest management for {crop_name}',
                f'Harvest {crop_name} at optimal maturity',
                f'Proper post-harvest handling for {crop_name}',
                cultivation_info['soil_type'],
                cultivation_info['water_requirements'],
                'Full sun to partial shade',
                '20-30°C optimal temperature range',
                crop_info['season'],
                cultivation_info['growing_duration_days'],
                datetime.utcnow(),
                datetime.utcnow()
            ))
            
            crops_added += 1
            
            # Print progress every 20 crops
            if crops_added % 20 == 0:
                print(f"  ✅ Added {crops_added}/{len(ALL_CROPS)} crops...")
        
        connection.commit()
        cursor.close()
        print(f"✅ Successfully added {crops_added} crops with cultivation information!")
        return True
        
    except Error as e:
        print(f"Error adding crops: {e}")
        return False
    finally:
        if connection.is_connected():
            connection.close()

def main():
    """Main function to create comprehensive test data"""
    print("Creating comprehensive test seller with all crops...")
    print("=" * 60)
    
    # Step 1: Create test user
    print("1. Creating test user account...")
    user_id = create_test_user()
    if not user_id:
        print("❌ Failed to create test user")
        return
    
    # Step 2: Get/create location data
    print("\n2. Setting up location data...")
    province_id, district_id, city_id = get_or_create_location_ids()
    if not all([province_id, district_id, city_id]):
        print("❌ Failed to setup location data")
        return
    
    # Step 3: Create comprehensive seller
    print("\n3. Creating comprehensive test seller...")
    seller_id = create_test_seller(user_id, province_id, district_id, city_id)
    if not seller_id:
        print("❌ Failed to create test seller")
        return
    
    # Step 4: Add all crops with cultivation info
    print(f"\n4. Adding all {len(ALL_CROPS)} crops with cultivation information...")
    success = add_crops_for_seller(seller_id)
    if not success:
        print("❌ Failed to add crops")
        return
    
    print("\n" + "=" * 60)
    print("🎉 SUCCESS! Test seller created successfully!")
    print("=" * 60)
    print(f"📊 Summary:")
    print(f"   • User ID: {user_id}")
    print(f"   • Seller ID: {seller_id}")
    print(f"   • Business: AgriConnect Test Farm & Nursery")
    print(f"   • Crops Added: {len(ALL_CROPS)} varieties")
    print(f"   • Location: Colombo, Western Province")
    print(f"   • Status: Verified & Active")
    print("=" * 60)
    print("🧪 Now you can test ML predictions - all crops will show this seller!")
    print("🌐 Frontend: http://localhost:3000")
    print("🔗 API: http://localhost:5001/predict")

if __name__ == "__main__":
    main()
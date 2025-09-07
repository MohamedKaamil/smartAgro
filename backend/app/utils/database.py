from app import db
from app.models import Province, District, City

# Sri Lankan location data
SRI_LANKA_LOCATIONS = {
    "Western": {
        "Colombo": ["Colombo", "Dehiwala-Mount Lavinia", "Moratuwa", "Sri Jayawardenepura Kotte"],
        "Gampaha": ["Gampaha", "Negombo", "Katunayake", "Ja-Ela", "Wattala"],
        "Kalutara": ["Kalutara", "Panadura", "Horana", "Beruwala"]
    },
    "Central": {
        "Kandy": ["Kandy", "Gampola", "Nawalapitiya", "Wattegama"],
        "Matale": ["Matale", "Dambulla", "Sigiriya", "Nalanda"],
        "Nuwara Eliya": ["Nuwara Eliya", "Hatton", "Talawakele", "Nanu Oya"]
    },
    "Southern": {
        "Galle": ["Galle", "Hikkaduwa", "Ambalangoda", "Elpitiya"],
        "Matara": ["Matara", "Weligama", "Mirissa", "Akuressa"],
        "Hambantota": ["Hambantota", "Tangalle", "Tissamaharama", "Kataragama"]
    },
    "Northern": {
        "Jaffna": ["Jaffna", "Chavakachcheri", "Point Pedro", "Karainagar"],
        "Kilinochchi": ["Kilinochchi", "Pallai", "Paranthan"],
        "Mannar": ["Mannar", "Nanattan", "Madhu"]
    },
    "Eastern": {
        "Trincomalee": ["Trincomalee", "Kinniya", "Mutur"],
        "Batticaloa": ["Batticaloa", "Kalmunai", "Valachchenai"],
        "Ampara": ["Ampara", "Akkaraipattu", "Kalmunai", "Sainthamaruthu"]
    },
    "North Western": {
        "Kurunegala": ["Kurunegala", "Kuliyapitiya", "Narammala", "Wariyapola"],
        "Puttalam": ["Puttalam", "Chilaw", "Nattandiya", "Wennappuwa"]
    },
    "North Central": {
        "Anuradhapura": ["Anuradhapura", "Kekirawa", "Thambuttegama", "Eppawala"],
        "Polonnaruwa": ["Polonnaruwa", "Kaduruwela", "Medirigiriya", "Hingurakgoda"]
    },
    "Uva": {
        "Badulla": ["Badulla", "Bandarawela", "Haputale", "Welimada"],
        "Monaragala": ["Monaragala", "Bibile", "Wellawaya", "Buttala"]
    },
    "Sabaragamuwa": {
        "Ratnapura": ["Ratnapura", "Embilipitiya", "Balangoda", "Pelmadulla"],
        "Kegalle": ["Kegalle", "Mawanella", "Warakapola", "Rambukkana"]
    }
}

def init_database():
    """Initialize database and populate with location data"""
    try:
        # Create all tables
        db.create_all()
        print("Database tables created successfully")
        
        # Populate location data if empty
        if Province.query.count() == 0:
            populate_location_data()
            print("Location data populated successfully")
        else:
            print("Location data already exists")
            
    except Exception as e:
        print(f"Database initialization error: {str(e)}")
        db.session.rollback()

def populate_location_data():
    """Populate provinces, districts, and cities"""
    try:
        for province_name, districts in SRI_LANKA_LOCATIONS.items():
            # Create province
            province = Province(name=province_name)
            db.session.add(province)
            db.session.flush()  # Get the ID immediately
            
            for district_name, cities in districts.items():
                # Create district
                district = District(name=district_name, province_id=province.id)
                db.session.add(district)
                db.session.flush()  # Get the ID immediately
                
                # Create cities
                for city_name in cities:
                    city = City(name=city_name, district_id=district.id)
                    db.session.add(city)
        
        db.session.commit()
        
    except Exception as e:
        print(f"Error populating location data: {str(e)}")
        db.session.rollback()
        raise
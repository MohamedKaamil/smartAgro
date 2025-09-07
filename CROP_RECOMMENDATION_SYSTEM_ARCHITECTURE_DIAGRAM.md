# Crop Recommendation System - System Architecture Diagrams

## 1. Overall System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        Crop Recommendation System                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐   │
│  │                 │         │                 │         │                 │   │
│  │   CLIENT TIER   │◄───────►│  SERVER TIER    │◄───────►│   DATA TIER     │   │
│  │                 │   HTTPS │                 │   API   │                 │   │
│  │                 │  JSON   │                 │  Calls  │                 │   │
│  └─────────────────┘         └─────────────────┘         └─────────────────┘   │
│           │                           │                           │             │
│  ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐   │
│  │ React Frontend  │         │  Flask Backend  │         │  MySQL Database │   │
│  │                 │         │                 │         │  & ML Models    │   │
│  │ • Authentication│         │ • REST APIs     │         │                 │   │
│  │ • Crop Recommend│         │ • ML Pipeline   │         │ • User Data     │   │
│  │ • Seller Dashbd │         │ • Auth System   │         │ • Seller Info   │   │
│  │ • Buyer Search  │         │ • Seller Mgmt   │         │ • Crop Data     │   │
│  │ • Registration  │         │ • Location APIs │         │ • Cultivation   │   │
│  │ • Crop Management│        │ • Search Engine │         │ • Location Tree │   │
│  └─────────────────┘         └─────────────────┘         └─────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 2. Detailed Frontend Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              REACT FRONTEND                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           PRESENTATION LAYER                                │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐  │ │
│  │  │    Login      │ │   Register    │ │SimpleDashboard│ │CropRecommend  │  │ │
│  │  │               │ │               │ │               │ │ation          │  │ │
│  │  │ • Auth Form   │ │ • User Types  │ │ • Role Based  │ │ • ML Form     │  │ │
│  │  │ • Validation  │ │ • Validation  │ │ • Navigation  │ │ • Conditions  │  │ │
│  │  │ • Error Hand  │ │ • Password    │ │ • User Info   │ │ • Prediction  │  │ │
│  │  │ • Redirect    │ │ • Email Check │ │ • Quick Access│ │ • Seller List │  │ │
│  │  └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘  │ │
│  │                                                                             │ │
│  │  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐  │ │
│  │  │SellerDashboard│ │BuyerDashboard │ │BusinessRegist │ │CropManagement │  │ │
│  │  │               │ │               │ │               │ │               │  │ │
│  │  │ • Crop CRUD   │ │ • Crop Search │ │ • Multi-Step  │ │ • Add/Edit    │  │ │
│  │  │ • Inventory   │ │ • Seller View │ │ • Location    │ │ • Pricing     │  │ │
│  │  │ • Profile Mgmt│ │ • Filters     │ │ • Documents   │ │ • Availability│  │ │
│  │  │ • Analytics   │ │ • Contact     │ │ • Verification│ │ • Cultivation │  │ │
│  │  └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘  │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                            STATE MANAGEMENT                                 │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │  ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐ │ │
│  │  │  User Context   │         │   Form State    │         │  Component      │ │ │
│  │  │                 │         │                 │         │  Local State    │ │ │
│  │  │ • isLoggedIn    │         │ • React Hook    │         │                 │ │ │
│  │  │ • user          │         │   Form          │         │ • useState      │ │ │
│  │  │ • userType      │         │ • Form Data     │         │ • useEffect     │ │ │
│  │  │ • sellerInfo    │         │ • Validation    │         │ • Navigation    │ │ │
│  │  │ • onLogin/out   │         │ • Error States  │         │ • API Calls     │ │ │
│  │  └─────────────────┘         └─────────────────┘         └─────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           SERVICE LAYER                                     │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │  ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐ │ │
│  │  │   API Service   │         │ Location Service│         │  Search Service │ │ │
│  │  │                 │         │                 │         │                 │ │ │
│  │  │ • Axios HTTP    │         │ • Province Load │         │ • Crop Search   │ │ │
│  │  │ • Auth Headers  │         │ • District Load │         │ • Seller Filter │ │ │
│  │  │ • Error Handle  │         │ • City Load     │         │ • Results Parse │ │ │
│  │  │ • Response Parse│         │ • Hierarchy Mgmt│         │ • Pagination    │ │ │
│  │  └─────────────────┘         └─────────────────┘         └─────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 3. Backend Architecture Detailed

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FLASK BACKEND                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              API LAYER                                      │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │ │
│  │    │     AUTH     │    │   SELLER     │    │   BUYER      │               │ │
│  │    │  ENDPOINTS   │    │  ENDPOINTS   │    │  ENDPOINTS   │               │ │
│  │    │              │    │              │    │              │               │ │
│  │    │POST /login   │    │POST /seller  │    │GET /search   │               │ │
│  │    │POST /register│    │GET /profile  │    │GET /crops    │               │ │
│  │    │GET /profile  │    │PUT /profile  │    │GET /sellers  │               │ │
│  │    │PUT /profile  │    │POST /crops   │    │GET /details  │               │ │
│  │    └──────────────┘    │PUT /crops    │    └──────────────┘               │ │
│  │                        │DELETE /crops │                                   │ │
│  │    ┌──────────────┐    └──────────────┘    ┌──────────────┐               │ │
│  │    │   LOCATION   │                        │  ML PREDICT  │               │ │
│  │    │  ENDPOINTS   │                        │  ENDPOINTS   │               │ │
│  │    │              │                        │              │               │ │
│  │    │GET /provinces│                        │POST /predict │               │ │
│  │    │GET /districts│                        │GET /health   │               │ │
│  │    │GET /cities   │                        │              │               │ │
│  │    └──────────────┘                        └──────────────┘               │ │
│  │                                   │                                        │ │
│  └───────────────────────────────────┼────────────────────────────────────────┘ │
│                                      │                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                          BUSINESS LOGIC LAYER                              │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │  ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐ │ │
│  │  │ Authentication  │         │  Seller Service │         │  Location       │ │ │
│  │  │   Service       │         │                 │         │  Service        │ │ │
│  │  │                 │         │                 │         │                 │ │ │
│  │  │ • User Create   │         │ • Profile CRUD  │         │ • Province Load │ │ │
│  │  │ • Login Verify  │         │ • Crop CRUD     │         │ • District Load │ │ │
│  │  │ • Password Hash │         │ • Verification  │         │ • City Load     │ │ │
│  │  │ • Session Mgmt  │         │ • Business Mgmt │         │ • Hierarchy Mgmt│ │ │
│  │  └─────────────────┘         └─────────────────┘         └─────────────────┘ │ │
│  │                                      │                                      │ │
│  │  ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐ │ │
│  │  │   ML Service    │         │  Search Service │         │  Buyer Service  │ │ │
│  │  │                 │         │                 │         │                 │ │ │
│  │  │ • Model Load    │         │ • Crop Search   │         │ • Crop Browse   │ │ │
│  │  │ • Feature Prep  │         │ • Seller Search │         │ • Seller View   │ │ │
│  │  │ • Prediction    │         │ • Filter Logic  │         │ • Contact Info  │ │ │
│  │  │ • Seller Match  │         │ • Result Format │         │ • Search History│ │ │
│  │  │ • Confidence    │         │ • Availability  │         │ • Recommendations│ │ │
│  │  └─────────────────┘         └─────────────────┘         └─────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                             DATA ACCESS LAYER                              │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │  ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐ │ │
│  │  │  User Data      │         │  Seller Data    │         │  Location Data  │ │ │
│  │  │   Manager       │         │    Manager      │         │    Manager      │ │ │
│  │  │                 │         │                 │         │                 │ │ │
│  │  │ • User CRUD     │         │ • Seller CRUD   │         │ • Province CRUD │ │ │
│  │  │ • Auth Queries  │         │ • Crop CRUD     │         │ • District CRUD │ │ │
│  │  │ • Profile Mgmt  │         │ • Cultivation   │         │ • City CRUD     │ │ │
│  │  │ • Session Store │         │ • Search Queries│         │ • Hierarchy Load│ │ │
│  │  └─────────────────┘         └─────────────────┘         └─────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 4. Machine Learning Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          MACHINE LEARNING PIPELINE                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA FLOW                                      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │              │    │              │    │              │    │              │  │
│  │   RAW DATA   │───►│    DATA      │───►│   FEATURE    │───►│   TRAINED    │  │
│  │              │    │ PREPROCESSING│    │ ENGINEERING  │    │    MODEL     │  │
│  │              │    │              │    │              │    │              │  │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                     │                     │                    │      │
│         ▼                     ▼                     ▼                    ▼      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │• Soil Data   │    │• Data Clean  │    │• Categorical │    │• Random Forest│ │
│  │• Climate Data│    │• Missing Val │    │  Encoding    │    │• Label Encoders│ │
│  │• NPK Levels  │    │• Outlier Rm  │    │• Label Encode│    │• Validation  │  │
│  │• pH Values   │    │• Normalization│    │• Feature Sel │    │• Confidence  │  │
│  │• Rainfall    │    │• Validation  │    │• Scaling     │    │• Pickle Save │  │
│  │• Temperature │    │• Type Check  │    │• Transform   │    │• Model Metrics│ │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           PREDICTION FLOW                                   │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │              │    │              │    │              │    │              │  │
│  │  USER INPUT  │───►│  VALIDATION  │───►│  PREDICTION  │───►│   OUTPUT     │  │
│  │   (FORM)     │    │ & PROCESSING │    │   ENGINE     │    │ GENERATION   │  │
│  │              │    │              │    │              │    │              │  │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                     │                     │                    │      │
│         ▼                     ▼                     ▼                    ▼      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │• Nitrogen    │    │• Range Check │    │• Model Load  │    │• Crop Name   │  │
│  │• Phosphorous │    │• Type Valid  │    │• Feature Prep│    │• Confidence  │  │
│  │• Potassium   │    │• Required    │    │• Prediction  │    │• Seller List │  │
│  │• Temperature │    │  Fields      │    │• Encode Input│    │• Availability│  │
│  │• Humidity    │    │• Sanitization│    │• Transform   │    │• Cultivation │  │
│  │• pH Level    │    │• Format Check│    │• Confidence  │    │• Contact Info│  │
│  │• Rainfall    │    │• Error Handle│    │• Seller Match│    │• Pricing     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 5. Database Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            DATABASE ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                          CORE DATA ENTITIES                                 │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │    ┌──────────────┐              ┌──────────────┐              ┌─────────────┐ │ │
│  │    │    USERS     │              │   SELLERS    │              │ SELLER_CROPS│ │ │
│  │    │              │   1      1   │              │   1     *    │             │ │ │
│  │    │ • id (PK)    │─────────────►│ • id (PK)    │─────────────►│ • id (PK)   │ │ │
│  │    │ • email (UK) │              │ • user_id(FK)│              │ • seller_id │ │ │
│  │    │ • password   │              │ • business   │              │ • crop_name │ │ │
│  │    │ • user_type  │              │ • contact    │              │ • variety   │ │ │
│  │    │ • is_active  │              │ • location   │              │ • price     │ │ │
│  │    │ • created_at │              │ • verified   │              │ • available │ │ │
│  │    └──────────────┘              └──────────────┘              └─────────────┘ │ │
│  │                                          │                              │    │ │
│  │                                          │                              │    │ │
│  │    ┌──────────────┐              ┌──────────────┐              ┌─────────────┐ │ │
│  │    │  PROVINCES   │   1      *   │  DISTRICTS   │   1      *   │   CITIES    │ │ │
│  │    │              │─────────────►│              │─────────────►│             │ │ │
│  │    │ • id (PK)    │              │ • id (PK)    │              │ • id (PK)   │ │ │
│  │    │ • name (UK)  │              │ • name       │              │ • name      │ │ │
│  │    │ • created_at │              │ • province_id│              │ • district  │ │ │
│  │    └──────────────┘              └──────────────┘              └─────────────┘ │ │
│  │                                                                             │ │
│  │                                                                             │ │
│  │                        ┌──────────────┐                                    │ │
│  │                        │CROP_CULTIVATN│                                    │ │
│  │                        │              │                                    │ │
│  │                        │ • id (PK)    │                                    │ │
│  │                        │ • seller_crop│                                    │ │
│  │                        │ • seed_info  │                                    │ │
│  │                        │ • cultivation│                                    │ │
│  │                        │ • irrigation │                                    │ │
│  │                        │ • fertilizer │                                    │ │
│  │                        │ • soil_type  │                                    │ │
│  │                        └──────────────┘                                    │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                        DATA RELATIONSHIPS                                   │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │  • Users (1:1) Sellers          - Each user can have one seller profile    │ │
│  │  • Sellers (1:N) SellerCrops    - Each seller can offer multiple crops    │ │
│  │  • SellerCrops (1:1) Cultivation - Each crop has cultivation information   │ │
│  │  • Provinces (1:N) Districts    - Hierarchical location structure         │ │
│  │  • Districts (1:N) Cities       - Administrative boundaries               │ │
│  │  • Cities (1:N) Sellers         - Sellers located in cities              │ │
│  │                                                                             │ │
│  │  Key Features:                                                              │ │
│  │  • UUID Primary Keys for distributed system support                        │ │
│  │  • Comprehensive indexing for search performance                           │ │
│  │  • Soft deletes with is_active flags                                      │ │
│  │  • Created/Updated timestamps for audit trails                            │ │
│  │  • Foreign key constraints for data integrity                             │ │
│  │  • Unique constraints on email and business registration                  │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 6. Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW DIAGRAM                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐                                     ┌─────────────────┐   │
│  │                 │          1. Authentication          │                 │   │
│  │    BROWSER      │◄───────────────────────────────────►│   FLASK API     │   │
│  │   (React App)   │          Request (POST)             │    (Auth)       │   │
│  │                 │◄───────────────────────────────────►│                 │   │
│  └─────────────────┘          2. Session/User           └─────────────────┘   │
│           │                     Response                           │            │
│           │                                                        │            │
│           │  3. Crop Recommendation Request                       │            │
│           │     (Soil/Climate Conditions)                         │            │
│           ▼                                                        ▼            │
│  ┌─────────────────┐                                     ┌─────────────────┐   │
│  │   PREDICTION    │          4. Form Submission         │   ML PREDICT    │   │
│  │     FORM        │────────────────────────────────────►│    ENDPOINT     │   │
│  │                 │          (POST /predict)            │                 │   │
│  └─────────────────┘                                     └─────────────────┘   │
│                                                                   │            │
│                                                                   │            │
│                                          5. ML Processing        │            │
│                                             & Validation          │            │
│                                                                   ▼            │
│                                                         ┌─────────────────┐   │
│                                                         │   ML PIPELINE   │   │
│                                                         │                 │   │
│                                                         │ • Feature Prep  │   │
│                                                         │ • Model Load    │   │
│                                                         │ • Prediction    │   │
│                                                         │ • Confidence    │   │
│                                                         │ • Crop Identify │   │
│                                                         └─────────────────┘   │
│                                                                   │            │
│                                          6. Seller Lookup        │            │
│                                                                   ▼            │
│  ┌─────────────────┐          7. Prediction + Sellers   ┌─────────────────┐   │
│  │    RESULTS      │◄────────────────────────────────────│  SELLER LOOKUP  │   │
│  │   COMPONENT     │         (JSON Response)             │    SERVICE      │   │
│  │                 │                                     │                 │   │
│  └─────────────────┘                                     │ • Crop Match    │   │
│           │                                              │ • Availability  │   │
│           │                                              │ • Location      │   │
│           ▼                                              │ • Contact Info  │   │
│  ┌─────────────────┐          8. Seller Actions         │ • Cultivation   │   │
│  │                 │                                     └─────────────────┘   │
│  │  SELLER INFO    │          9. Business Registration                        │
│  │  CONTACT FORMS  │                                                           │
│  │                 │          ┌─────────────────┐                             │
│  │ • Business View │─────────►│ SELLER SERVICE  │                             │
│  │ • Registration  │          │                 │                             │
│  │ • Crop Mgmt     │          │ • Profile CRUD  │                             │
│  └─────────────────┘          │ • Crop CRUD     │                             │
│                               │ • Verification  │                             │
│                               └─────────────────┘                             │
│                                        │                                       │
│                               10. Database Updates                            │
│                                        ▼                                       │
│                              ┌─────────────────┐                             │
│                              │  MYSQL DATABASE │                             │
│                              │                 │                             │
│                              │ • Users         │                             │
│                              │ • Sellers       │                             │
│                              │ • Crops         │                             │
│                              │ • Cultivation   │                             │
│                              │ • Locations     │                             │
│                              └─────────────────┘                             │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 7. Security Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                             SECURITY ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           FRONTEND SECURITY                                 │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │ │
│  │  │   SESSION       │    │  INPUT VALID    │    │  HTTPS/TLS      │         │ │
│  │  │   MANAGEMENT    │    │   ATION         │    │  ENCRYPTION     │         │ │
│  │  │                 │    │                 │    │                 │         │ │
│  │  │ • Local Storage │    │ • Form Valid    │    │ • Secure Trans  │         │ │
│  │  │ • Session Check │    │ • XSS Prevent   │    │ • Certificate   │         │ │
│  │  │ • Auto Logout   │    │ • Sanitization  │    │ • Data Integrity│         │ │
│  │  │ • Route Guards  │    │ • Type Checking │    │ • MITM Prevent  │         │ │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘         │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                         │
│                                        ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           BACKEND SECURITY                                  │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │ │
│  │  │  AUTHENTICATION │    │  AUTHORIZATION  │    │  DATA PROTECTION│         │ │
│  │  │                 │    │                 │    │                 │         │ │
│  │  │ • Session Based │    │ • Role Based    │    │ • Input Sanitize│         │ │
│  │  │ • Password Hash │    │ • Route Protect │    │ • SQL Injection │         │ │
│  │  │ • Login Attempts│    │ • User Type     │    │ • Data Validation│        │ │
│  │  │ • Session Expire│    │ • Permission    │    │ • Error Handling│         │ │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘         │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │ │
│  │  │   API SECURITY  │    │ CORS PROTECTION │    │  RATE LIMITING  │         │ │
│  │  │                 │    │                 │    │                 │         │ │
│  │  │ • Input Valid   │    │ • Origin Check  │    │ • Request Limit │         │ │
│  │  │ • Parameter     │    │ • Method Allow  │    │ • IP Tracking   │         │ │
│  │  │   Sanitization  │    │ • Header Valid  │    │ • Abuse Prevent │         │ │
│  │  │ • Error Logging │    │ • Secure Headers│    │ • API Throttle  │         │ │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘         │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                         │
│                                        ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                          DATABASE SECURITY                                  │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │ │
│  │  │  ACCESS CONTROL │    │  DATA INTEGRITY │    │  AUDIT LOGGING  │         │ │
│  │  │                 │    │                 │    │                 │         │ │
│  │  │ • User Roles    │    │ • Foreign Keys  │    │ • Access Logs   │         │ │
│  │  │ • Connection    │    │ • Constraints   │    │ • Change Track  │         │ │
│  │  │   Security      │    │ • Validation    │    │ • Error Logging │         │ │
│  │  │ • Query Limits  │    │ • Backup Policy │    │ • User Activity │         │ │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘         │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 8. Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            DEPLOYMENT ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           DEVELOPMENT ENVIRONMENT                           │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │    ┌─────────────────┐              ┌─────────────────┐                     │ │
│  │    │                 │   Proxy      │                 │                     │ │
│  │    │ React Dev Server│◄────────────►│ Flask Dev Server│                     │ │
│  │    │  (Port 3000)    │   API Calls  │  (Port 5000)    │                     │ │
│  │    │                 │              │                 │                     │ │
│  │    │ • Hot Reload    │              │ • Debug Mode    │                     │ │
│  │    │ • Dev Tools     │              │ • Auto Restart  │                     │ │
│  │    │ • Source Maps   │              │ • Error Traces  │                     │ │
│  │    │ • Fast Refresh  │              │ • SQL Logging   │                     │ │
│  │    └─────────────────┘              └─────────────────┘                     │ │
│  │             │                                │                              │ │
│  │             ▼                                ▼                              │ │
│  │    ┌─────────────────┐              ┌─────────────────┐                     │ │
│  │    │  Node Modules   │              │  Python Env     │                     │ │
│  │    │  React Libs     │              │  Flask/ML Libs  │                     │ │
│  │    │                 │              │                 │                     │ │
│  │    │ • React 18      │              │ • Flask 2.x     │                     │ │
│  │    │ • TypeScript    │              │ • SQLAlchemy    │                     │ │
│  │    │ • Axios         │              │ • Scikit-learn  │                     │ │
│  │    │ • React Router  │              │ • MySQL Conn    │                     │ │
│  │    └─────────────────┘              └─────────────────┘                     │ │
│  │                                               │                             │ │
│  │                                               ▼                             │ │
│  │                                     ┌─────────────────┐                     │ │
│  │                                     │  MySQL Database │                     │ │
│  │                                     │   (Local Dev)   │                     │ │
│  │                                     └─────────────────┘                     │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           PRODUCTION ENVIRONMENT                            │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │ ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐           │ │
│  │ │                 │    │                 │    │                 │           │ │
│  │ │  LOAD BALANCER  │───►│   WEB SERVER    │───►│  APP SERVER     │           │ │
│  │ │    (Nginx)      │    │    (Nginx)      │    │  (Gunicorn)     │           │ │
│  │ │                 │    │                 │    │                 │           │ │
│  │ │ • SSL Terminate │    │ • Static Files  │    │ • Flask App     │           │ │
│  │ │ • Request Route │    │ • Gzip Compress │    │ • Multiple      │           │ │
│  │ │ • Health Check  │    │ • React Build   │    │   Workers       │           │ │
│  │ │ • Rate Limiting │    │ • API Proxy     │    │ • Process Mgmt  │           │ │
│  │ └─────────────────┘    └─────────────────┘    └─────────────────┘           │ │
│  │          │                       │                       │                  │ │
│  │          ▼                       ▼                       ▼                  │ │
│  │ ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐           │ │
│  │ │   CDN/STATIC    │    │  REACT BUILD    │    │   ML MODELS     │           │ │
│  │ │    ASSETS       │    │   (Production)  │    │   (In Memory)   │           │ │
│  │ │                 │    │                 │    │                 │           │ │
│  │ │ • Image Cache   │    │ • Minified JS   │    │ • Pickle Files  │           │ │
│  │ │ • CSS/JS Cache  │    │ • CSS Bundle    │    │ • Label Encoders│           │ │
│  │ │ • Global Distrib│    │ • Asset Hash    │    │ • Model Cache   │           │ │
│  │ │ • Fast Delivery │    │ • Service Worker│    │ • Preprocessing │           │ │
│  │ └─────────────────┘    └─────────────────┘    └─────────────────┘           │ │
│  │                                                         │                  │ │
│  │                                                         ▼                  │ │
│  │                                               ┌─────────────────┐           │ │
│  │                                               │  MYSQL DATABASE │           │ │
│  │                                               │   (Production)  │           │ │
│  │                                               │                 │           │ │
│  │                                               │ • User Data     │           │ │
│  │                                               │ • Seller Info   │           │ │
│  │                                               │ • Crop Data     │           │ │
│  │                                               │ • Cultivation   │           │ │
│  │                                               │ • Location Tree │           │ │
│  │                                               │ • Search Indices│           │ │
│  │                                               │ • Audit Logs    │           │ │
│  │                                               └─────────────────┘           │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 9. Sequence Diagrams

### 9.1 User Authentication Sequence

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Browser   │    │   React     │    │   Flask     │    │   Database  │
│             │    │   Frontend  │    │   Backend   │    │             │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │                  │
       │  1. User Login    │                  │                  │
       ├─────────────────►│                  │                  │
       │  (email/password) │                  │                  │
       │                  │                  │                  │
       │                  │  2. POST /login  │                  │
       │                  ├─────────────────►│                  │
       │                  │  {email,password}│                  │
       │                  │                  │                  │
       │                  │                  │  3. Query User   │
       │                  │                  ├─────────────────►│
       │                  │                  │  WHERE email=?   │
       │                  │                  │                  │
       │                  │                  │  4. User Record  │
       │                  │                  │◄─────────────────┤
       │                  │                  │                  │
       │                  │                  │  5. Check Hash   │
       │                  │                  │     Password     │
       │                  │                  │                  │
       │                  │  6. Session Data │                  │
       │                  │◄─────────────────┤                  │
       │                  │  {user, session} │                  │
       │                  │                  │                  │
       │  7. Login Success │                  │                  │
       │◄─────────────────┤                  │                  │
       │  (user data)     │                  │                  │
       │                  │                  │                  │
       │  8. Redirect to   │                  │                  │
       │     Dashboard     │                  │                  │
       │◄─────────────────┤                  │                  │
       │                  │                  │                  │
```

### 9.2 Crop Recommendation Generation Sequence

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   User      │  │ CropRecommend│  │   Flask     │  │ ML Service  │  │  Database   │
│             │  │   Component  │  │   API       │  │             │  │             │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │                │                │
       │ 1. Fill Form   │                │                │                │
       │   (NPK, pH,    │                │                │                │
       │   Climate)     │                │                │                │
       ├───────────────►│                │                │                │
       │                │                │                │                │
       │ 2. Submit      │                │                │                │
       ├───────────────►│                │                │                │
       │                │                │                │                │
       │                │ 3. Validate    │                │                │
       │                │    Form Data   │                │                │
       │                │                │                │                │
       │                │ 4. POST        │                │                │
       │                │   /predict     │                │                │
       │                ├───────────────►│                │                │
       │                │ + Session Auth │                │                │
       │                │                │                │                │
       │                │                │ 5. Load ML     │                │
       │                │                │   Model        │                │
       │                │                ├───────────────►│                │
       │                │                │                │                │
       │                │                │                │ 6. Preprocess  │
       │                │                │                │   Features     │
       │                │                │                │                │
       │                │                │                │ 7. Predict     │
       │                │                │                │   Crop Type    │
       │                │                │                │                │
       │                │                │                │ 8. Calculate   │
       │                │                │                │   Confidence   │
       │                │                │                │                │
       │                │                │ 9. Crop Name   │                │
       │                │                │   + Confidence │                │
       │                │                │◄───────────────┤                │
       │                │                │                │                │
       │                │                │10. Find Sellers│                │
       │                │                │   for Crop     │                │
       │                │                ├───────────────────────────────►│
       │                │                │   WHERE crop=? │                │
       │                │                │                │                │
       │                │                │11. Seller List │                │
       │                │                │   + Details    │                │
       │                │                │◄───────────────────────────────┤
       │                │                │                │                │
       │                │12. Complete    │                │                │
       │                │   Response     │                │                │
       │                │◄───────────────┤                │                │
       │                │                │                │                │
       │13. Display     │                │                │                │
       │    Results     │                │                │                │
       │◄───────────────┤                │                │                │
       │                │                │                │                │
```

### 9.3 Seller Registration and Crop Management Sequence

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Seller    │ │   Business  │ │   Flask     │ │  Seller     │ │  Database   │
│   User      │ │Registration │ │   API       │ │  Service    │ │             │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │               │               │
       │ 1. Fill Reg   │               │               │               │
       │   Form        │               │               │               │
       ├──────────────►│               │               │               │
       │               │               │               │               │
       │ 2. Submit     │               │               │               │
       │   Business    │               │               │               │
       │   Details     │               │               │               │
       ├──────────────►│               │               │               │
       │               │               │               │               │
       │               │ 3. POST       │               │               │
       │               │   /seller     │               │               │
       │               │   /register   │               │               │
       │               ├──────────────►│               │               │
       │               │               │               │               │
       │               │               │ 4. Validate   │               │
       │               │               │   Business    │               │
       │               │               │   Info        │               │
       │               │               ├──────────────►│               │
       │               │               │               │               │
       │               │               │               │ 5. Create     │
       │               │               │               │   Seller      │
       │               │               │               ├──────────────►│
       │               │               │               │   Record      │
       │               │               │               │               │
       │               │               │               │ 6. Success    │
       │               │               │               │◄──────────────┤
       │               │               │               │               │
       │               │               │ 7. Seller ID  │               │
       │               │               │◄──────────────┤               │
       │               │               │               │               │
       │               │ 8. Success    │               │               │
       │               │◄──────────────┤               │               │
       │               │               │               │               │
       │ 9. Redirect   │               │               │               │
       │   to Crop     │               │               │               │
       │   Management  │               │               │               │
       │◄──────────────┤               │               │               │
       │               │               │               │               │
       │10. Add Crop   │               │               │               │
       │    Details    │               │               │               │
       ├──────────────────────────────────────────────►│               │
       │               │               │               │               │
       │               │               │11. POST       │               │
       │               │               │   /crops      │               │
       │               │               ├──────────────►│               │
       │               │               │               │               │
       │               │               │               │12. Create     │
       │               │               │               │   Crop +      │
       │               │               │               │   Cultivation │
       │               │               │               ├──────────────►│
       │               │               │               │               │
       │               │               │               │13. Success    │
       │               │               │               │◄──────────────┤
       │               │               │               │               │
       │               │               │14. Crop Added │               │
       │               │               │◄──────────────┤               │
       │               │               │               │               │
       │15. Success    │               │               │               │
       │    Message    │               │               │               │
       │◄──────────────┤               │               │               │
       │               │               │               │               │
```

### 9.4 Buyer Crop Search Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Buyer     │    │   Buyer     │    │   Flask     │    │  Database   │
│             │    │ Dashboard   │    │   API       │    │             │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │                  │
       │ 1. Search for    │                  │                  │
       │    Crops         │                  │                  │
       ├─────────────────►│                  │                  │
       │                  │                  │                  │
       │                  │ 2. GET           │                  │
       │                  │   /search        │                  │
       │                  │   ?query=rice    │                  │
       │                  ├─────────────────►│                  │
       │                  │                  │                  │
       │                  │                  │ 3. Search Query  │
       │                  │                  │   JOIN sellers   │
       │                  │                  │   WHERE crop     │
       │                  │                  │   LIKE '%rice%'  │
       │                  │                  ├─────────────────►│
       │                  │                  │                  │
       │                  │                  │ 4. Results with  │
       │                  │                  │   Seller Info    │
       │                  │                  │◄─────────────────┤
       │                  │                  │                  │
       │                  │ 5. Formatted     │                  │
       │                  │   Search Results │                  │
       │                  │◄─────────────────┤                  │
       │                  │                  │                  │
       │ 6. Display       │                  │                  │
       │    Results       │                  │                  │
       │◄─────────────────┤                  │                  │
       │                  │                  │                  │
       │ 7. View Crop     │                  │                  │
       │    Details       │                  │                  │
       ├─────────────────►│                  │                  │
       │                  │                  │                  │
       │                  │ 8. GET           │                  │
       │                  │   /crops/123     │                  │
       │                  │   /details       │                  │
       │                  ├─────────────────►│                  │
       │                  │                  │                  │
       │                  │                  │ 9. Detailed      │
       │                  │                  │   Query with     │
       │                  │                  │   Cultivation    │
       │                  │                  ├─────────────────►│
       │                  │                  │                  │
       │                  │                  │10. Complete      │
       │                  │                  │   Crop Info      │
       │                  │                  │◄─────────────────┤
       │                  │                  │                  │
       │                  │11. Crop Details  │                  │
       │                  │   + Cultivation  │                  │
       │                  │◄─────────────────┤                  │
       │                  │                  │                  │
       │12. Detailed      │                  │                  │
       │    Crop View     │                  │                  │
       │◄─────────────────┤                  │                  │
       │                  │                  │                  │
```

## 10. Implementation Guidelines

### Recommended Tools:
1. **Draw.io (Diagrams.net)** - Free, web-based
2. **Lucidchart** - Professional diagramming
3. **Microsoft Visio** - Enterprise standard
4. **Miro** - Collaborative diagramming
5. **PlantUML** - Code-based diagrams

### Diagram Elements to Include:
1. **System Components**: Clearly labeled boxes/rectangles
2. **Data Flow**: Arrows showing direction and type
3. **Technology Labels**: React, Flask, MySQL, ML models
4. **Security Boundaries**: Dashed lines or special colors
5. **External Services**: Different styling for external APIs
6. **Database Symbols**: Cylinder shapes for data storage
7. **User Icons**: Human figures for user interactions
8. **Network Boundaries**: Cloud shapes or network symbols

### Color Coding Suggestions:
- **Frontend**: Blue tones (#3B82F6)
- **Backend**: Green tones (#10B981)
- **Database**: Orange tones (#F59E0B)
- **ML Models**: Purple tones (#8B5CF6)
- **Security**: Red tones (#EF4444)
- **Data Flow**: Gray arrows (#6B7280)

### Export Formats:
- **PNG**: High resolution for documents
- **SVG**: Scalable vector graphics
- **PDF**: Professional reports
- **JSON**: Editable format for future updates

## 11. System Architecture Summary

This comprehensive architecture documentation for the Crop Recommendation System provides:

1. **Overall System Architecture**: Three-tier architecture with clear separation of concerns
2. **Frontend Architecture**: React-based presentation layer with state management
3. **Backend Architecture**: Flask-based API layer with business logic separation
4. **ML Pipeline**: Complete machine learning workflow from data to prediction
5. **Database Architecture**: MySQL-based data tier with comprehensive entity relationships
6. **Data Flow**: Clear data movement patterns throughout the system
7. **Security Architecture**: Multi-layered security approach across all tiers
8. **Deployment Architecture**: Development and production environment configurations
9. **Sequence Diagrams**: Key system interaction flows and processes

The system integrates modern web technologies with machine learning to provide a complete agricultural marketplace solution, supporting both crop recommendation and comprehensive seller-buyer connections with detailed cultivation information and location-based services.

## 12. Entity-Relationship (ER) Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          ENTITY-RELATIONSHIP DIAGRAM                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ENTITIES                                       │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │    ┌──────────────────┐         ┌──────────────────┐                        │ │
│  │    │      USERS       │         │    PROVINCES     │                        │ │
│  │    ├──────────────────┤         ├──────────────────┤                        │ │
│  │    │ id (PK)          │         │ id (PK)          │                        │ │
│  │    │ email (UK)       │         │ name (UK)        │                        │ │
│  │    │ password_hash    │         │ created_at       │                        │ │
│  │    │ user_type        │         └──────────────────┘                        │ │
│  │    │ is_active        │                   │                                 │ │
│  │    │ email_verified   │                   │ 1                               │ │
│  │    │ created_at       │                   │                                 │ │
│  │    │ updated_at       │                   │ contains                        │ │
│  │    └──────────────────┘                   │                                 │ │
│  │            │                              │ *                               │ │
│  │            │ 1                            │                                 │ │
│  │            │                              ▼                                 │ │
│  │            │ has_profile        ┌──────────────────┐                        │ │
│  │            │                    │    DISTRICTS     │                        │ │
│  │            │ *                  ├──────────────────┤                        │ │
│  │            ▼                    │ id (PK)          │                        │ │
│  │    ┌──────────────────┐         │ name             │                        │ │
│  │    │     SELLERS      │         │ province_id (FK) │                        │ │
│  │    ├──────────────────┤         │ created_at       │                        │ │
│  │    │ id (PK)          │         └──────────────────┘                        │ │
│  │    │ user_id (FK)     │                   │                                 │ │
│  │    │ business_name    │                   │ 1                               │ │
│  │    │ business_reg_no  │                   │                                 │ │
│  │    │ business_type    │                   │ contains                        │ │
│  │    │ contact_number   │                   │                                 │ │
│  │    │ secondary_contact│                   │ *                               │ │
│  │    │ business_email   │                   │                                 │ │
│  │    │ website          │                   ▼                                 │ │
│  │    │ address_line_1   │         ┌──────────────────┐                        │ │
│  │    │ address_line_2   │         │      CITIES      │                        │ │
│  │    │ postal_code      │         ├──────────────────┤                        │ │
│  │    │ province_id (FK) │         │ id (PK)          │                        │ │
│  │    │ district_id (FK) │         │ name             │                        │ │
│  │    │ city_id (FK)     │         │ district_id (FK) │                        │ │
│  │    │ shop_name        │         │ created_at       │                        │ │
│  │    │ shop_type        │         └──────────────────┘                        │ │
│  │    │ establishment_yr │                                                     │ │
│  │    │ shop_size_sqft   │                                                     │ │
│  │    │ opening_hours    │                                                     │ │
│  │    │ operating_days   │                                                     │ │
│  │    │ services_offered │                                                     │ │
│  │    │ delivery_avail   │                                                     │ │
│  │    │ home_delivery    │                                                     │ │
│  │    │ pickup_available │                                                     │ │
│  │    │ is_verified      │                                                     │ │
│  │    │ verification_docs│                                                     │ │
│  │    │ is_active        │                                                     │ │
│  │    │ description      │                                                     │ │
│  │    │ specialties      │                                                     │ │
│  │    │ certifications   │                                                     │ │
│  │    │ created_at       │                                                     │ │
│  │    │ updated_at       │                                                     │ │
│  │    │ verified_at      │                                                     │ │
│  │    └──────────────────┘                                                     │ │
│  │            │                                                                │ │
│  │            │ 1                                                              │ │
│  │            │                                                                │ │
│  │            │ offers                                                         │ │
│  │            │                                                                │ │
│  │            │ *                                                              │ │
│  │            ▼                                                                │ │
│  │    ┌──────────────────┐                                                     │ │
│  │    │   SELLER_CROPS   │                                                     │ │
│  │    ├──────────────────┤                                                     │ │
│  │    │ id (PK)          │                                                     │ │
│  │    │ seller_id (FK)   │                                                     │ │
│  │    │ crop_name        │                                                     │ │
│  │    │ crop_variety     │                                                     │ │
│  │    │ is_available     │                                                     │ │
│  │    │ price_per_kg     │                                                     │ │
│  │    │ price_per_unit   │                                                     │ │
│  │    │ unit_type        │                                                     │ │
│  │    │ quantity_avail   │                                                     │ │
│  │    │ minimum_order    │                                                     │ │
│  │    │ harvest_season   │                                                     │ │
│  │    │ best_quality_mth │                                                     │ │
│  │    │ quality_grade    │                                                     │ │
│  │    │ organic_certified│                                                     │ │
│  │    │ pesticide_free   │                                                     │ │
│  │    │ created_at       │                                                     │ │
│  │    │ updated_at       │                                                     │ │
│  │    └──────────────────┘                                                     │ │
│  │            │                                                                │ │
│  │            │ 1                                                              │ │
│  │            │                                                                │ │
│  │            │ has_cultivation                                                │ │
│  │            │                                                                │ │
│  │            │ 1                                                              │ │
│  │            ▼                                                                │ │
│  │    ┌──────────────────┐                                                     │ │
│  │    │CROP_CULTIVATIONS │                                                     │ │
│  │    ├──────────────────┤                                                     │ │
│  │    │ id (PK)          │                                                     │ │
│  │    │ seller_crop_id   │                                                     │ │
│  │    │   (FK, UK)       │                                                     │ │
│  │    │ seed_nursery     │                                                     │ │
│  │    │ land_preparation │                                                     │ │
│  │    │ planting         │                                                     │ │
│  │    │ crop_management  │                                                     │ │
│  │    │ seed_requirements│                                                     │ │
│  │    │ cultivation_steps│                                                     │ │
│  │    │ irrigation_method│                                                     │ │
│  │    │ fertilizer_used  │                                                     │ │
│  │    │ pest_control_mth │                                                     │ │
│  │    │ harvesting_method│                                                     │ │
│  │    │ post_harvest_hnd │                                                     │ │
│  │    │ soil_type        │                                                     │ │
│  │    │ water_reqmnts    │                                                     │ │
│  │    │ sunlight_reqmnts │                                                     │ │
│  │    │ temperature_range│                                                     │ │
│  │    │ planting_season  │                                                     │ │
│  │    │ growing_duration │                                                     │ │
│  │    │ created_at       │                                                     │ │
│  │    │ updated_at       │                                                     │ │
│  │    └──────────────────┘                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                            RELATIONSHIPS                                    │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │  • USERS (1:1) SELLERS                                                     │ │
│  │    - One user can have one seller profile                                  │ │
│  │    - Identifying relationship (seller cannot exist without user)           │ │
│  │                                                                             │ │
│  │  • SELLERS (1:N) SELLER_CROPS                                              │ │
│  │    - One seller can offer multiple crops                                   │ │
│  │    - Non-identifying relationship (crops belong to seller)                 │ │
│  │                                                                             │ │
│  │  • SELLER_CROPS (1:1) CROP_CULTIVATIONS                                    │ │
│  │    - Each crop has detailed cultivation information                        │ │
│  │    - Identifying relationship (cultivation tied to specific crop)          │ │
│  │                                                                             │ │
│  │  • PROVINCES (1:N) DISTRICTS                                               │ │
│  │    - One province contains multiple districts                              │ │
│  │    - Hierarchical administrative structure                                 │ │
│  │                                                                             │ │
│  │  • DISTRICTS (1:N) CITIES                                                  │ │
│  │    - One district contains multiple cities                                 │ │
│  │    - Hierarchical administrative structure                                 │ │
│  │                                                                             │ │
│  │  • PROVINCES (1:N) SELLERS                                                 │ │
│  │  • DISTRICTS (1:N) SELLERS                                                 │ │
│  │  • CITIES (1:N) SELLERS                                                    │ │
│  │    - Sellers are located within the administrative hierarchy              │ │
│  │    - Multiple foreign key references for complete location data           │ │
│  │                                                                             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           KEY ATTRIBUTES                                    │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │  Primary Keys (PK): Unique identifiers using UUID format                   │ │
│  │  Foreign Keys (FK): References to related entities                         │ │
│  │  Unique Keys (UK): Unique constraints on specific fields                   │ │
│  │                                                                             │ │
│  │  Data Types:                                                                │ │
│  │  • VARCHAR(36)  - UUID primary keys                                        │ │
│  │  • VARCHAR(n)   - Text fields with length constraints                      │ │
│  │  • TEXT         - Large text fields (descriptions, JSON data)             │ │
│  │  • BOOLEAN      - True/false flags                                         │ │
│  │  • FLOAT        - Decimal numbers (prices, quantities)                     │ │
│  │  • INTEGER      - Whole numbers (years, durations)                         │ │
│  │  • DATETIME     - Timestamp fields                                         │ │
│  │                                                                             │ │
│  │  Indexes:                                                                   │ │
│  │  • email (Users) - Unique index for authentication                         │ │
│  │  • crop_name (SellerCrops) - Index for search performance                  │ │
│  │  • business_name (Sellers) - Index for business search                     │ │
│  │  • is_available (SellerCrops) - Index for availability filtering           │ │
│  │  • location fields - Composite indexes for geographical searches           │ │
│  │                                                                             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 13. Use Case Diagram with UML Notation

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           USE CASE DIAGRAM                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│                                                                                 │
│     👤                                                                          │
│   Farmer/                                                                       │
│   Buyer                    SYSTEM BOUNDARY                                      │
│     │                     ┌─────────────────────────────────────────────────────┐│
│     │                     │        Crop Recommendation System              │ │
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│   Register   │             │                                       ││
│     │      │   Account    │             │ <<include>>                           ││
│     │      └──────────────┼─────────────┘     │                               ││
│     │                     │                   ▼                               ││
│     │      ┌──────────────┼─────────────┐ ┌──────────────────┐                ││
│     ├─────►│    Login     │             │ │  Validate User   │                ││
│     │      │   System     │             │ │  Credentials     │                ││
│     │      └──────────────┼─────────────┘ └──────────────────┘                ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│   Get Crop   │             │                                       ││
│     │      │Recommendation│             │ <<include>>                           ││
│     │      └──────────────┼─────────────┘     │                               ││
│     │                     │                   ▼                               ││
│     │                     │               ┌──────────────────┐                ││
│     │                     │               │  Process ML      │                ││
│     │                     │               │  Prediction      │                ││
│     │                     │               └──────────────────┘                ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│ Search Crops │             │ <<extend>>                            ││
│     │      │ and Sellers  │             │     │                               ││
│     │      └──────────────┼─────────────┘     ▼                               ││
│     │                     │               ┌──────────────────┐                ││
│     │                     │               │   Apply          │                ││
│     │                     │               │   Filters        │                ││
│     │                     │               └──────────────────┘                ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│ View Seller  │             │                                       ││
│     │      │   Details    │             │                                       ││
│     │      └──────────────┼─────────────┘                                       ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     └─────►│ View Crop    │             │ <<include>>                           ││
│            │ Cultivation  │             │     │                               ││
│            │    Info      │             │     ▼                               ││
│            └──────────────┼─────────────┘ ┌──────────────────┐                ││
│                           │               │   Load Detailed  │                ││
│                           │               │ Cultivation Data │                ││
│                           │               └──────────────────┘                ││
│                           │                                                     ││
│     🏪                    │                                                     ││
│ Agricultural              │                                                     ││
│   Seller                  │                                                     ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│ Register     │             │ <<include>>                           ││
│     │      │ Business     │             │     │                               ││
│     │      └──────────────┼─────────────┘     ▼                               ││
│     │                     │               ┌──────────────────┐                ││
│     │                     │               │ Verify Business  │                ││
│     │                     │               │   Documents      │                ││
│     │                     │               └──────────────────┘                ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│ Manage       │             │ <<extend>>                            ││
│     │      │ Crop         │             │     │                               ││
│     │      │ Listings     │             │     ▼                               ││
│     │      └──────────────┼─────────────┘ ┌──────────────────┐                ││
│     │                     │               │ Update Inventory │                ││
│     │                     │               │  Availability    │                ││
│     │                     │               └──────────────────┘                ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│ Add Crop     │             │ <<include>>                           ││
│     │      │ Cultivation  │             │     │                               ││
│     │      │    Details   │             │     ▼                               ││
│     │      └──────────────┼─────────────┘ ┌──────────────────┐                ││
│     │                     │               │   Validate       │                ││
│     │                     │               │ Cultivation Info │                ││
│     │                     │               └──────────────────┘                ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│ Update       │             │                                       ││
│     │      │ Business     │             │                                       ││
│     │      │ Profile      │             │                                       ││
│     │      └──────────────┼─────────────┘                                       ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     └─────►│ Manage       │             │ <<extend>>                            ││
│            │ Pricing &    │             │     │                               ││
│            │ Availability │             │     ▼                               ││
│            └──────────────┼─────────────┘ ┌──────────────────┐                ││
│                           │               │  Set Seasonal    │                ││
│                           │               │    Pricing       │                ││
│                           │               └──────────────────┘                ││
│                           │                                                     ││
│     👨‍💼                    │                                                     ││
│   System                  │                                                     ││
│Administrator              │                                                     ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│   Verify     │             │                                       ││
│     │      │  Seller      │             │                                       ││
│     │      │  Accounts    │             │                                       ││
│     │      └──────────────┼─────────────┘                                       ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│   Manage     │             │                                       ││
│     │      │  Location    │             │                                       ││
│     │      │    Data      │             │                                       ││
│     │      └──────────────┼─────────────┘                                       ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│  Monitor     │             │                                       ││
│     │      │  System      │             │                                       ││
│     │      │  Health      │             │                                       ││
│     │      └──────────────┼─────────────┘                                       ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     └─────►│  Manage      │             │                                       ││
│            │  User        │             │                                       ││
│            │  Accounts    │             │                                       ││
│            └──────────────┼─────────────┘                                       ││
│                           │                                                     ││
│     🤖                    │                                                     ││
│   ML Recommendation      │                                                     ││
│     Engine                │                                                     ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│   Process    │             │                                       ││
│     │      │ Prediction   │             │                                       ││
│     │      │  Requests    │             │                                       ││
│     │      └──────────────┼─────────────┘                                       ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│  Load ML     │             │                                       ││
│     │      │   Model      │             │                                       ││
│     │      └──────────────┼─────────────┘                                       ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     ├─────►│ Generate     │             │                                       ││
│     │      │Recommendations│            │                                       ││
│     │      └──────────────┼─────────────┘                                       ││
│     │                     │                                                     ││
│     │      ┌──────────────┼─────────────┐                                       ││
│     └─────►│ Calculate    │             │                                       ││
│            │ Confidence   │             │                                       ││
│            │   Scores     │             │                                       ││
│            └──────────────┼─────────────┘                                       ││
│                           │                                                     ││
│                           └─────────────────────────────────────────────────────┘│
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           UML RELATIONSHIPS LEGEND                          │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                             │ │
│  │  <<include>>  - Mandatory behavior that is always executed                 │ │
│  │               - Base use case cannot complete without included use case     │ │
│  │               - Examples: Login includes Validate User Credentials         │ │
│  │                                                                             │ │
│  │  <<extend>>   - Optional behavior that may be executed under conditions    │ │
│  │               - Extension points define where behavior can be inserted     │ │
│  │               - Examples: Search Crops extends with Apply Filters          │ │
│  │                                                                             │ │
│  │  Actor ────► Use Case  - Association (actor participates in use case)      │ │
│  │                                                                             │ │
│  │  System Boundary - Defines the scope of the system being modeled          │ │
│  │                                                                             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 14. Comprehensive Test Case Chart

| **Page / Feature** | **Objectives** | **Scope** | **Responsibility** |
|-------------------|----------------|-----------|-------------------|
| **Login** | Successful login; invalid credentials error; redirects/session management | Username/password authentication, error states, redirect to Dashboard, session timeout handling | QA (test scenarios), Backend Dev (auth API/session mgmt), Security/DevOps (session config, rate limiting) |
| **Registration** | User account creation; email validation; duplicate email handling; user type selection | Form validation, password strength, email uniqueness check, buyer/seller type selection | QA (validation testing), Backend Dev (user creation API), Frontend Dev (form validation), Email service (verification) |
| **Crop Recommendation** | ML prediction accuracy; input validation; seller integration; confidence scoring | Soil/climate parameter validation, ML model inference, seller lookup integration, prediction confidence display | QA (accuracy testing), Data Science (ML model validation), Backend Dev (prediction API), Frontend Dev (form handling) |
| **Seller Dashboard** | CRUD operations for crops; business profile management; inventory tracking; verification status | Seller authentication, crop management, business information updates, document upload | QA (functional testing), Backend Dev (seller APIs), Frontend Dev (dashboard UI), Admin (verification process) |
| **Buyer Dashboard** | Crop search functionality; seller discovery; detailed crop information; contact features | Search algorithms, filtering by location/price, seller profile viewing, crop details with cultivation info | QA (search testing), Backend Dev (search APIs), Frontend Dev (search interface), Database Admin (search optimization) |
| **Business Registration** | Seller onboarding; document verification; location selection; multi-step process | Multi-step form validation, file upload functionality, location hierarchy selection, business verification workflow | QA (workflow testing), Backend Dev (registration flow), Admin (verification process), Frontend Dev (multi-step forms) |
| **Crop Management** | Add/edit/delete crops; cultivation details; pricing management; availability tracking | Crop CRUD operations, detailed cultivation information, pricing models, seasonal availability | QA (CRUD testing), Backend Dev (crop APIs), Seller (content management), Agricultural Expert (cultivation validation) |
| **ML Model Integration** | Prediction accuracy; response time; error handling; model loading | Model loading performance, feature preprocessing, prediction generation, confidence calculation | Data Science (model accuracy), QA (performance testing), Backend Dev (API integration), DevOps (model deployment) |
| **Location Management** | Province/district/city hierarchy; location-based filtering; administrative boundaries | Location hierarchy integrity, search by location, administrative data consistency | QA (hierarchy testing), Backend Dev (location APIs), Admin (location data management), Database Admin (referential integrity) |
| **Seller Search** | Crop-based seller discovery; availability filtering; contact information; sorting options | Search algorithms, availability status filtering, seller details display, contact methods | QA (search functionality), Backend Dev (search logic), Seller (profile accuracy), UI/UX (results display) |
| **User Profile Management** | Profile updates; password changes; account deactivation; data export | User data modification, security settings, account management, GDPR compliance | QA (profile testing), Backend Dev (profile APIs), Security (password policies), Legal (data compliance) |
| **Authentication & Authorization** | Role-based access; session management; password policies; account lockout | User roles (buyer/seller/admin), session timeout, password requirements, brute force protection | Security/DevOps (auth policies), Backend Dev (auth implementation), QA (security testing), Admin (user management) |
| **File Upload & Management** | Document upload; image handling; file validation; storage management | Business documents, crop images, file type validation, storage quotas | Backend Dev (file APIs), QA (upload testing), DevOps (storage config), Security (file validation) |
| **Search & Filtering** | Advanced search; multi-criteria filtering; sorting; pagination | Crop search by name/type, location filtering, price range filtering, results pagination | Backend Dev (search engine), QA (search testing), Database Admin (indexing), Frontend Dev (filter UI) |
| **Notification System** | Email notifications; in-app alerts; verification emails; system messages | Account verification, crop availability alerts, system announcements | Backend Dev (notification service), QA (notification testing), Email service (delivery), Admin (message management) |
| **Data Import/Export** | Bulk crop import; data export; CSV handling; data validation | Seller bulk crop upload, user data export, file format validation, data integrity | Backend Dev (import/export APIs), QA (data testing), Admin (bulk operations), Database Admin (data validation) |
| **Analytics & Reporting** | Usage statistics; crop popularity; seller performance; system metrics | Prediction analytics, search trends, user engagement, performance metrics | Backend Dev (analytics APIs), QA (reporting testing), Admin (dashboard), Business Analyst (metrics definition) |
| **Mobile Responsiveness** | Cross-device compatibility; touch interactions; performance optimization; offline functionality | Mobile browser testing, tablet compatibility, touch-friendly UI, responsive design | Frontend Dev (responsive design), QA (device testing), UI/UX (mobile experience), Performance team (optimization) |
| **API Security & Testing** | Authentication security; input validation; rate limiting; error handling | API endpoint security, parameter sanitization, request throttling, proper error responses | Security (penetration testing), Backend Dev (security implementation), QA (API testing), DevOps (rate limiting) |
| **Performance & Scalability** | Load testing; response times; concurrent users; database performance | ML prediction performance, search response times, concurrent user handling, database query optimization | Performance team (load testing), Backend Dev (optimization), Database Admin (query tuning), DevOps (scaling) |
| **Backup & Recovery** | Data backup; disaster recovery; system restoration; data integrity | Regular data backups, system recovery procedures, data consistency checks | DevOps (backup systems), Database Admin (recovery testing), Admin (data management), IT (infrastructure) |

### **Additional Test Categories & Specifications:**

#### **Functional Testing Details:**

| **Category** | **Test Cases** | **Acceptance Criteria** | **Priority** |
|--------------|----------------|------------------------|--------------|
| **Authentication** | Valid login, invalid credentials, password reset, session timeout | 100% authentication accuracy, < 2 sec response time | High |
| **Crop Recommendation** | ML prediction accuracy, input validation, edge cases | >85% model accuracy, handle all input combinations | High |
| **Search Functionality** | Text search, filter combinations, sorting, pagination | <3 sec search results, accurate filtering | High |
| **Data Management** | CRUD operations, data validation, referential integrity | Zero data corruption, proper validation | High |
| **User Interface** | Form validation, responsive design, accessibility | WCAG 2.1 compliance, cross-browser compatibility | Medium |

#### **Non-Functional Testing Details:**

| **Category** | **Metrics** | **Target** | **Tools** |
|--------------|-------------|------------|-----------|
| **Performance** | Response time, throughput, resource usage | <3s page load, 1000 concurrent users | JMeter, LoadRunner |
| **Security** | Authentication, authorization, data encryption | Zero security vulnerabilities | OWASP ZAP, Burp Suite |
| **Usability** | User satisfaction, task completion rate | >90% task completion, <5 clicks to goal | User testing, Analytics |
| **Reliability** | Uptime, error rates, recovery time | 99.5% uptime, <1% error rate | Monitoring tools |
| **Scalability** | User load, data volume, system resources | Support 10,000 users, 1M crop records | Cloud scaling tests |

#### **Test Environment Requirements:**

| **Environment** | **Purpose** | **Configuration** | **Data** |
|-----------------|-------------|-------------------|----------|
| **Development** | Feature development, unit testing | Local setup, mock data | Synthetic test data |
| **Testing** | Integration testing, QA validation | Staging environment, test data | Realistic test scenarios |
| **UAT** | User acceptance testing | Production-like setup | Sanitized production data |
| **Production** | Live system, monitoring | Full production stack | Real user data |

#### **Automation Strategy:**

| **Test Type** | **Automation Level** | **Tools** | **Frequency** |
|---------------|----------------------|-----------|---------------|
| **Unit Tests** | 100% | Jest, PyTest | Every commit |
| **Integration Tests** | 80% | Cypress, Postman | Daily build |
| **API Tests** | 95% | Postman, REST Assured | Continuous |
| **UI Tests** | 60% | Selenium, Cypress | Nightly |
| **Performance Tests** | Manual + Auto | JMeter | Weekly |

This comprehensive test case chart provides complete coverage of your crop recommendation system with specific objectives, scope definitions, and clear responsibility assignments for each feature and component.
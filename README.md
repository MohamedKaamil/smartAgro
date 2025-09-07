# 🌾 SmartAgro - Intelligent Crop Recommendation System

An AI-powered agricultural solution that provides intelligent crop recommendations based on soil conditions, weather data, and environmental factors to help farmers make data-driven decisions.

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Machine Learning Model](#-machine-learning-model)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **Intelligent Crop Recommendation**: ML-powered suggestions based on soil and environmental parameters
- **Real-time Analysis**: Instant crop recommendations based on input parameters
- **User-friendly Interface**: Modern React-based frontend with responsive design
- **RESTful API**: Flask-based backend API for crop predictions
- **Data Visualization**: Interactive charts and graphs for better insights
- **Multi-format Export**: Export recommendations in various formats
- **Performance Analytics**: Model performance tracking and reporting

## 🛠 Technology Stack

### Backend
- **Python 3.7+**
- **Flask** - Web framework
- **Scikit-learn** - Machine learning library
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Joblib** - Model serialization

### Frontend
- **React** - Frontend framework
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Node.js** - JavaScript runtime

### Machine Learning
- **Random Forest** - Crop recommendation algorithm
- **Jupyter Notebook** - Model development and analysis
- **Matplotlib/Seaborn** - Data visualization

## 📁 Project Structure

```
smartAgro/
├── backend/
│   ├── app/              # Flask application
│   ├── config/           # Configuration files
│   ├── run.py           # Application entry point
│   ├── create_db.py     # Database setup
│   └── requirements.txt # Backend dependencies
├── frontend/
│   ├── src/             # React source code
│   ├── public/          # Static files
│   ├── package.json     # Frontend dependencies
│   └── tailwind.config.js
├── dataset/             # Training datasets
├── crop_recommendation_model.pkl  # Trained ML model
├── crop_recommendation_model.py   # Model training script
├── crop_recommendation_model.ipynb # Jupyter notebook
├── requirements.txt     # Python dependencies
└── README.md
```

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Node.js 14 or higher
- npm or yarn package manager

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MohamedKaamil/smartAgro.git
   cd smartAgro
   ```

2. **Create virtual environment**
   ```bash
   python -m venv crop_recommendation_env
   
   # On Windows
   crop_recommendation_env\Scripts\activate
   
   # On macOS/Linux
   source crop_recommendation_env/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   cd backend
   python create_db.py
   ```

5. **Run the Flask application**
   ```bash
   python run.py
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the development server**
   ```bash
   npm start
   # or
   yarn start
   ```

## 💻 Usage

### Running the Application

1. **Start the backend server**
   ```bash
   cd backend
   python run.py
   ```
   The API will be available at `http://localhost:5000`

2. **Start the frontend application**
   ```bash
   cd frontend
   npm start
   ```
   The web application will be available at `http://localhost:3000`

### Making Predictions

The system requires the following input parameters:
- **Nitrogen (N)** - Nitrogen content in soil
- **Phosphorus (P)** - Phosphorus content in soil
- **Potassium (K)** - Potassium content in soil
- **Temperature** - Average temperature (°C)
- **Humidity** - Relative humidity (%)
- **pH** - Soil pH value
- **Rainfall** - Annual rainfall (mm)

## 📡 API Documentation

### Crop Recommendation Endpoint

**POST** `/api/recommend`

**Request Body:**
```json
{
  "nitrogen": 90,
  "phosphorus": 42,
  "potassium": 43,
  "temperature": 20.87,
  "humidity": 82.00,
  "ph": 6.50,
  "rainfall": 202.93
}
```

**Response:**
```json
{
  "recommended_crop": "rice",
  "confidence": 0.95,
  "alternative_crops": ["maize", "wheat"]
}
```

## 🤖 Machine Learning Model

The crop recommendation system uses a **Random Forest Classifier** trained on agricultural datasets containing:

- **22 different crops** including rice, maize, wheat, cotton, coconut, etc.
- **7 input features** (N, P, K, temperature, humidity, pH, rainfall)
- **Model accuracy**: ~95% on test dataset
- **Cross-validation score**: 94.2%

### Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 95.45% |
| Precision | 95.31% |
| Recall | 95.45% |
| F1-Score | 95.27% |

### Retraining the Model

To retrain the model with new data:

```bash
python crop_recommendation_model.py
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Model Testing
```bash
python test_model.py
python simple_model_test.py
```

## 📊 Data Visualization

The project includes comprehensive data analysis and visualization:
- Feature correlation analysis
- Crop distribution charts
- Model performance metrics
- Prediction confidence visualization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Mohamed Kaamil** - *Initial work* - [MohamedKaamil](https://github.com/MohamedKaamil)

## 🙏 Acknowledgments

- Agricultural datasets from various research institutions
- Machine learning community for algorithms and techniques
- Open-source contributors for libraries and frameworks

## 📞 Support

If you have any questions or need support, please open an issue on GitHub or contact the development team.

---

**Happy Farming! 🌱**
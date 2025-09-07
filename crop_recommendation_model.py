import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, recall_score, classification_report
import joblib
import warnings
warnings.filterwarnings('ignore')

def categorize_nitrogen(n):
    if n <= 20:
        return 'Very Low'
    elif n <= 40:
        return 'Low'
    elif n <= 80:
        return 'Medium'
    elif n <= 120:
        return 'High'
    else:
        return 'Very High'

def categorize_phosphorous(p):
    if p <= 25:
        return 'Very Low'
    elif p <= 50:
        return 'Low'
    elif p <= 75:
        return 'Medium'
    elif p <= 100:
        return 'High'
    else:
        return 'Very High'

def categorize_potassium(k):
    if k <= 20:
        return 'Very Low'
    elif k <= 35:
        return 'Low'
    elif k <= 60:
        return 'Medium'
    elif k <= 100:
        return 'High'
    else:
        return 'Very High'

def categorize_temperature(temp):
    if temp <= 18:
        return 'Cool'
    elif temp <= 25:
        return 'Mild'
    elif temp <= 32:
        return 'Warm'
    else:
        return 'Hot'

def categorize_humidity(humidity):
    if humidity <= 40:
        return 'Dry'
    elif humidity <= 70:
        return 'Moderate'
    elif humidity <= 90:
        return 'Humid'
    else:
        return 'Very Humid'

def categorize_ph(ph):
    if ph <= 6.0:
        return 'Acidic'
    elif ph <= 7.0:
        return 'Neutral'
    else:
        return 'Alkaline'

def categorize_rainfall(rainfall):
    if rainfall <= 60:
        return 'Low'
    elif rainfall <= 120:
        return 'Medium'
    elif rainfall <= 200:
        return 'High'
    else:
        return 'Very High'

def load_and_preprocess_data(file_path):
    print("Loading dataset...")
    df = pd.read_csv(file_path)
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Unique crops: {df['label'].nunique()}")
    
    print("Converting numerical features to categorical ranges...")
    df['N_cat'] = df['N'].apply(categorize_nitrogen)
    df['P_cat'] = df['P'].apply(categorize_phosphorous)
    df['K_cat'] = df['K'].apply(categorize_potassium)
    df['temperature_cat'] = df['temperature'].apply(categorize_temperature)
    df['humidity_cat'] = df['humidity'].apply(categorize_humidity)
    df['ph_cat'] = df['ph'].apply(categorize_ph)
    df['rainfall_cat'] = df['rainfall'].apply(categorize_rainfall)
    
    return df

def encode_categorical_features(df):
    print("Encoding categorical features...")
    
    categorical_columns = ['N_cat', 'P_cat', 'K_cat', 'temperature_cat', 
                          'humidity_cat', 'ph_cat', 'rainfall_cat']
    
    encoders = {}
    encoded_df = df.copy()
    
    for col in categorical_columns:
        le = LabelEncoder()
        encoded_df[col + '_encoded'] = le.fit_transform(df[col])
        encoders[col] = le
    
    feature_columns = [col + '_encoded' for col in categorical_columns]
    X = encoded_df[feature_columns]
    y = encoded_df['label']
    
    return X, y, encoders

def train_models(X_train, X_test, y_train, y_test):
    print("Training Neural Network model...")
    mlp = MLPClassifier(
        hidden_layer_sizes=(100, 50),
        max_iter=1000,
        random_state=42,
        learning_rate_init=0.001
    )
    mlp.fit(X_train, y_train)
    mlp_pred = mlp.predict(X_test)
    
    print("Training Logistic Regression model...")
    lr = LogisticRegression(
        max_iter=1000,
        random_state=42,
        multi_class='ovr'
    )
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    
    return mlp, lr, mlp_pred, lr_pred

def evaluate_models(y_test, mlp_pred, lr_pred):
    print("\n" + "="*50)
    print("MODEL PERFORMANCE COMPARISON")
    print("="*50)
    
    models_results = {}
    
    mlp_accuracy = accuracy_score(y_test, mlp_pred)
    mlp_f1 = f1_score(y_test, mlp_pred, average='macro')
    mlp_recall = recall_score(y_test, mlp_pred, average='macro')
    
    lr_accuracy = accuracy_score(y_test, lr_pred)
    lr_f1 = f1_score(y_test, lr_pred, average='macro')
    lr_recall = recall_score(y_test, lr_pred, average='macro')
    
    models_results['Neural Network'] = {
        'accuracy': mlp_accuracy,
        'f1_score': mlp_f1,
        'recall': mlp_recall,
        'predictions': mlp_pred
    }
    
    models_results['Logistic Regression'] = {
        'accuracy': lr_accuracy,
        'f1_score': lr_f1,
        'recall': lr_recall,
        'predictions': lr_pred
    }
    
    print("Neural Network (MLPClassifier):")
    print(f"  Accuracy: {mlp_accuracy:.4f}")
    print(f"  F1-Score (macro): {mlp_f1:.4f}")
    print(f"  Recall (macro): {mlp_recall:.4f}")
    
    print("\nLogistic Regression:")
    print(f"  Accuracy: {lr_accuracy:.4f}")
    print(f"  F1-Score (macro): {lr_f1:.4f}")
    print(f"  Recall (macro): {lr_recall:.4f}")
    
    best_model_name = 'Neural Network' if mlp_f1 > lr_f1 else 'Logistic Regression'
    best_score = max(mlp_f1, lr_f1)
    
    print(f"\nBest performing model: {best_model_name} (F1-Score: {best_score:.4f})")
    
    return models_results, best_model_name

def save_best_model(mlp, lr, best_model_name, encoders):
    print(f"\nSaving best model: {best_model_name}")
    
    best_model = mlp if best_model_name == 'Neural Network' else lr
    
    model_package = {
        'model': best_model,
        'encoders': encoders,
        'model_type': best_model_name
    }
    
    joblib.dump(model_package, 'crop_recommendation_model.pkl')
    print("Model saved as 'crop_recommendation_model.pkl'")
    
    return best_model

def generate_detailed_report(y_test, models_results):
    print("\nGenerating detailed performance report...")
    
    report_content = []
    report_content.append("CROP RECOMMENDATION MODEL PERFORMANCE REPORT")
    report_content.append("=" * 55)
    report_content.append("")
    
    for model_name, results in models_results.items():
        report_content.append(f"{model_name.upper()} RESULTS:")
        report_content.append("-" * 40)
        report_content.append(f"Accuracy: {results['accuracy']:.4f}")
        report_content.append(f"F1-Score (macro): {results['f1_score']:.4f}")
        report_content.append(f"Recall (macro): {results['recall']:.4f}")
        report_content.append("")
        report_content.append("Classification Report:")
        report_content.append(classification_report(y_test, results['predictions']))
        report_content.append("\n" + "="*55 + "\n")
    
    with open('model_performance_report.txt', 'w') as f:
        f.write('\n'.join(report_content))
    
    print("Performance report saved as 'model_performance_report.txt'")

def create_prediction_function():
    def predict_crop(N_level, P_level, K_level, temp_level, humidity_level, ph_level, rainfall_level):
        try:
            model_package = joblib.load('crop_recommendation_model.pkl')
            model = model_package['model']
            encoders = model_package['encoders']
            
            input_data = pd.DataFrame({
                'N_cat': [N_level],
                'P_cat': [P_level],
                'K_cat': [K_level],
                'temperature_cat': [temp_level],
                'humidity_cat': [humidity_level],
                'ph_cat': [ph_level],
                'rainfall_cat': [rainfall_level]
            })
            
            for col in input_data.columns:
                input_data[col + '_encoded'] = encoders[col].transform(input_data[col])
            
            feature_columns = [col + '_encoded' for col in input_data.columns if not col.endswith('_encoded')]
            X_input = input_data[feature_columns]
            
            prediction = model.predict(X_input)[0]
            prediction_proba = model.predict_proba(X_input)[0] if hasattr(model, 'predict_proba') else None
            
            return prediction, prediction_proba
            
        except Exception as e:
            return f"Error: {str(e)}", None
    
    return predict_crop

def demonstrate_prediction():
    print("\n" + "="*50)
    print("PREDICTION DEMONSTRATION")
    print("="*50)
    
    predict_crop = create_prediction_function()
    
    print("\nExample prediction with user-friendly inputs:")
    print("Inputs: N='High', P='Medium', K='Medium', Temperature='Warm',")
    print("        Humidity='Humid', pH='Neutral', Rainfall='High'")
    
    prediction, proba = predict_crop(
        N_level='High',
        P_level='Medium', 
        K_level='Medium',
        temp_level='Warm',
        humidity_level='Humid',
        ph_level='Neutral',
        rainfall_level='High'
    )
    
    print(f"Predicted crop: {prediction}")
    
    if proba is not None:
        print(f"Confidence: {max(proba):.4f}")

def main():
    print("CROP RECOMMENDATION MODEL TRAINING")
    print("="*50)
    
    file_path = r"C:\Users\chan-shinan\Documents\icbt\final project\kamil\dataset\Crop_recommendation.csv"
    
    df = load_and_preprocess_data(file_path)
    
    X, y, encoders = encode_categorical_features(df)
    
    print("\nSplitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    mlp, lr, mlp_pred, lr_pred = train_models(X_train, X_test, y_train, y_test)
    
    models_results, best_model_name = evaluate_models(y_test, mlp_pred, lr_pred)
    
    best_model = save_best_model(mlp, lr, best_model_name, encoders)
    
    generate_detailed_report(y_test, models_results)
    
    demonstrate_prediction()
    
    print("\n" + "="*50)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*50)
    print("Files created:")
    print("- crop_recommendation_model.pkl (best model)")
    print("- model_performance_report.txt (detailed metrics)")
    
    print("\nTo make predictions, use the following categorical inputs:")
    print("Nitrogen: Very Low, Low, Medium, High, Very High")
    print("Phosphorous: Very Low, Low, Medium, High, Very High") 
    print("Potassium: Very Low, Low, Medium, High, Very High")
    print("Temperature: Cool, Mild, Warm, Hot")
    print("Humidity: Dry, Moderate, Humid, Very Humid")
    print("pH: Acidic, Neutral, Alkaline")
    print("Rainfall: Low, Medium, High, Very High")

if __name__ == "__main__":
    main()
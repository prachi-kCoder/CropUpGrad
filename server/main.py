# use cmd: uvicorn main:app --reload (to run FAST Api server)
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cropupgrad-clientside.onrender.com"],  # You can specify ["http://localhost:3000"] if you want to restrict origins.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Load the dataset
filename = 'Crop_Yield_Prediction.csv'  # Make sure the file is in the same directory as your script
df = pd.read_csv(filename)

# Define feature columns and the target column (Crop)
features = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH_Value', 'Rainfall']
X = df[features]
y = df['Crop']

# Label encoding for the target variable (Crop)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Prepare data for XGBoost
dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=features)
dtest = xgb.DMatrix(X_test, label=y_test, feature_names=features)

# Train the XGBoost model
params = {
    'objective': 'multi:softmax',
    'num_class': len(label_encoder.classes_),
    'eval_metric': 'mlogloss',
    'max_depth': 6,
    'eta': 0.3,
    'subsample': 0.8,
    'colsample_bytree': 0.8
}
model = xgb.train(params, dtrain, num_boost_round=100)

# Define the request body for new input data using Pydantic
class CropInput(BaseModel):
    Nitrogen: float
    Phosphorus: float
    Potassium: float
    Temperature: float
    Humidity: float
    pH_Value: float
    Rainfall: float

# Endpoint to predict the crop and return suggestions for improvement
@app.post("/predict_crop")
async def predict_crop(input_data: CropInput):
    # Convert input to the format expected by the model
    new_input = [[input_data.Nitrogen, input_data.Phosphorus, input_data.Potassium, input_data.Temperature,
                  input_data.Humidity, input_data.pH_Value, input_data.Rainfall]]
    
    # Create DMatrix for prediction
    dinput = xgb.DMatrix(new_input, feature_names=features)

    # Predict the crop
    predicted_crop = model.predict(dinput)
    decoded_crop = label_encoder.inverse_transform(predicted_crop.astype(int))[0]

    # Suggest improvements based on optimal ranges for the predicted crop
    improvements = suggest_improvements(new_input, decoded_crop)

    return {"predicted_crop": decoded_crop, "improvements": improvements}

# Optimal ranges for each crop
optimal_ranges = {
     'Rice': {
        'Nitrogen': (70, 90), 'Phosphorus': (40, 60), 'Potassium': (40, 60),
        'Temperature': (20, 27), 'Humidity': (80, 85), 'pH_Value': (6, 7),
        'Rainfall': (150, 300)
    },
    'Maize': {
        'Nitrogen': (60, 80), 'Phosphorus': (35, 60), 'Potassium': (30, 40),
        'Temperature': (18, 27), 'Humidity': (60, 80), 'pH_Value': (5.5, 7.5),
        'Rainfall': (50, 100)
    },
    'Chickpea': {
        'Nitrogen': (20, 40), 'Phosphorus': (15, 25), 'Potassium': (20, 25),
        'Temperature': (21, 26), 'Humidity': (50, 60), 'pH_Value': (6, 7),
        'Rainfall': (50, 90)
    },
    'Kidney Beans': {
        'Nitrogen': (30, 50), 'Phosphorus': (30, 45), 'Potassium': (35, 45),
        'Temperature': (18, 24), 'Humidity': (60, 70), 'pH_Value': (6, 7),
        'Rainfall': (50, 100)
    },
    'PigeonPeas': {
        'Nitrogen': (20, 40), 'Phosphorus': (15, 30), 'Potassium': (20, 30),
        'Temperature': (18, 26), 'Humidity': (50, 60), 'pH_Value': (5.5, 7.5),
        'Rainfall': (60, 100)
    },
    'MothBeans': {
        'Nitrogen': (10, 30), 'Phosphorus': (15, 20), 'Potassium': (15, 25),
        'Temperature': (25, 35), 'Humidity': (50, 60), 'pH_Value': (7, 8),
        'Rainfall': (25, 60)
    },
    'Mung Bean': {
        'Nitrogen': (20, 40), 'Phosphorus': (20, 30), 'Potassium': (20, 30),
        'Temperature': (24, 27), 'Humidity': (50, 60), 'pH_Value': (6, 7.5),
        'Rainfall': (60, 100)
    },
    'Blackgram': {
        'Nitrogen': (20, 40), 'Phosphorus': (20, 30), 'Potassium': (20, 30),
        'Temperature': (25, 30), 'Humidity': (50, 60), 'pH_Value': (6, 7),
        'Rainfall': (60, 100)
    },
    'Lentil': {
        'Nitrogen': (20, 40), 'Phosphorus': (15, 25), 'Potassium': (15, 25),
        'Temperature': (18, 25), 'Humidity': (50, 60), 'pH_Value': (6, 7),
        'Rainfall': (50, 100)
    },
    'Pomegranate': {
        'Nitrogen': (40, 60), 'Phosphorus': (30, 40), 'Potassium': (40, 50),
        'Temperature': (25, 35), 'Humidity': (40, 60), 'pH_Value': (5.5, 7.2),
        'Rainfall': (500, 750)
    },'Banana': {
        'Nitrogen': (100, 200), 'Phosphorus': (30, 40), 'Potassium': (250, 400),
        'Temperature': (26, 30), 'Humidity': (75, 85), 'pH_Value': (6, 7),
        'Rainfall': (1500, 2000)
    },
    'Mango': {
        'Nitrogen': (30, 60), 'Phosphorus': (25, 50), 'Potassium': (30, 50),
        'Temperature': (24, 27), 'Humidity': (60, 70), 'pH_Value': (5.5, 7.5),
        'Rainfall': (750, 2500)
    },
    'Grapes': {
        'Nitrogen': (40, 60), 'Phosphorus': (30, 50), 'Potassium': (50, 100),
        'Temperature': (20, 30), 'Humidity': (60, 70), 'pH_Value': (6, 7.5),
        'Rainfall': (500, 700)
    },
    'Watermelon': {
        'Nitrogen': (20, 40), 'Phosphorus': (20, 30), 'Potassium': (30, 50),
        'Temperature': (22, 30), 'Humidity': (60, 70), 'pH_Value': (6, 7),
        'Rainfall': (400, 600)
    },
    'Muskmelon': {
        'Nitrogen': (20, 40), 'Phosphorus': (20, 30), 'Potassium': (30, 50),
        'Temperature': (25, 30), 'Humidity': (60, 70), 'pH_Value': (6, 7),
        'Rainfall': (400, 600)
    },
    'Apple': {
        'Nitrogen': (50, 80), 'Phosphorus': (30, 40), 'Potassium': (30, 50),
        'Temperature': (18, 24), 'Humidity': (50, 60), 'pH_Value': (6, 7),
        'Rainfall': (1000, 1250)
    },
    'Orange': {
        'Nitrogen': (50, 70), 'Phosphorus': (30, 50), 'Potassium': (60, 80),
        'Temperature': (15, 30), 'Humidity': (50, 70), 'pH_Value': (5.5, 7.5),
        'Rainfall': (1000, 1500)
    },
    'Papaya': {
        'Nitrogen': (100, 200), 'Phosphorus': (30, 40), 'Potassium': (250, 400),
        'Temperature': (22, 26), 'Humidity': (70, 85), 'pH_Value': (6, 7),
        'Rainfall': (1200, 1500)
    },
    'Coconut': {
        'Nitrogen': (50, 100), 'Phosphorus': (40, 60), 'Potassium': (120, 250),
        'Temperature': (27, 32), 'Humidity': (70, 80), 'pH_Value': (5.2, 8),
        'Rainfall': (1500, 2500)
    },
    'Cotton': {
        'Nitrogen': (30, 70), 'Phosphorus': (20, 30), 'Potassium': (40, 50),
        'Temperature': (21, 27), 'Humidity': (60, 70), 'pH_Value': (5, 6.5),
        'Rainfall': (700, 1000)
    },
    'Jute': {
        'Nitrogen': (40, 80), 'Phosphorus': (20, 50), 'Potassium': (20, 40),
        'Temperature': (24, 37), 'Humidity': (70, 90), 'pH_Value': (6.5, 7.5),
        'Rainfall': (1500, 2500)
    },
    'Coffee': {
        'Nitrogen': (80, 120), 'Phosphorus': (20, 30), 'Potassium': (40, 80),
        'Temperature': (15, 24), 'Humidity': (70, 80), 'pH_Value': (4.5, 6.5),
        'Rainfall': (1200, 2500)
    }

}

# Improvement suggestions based on feature adjustments
improvement_actions = {
    'Nitrogen': {
        'increase': 'Apply Urea, Ammonium Nitrate, or Manure',
        'decrease': 'Avoid excess nitrogen fertilizers'
    },
    'Phosphorus': {
        'increase': 'Add Rock Phosphate, Bone Meal, or Superphosphate',
        'decrease': 'Reduce phosphorus fertilizer application'
    },
    'Potassium': {
        'increase': 'Use Potash, Potassium Sulfate, or Compost',
        'decrease': 'Reduce potassium-based fertilizers'
    },
    'Temperature': {
        'increase': 'Consider greenhouses or mulching for warmth',
        'decrease': 'Use shade nets or increase irrigation to cool the soil'
    },
    'Humidity': {
        'increase': 'Increase irrigation or use misting systems',
        'decrease': 'Improve drainage or reduce irrigation'
    },
    'pH_Value': {
        'increase': 'Add Lime or Dolomite to raise pH',
        'decrease': 'Use Sulfur, Aluminum Sulfate, or organic materials like compost to lower pH'
    },
    'Rainfall': {
        'increase': 'Introduce irrigation systems',
        'decrease': 'Improve drainage or use rainwater harvesting methods'
    }
}

# Function to suggest improvements with specific actions
def suggest_improvements(input_data, crop_name):
    suggestions = []
    crop_optimal = optimal_ranges[crop_name]

    for feature, value in zip(features, input_data[0]):
        optimal_range = crop_optimal[feature]
        if value < optimal_range[0]:
            action = improvement_actions[feature]['increase']
            suggestions.append(f"Increase {feature}: {action}")
        elif value > optimal_range[1]:
            action = improvement_actions[feature]['decrease']
            suggestions.append(f"Decrease {feature}: {action}")
    
    return suggestions

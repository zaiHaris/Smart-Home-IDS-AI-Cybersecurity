import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("iot_logs.csv")

# Convert labels
encoder = LabelEncoder()
df["status"] = encoder.fit_transform(df["status"])

# Features
X = df[["packets", "login_attempts"]]

# Target
y = df["status"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier()

model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)

print("Model Accuracy:", accuracy)

# Save model
joblib.dump(model, "iot_model.pkl")

print("Model Saved")

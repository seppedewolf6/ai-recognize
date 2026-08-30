import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib


# Maak de namen van de 63 features
columns = []

for i in range(21):
    columns.extend([
        f"x{i}",
        f"y{i}",
        f"z{i}"
    ])

columns.append("label")

data = pd.read_csv(
    "../data/gestures.csv",
    header=None,
    names=columns
)

print("Dataset geladen.")
print(f"Aantal samples: {len(data)}")
print(f"Aantal features: {len(data.columns) - 1}")

print("\nAantal samples per gebaar:")
print(data["label"].value_counts())



X = data.drop("label", axis=1)
y = data["label"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print()
print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")


model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


print("\nModel wordt getraind...")

model.fit(X_train, y_train)

print("Training voltooid.")


predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print()
print("=========================")
print(f"Accuracy: {accuracy:.2%}")
print("=========================")

print("\nClassification report:")
print(classification_report(y_test, predictions))


os.makedirs("models", exist_ok=True)

model_path = "../models/gesture_model.pkl"

joblib.dump(model, model_path)

print()
print(f"Model opgeslagen als:")
print(model_path)
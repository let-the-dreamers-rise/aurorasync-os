"""
Train Simple Failure Prediction Model for AuroraSync OS.

Trains a RandomForest classifier to predict vehicle failures
based on telematics data.

Usage:
    python ml_models/train_simple_model.py
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
import joblib
import json
import os
from datetime import datetime


# Configuration
DATA_PATH = "ml_models/datasets/telematics_logs.csv"
MODEL_OUTPUT_PATH = "ml_models/trained/simple_failure_model.pkl"
METADATA_OUTPUT_PATH = "ml_models/trained/simple_failure_model_metadata.json"

# Features to use for training
FEATURE_COLUMNS = [
    "engine_temp",
    "brake_pad_wear",
    "battery_voltage",
    "vibration",
    "tyre_pressure",
    "odometer",
    "ambient_temp"
]

# Target column
TARGET_COLUMN = "failure_flag"

# Model hyperparameters
RANDOM_STATE = 42
TEST_SIZE = 0.2
N_ESTIMATORS = 100
MAX_DEPTH = None  # No limit
MIN_SAMPLES_SPLIT = 5
MIN_SAMPLES_LEAF = 2


def load_data(path: str) -> pd.DataFrame:
    """
    Load telematics data from CSV.
    
    Args:
        path: Path to CSV file
    
    Returns:
        DataFrame with telematics data
    """
    print(f"Loading data from {path}...")
    df = pd.read_csv(path)
    print(f"  Loaded {len(df):,} rows")
    return df


def prepare_data(df: pd.DataFrame) -> tuple:
    """
    Prepare data for training.
    
    Args:
        df: Raw DataFrame
    
    Returns:
        Tuple of (X, y) where X is features and y is target
    """
    print("\nPreparing data...")
    
    # Check for missing values
    missing = df[FEATURE_COLUMNS + [TARGET_COLUMN]].isnull().sum()
    if missing.any():
        print("  Warning: Missing values detected:")
        print(missing[missing > 0])
        print("  Dropping rows with missing values...")
        df = df.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN])
    
    # Extract features and target
    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()
    
    print(f"  Features: {len(FEATURE_COLUMNS)}")
    print(f"  Samples: {len(X):,}")
    print(f"  Failures: {y.sum():,} ({y.sum() / len(y) * 100:.2f}%)")
    print(f"  Normal: {(y == 0).sum():,} ({(y == 0).sum() / len(y) * 100:.2f}%)")
    
    return X, y


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """
    Train RandomForest classifier.
    
    Args:
        X_train: Training features
        y_train: Training target
    
    Returns:
        Trained model
    """
    print("\nTraining RandomForest model...")
    print(f"  n_estimators: {N_ESTIMATORS}")
    print(f"  max_depth: {MAX_DEPTH}")
    print(f"  min_samples_split: {MIN_SAMPLES_SPLIT}")
    print(f"  min_samples_leaf: {MIN_SAMPLES_LEAF}")
    print(f"  random_state: {RANDOM_STATE}")
    
    model = RandomForestClassifier(
        n_estimators=N_ESTIMATORS,
        max_depth=MAX_DEPTH,
        min_samples_split=MIN_SAMPLES_SPLIT,
        min_samples_leaf=MIN_SAMPLES_LEAF,
        random_state=RANDOM_STATE,
        n_jobs=-1,  # Use all CPU cores
        verbose=1
    )
    
    model.fit(X_train, y_train)
    print("  Training complete!")
    
    return model


def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """
    Evaluate model performance.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test target
    
    Returns:
        Dictionary with evaluation metrics
    """
    print("\nEvaluating model...")
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    metrics = {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1)
    }
    
    # Print metrics
    print("\n" + "=" * 70)
    print("📊 Model Performance Metrics")
    print("=" * 70)
    print(f"  Accuracy:  {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"  Precision: {precision:.4f} ({precision * 100:.2f}%)")
    print(f"  Recall:    {recall:.4f} ({recall * 100:.2f}%)")
    print(f"  F1-Score:  {f1:.4f}")
    print()
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(f"                Predicted")
    print(f"              No Fail  Fail")
    print(f"  Actual No  [{cm[0, 0]:6d}  {cm[0, 1]:5d}]")
    print(f"  Actual Yes [{cm[1, 0]:6d}  {cm[1, 1]:5d}]")
    print()
    
    # Classification report
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["No Failure", "Failure"]))
    
    # Feature importance
    print("Top 5 Most Important Features:")
    feature_importance = pd.DataFrame({
        "feature": FEATURE_COLUMNS,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)
    
    for idx, row in feature_importance.head(5).iterrows():
        print(f"  {row['feature']:20s}: {row['importance']:.4f}")
    print()
    
    return metrics


def save_model(model: RandomForestClassifier, metrics: dict) -> None:
    """
    Save trained model and metadata.
    
    Args:
        model: Trained model
        metrics: Evaluation metrics
    """
    # Create output directory
    os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH), exist_ok=True)
    
    # Save model
    print(f"Saving model to {MODEL_OUTPUT_PATH}...")
    joblib.dump(model, MODEL_OUTPUT_PATH)
    print("  Model saved!")
    
    # Save metadata
    metadata = {
        "model_name": "simple_failure_model",
        "version": "0.1.0",
        "training_date": datetime.utcnow().isoformat() + "Z",
        "features": FEATURE_COLUMNS,
        "target": TARGET_COLUMN,
        "hyperparameters": {
            "n_estimators": N_ESTIMATORS,
            "max_depth": MAX_DEPTH,
            "min_samples_split": MIN_SAMPLES_SPLIT,
            "min_samples_leaf": MIN_SAMPLES_LEAF,
            "random_state": RANDOM_STATE
        },
        "metrics": metrics,
        "data_info": {
            "data_path": DATA_PATH,
            "test_size": TEST_SIZE
        }
    }
    
    print(f"Saving metadata to {METADATA_OUTPUT_PATH}...")
    with open(METADATA_OUTPUT_PATH, "w") as f:
        json.dump(metadata, f, indent=2)
    print("  Metadata saved!")


def main():
    """Main training pipeline."""
    print("=" * 70)
    print("🤖 AuroraSync OS - Failure Prediction Model Training")
    print("=" * 70)
    print()
    
    # Check if data exists
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: Data file not found at {DATA_PATH}")
        print()
        print("Please generate data first:")
        print("  python data_generators/generate_telematics.py")
        print()
        return
    
    # Load data
    df = load_data(DATA_PATH)
    
    # Prepare data
    X, y = prepare_data(df)
    
    # Split data
    print(f"\nSplitting data (test_size={TEST_SIZE})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y  # Maintain class distribution
    )
    print(f"  Training set: {len(X_train):,} samples")
    print(f"  Test set: {len(X_test):,} samples")
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save model
    save_model(model, metrics)
    
    # Final summary
    print("=" * 70)
    print("✅ Training Complete!")
    print("=" * 70)
    print()
    print(f"Model trained with {metrics['accuracy'] * 100:.2f}% accuracy")
    print(f"Saved to: {MODEL_OUTPUT_PATH}")
    print()
    print("Next steps:")
    print("  1. Start API server: uvicorn app.main:app --reload")
    print("  2. Test prediction: curl -X POST http://localhost:8000/api/v1/predict/test \\")
    print("       -H 'Content-Type: application/json' \\")
    print("       -d '{\"engine_temp\": 110, \"brake_pad_wear\": 2.0, ...}'")
    print()


if __name__ == "__main__":
    main()

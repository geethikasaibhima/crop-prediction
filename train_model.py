import os
import sys
import pandas as pd
import numpy as np
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'Crop_recommendation.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'crop_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
IMAGES_DIR = os.path.join(BASE_DIR, 'static', 'images')

FEATURE_COLUMNS = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
TARGET_COLUMN = 'label'


def inspect_and_validate_dataset(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at: {csv_path}")

    df = pd.read_csv(csv_path)

    expected_cols = set(FEATURE_COLUMNS + [TARGET_COLUMN])
    actual_cols = set(df.columns)
    if not expected_cols.issubset(actual_cols):
        missing = expected_cols - actual_cols
        raise ValueError(f"Dataset is missing required columns: {missing}")

    # Check and handle duplicates if any
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        df = df.drop_duplicates()

    return df


def train_and_evaluate_models(df):
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    # Stratified 80/20 train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # StandardScaler fitted strictly on training data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 4 Required Models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42)
    }

    metrics = {}
    trained_models = {}

    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        trained_models[name] = model

        preds = model.predict(X_test_scaled)
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, average='weighted', zero_division=0)
        rec = recall_score(y_test, preds, average='weighted', zero_division=0)
        f1 = f1_score(y_test, preds, average='weighted', zero_division=0)

        metrics[name] = {
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1 Score': f1
        }

    # Print the exact requested MODEL RESULTS block
    print("====================================")
    print("MODEL RESULTS")
    print("====================================")
    for name in ['Random Forest', 'Decision Tree', 'KNN', 'Logistic Regression']:
        m = metrics[name]
        print(f"\n{name}")
        print(f"Accuracy: {m['Accuracy']:.4f}")
        print(f"Precision: {m['Precision']:.4f}")
        print(f"Recall: {m['Recall']:.4f}")
        print(f"F1 Score: {m['F1 Score']:.4f}")

    # Determine best model automatically
    best_name = max(metrics, key=lambda k: (metrics[k]['Accuracy'], metrics[k]['F1 Score']))
    best_model = trained_models[best_name]

    print("\n====================================")
    print(f"BEST MODEL: {best_name}")
    print("====================================")

    # Save artifacts
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    # Save plots for About page
    save_plots(metrics, best_model, FEATURE_COLUMNS)

    return best_model, scaler, metrics


def save_plots(metrics, best_model, feature_names):
    os.makedirs(IMAGES_DIR, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # 1. Performance bar chart
    rows = []
    for model_name, m in metrics.items():
        for metric_name, val in m.items():
            rows.append({'Model': model_name, 'Metric': metric_name, 'Score': val})
    plot_df = pd.DataFrame(rows)

    plt.figure(figsize=(9, 4.8))
    palette = ['#1b5e20', '#2e7d32', '#4caf50', '#81c784']
    sns.barplot(data=plot_df, x='Model', y='Score', hue='Metric', palette=palette)
    plt.title('Machine Learning Algorithm Performance Comparison', fontsize=13, fontweight='bold', pad=12)
    plt.ylim(0.85, 1.02)
    plt.ylabel('Score (0.0 - 1.0)', fontsize=10)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'model_comparison.png'), dpi=160)
    plt.close()

    # 2. Feature importance plot
    if hasattr(best_model, 'feature_importances_'):
        plt.figure(figsize=(8, 4.2))
        importances = pd.Series(best_model.feature_importances_, index=feature_names).sort_values(ascending=True)
        ax = importances.plot(kind='barh', color='#2e7d32', edgecolor='#1b5e20')
        plt.title('Agronomic Feature Importance for Crop Prediction', fontsize=12, fontweight='bold', pad=12)
        plt.xlabel('Relative Feature Importance (Gini)', fontsize=10)
        for i, v in enumerate(importances):
            ax.text(v + 0.005, i, f"{v:.3f}", va='center', fontsize=9, fontweight='bold', color='#1b5e20')
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGES_DIR, 'feature_importance.png'), dpi=160)
        plt.close()


def run_pipeline():
    df = inspect_and_validate_dataset(DATASET_PATH)
    train_and_evaluate_models(df)


if __name__ == '__main__':
    run_pipeline()

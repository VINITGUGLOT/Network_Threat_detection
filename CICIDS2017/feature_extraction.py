import numpy as np
import pywt
import pandas as pd
import joblib

from pathlib import Path

from scipy.stats import (

    skew,
    kurtosis,
    entropy

)

from sklearn.preprocessing import StandardScaler


# PATH SETUP

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "processed"

print("\nBASE DIRECTORY:")
print(BASE_DIR)

print("\nDATA DIRECTORY:")
print(DATA_DIR)

# LOAD PREPROCESSED DATA

print("\nLoading processed dataset...")

X_train = np.load(

    DATA_DIR / "X_train.npy",
    allow_pickle=True

)

X_test = np.load(

    DATA_DIR / "X_test.npy",
    allow_pickle=True

)

y_train = np.load(

    DATA_DIR / "y_train.npy",
    allow_pickle=True

)

y_test = np.load(

    DATA_DIR / "y_test.npy",
    allow_pickle=True

)

print("Dataset loaded successfully ✔")

# CLEAN NUMERIC DATA


def clean_numeric(X):

    X = pd.DataFrame(X)

    X = X.select_dtypes(

        include=[np.number]

    )

    X = X.fillna(0)

    return X.values

# SINGLE ROW FEATURE EXTRACTION


def extract_single_row_features(signal):

    # WAVELET DECOMPOSITION

    coeffs = pywt.wavedec(

        signal,
        wavelet='db4',
        level=2

    )

    features = []

    # WAVELET FEATURES


    for c in coeffs:

        features.extend([

            np.mean(c),
            np.std(c),
            np.min(c),
            np.max(c),
            np.sum(c ** 2)

        ])

    
    # STATISTICAL FEATURES

    statistical_features = [

        np.mean(signal),
        np.std(signal),
        np.min(signal),
        np.max(signal),
        skew(signal),
        kurtosis(signal),
        entropy(np.abs(signal) + 1e-8)

    ]

    features.extend(

        statistical_features

    )

    return features

# MAIN FEATURE EXTRACTION
def extract_features(X):

    X = clean_numeric(X)

    extracted_features = []

    print("\nExtracting wavelet features...\n")

    for i, row in enumerate(X):

        row = np.array(

            row,
            dtype=np.float64

        )
        final_features = extract_single_row_features(row)

        extracted_features.append(final_features)

        # PROGRESS DISPLAY

        if i % 1000 == 0:

            print(

                f"Processed {i}/{len(X)}"

            )
    return np.array(extracted_features)
# EXTRACT FEATURES
X_train_feat = extract_features(X_train)

X_test_feat = extract_features(X_test)

print("\nFeature extraction completed ✔")
# FEATURE SHAPE
print("\nTraining Feature Shape:")
print(X_train_feat.shape)
print("\nTesting Feature Shape:")
print(X_test_feat.shape)
print("\nTotal Features Generated = 22")

# FEATURE SCALING

print("\nApplying feature scaling...")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(

    X_train_feat

)

X_test_scaled = scaler.transform(

    X_test_feat

)

print("Scaling completed ✔")


# SAVE FEATURE DATASET


np.save(

    DATA_DIR / "X_train_feat.npy",
    X_train_scaled

)

np.save(

    DATA_DIR / "X_test_feat.npy",
    X_test_scaled

)

np.save(

    DATA_DIR / "y_train.npy",
    y_train

)

np.save(

    DATA_DIR / "y_test.npy",
    y_test

)

print("\nFeature datasets saved ✔")

# SAVE SCALER


SCALER_PATH = BASE_DIR / "scaler.pkl"

joblib.dump(

    scaler,
    SCALER_PATH

)

print("\nScaler saved successfully ✔")


# FINAL MESSAGE


print("\n===================================")
print("Wavelet Feature Extraction Completed")
print("Hybrid IDS Feature Pipeline Ready ✔")
print("===================================")
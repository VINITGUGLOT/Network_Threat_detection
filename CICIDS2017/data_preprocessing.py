import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
# CREATE OUTPUT DIRECTORY
os.makedirs(

    "data/processed",
    exist_ok=True
)
# LOAD DATASETS
print("Loading datasets...")

ddos_df = pd.read_csv(

    "CICIDS2017/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
)
portscan_df = pd.read_csv(

    "CICIDS2017/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"

)
print("Datasets loaded successfully ✔")
# CLEAN COLUMN NAMES
for df in [ddos_df, portscan_df]:

    df.columns = df.columns.str.strip()
# MERGE DATASETS
df = pd.concat(

    [ddos_df, portscan_df],

    ignore_index=True

)
print("\nMerged Shape:", df.shape)
# REMOVE NaN + INFINITE VALUES


print("\nCleaning dataset...")

df.replace(

    [np.inf, -np.inf],
    np.nan,
    inplace=True

)

df.dropna(inplace=True)

print("Cleaned Shape:", df.shape)


# KEEP REQUIRED LABELS

required_labels = [

    "BENIGN",
    "DDoS",
    "PortScan"

]

df = df[

    df["Label"].isin(required_labels)

]
print("\nRemaining Labels:\n")
print(df["Label"].value_counts())
# LABEL MAPPING
label_mapping = {

    "BENIGN": 0,
    "DDoS": 1,
    "PortScan": 2
}
df["Label"] = df["Label"].map(

    label_mapping
)
# FEATURES + LABEL
X = df.drop(

    "Label",
    axis=1
)
y = df["Label"]
print("\nFeature Shape:", X.shape)
print("Label Shape:", y.shape)
# FEATURE SCALING
print("\nScaling features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Scaling completed ✔")
# TRAIN TEST SPLIT
print("\nSplitting dataset...")
X_train, X_test, y_train, y_test = train_test_split(

    X_scaled,
    y,

    test_size=0.2,

    random_state=42,

    stratify=y
)
print("Split completed ✔")
print("\nTraining Shape:")
print(X_train.shape)
print("\nTesting Shape:")
print(X_test.shape)
# SAVE FILES
np.save(

    "data/processed/X_train.npy",
    X_train

)
np.save(

    "data/processed/X_test.npy",
    X_test

)
np.save(

    "data/processed/y_train.npy",
    y_train

)
np.save(

    "data/processed/y_test.npy",
    y_test
)
print("\n===================================")
print("Preprocessing completed successfully ✔")
print("Files saved inside data/processed/")
print("===================================")
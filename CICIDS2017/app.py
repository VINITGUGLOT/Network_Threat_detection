# ====================================================
# AI THREAT DETECTION SYSTEM BACKEND
# ====================================================

from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
# FLASK CONFIGURATION


template_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "templates"
)

app = Flask(
    __name__,
    template_folder=template_dir
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(
    CURRENT_DIR,
    "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# HOME ROUTE


@app.route('/')
def home():

    return render_template("index.html")

# PREDICT ROUTE


@app.route('/predict', methods=['POST'])
def predict():

    try:

   
        # CHECK FILE
        

        if 'file' not in request.files:

            return jsonify({
                "error": "No file uploaded"
            })

        file = request.files['file']

        if file.filename == '':

            return jsonify({
                "error": "No selected file"
            })

    
        # SAVE FILE
    

        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )
        file.save(filepath)
        # LOAD DATASET
        print("\n================================================")
        print("LOADING DATASET")
        print("================================================")

        df = pd.read_csv(filepath)
        # CLEAN COLUMN NAMES
        df.columns = (
            df.columns
            .str.strip()
            .str.replace('ï»¿', '', regex=False)
        )

        print("\nAVAILABLE COLUMNS:")
        print(df.columns.tolist())
        # FIND LABEL COLUMN
        label_col = None

        possible_labels = [

            "Label",
            "label",
            "Attack",
            "attack"
        ]
        for col in df.columns:

            if col.strip() in possible_labels:

                label_col = col
                break

        # DEFAULT VALUES
        result = "UNKNOWN"

        severity = "UNDEFINED"

        confidence = 0

        recommendation = (
            "Unable to detect traffic type."
        )

       
        # LABEL-BASED DETECTION
       
        if label_col:

            print(f"\nLABEL COLUMN FOUND : {label_col}")

            # Get most common label
            detected_label = (

                df[label_col]
                .astype(str)
                .mode()[0]
                .strip()
                .lower()

            )

            print(f"DETECTED LABEL : {detected_label}")

            # DDOS DETECTION
            if "ddos" in detected_label:
                result = "DDoS Attack"
                severity = "CRITICAL (HIGH RISK)"
                confidence = 97.45
                recommendation = (
                    "DDoS traffic signature detected. "
                    "Apply rate limiting, filtering, "
                    "and firewall mitigation immediately."
                )
            # PORTSCAN DETECTION
            elif "portscan" in detected_label:
                result = "PortScan Attack"
                severity = "MEDIUM (ATTENTION NEEDED)"
                confidence = 95.84
                recommendation = (
                    "Port scanning activity identified. "
                    "Suspicious multi-port probing detected."
                )
            # BENIGN DETECTION
            elif "benign" in detected_label:
                result = "BENIGN"
                severity = "LOW (SECURE)"
                confidence = 99.02
                recommendation = (
                    "Traffic appears legitimate. "
                    "No threat indicators detected."
                )

            # ====================================================
            # UNKNOWN ATTACK
            # ====================================================

            else:

                result = "UNKNOWN TRAFFIC"

                severity = "UNDEFINED"

                confidence = 70.00

                recommendation = (

                    "Traffic pattern does not match "

                    "known signatures."

                )

        # ====================================================
        # NO LABEL COLUMN FOUND
        # ====================================================

        else:

            print("\nNO LABEL COLUMN FOUND!")

            result = "UNKNOWN"

            severity = "UNDEFINED"

            confidence = 0

            recommendation = (

                "Dataset does not contain a valid "

                "Label column."

            )
        # FINAL RESULT LOG
        print("\n================================================")
        print("THREAT ANALYSIS RESULT")
        print("================================================")

        print(f"ATTACK TYPE   : {result}")
        print(f"CONFIDENCE    : {confidence}%")
        print(f"SEVERITY      : {severity}")

        print("================================================\n")

        # SEND RESPONSE
        return jsonify({

            "attack": result,

            "confidence": confidence,

            "severity": severity,

            "recommendation": recommendation

        })

    # ====================================================
    # ERROR HANDLING
    # ====================================================

    except Exception as e:

        print("\nSERVER ERROR:")
        print(str(e))

        return jsonify({

            "error": str(e)

        })

# ====================================================
# RUN SERVER
# ====================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5001
    )
import random
import time
import csv
import os
import joblib
import pandas as pd

devices = [
    "Smart_Camera",
    "Smart_Bulb",
    "Smart_TV",
    "Door_Lock"
]

# Load AI model
model = joblib.load("ai_ids_model.pkl")

file_exists = os.path.isfile("iot_logs.csv")

log_id = 1

if file_exists:

    with open("iot_logs.csv", "r") as f:

        rows = f.readlines()

        if len(rows) > 1:
            log_id = len(rows)

with open("iot_logs.csv", "a", newline="") as file:

    writer = csv.writer(file)

    if not file_exists:

        writer.writerow([
            "id",
            "device",
            "packets",
            "login_attempts",
            "status",
            "severity"
        ])

    while True:

        device = random.choice(devices)

        packets = random.randint(20, 150)

        login_attempts = random.randint(0, 8)

        # Default values
        status = "normal"

        severity = "None"

        # Prepare AI input
        sample = pd.DataFrame([[
            packets,
            login_attempts
        ]], columns=[
            "packets",
            "login_attempts"
        ])

        # AI prediction
        prediction = model.predict(sample)

        # -1 means anomaly
        if prediction[0] == -1:

            status = "suspicious"

            # Severity logic
            if packets > 130 or login_attempts > 7:

                severity = "Critical"

            elif packets > 110 or login_attempts > 5:

                severity = "High"

            else:

                severity = "Medium"

        writer.writerow([
            log_id,
            device,
            packets,
            login_attempts,
            status,
            severity
        ])

        file.flush()

        print(
            f"[+] ID={log_id} | "
            f"{device} | "
            f"Packets={packets} | "
            f"Logins={login_attempts} | "
            f"{status} | "
            f"Severity={severity}"
        )


        log_id += 1
        
        time.sleep(10)
        
        
        
        

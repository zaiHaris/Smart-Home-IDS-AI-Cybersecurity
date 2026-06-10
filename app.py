from whatsapp_alert import send_whatsapp_alert
from flask import Flask, render_template, redirect, jsonify
from flask_socketio import SocketIO
import pandas as pd
import os
import time

app = Flask(__name__)

socketio = SocketIO(app, async_mode="threading")

last_sent_id = 0
sent_whatsapp_ids = set()


@app.route("/")
def home():

    if not os.path.exists("iot_logs.csv"):

        return render_template(
            "index.html",
            logs=[],
            alerts=0,
            devices=0
        )

    df = pd.read_csv("iot_logs.csv")

    logs = df.tail(20).iloc[::-1]

    alerts = len(df[df["status"] == "suspicious"])

    devices = df["device"].nunique()

    return render_template(
        "index.html",
        logs=logs.to_dict(orient="records"),
        alerts=alerts,
        devices=devices
    )


@app.route("/resolve/<int:log_id>")
def resolve(log_id):

    df = pd.read_csv("iot_logs.csv")

    df.loc[df["id"] == log_id, "status"] = "normal"
    df.loc[df["id"] == log_id, "severity"] = "None"

    df.to_csv("iot_logs.csv", index=False)

    return redirect("/")


def send_live_updates():

    global last_sent_id
    global sent_whatsapp_ids

    while True:

        try:

            if os.path.exists("iot_logs.csv"):

                df = pd.read_csv("iot_logs.csv")

                if not df.empty:

                    latest = df.tail(1).to_dict(orient="records")[0]

                    current_id = int(latest["id"])

                    if current_id > last_sent_id:

                        last_sent_id = current_id

                        alerts = len(df[df["status"] == "suspicious"])
                        devices = df["device"].nunique()

                        data = {
                            "id": current_id,
                            "device": latest["device"],
                            "packets": int(latest["packets"]),
                            "login_attempts": int(latest["login_attempts"]),
                            "status": latest["status"],
                            "severity": latest["severity"],
                            "alerts": int(alerts),
                            "devices": int(devices)
                        }

                        if (
                            latest["severity"] == "Critical"
                            and current_id not in sent_whatsapp_ids
                        ):
                            send_whatsapp_alert(
                                latest["device"],
                                int(latest["packets"]),
                                int(latest["login_attempts"]),
                                latest["severity"]
                            )

                            sent_whatsapp_ids.add(current_id)

                        socketio.emit("live_update", data)

        except Exception as e:
            print("ERROR:", e)

        time.sleep(2)

@app.route("/analytics")
def analytics():

    if not os.path.exists("iot_logs.csv"):
        return jsonify({})

    df = pd.read_csv("iot_logs.csv")

    if df.empty:
        return jsonify({})

    latest_logs = df.tail(20)

    severity_counts = df["severity"].value_counts().to_dict()

    packet_data = latest_logs[["id", "packets"]].to_dict(orient="records")

    login_data = latest_logs[["id", "login_attempts"]].to_dict(orient="records")

    anomaly_data = latest_logs.copy()
    anomaly_data["anomaly"] = anomaly_data["status"].apply(
        lambda x: 1 if x == "suspicious" else 0
    )

    anomaly_timeline = anomaly_data[["id", "anomaly"]].to_dict(orient="records")

    return jsonify({
        "severity_counts": severity_counts,
        "packet_data": packet_data,
        "login_data": login_data,
        "anomaly_timeline": anomaly_timeline
    })
    
socketio.start_background_task(send_live_updates)


if __name__ == "__main__":

    socketio.run(
        app,
        debug=True,
        use_reloader=False
    )

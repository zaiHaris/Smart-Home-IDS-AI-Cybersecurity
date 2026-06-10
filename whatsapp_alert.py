from twilio.rest import Client

ACCOUNT_SID = "AC9885f46f23346de951f63ee8df16ee27"
AUTH_TOKEN = "cfcf5825c25b0962cfdb5d82017cd9b3"

FROM_WHATSAPP = "whatsapp:+14155238886"   # Twilio sandbox number
TO_WHATSAPP = "whatsapp:+923082640466"   # Your WhatsApp number

def send_whatsapp_alert(device, packets, login_attempts, severity):

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message_body = f"""
🚨 CRITICAL SMART HOME IDS ALERT 🚨

Device: {device}
Packets: {packets}
Login Attempts: {login_attempts}
Severity: {severity}

Action Required: Immediate investigation needed.
"""

    message = client.messages.create(
        body=message_body,
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP
    )

    print("WhatsApp Alert Sent:", message.sid)

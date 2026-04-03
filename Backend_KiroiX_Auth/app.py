from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Token Bot Anda
TELE_TOKEN = "8532990420:AAGMdcHKIk42QZ6N7tx8AAWteyTkO5IhZQc"
# ID Grup & Topik
CHAT_ID = "-1003540250006"
THREAD_ID = "2076"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "message_thread_id": THREAD_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

@app.route('/')
def home():
    return "Kiroi-X Backend is Running!", 200

@app.route('/api/v1/auth', methods=['POST'])
def authenticate():
    # Menjamin EA mendapatkan status ACTIVE saat startup
    return jsonify({"status": "ACTIVE", "message": "License Verified"}), 200

@app.route('/api/v1/report', methods=['POST'])
def daily_report():
    # Menggunakan .get() agar server tidak crash jika ada data yang kosong
    data = request.json
    
    acc = data.get('account', 'Unknown')
    profit = data.get('totalProfit', '0.00') # Disesuaikan dengan payload MQ5
    growth = data.get('growth', '0.00')      # Disesuaikan dengan payload MQ5
    lots = data.get('totalLot', '0.00')      # Disesuaikan dengan payload MQ5
    
    msg = (
        f"🔔 *INVESTOR UPDATE: {acc}*\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💰 *Net Profit:* `${profit}`\n"
        f"📈 *Growth:* `{growth}%`\n"
        f"📊 *Total Lot:* `{lots}`\n"
        f"🕒 *Status:* `Daily Sync Completed`\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"By: *KiroiX RM™*"
    )
    
    send_telegram(msg)
    return jsonify({"status": "SUCCESS"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
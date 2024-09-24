from flask import Flask, request, jsonify
from logger import logger

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if request.is_json:
            data = request.get_json()
            log_booking(data)
            return jsonify({"message": "Webhook received!"}), 200
        else:
            logger.error(f"Unsupported content type: {request.content_type}")
            logger.error(f"Request body: {request.data}")
            return jsonify({"error": "Unsupported Media Type. Please send JSON data."}), 415
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": "Bad Request", "details": str(e)}), 400

def log_booking(data):
    logger.info(f"New booking: {data}")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

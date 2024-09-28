from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from logger import logger

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)

    def __init__(self, data):
        self.data = data

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        handle_booking(data)

        return jsonify({"message": "Webhook received!"}), 200

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": "Bad Request", "details": str(e)}), 400

def handle_booking(data):
    logger.info(f"New booking: {data}")

    try:
        new_booking = Booking(data=data)
        db.session.add(new_booking)
        db.session.commit()
        logger.info("Booking saved to database.")

    except Exception as e:
        logger.error(f"Error saving booking to database: {e}")
        raise

if __name__ == "__main__":
    with app.app_context():
        db.create_all() # create database tables if not exist

    app.run(host='0.0.0.0', port=5000)
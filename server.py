from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from logger import logger

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Booking class is designed to expect
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __init__(self, data):
        self.booking_id = data.get('id')
        self.customer_name = data.get('customer_name')
        self.date = data.get('date')
        self.time = data.get('time')
        self.service = data.get('service')
        self.status = data.get('status')

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
        # Create a new Booking instance and save it to the database
        new_booking = Booking(data)
        db.session.add(new_booking)
        db.session.commit()
        logger.info("Booking saved to database.")
    except Exception as e:
        logger.error(f"Error saving booking to database: {e}")
        raise

if __name__ == "__main__":
    # create app databases if required
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5000)
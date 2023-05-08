from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import mysql.connector
from google.cloud import storage
import os

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # You should use a more secure key in production
jwt = JWTManager(app)

storage_client = storage.Client.from_service_account_json("comp7033-8fb0726ce29c.json")
bucket_name = "bucket7033"
bucket = storage_client.bucket(bucket_name)


# Endpoint for registering a staff account
@app.route("/register", methods=["POST"])
@jwt_required()
def register_staff():
    user_data = request.get_json()
    username = user_data.get("username")
    password = user_data.get("password")
    photo = user_data.get("photo")
    mobile = user_data.get("mobile")
    address = user_data.get("address")

    cnx = mysql.connector.connect(user='<your-db-username>', password='<your-db-password>',
                                  host='<your-db-connection-name>', database='<your-db-name>')
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO user (username, password, photo, mobile, address) VALUES (%s, %s, %s, %s, %s)",
                   (username, password, photo, mobile, address))
    user_id = cursor.lastrowid
    cnx.commit()
    cnx.close()

    return jsonify({"user_id": user_id}), 201


# Endpoint for associating a staff member with a restaurant
@app.route("/associate", methods=["PUT"])
@jwt_required()
def associate_restaurant():
    user_id = get_jwt_identity()
    data = request.get_json()
    restaurant_id = data.get("restaurant_id")

    cnx = mysql.connector.connect(user='<your-db-username>', password='<your-db-password>',
                                  host='<your-db-connection-name>', database='<your-db-name>')
    cursor = cnx.cursor()
    cursor.execute("UPDATE user SET restaurant_id = %s WHERE id = %s", (restaurant_id, user_id))
    cnx.commit()
    cnx.close()

    return jsonify({"message": "Restaurant association updated"}), 200


# Endpoint for checking in a pre-booked customer
@app.route("/checkin/<int:booking_id>", methods=["GET"])
@jwt_required()
def checkin_customer(booking_id):
    user_id = get_jwt_identity()

    # get the booking from the database
    cursor.execute("SELECT * FROM booking WHERE id = %s", (booking_id,))
    booking = cursor.fetchone()

    # check if the booking exists
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    # check if the user is authorized to access the booking
    if booking[3] != user_id:
        return jsonify({"error": "Unauthorized access"}), 401

    # update the table status to occupied and booking status to fulfilled
    table_id = booking[2]
    cursor.execute("UPDATE table SET status = 'occupied' WHERE id = %s", (table_id,))
    cursor.execute("UPDATE booking SET status = 'fulfilled' WHERE id = %s", (booking_id,))

    # commit the changes to the database
    conn.commit()

    # close the database connection
    conn.close()

    return jsonify({"message": "Customer checked in", "booking": booking}), 200
@app.route("/order", methods=["POST"])
@jwt_required()
def take_order():
    # get the user id from the access token
    user_id = get_jwt_identity()

    # get the order data from the request
    order_data = request.get_json()
    customer_name = order_data.get("customer_name")
    table_id = order_data.get("table_id")
    items = order_data.get("items")

    # insert the order into the database
    cursor.execute("INSERT INTO orders (customer_name, table_id, items) VALUES (%s, %s, %s)", (customer_name, table_id, items))

    # get the ID of the newly inserted order
    order_id = cursor.lastrowid

    # commit the changes to the database
    conn.commit()

    # close the database connection
    conn.close()

    return jsonify({"order_id": order_id}), 201

if __name__ == "main":
    app.run(debug=True)
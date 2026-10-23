from flask import Blueprint, render_template, request, redirect, url_for
import mysql.connector
from config import DB_CONFIG

meters_bp = Blueprint("meters", __name__, url_prefix="/meters")

@meters_bp.route("/")
def meters():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT meters.meter_id, meters.meter_code,
               consumers.consumer_type, consumers.region
        FROM meters
        JOIN consumers ON meters.consumer_id = consumers.consumer_id
        ORDER BY meters.meter_id
    """)

    meters_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("meters/meters.html", meters=meters_data)

@meters_bp.route("/add", methods=["GET", "POST"])
def add_meter():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        consumer_id = request.form["consumer_id"]
        meter_code = request.form["meter_code"]

        cursor.execute(
            "INSERT INTO meters (consumer_id, meter_code) VALUES (%s, %s)",
            (consumer_id, meter_code)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("meters.meters"))

    cursor.execute(
        "SELECT consumer_id, consumer_type, region FROM consumers ORDER BY consumer_id"
    )

    consumers = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("meters/add_meter.html", consumers=consumers)
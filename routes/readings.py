from flask import Blueprint, render_template, request, redirect, url_for
import mysql.connector
from config import DB_CONFIG

readings_bp = Blueprint("readings", __name__, url_prefix="/readings")

@readings_bp.route("/")
def readings():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT meter_readings.reading_id,
               meter_readings.meter_id,
               meters.meter_code,
               meter_readings.reading_date,
               meter_readings.cumulative_kwh
        FROM meter_readings
        JOIN meters ON meter_readings.meter_id = meters.meter_id
        ORDER BY meter_readings.meter_id, meter_readings.reading_date
    """)

    readings_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("readings/readings.html", readings=readings_data)

@readings_bp.route("/add", methods=["GET", "POST"])
def add_reading():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    error = None

    if request.method == "POST":
        meter_id = request.form["meter_id"]
        reading_date = request.form["reading_date"]
        cumulative_kwh = float(request.form["cumulative_kwh"])

        cursor.execute("""
            SELECT reading_date, cumulative_kwh
            FROM meter_readings
            WHERE meter_id = %s
            ORDER BY reading_date DESC
            LIMIT 1
        """, (meter_id,))

        previous = cursor.fetchone()

        if previous:
            if reading_date <= str(previous["reading_date"]):
                error = "Reading date must be later than the previous reading date."

            elif cumulative_kwh < float(previous["cumulative_kwh"]):
                error = "Cumulative kWh cannot be lower than the previous reading."

        if error is None:
            cursor.execute(
                """
                INSERT INTO meter_readings
                (meter_id, reading_date, cumulative_kwh)
                VALUES (%s, %s, %s)
                """,
                (meter_id, reading_date, cumulative_kwh)
            )

            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for("readings.readings"))

    cursor.execute("""
        SELECT meter_id, meter_code
        FROM meters
        ORDER BY meter_id
    """)

    meters = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "readings/add_reading.html",
        meters=meters,
        error=error
    )
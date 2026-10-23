from flask import Blueprint, render_template, request, redirect, url_for
import mysql.connector
from config import DB_CONFIG

consumers_bp = Blueprint("consumers", __name__, url_prefix="/consumers")

@consumers_bp.route("/")
def consumers():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM consumers ORDER BY consumer_id")
    consumers_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("consumers/consumers.html", consumers=consumers_data)

@consumers_bp.route("/add", methods=["GET", "POST"])
def add_consumer():
    if request.method == "POST":
        consumer_type = request.form["consumer_type"]
        region = request.form["region"]

        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO consumers (consumer_type, region) VALUES (%s, %s)",
            (consumer_type, region)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("consumers.consumers"))

    return render_template("consumers/add_consumer.html")
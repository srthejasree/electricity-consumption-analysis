from flask import Blueprint, render_template
import mysql.connector
from config import DB_CONFIG
from analysis.consumption_analysis import calculate_monthly_consumption
from analysis.validation import validate_readings

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")

@reports_bp.route("/monthly")
def monthly_report():
    connection = mysql.connector.connect(**DB_CONFIG)

    monthly_data = calculate_monthly_consumption(connection)

    connection.close()

    monthly_records = monthly_data.to_dict("records")

    return render_template(
        "reports/monthly_report.html",
        monthly_records=monthly_records
    )

@reports_bp.route("/yearly")
def yearly_report():
    connection = mysql.connector.connect(**DB_CONFIG)

    monthly_data = calculate_monthly_consumption(connection)

    connection.close()

    monthly_data["year"] = monthly_data["reading_date"].dt.year

    yearly_data = (
        monthly_data
        .groupby(["meter_id", "year"])["consumption_kwh"]
        .sum()
        .reset_index()
    )

    yearly_records = yearly_data.to_dict("records")

    return render_template(
        "reports/yearly_report.html",
        yearly_records=yearly_records
    )
@reports_bp.route("/high-usage")
def high_usage_report():
    connection = mysql.connector.connect(**DB_CONFIG)

    monthly_data = calculate_monthly_consumption(connection)

    connection.close()

    high_usage_data = monthly_data[
        monthly_data["consumption_kwh"] > 500
    ]

    high_usage_records = high_usage_data.to_dict("records")

    return render_template(
        "reports/high_usage.html",
        high_usage_records=high_usage_records
    )
@reports_bp.route("/validation")
def validation_report():
    connection = mysql.connector.connect(**DB_CONFIG)

    validation_data = validate_readings(connection)

    connection.close()

    validation_records = validation_data.to_dict("records")

    return render_template(
        "reports/validation.html",
        validation_records=validation_records
    )
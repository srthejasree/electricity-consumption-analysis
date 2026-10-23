from flask import Flask, render_template
import mysql.connector
from config import DB_CONFIG
from analysis.consumption_analysis import calculate_monthly_consumption, find_high_usage, create_usage_chart
from routes.consumers import consumers_bp
from routes.meters import meters_bp
from routes.readings import readings_bp
from routes.reports import reports_bp
app = Flask(__name__)
app.register_blueprint(consumers_bp)
app.register_blueprint(meters_bp)
app.register_blueprint(readings_bp)
app.register_blueprint(reports_bp)
@app.route("/")
def dashboard():
    connection = mysql.connector.connect(**DB_CONFIG)

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM consumers")
    total_consumers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM meters")
    total_meters = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM meter_readings")
    total_readings = cursor.fetchone()[0]

    monthly_data = calculate_monthly_consumption(connection)
    total_consumption = monthly_data["consumption_kwh"].sum()
    create_usage_chart(monthly_data)


    monthly_records = monthly_data.to_dict("records")
    high_usage_data = find_high_usage(monthly_data, threshold=500)
    high_usage_records = high_usage_data.to_dict("records")

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        total_consumers=total_consumers,
        total_meters=total_meters,
        total_readings=total_readings,
        total_consumption=total_consumption,
        monthly_records=monthly_records,
        high_usage_records=high_usage_records
    )

if __name__ == "__main__":
    app.run(debug=True)
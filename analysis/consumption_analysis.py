import pandas as pd
import os
import matplotlib.pyplot as plt

def calculate_monthly_consumption(connection):
    query = """
        SELECT meter_id, reading_date, cumulative_kwh
        FROM meter_readings
        ORDER BY meter_id, reading_date
    """

    df = pd.read_sql(query, connection)

    df["reading_date"] = pd.to_datetime(df["reading_date"])

    df["consumption_kwh"] = (
        df.groupby("meter_id")["cumulative_kwh"].diff()
    )

    df = df.dropna(subset=["consumption_kwh"])

    df["month"] = df["reading_date"].dt.strftime("%B %Y")

    return df
def find_high_usage(df, threshold=500):
    high_usage = df[df["consumption_kwh"] > threshold]
    return high_usage
def create_usage_chart(df):
    chart_dir = os.path.join("static", "charts")
    os.makedirs(chart_dir, exist_ok=True)

    chart_path = os.path.join(chart_dir, "usage_chart.png")

    plt.figure(figsize=(8, 4))

    for meter_id, meter_data in df.groupby("meter_id"):
        plt.plot(
            meter_data["month"],
            meter_data["consumption_kwh"],
            marker="o",
            label=f"Meter {meter_id}"
        )

    plt.title("Electricity Consumption Trend")
    plt.xlabel("Month")
    plt.ylabel("Consumption (kWh)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(chart_path)
    plt.close()
import pandas as pd

def validate_readings(connection):
    query = """
        SELECT meter_id, reading_date, cumulative_kwh
        FROM meter_readings
        ORDER BY meter_id, reading_date
    """

    df = pd.read_sql(query, connection)

    df["reading_date"] = pd.to_datetime(df["reading_date"])

    df["previous_reading"] = (
        df.groupby("meter_id")["cumulative_kwh"].shift(1)
    )

    df["status"] = "Valid"

    df.loc[
        df["cumulative_kwh"] < df["previous_reading"],
        "status"
    ] = "Possible Reset/Rollover"

    return df
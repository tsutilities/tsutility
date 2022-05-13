""" Forecasting Utilities """

# https://machinelearningmastery.com/basic-feature-engineering-time-series-dataa-python/
import pandas as pd  # type: ignore


def get_time_features(data, time_col, date_dim="day"):
    """Add date related features for Time Series"""

    if date_dim == "day":
        data.loc[:, time_col] = pd.to_datetime(data[time_col])
        data.loc[:, "year"] = data[time_col].dt.year
        data.loc[:, "month"] = data[time_col].dt.month
        data.loc[:, "day_of_month"] = data[time_col].dt.day
        data.loc[:, "day_of_week"] = data[time_col].dt.dayofweek
        data.loc[:, "week_of_year"] = data[time_col].dt.isocalendar().week
        data.loc[:, "day_of_year"] = data[time_col].dt.dayofyear
        data.loc[:, "quarter"] = data[time_col].dt.quarter
        data.loc[:, "weekend"] = data["day_of_week"] > 4
    if date_dim == "week":
        data.loc[:, time_col] = pd.to_datetime(data[time_col])
        data.loc[:, "year"] = data[time_col].dt.year
        data.loc[:, "month"] = data[time_col].dt.month
        data.loc[:, "week_of_year"] = data[time_col].dt.isocalendar().week
        data.loc[:, "quarter"] = data[time_col].dt.quarter
    return data

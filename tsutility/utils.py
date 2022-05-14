""" Forecasting Utilities """

# https://machinelearningmastery.com/basic-feature-engineering-time-series-dataa-python/
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


def _week_of_month(data: pd.DataFrame, time_col: str) -> int:
    """Get Week of the month"""
    return (data[time_col].dt.day / 7).apply(np.ceil).astype(int)


def _weekend(data: pd.DataFrame, day_col: str) -> int:
    """weekend - True/False"""
    return (data[day_col] > 4).astype(int)


def _is_month_start(data: pd.DataFrame, day_col: str) -> int:
    """is month start --> first 4 days of month"""
    return data[day_col].isin([1, 2, 3, 4]).astype(int)


def _is_month_end(data: pd.DataFrame, day_col: str) -> int:
    """Is month end --> last 4 days of month"""
    return data[day_col].isin([28, 29, 30, 31]).astype(int)


def _is_quarter_start(data: pd.DataFrame, month_col: str, week_col: str) -> int:
    """is quarter start --> first week of quarter"""
    return (data[month_col].isin([1, 4, 7, 10]) & data[week_col].isin([1])).astype(int)


def _is_quarter_end(data: pd.DataFrame, month_col: str, week_col: str) -> int:
    """is quarter end --> last week of quarter"""
    return (data[month_col].isin([3, 6, 9, 12]) & data[week_col].isin([4, 5])).astype(int)


def _is_year_start(data: pd.DataFrame, week_col: str) -> int:
    """is year start --> first two weeks of year"""
    return data[week_col].isin([1, 2]).astype(int)


def _is_year_end(data: pd.DataFrame, week_col: str) -> int:
    """is year end --> last two weeks of year"""
    return data[week_col].isin([51, 52]).astype(int)


def get_time_features(data: pd.DataFrame, time_col: str, date_dim: str="day") -> pd.DataFrame:
    """Add date related features for Time Series"""

    if date_dim == "day":
        data.loc[:, time_col] = pd.to_datetime(data[time_col])

        data.loc[:, "month"] = data[time_col].dt.month
        data.loc[:, "quarter"] = data[time_col].dt.quarter
        data.loc[:, "year"] = data[time_col].dt.year

        data.loc[:, "day_of_week"] = data[time_col].dt.dayofweek
        data.loc[:, "day_of_month"] = data[time_col].dt.day
        data.loc[:, "day_of_year"] = data[time_col].dt.dayofyear

        data.loc[:, "week_of_month"] = _week_of_month(data, time_col)
        data.loc[:, "week_of_year"] = data[time_col].dt.isocalendar().week
        data.loc[:, "weekend"] = _weekend(data, day_col="day_of_week")

        data.loc[:, "is_month_start"] = _is_month_start(data, day_col="day_of_month")
        data.loc[:, "is_month_end"] = _is_month_end(data, day_col="day_of_month")
        data.loc[:, "is_quarter_start"] = _is_quarter_start(data, month_col="month", week_col="week_of_month")
        data.loc[:, "is_quarter_end"] = _is_quarter_end(data, month_col="month", week_col="week_of_month")
        data.loc[:, "is_year_start"] = _is_year_start(data, week_col="week_of_year")
        data.loc[:, "is_year_end"] = _is_year_end(data, week_col="week_of_year")

    if date_dim == "week":
        data.loc[:, time_col] = pd.to_datetime(data[time_col])

        data.loc[:, "month"] = data[time_col].dt.month
        data.loc[:, "quarter"] = data[time_col].dt.quarter
        data.loc[:, "year"] = data[time_col].dt.year

        data.loc[:, "week_of_month"] = data[time_col].dt.day // 7 + 1
        data.loc[:, "week_of_year"] = data[time_col].dt.isocalendar().week

    return data

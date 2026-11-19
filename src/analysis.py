# Import numpy for numerical and scientific calculations.
import numpy as np

# Import pandas for grouping and statistical analysis.
import pandas as pd


def calculate_annual_temperatures(df):
    """
    Calculate mean temperature for each year.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned daily weather observations.

    Returns
    -------
    pandas.DataFrame
        Annual mean temperatures.
    """

    # Group observations by year and calculate the mean.
    annual = df.groupby("year")["mean_temp"].mean()

    # Convert the Series into a DataFrame.
    annual = annual.reset_index()

    # Rename the temperature column.
    annual = annual.rename(columns={
        "mean_temp": "annual_mean"
    })

    return annual


def calculate_monthly_temperatures(df):
    """
    Calculate average temperature for each calendar month.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned daily weather observations.

    Returns
    -------
    pandas.DataFrame
        Mean temperatures for January through December.
    """

    # Group all observations by month.
    monthly = df.groupby("month")["mean_temp"].mean()

    # Convert the result into a DataFrame.
    monthly = monthly.reset_index()

    return monthly


def calculate_hot_days(df):
    """
    Count days with maximum temperature >= 30°C each year.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned daily weather observations.

    Returns
    -------
    pandas.DataFrame
        Annual counts of hot days.
    """

    # Copy the data to avoid modifying the original.
    df = df.copy()

    # Mark days with a maximum temperature of at least 30°C.
    df["hot_day"] = df["max_temp"] >= 30

    # Sum True values to count hot days for each year.
    hot_days = df.groupby("year")["hot_day"].sum()

    # Convert the result into a DataFrame.
    hot_days = hot_days.reset_index()

    # Rename the count column.
    hot_days = hot_days.rename(columns={
        "hot_day": "hot_days"
    })

    return hot_days


def calculate_temperature_trend(annual):
    """
    Calculate the linear temperature trend in °C per decade.

    Parameters
    ----------
    annual : pandas.DataFrame
        Annual mean temperatures.

    Returns
    -------
    tuple
        Temperature trend per decade and fitted values.
    """

    # Extract the years as a NumPy array.
    years = annual["year"].to_numpy()

    # Extract annual temperatures as a NumPy array.
    temperatures = annual["annual_mean"].to_numpy()

    # Ensure there are at least two observations.
    if len(years) < 2:
        raise ValueError("At least two years are required.")

    # Fit a first-degree polynomial (straight line).
    slope, intercept = np.polyfit(
        years,
        temperatures,
        1
    )

    # Convert the annual temperature slope to a decade.
    trend_per_decade = slope * 10

    # Calculate predicted temperatures along the fitted line.
    fitted_values = slope * years + intercept

    return trend_per_decade, fitted_values


def calculate_summary_statistics(annual, hot_days):
    """
    Calculate descriptive statistics for the weather dataset.

    Parameters
    ----------
    annual : pandas.DataFrame
        Annual mean temperatures.
    hot_days : pandas.DataFrame
        Annual hot-day counts.

    Returns
    -------
    dict
        Summary statistics for the analysis.
    """

    # Identify the warmest year.
    warmest = annual.loc[
        annual["annual_mean"].idxmax()
    ]

    # Identify the coldest year.
    coldest = annual.loc[
        annual["annual_mean"].idxmin()
    ]

    # Identify the year with the most hot days.
    most_hot_days = hot_days.loc[
        hot_days["hot_days"].idxmax()
    ]

    # Store the results in a dictionary.
    statistics = {
        "average_annual_temp": annual["annual_mean"].mean(),
        "standard_deviation": annual["annual_mean"].std(),
        "warmest_year": int(warmest["year"]),
        "warmest_temperature": float(warmest["annual_mean"]),
        "coldest_year": int(coldest["year"]),
        "coldest_temperature": float(coldest["annual_mean"]),
        "most_hot_days_year": int(most_hot_days["year"]),
        "most_hot_days_count": int(most_hot_days["hot_days"])
    }

    return statistics


def compare_decades(annual):
    """
    Compare average temperatures in two ten-year periods.

    Parameters
    ----------
    annual : pandas.DataFrame
        Annual mean temperatures.

    Returns
    -------
    dict
        Early and recent decade averages and their difference.
    """

    # Select the earlier period, 1995 through 2004.
    early = annual[
        annual["year"].between(1995, 2004)
    ]["annual_mean"]

    # Select the recent period, 2016 through 2025.
    recent = annual[
        annual["year"].between(2016, 2025)
    ]["annual_mean"]

    # Ensure both periods contain all ten annual values.
    if len(early) != 10 or len(recent) != 10:
        raise ValueError("Both periods must contain 10 years.")

    # Calculate average temperatures for each period.
    early_mean = early.mean()
    recent_mean = recent.mean()

    # Calculate the difference between the two periods.
    difference = recent_mean - early_mean

    return {
        "1995_2004": early_mean,
        "2016_2025": recent_mean,
        "difference": difference
    }
# Import pandas for data cleaning and manipulation.
import pandas as pd


def clean_weather_data(df):
    """
    Clean and prepare historical weather observations.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw weather observations.

    Returns
    -------
    pandas.DataFrame
        Cleaned weather data with year and month columns.
    """

    # Copy the data to preserve the original DataFrame.
    df = df.copy()

    # Rename the API columns to simpler names.
    df = df.rename(columns={
        "time": "date",
        "temperature_2m_mean": "mean_temp",
        "temperature_2m_max": "max_temp"
    })

    # Check whether the required columns exist.
    required_columns = ["date", "mean_temp", "max_temp"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")

    # Convert the date column to datetime format.
    # Invalid dates will become missing values (NaT).
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    # Convert temperatures into numeric values.
    # Invalid numbers will become NaN.
    df["mean_temp"] = pd.to_numeric(
        df["mean_temp"],
        errors="coerce"
    )

    df["max_temp"] = pd.to_numeric(
        df["max_temp"],
        errors="coerce"
    )

    # Display the number of missing values.
    print("\nMissing values before cleaning:")
    print(df[required_columns].isnull().sum())

    # Remove duplicate dates.
    df = df.drop_duplicates(subset=["date"])

    # Remove rows containing missing required values.
    df = df.dropna(subset=required_columns)

    # Sort observations chronologically.
    df = df.sort_values("date")

    # Create a year column from the date.
    df["year"] = df["date"].dt.year

    # Create a month column from the date.
    df["month"] = df["date"].dt.month

    # Reset the row index after cleaning.
    df = df.reset_index(drop=True)

    # Display information about the cleaned data.
    print("\nCleaned dataset:")
    print(df.head())

    print(f"\nTotal valid observations: {len(df)}")

    # Return the cleaned DataFrame.
    return df


def check_data_completeness(df):
    """
    Check how many daily observations are available per year.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned weather observations.

    Returns
    -------
    pandas.DataFrame
        Annual counts, expected days and completeness rates.
    """

    # Count the number of valid daily observations per year.
    completeness = df.groupby("year").size().reset_index(
        name="observed_days"
    )

    # Determine whether each year is a leap year.
    years = pd.to_datetime(
        completeness["year"].astype(str) + "-01-01"
    )

    # Leap years contain 366 days; others contain 365.
    completeness["expected_days"] = [
        366 if date.is_leap_year else 365
        for date in years
    ]

    # Calculate the percentage of available observations.
    completeness["completeness_pct"] = (
        completeness["observed_days"]
        / completeness["expected_days"]
        * 100
    )

    # Display the result.
    print("\nData completeness by year:")
    print(completeness)

    return completeness
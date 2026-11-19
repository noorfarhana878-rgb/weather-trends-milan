# Import requests to communicate with the weather API.
import requests

# Import pandas to create and read data tables.
import pandas as pd

# Import Path to manage folders and file paths.
from pathlib import Path


# Define the API URL for historical weather data.
API_URL = "https://archive-api.open-meteo.com/v1/archive"

# Set Milan's geographic coordinates.
LATITUDE = 45.4642
LONGITUDE = 9.1900

# Define the historical period for analysis.
START_DATE = "1995-01-01"
END_DATE = "2025-12-31"

# Define the folder for storing weather data.
DATA_FOLDER = Path("data")

# Create the data folder if it does not exist.
DATA_FOLDER.mkdir(parents=True, exist_ok=True)


def download_weather_data():
    """
    Download historical daily weather data for Milan.

    Returns
    -------
    pandas.DataFrame
        Daily dates, mean temperatures and maximum temperatures.
    """

    # Define the parameters to send to Open-Meteo.
    parameters = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": [
            "temperature_2m_mean",
            "temperature_2m_max"
        ],
        "timezone": "Europe/Rome"
    }

    # Send the HTTP request to the API.
    response = requests.get(
        API_URL,
        params=parameters,
        timeout=120
    )

    # Check whether the request was successful.
    response.raise_for_status()

    # Convert the response from JSON to a dictionary.
    weather_json = response.json()

    # Verify that daily weather data is present.
    required_columns = {
        "time",
        "temperature_2m_mean",
        "temperature_2m_max"
    }

    if "daily" not in weather_json:
        raise ValueError("The API returned no daily data.")

    # Convert the JSON daily data into a DataFrame.
    df = pd.DataFrame(weather_json["daily"])

    # Check that all required columns exist.
    if not required_columns.issubset(df.columns):
        raise ValueError("Missing required weather columns.")

    # Save the original data as a CSV file.
    file_path = DATA_FOLDER / "milan_weather.csv"
    df.to_csv(file_path, index=False)

    print(f"Weather data saved to {file_path}")

    # Return the downloaded data.
    return df


def load_weather_data():
    """
    Load weather data from CSV or download it if unavailable.

    Returns
    -------
    pandas.DataFrame
        Historical daily weather observations.
    """

    # Define the location of the saved CSV file.
    file_path = DATA_FOLDER / "milan_weather.csv"

    # Check whether the file already exists.
    if file_path.exists():

        # Load the existing CSV file.
        print("Loading weather data from CSV...")
        df = pd.read_csv(file_path)

    else:

        # Download the data if no CSV file exists.
        print("Downloading weather data from Open-Meteo...")
        df = download_weather_data()

    # Return the DataFrame.
    return df
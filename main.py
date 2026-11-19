# Import Path for saving results.
from pathlib import Path

# Import functions from our data loader module.
from src.data_loader import load_weather_data

# Import functions from our data processing module.
from src.data_processing import (
    clean_weather_data,
    check_data_completeness
)

# Import functions from our analysis module.
from src.analysis import (
    calculate_annual_temperatures,
    calculate_monthly_temperatures,
    calculate_hot_days,
    calculate_temperature_trend,
    calculate_summary_statistics,
    compare_decades
)

# Import functions from our visualization module.
from src.visualization import (
    plot_annual_temperature,
    plot_monthly_temperature,
    plot_temperature_heatmap,
    plot_hot_days
)


def main():
    """Execute the complete Milan weather analysis."""

    # Step 1: Load the original weather dataset.
    print("Step 1: Loading weather data...")
    raw_data = load_weather_data()

    # Step 2: Clean and prepare the dataset.
    print("\nStep 2: Cleaning weather data...")
    weather = clean_weather_data(raw_data)

    # Step 3: Check the number of observations per year.
    print("\nStep 3: Checking data completeness...")
    completeness = check_data_completeness(weather)

    # Stop if any year has less than 95% coverage.
    incomplete = completeness[
        completeness["completeness_pct"] < 95
    ]

    if not incomplete.empty:
        raise ValueError(
            "Some years have less than 95% data coverage."
        )

    # Step 4: Calculate annual temperatures.
    print("\nStep 4: Calculating annual temperatures...")
    annual = calculate_annual_temperatures(weather)

    # Step 5: Calculate monthly temperatures.
    print("\nStep 5: Calculating monthly temperatures...")
    monthly = calculate_monthly_temperatures(weather)

    # Step 6: Calculate the number of hot days.
    print("\nStep 6: Counting hot days...")
    hot_days = calculate_hot_days(weather)

    # Step 7: Calculate the linear temperature trend.
    print("\nStep 7: Calculating temperature trend...")
    trend, fitted_values = calculate_temperature_trend(
        annual
    )

    # Step 8: Calculate descriptive statistics.
    statistics = calculate_summary_statistics(
        annual,
        hot_days
    )

    # Step 9: Compare two ten-year periods.
    decade_comparison = compare_decades(annual)

    # Step 10: Display the results.
    print("\n--- MILAN WEATHER RESULTS ---")

    for name, value in statistics.items():
        print(f"{name}: {value}")

    print(f"\nTemperature trend: {trend:+.2f} °C/decade")

    print("\nDecade comparison:")
    for name, value in decade_comparison.items():
        print(f"{name}: {value:.2f} °C")

    # Step 11: Generate the four graphs.
    print("\nGenerating visualizations...")

    plot_annual_temperature(annual, fitted_values)
    plot_monthly_temperature(monthly)
    plot_temperature_heatmap(weather)
    plot_hot_days(hot_days)

    # Step 12: Save cleaned data and statistics.
    output_folder = Path("outputs")
    output_folder.mkdir(exist_ok=True)

    weather.to_csv(
        output_folder / "cleaned_weather.csv",
        index=False
    )

    annual.to_csv(
        output_folder / "annual_statistics.csv",
        index=False
    )

    monthly.to_csv(
        output_folder / "monthly_statistics.csv",
        index=False
    )

    hot_days.to_csv(
        output_folder / "hot_days_statistics.csv",
        index=False
    )

    # Display the completion message.
    print("\nProject analysis completed successfully!")


# Run main() only when this script is executed directly.
if __name__ == "__main__":
    main()
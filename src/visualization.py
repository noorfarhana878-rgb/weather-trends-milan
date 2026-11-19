# Import matplotlib for creating graphs.
import matplotlib.pyplot as plt

# Import Path to manage output folders.
from pathlib import Path


# Define the folder where graphs will be saved.
OUTPUT_FOLDER = Path("outputs")

# Create the output folder if necessary.
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


def plot_annual_temperature(annual, fitted_values):
    """
    Plot annual temperatures and the fitted trend line.

    Parameters
    ----------
    annual : pandas.DataFrame
        Annual mean temperatures.
    fitted_values : numpy.ndarray
        Values of the fitted linear trend.

    Returns
    -------
    None
    """

    # Create a figure with a suitable size.
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot the observed annual temperatures.
    ax.plot(
        annual["year"],
        annual["annual_mean"],
        marker="o",
        color="royalblue",
        label="Annual mean temperature"
    )

    # Plot the linear trend line.
    ax.plot(
        annual["year"],
        fitted_values,
        color="red",
        linestyle="--",
        label="Linear trend"
    )

    # Add a title and axis labels.
    ax.set_title("Annual Temperature in Milan (1995–2025)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature (°C)")

    # Add a legend and grid.
    ax.legend()
    ax.grid(alpha=0.3)

    # Adjust spacing.
    fig.tight_layout()

    # Save the figure as a PNG file.
    fig.savefig(
        OUTPUT_FOLDER / "annual_temperature.png",
        dpi=300
    )

    # Display the graph.
    plt.show()

    # Close the figure.
    plt.close(fig)


def plot_monthly_temperature(monthly):
    """
    Create a bar chart of average monthly temperatures.

    Parameters
    ----------
    monthly : pandas.DataFrame
        Monthly mean temperatures.

    Returns
    -------
    None
    """

    # Define the names of the months.
    month_names = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

    # Create a figure.
    fig, ax = plt.subplots(figsize=(10, 5))

    # Draw a bar for each month.
    ax.bar(
        monthly["month"],
        monthly["mean_temp"],
        color="orange"
    )

    # Display the month names on the x-axis.
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names)

    # Add labels and title.
    ax.set_title("Average Monthly Temperature in Milan")
    ax.set_xlabel("Month")
    ax.set_ylabel("Temperature (°C)")

    # Add horizontal grid lines.
    ax.grid(axis="y", alpha=0.3)

    # Adjust spacing and save.
    fig.tight_layout()
    fig.savefig(
        OUTPUT_FOLDER / "monthly_temperature.png",
        dpi=300
    )

    # Show and close the figure.
    plt.show()
    plt.close(fig)


def plot_temperature_heatmap(df):
    """
    Create a heatmap of average monthly temperatures by year.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned daily weather observations.

    Returns
    -------
    None
    """

    # Group the data by year and month.
    monthly_data = df.groupby(
        ["year", "month"]
    )["mean_temp"].mean()

    # Reshape the grouped data into a matrix.
    heatmap_data = monthly_data.unstack()

    # Ensure all twelve months appear in the matrix.
    heatmap_data = heatmap_data.reindex(
        columns=range(1, 13)
    )

    # Create a figure and axes.
    fig, ax = plt.subplots(figsize=(11, 8))

    # Display the matrix as a color-coded image.
    image = ax.imshow(
        heatmap_data,
        aspect="auto",
        cmap="coolwarm"
    )

    # Add a color bar showing the temperature scale.
    fig.colorbar(
        image,
        ax=ax,
        label="Temperature (°C)"
    )

    # Set the month labels.
    ax.set_xticks(range(12))
    ax.set_xticklabels([
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ])

    # Set the year labels.
    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index)

    # Add labels and title.
    ax.set_xlabel("Month")
    ax.set_ylabel("Year")
    ax.set_title("Monthly Temperature Heatmap — Milan")

    # Adjust spacing and save.
    fig.tight_layout()
    fig.savefig(
        OUTPUT_FOLDER / "temperature_heatmap.png",
        dpi=300
    )

    # Show and close the figure.
    plt.show()
    plt.close(fig)


def plot_hot_days(hot_days):
    """
    Plot the annual number of days reaching at least 30°C.

    Parameters
    ----------
    hot_days : pandas.DataFrame
        Annual counts of hot days.

    Returns
    -------
    None
    """

    # Create a figure.
    fig, ax = plt.subplots(figsize=(11, 5))

    # Plot the number of hot days in each year.
    ax.bar(
        hot_days["year"],
        hot_days["hot_days"],
        color="tomato"
    )

    # Add labels and title.
    ax.set_title("Hot Days in Milan (1995–2025)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of days ≥ 30°C")

    # Add a horizontal grid.
    ax.grid(axis="y", alpha=0.3)

    # Adjust spacing and save.
    fig.tight_layout()
    fig.savefig(
        OUTPUT_FOLDER / "hot_days.png",
        dpi=300
    )

    # Show and close the figure.
    plt.show()
    plt.close(fig)
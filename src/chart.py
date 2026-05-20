import sqlite3
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import src.logger

logger = logging.getLogger(__name__)


def generate_chart(database: str = "data/crime_data.db") -> None:
    """Generates a bar chart of crime counts by category and saves it as an SVG.

    Args:
        database (str): Path to the SQLite database file. Defaults to "data/crime_data.db".

    """
    logger.info("Connecting to database %s", database)
    with sqlite3.connect(database) as conn:
        df = pd.read_sql_query(
            "SELECT category, COUNT(*) as count FROM crime_data GROUP BY category ORDER BY count DESC",
            conn
        )

    logger.info("Loaded %s categories from database", len(df))

    with sqlite3.connect(database) as conn:
        date_range = pd.read_sql_query(
            "SELECT MIN(month) as start, MAX(month) as end FROM crime_data",
            conn
        )

    df["category"] = df["category"].str.replace("-", " ").str.capitalize()
    start = date_range.iloc[0]["start"]
    end = date_range.iloc[0]["end"]

    plt.style.use("afcharts.afcharts")

    fig, ax = plt.subplots()
    ax.bar(df["category"], df["count"])
    ax.set_title(f"Crimes by category — Oxford ({start} to {end})")
    ax.set_xlabel("Category")
    ax.set_ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_path = Path("docs/crime_by_category.svg")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)
    logger.info("Saved chart to %s", output_path)


if __name__ == "__main__":
    generate_chart()

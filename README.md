# Global Chess Trends Explorer Project
## Analysis of the top 100 players from every nation

## Overview

This project leverages FIDE (International Chess Federation) data to provide interactive insights into chess player performance and trends over the past 5 years. The application updates monthly to incorporate the latest data and remains a work in progress as additional features and final deployment, are being developed.  To see a preview [click here!](https://drive.google.com/file/d/1SLC-oTGvW6mfJFyd4r0HZIPEg85sQggm/view)

---

## Features

- Monthly updates to keep the insights current.
- Analysis of the top 100 chess players from each country.
- Interactive visualizations and data filtering options.
- Tools to compare countries, analyze trends, and view top players dynamically.

---

## 1. Data Collection

- Data sourced directly from the FIDE website, updated monthly.
- Downloaded data spanning 5 years, resulting in **60 text files** with comprehensive player details.

---

## 2. Data Cleaning and Preprocessing

- Extracted data for the **top 100 players per country**.
- Consolidated all extracted data into a single dataset for further analysis.
- Processed using Python and Jupyter Notebook.

---

## 3. Database Design and Setup

- Designed a **PostgreSQL** database with the following normalized structure:
  - **Players**: Stores static player information (e.g., name, birthdate).
  - **Countries**: Stores geographic data (e.g., continent, subregion).
  - **MonthlyUpdates**: Contains dynamic player data (e.g., rating, activity status) that changes monthly.

---

## 4. Data Aggregation and Analysis

- Utilized **DBeaver**, **Python**, and **SQLAlchemy** to analyze and extract insights.
- Key queries and functions include:
  - Median ratings, titled player counts, and Grandmasters per country.
  - Gender, age group, and rating distributions over time.
  - Player activity status percentages.
  - Participation trends by continent.

---

## 5. Streamlit Application Development

Learned Streamlit through a course from ALURA LATAM and developed a **6-page interactive web application**:

1. **Introduction**: Overview of the project.
2. **Outlook**: High-level data summary and key insights.
3. **Continent Analysis**: Regional performance and trends.
4. **Comparison Tool**: Compare two countries/regions across a selected period.
5. **Top 5 Chess Players**: Dynamic bar chart race showing top players over time.

---

## 6. Visualization and Interaction

- Built dynamic and interactive visualizations using **Plotly** and **Bar Chart Race**:
  - Rating trends, distributions, and player participation by gender and country.
  - Bar chart races for engaging visual storytelling.
- Integrated filter options to refine insights by:
  - Gender
  - Rating range
  - Country
  - Title
  - Activity status

---

## 7. Deployment (In Progress)

- Currently working on finalizing the deployment strategy to make the app accessible online.

---

## Future Work

- Finalize deployment to make the application publicly accessible.
- Explore additional features to enhance user interaction and insights.

---

This project combines data science, database management, and interactive web development to provide valuable insights into the chess world. Stay tuned for updates as new features are added!


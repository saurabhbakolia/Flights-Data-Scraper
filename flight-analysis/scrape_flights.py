from google_flight_analysis.scrape import Scrape
import pandas as pd

# Define the route and date range
origin = "CCU"  # Kolkata
destination = "MAA"  # Chennai
departure_date = "2024-11-01"  # Departure date
return_date = "2024-11-24"  # Return date

# Scraping flight data
result = Scrape(origin, destination, departure_date, return_date)

# Print the result object to understand its structure
print("Result object:", result)
print("Attributes of result object:", dir(result))

# Obtain data and print it
dataframe = result.data  # Outputs a Pandas DataFrame with flight prices/info

# Check if the dataframe is empty
if dataframe.empty:
    print("No flight data found. Please check the origin, destination, and dates.")
else:
    print("DataFrame columns:", dataframe.columns)  # Print DataFrame columns
    print("First few rows of the DataFrame:")
    print(dataframe.head())  # Print the first few rows of the DataFrame

    # Optionally, save the data to a CSV file
    dataframe.to_csv("ccu_to_maa_flights.csv", index=False)
    print("Flight data saved to ccu_to_maa_flights.csv.")

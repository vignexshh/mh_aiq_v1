import sqlite3
import pandas as pd

# Load the CSV file
df = pd.read_csv('/home/vignesh/Documents/AIQ_R1_Medical_Hunt/Data Cleaning/Python Data Cleaning/aiq_r1_app/data_cleaning_p1 - Copy of sorted_till_categories.csv')

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('neet_candidates.db')

# Write the dataframe to a new SQLite table
df.to_sql('neet_candidates', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

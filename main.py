import pandas as pd
import csv
from datetime import datetime, timedelta

# Load the Excel file into a DataFrame, specifying columns A to G
# Replace with the actual file
file_path = '2018_Posts.xlsx'
columns_to_read = ['id', 'Autor', 'Red',
                   'Date', 'Reactions', 'Comments', 'Shares']
# Read the file
df = pd.read_excel(file_path, sheet_name='Posts', usecols=columns_to_read)
# Convert the 'Date' column to datetime.date format
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.date

# These are the dates from the polls:
date_strings = [
    "30/10/17", "15/12/17", "27/01/18", "27/02/18", "25/03/18", "28/04/18",
    "26/05/17", "23/06/18", "30/10/17", "01/04/18", "09/05/18", "16/05/18",
    "21/05/18", "29/05/18", "13/06/18", "21/06/18", "17/12/17", "25/01/18",
    "16/02/18", "23/03/18", "25/04/18", "02/06/18", "14/06/18", "28/09/17",
    "08/12/17", "02/03/18", "17/03/18", "29/04/18", "26/05/18", "07/10/17",
    "13/11/17", "29/01/18", "10/03/18", "12/03/18", "28/04/18", "25/05/18",
    "03/01/18", "26/01/18", "24/03/18", "25/03/18", "06/05/18", "08/06/18",
    "10/02/18", "05/03/18", "24/03/18", "01/05/18", "29/05/18", "15/06/18"
]

# these are the equivalent in text for the dates above.
text_values = [
    "Parametría", "Parametría", "Parametría", "Parametría", "Parametría", "Parametría",
    "Parametría", "Parametría", "Impacto", "Impacto", "Impacto", "Impacto",
    "Impacto", "Impacto", "Impacto", "Impacto", "Arias Consultores", "Arias Consultores",
    "Arias Consultores", "Arias Consultores", "Arias Consultores", "Arias Consultores",
    "Arias Consultores", "Economista", "Economista", "Economista", "Economista",
    "Economista", "Economista", "Financiero", "Financiero", "Financiero", "Financiero",
    "Financiero", "Financiero", "Financiero", "Suasor", "Suasor", "Suasor", "Suasor",
    "Suasor", "Suasor", "Conteo", "Conteo", "Conteo", "Conteo", "Conteo", "Conteo"
]

# Create a relationship between dates and the corresponding poll.
polls_to_date = {date_strings[i]: text_values[i]
                 for i in range(len(date_strings))}

# Convert date strings to Python date objects
date_objects = [datetime.strptime(date, "%d/%m/%y").date()
                for date in date_strings]

# how many days before the poll:
days_before = [1, 2, 3, 4, 5, 6, 7, 14, 21, 28]

# candidates:
candidates = {
    1: "Andrés Manuel López Obrador",
    2: "Ricardo Anaya Cortés",
    3: "José Antonio Meade Kuribreña"
}

# for each candidate:
for candidate_id, candidate_name in candidates.items():
    # for each how many days before the poll:
    for day in days_before:
        # the name of the target file is candidate_id + days_before
        file_name = str(candidate_id) + "_" + str(day) + ".csv"
        r_columns = ['candidate', 'window', 'institute', 'ref_date',
                     'fb_posts', 'fb_reactions', 'fb_comments', 'fb_shares',
                     'tw_posts', 'tw_reactions', 'tw_comments', 'tw_shares',
                     'ig_posts', 'ig_reactions', 'ig_comments', 'ig_shares']
        csv_rows = []
        csv_rows.append(r_columns)
        for date in date_objects:
            # Calculate the start date based on the arbitrary_date and delta
            start_date = date - timedelta(days=day)
            # Filter the DataFrame based on the specified criteria
            filtered_df = df[(df['id'] == candidate_id) & (
                df['Date'] >= start_date) & (df['Date'] <= date)]
            candiate = candidates.get(candidate_id)
            window = day
            institute = polls_to_date.get(date.strftime("%d/%m/%y"))
            ref_date = date.strftime("%d/%m/%y")
            # how many rows are with df["Red"] === "facebook"
            fb_posts = len(filtered_df[filtered_df['Red'] == 'facebook'])
            # how many reactions are with df["Red"] === "facebook"
            fb_reactions = filtered_df[filtered_df['Red']
                                       == 'facebook']['Reactions'].sum()
            # how many comments are with df["Red"] === "facebook"
            fb_comments = filtered_df[filtered_df['Red']
                                      == 'facebook']['Comments'].sum()
            # how many shares are with df["Red"] === "facebook"
            fb_shares = filtered_df[filtered_df['Red']
                                    == 'facebook']['Shares'].sum()
            # how many rows are with df["Red"] === "twitter"
            tw_posts = len(filtered_df[filtered_df['Red'] == 'twitter'])
            # how many reactions are with df["Red"] === "twitter"
            tw_reactions = filtered_df[filtered_df['Red']
                                       == 'twitter']['Reactions'].sum()
            # how many comments are with df["Red"] === "twitter"
            tw_comments = filtered_df[filtered_df['Red']
                                      == 'twitter']['Comments'].sum()
            # how many shares are with df["Red"] === "twitter"
            tw_shares = filtered_df[filtered_df['Red']
                                    == 'twitter']['Shares'].sum()
            # how many rows are with df["Red"] === "instagram"
            ig_posts = len(filtered_df[filtered_df['Red'] == 'instagram'])
            # how many reactions are with df["Red"] === "instagram"
            ig_reactions = filtered_df[filtered_df['Red']
                                       == 'instagram']['Reactions'].sum()
            # how many comments are with df["Red"] === "instagram"
            ig_comments = filtered_df[filtered_df['Red']
                                      == 'instagram']['Comments'].sum()
            # how many shares are with df["Red"] === "instagram"
            ig_shares = filtered_df[filtered_df['Red']
                                    == 'instagram']['Shares'].sum()
            # create a row with the data
            row = [candiate, window, institute, ref_date,
                   fb_posts, fb_reactions, fb_comments, fb_shares,
                   tw_posts, tw_reactions, tw_comments, tw_shares,
                   ig_posts, ig_reactions, ig_comments, ig_shares]
            csv_rows.append(row)
        with open(file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(csv_rows)

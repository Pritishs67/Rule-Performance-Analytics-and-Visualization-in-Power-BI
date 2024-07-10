## Rulebook.ipynb

# Rule Book input file is 5 Train_5_months_csv
import pandas as pd
import datetime
def RuleBook(inputfile):
    df=pd.read_csv(inputfile)
    for column in df.columns[4:]:
        if '1' in df[column].values  or 1 in df[column].values:
            df[column] = df[column].replace({'1': 'AM1',1:'AM1'})
        if '0' in df[column].values or 0 in df[column].values:
            df[column] = df[column].replace({'0': 'AM0',0:'AM0'})
    # Assuming you have a DataFrame named 'df' with datetime columns
    df['createdOn'] = pd.to_datetime(df['createdOn'], utc=True)  # Convert to UTC timezone
# Repeat the above line for other datetime columns in your DataFrame

    column_names = df.columns[4:]  # Specify the columns you want to consider

    data = []  # List to store data for the result DataFrame

    # Define the ID mapping for 'AM0' and 'AM1'
    id_mapping = {'AM0': 'AM0', 'AM1': 'AM1'}

    # Iterate over each column and assign rule numbers
    rule_number = 1
    for column in column_names:
        # Perform groupby and count occurrences
        occur = df[column].value_counts()
    
        # Get the minimum and maximum dates for AM0 and AM1
        zero_start_date = df.loc[df[column] == 'AM0', 'createdOn'].min()
        zero_last_date = df.loc[df[column] == 'AM0', 'createdOn'].max()
        one_start_date = df.loc[df[column] == 'AM1', 'createdOn'].min()
        one_last_date = df.loc[df[column] == 'AM1', 'createdOn'].max()

        # Convert 'Usage Date' to datetime format
        zero_last_date = pd.to_datetime(zero_last_date)
        one_last_date = pd.to_datetime(one_last_date)

        # Handle cases where there are no 'AM0' or 'AM1' values
        if pd.isnull(zero_start_date) or pd.isnull(zero_last_date):
            zero_start_date = pd.NaT
            zero_last_date = pd.NaT
        if pd.isnull(one_start_date) or pd.isnull(one_last_date):
            one_start_date = pd.NaT
            one_last_date = pd.NaT

        # Calculate the previous usage count based on zero occurrences on the last date
        zero_usage_on_last_date = df[(df[column] == 'AM0') & (df['createdOn'] == zero_last_date)].shape[0]
        one_usage_on_last_date = df[(df[column] == 'AM1') & (df['createdOn'] == one_last_date)].shape[0]

        # Add data to the list
        data.append({
            'Rule Name': column,
            'Created Date': zero_start_date,
            'Usage Date': zero_last_date,
            'ID': id_mapping.get('AM0'),
            'Usage': occur.get('AM0', 0),
            'Monitoring Flag': 'YES' if occur.get('AM0', 0) > 10 else 'NO', # changed
            'Flag': 'Old' if (zero_start_date != pd.Timestamp.now(tz='UTC').normalize()) else 'New',
            'Previous Usage': occur.get('AM0', 0) - zero_usage_on_last_date,
            'Rule Number': rule_number
        })
        data.append({
            'Rule Name': column,
            'Created Date': one_start_date,
            'Usage Date': one_last_date,
            'ID': id_mapping.get('AM1'),
            'Usage': occur.get('AM1', 0),
            'Monitoring Flag': 'YES' if occur.get('AM0', 0) > 10 else 'NO', # changed
            'Flag': 'Old' if (one_start_date != pd.Timestamp.now(tz='UTC').normalize()) else 'New',
            'Previous Usage': occur.get('AM1', 0) - one_usage_on_last_date,
            'Rule Number': rule_number
        })

        rule_number += 1

    # Create the result DataFrame
    result = pd.DataFrame(data)

    # Optional: Convert the dates to datetime format if they are not already
    result['Created Date'] = pd.to_datetime(result['Created Date'])
    result['Usage Date'] = pd.to_datetime(result['Usage Date'])

    # Save the result to a CSV file
    result.to_csv('Rulebook.csv', index=False)
# RuleBook("Train_5_months.csv")

import pandas as pd

def algo_map_columns_to_rules(file_path, output_file_path):
    # Read the CSV file into a DataFrame
    dataframe = pd.read_csv(file_path)

    # Iterate over each column and map '1' and '0' values
    for column in dataframe.columns[4:]:
        # Check if the column contains '1' or '0'
        if '1' in dataframe[column].values or 1 in dataframe[column].values :
            dataframe[column] = dataframe[column].replace({'1': 'AM1',1:'AM1'})
        if '0' in dataframe[column].values or 0 in dataframe[column].values:
            dataframe[column] = dataframe[column].replace({'0': 'AM0', 0: 'AM0'})

    # Save the transformed DataFrame to a new CSV file
    dataframe.to_csv(output_file_path, index=False)


def algo_actual(map1):

    df = pd.read_csv(map1)
    df['createdOn'] = pd.to_datetime(df['createdOn']).dt.date

# Specify the rule columns
    rule_columns = df.columns[4:]
    print(rule_columns)

    # Create an empty list to store the statistics data
    statistics_data = []

    # Define the ID mapping for 'AM0' and 'AM1'
    id_mapping = {0: 'AM0', 1: 'AM1'}

    rule_numbers = {}  # Dictionary to store the rule number for each column

    for column in rule_columns:
        try:
            if column in rule_numbers:
                # Use the existing rule number if the column name is already encountered
                rule_number = rule_numbers[column]
            else:
                # Assign a new rule number for the column if it's encountered for the first time
                rule_number = len(rule_numbers) + 1
                rule_numbers[column] = rule_number

            # Group by 'createdOn' column and count zero and one occurrences
            column_counts = df.groupby(['createdOn', column])[column].count().unstack(fill_value=0)

            # Calculate percentages for the column
            column_counts['Percentage_0'] = (column_counts['AM0'] / (column_counts['AM0'] + column_counts['AM1'])) * 100
            column_counts['Percentage_1'] = (column_counts['AM1'] / (column_counts['AM0'] + column_counts['AM1'])) * 100

            # Get the dates and corresponding mean percentages for 'AM0' and 'AM1'
            dates = column_counts.index
            actual_percentage_0 = column_counts['Percentage_0']
            actual_percentage_1 = column_counts['Percentage_1']

            # Append the statistics data to the list for each date
            for date in dates:
                statistics_data.append({
                    'Rule Number': rule_number,
                    'Rule Name': column,
                    'ID': id_mapping.get(0),
                    'Date': date,
                    'Actual': actual_percentage_0.loc[date],
                    'Counts': column_counts['AM0'].loc[date]
                })
                statistics_data.append({
                    'Rule Number': rule_number,
                    'Rule Name': column,
                    'ID': id_mapping.get(1),
                    'Date': date,
                    'Actual': actual_percentage_1.loc[date],
                    'Counts': column_counts['AM1'].loc[date]
                })

        except KeyError:
            print(f"Column '{column}' not found in the DataFrame.")
        except ZeroDivisionError:
            print(f"Unable to calculate percentages for column '{column}'. Division by zero error.")

    # Create the final statistics DataFrame using the list of dictionaries
    statistics_df = pd.DataFrame(statistics_data)

    # Save the DataFrame to a CSV file
    statistics_df.to_csv('Actual.csv', index=False)

    print("Statistics saved to CSV file!")



# Read the CSV files into DataFrames
def algo_deviation(df_rule_file,df_actual_file):
    # df_rules = pd.read_csv('Unimodel Library.csv')
    # df_actual = pd.read_csv('Actual.csv')
    df_rules = pd.read_csv(df_rule_file)
    df_actual = pd.read_csv(df_actual_file)

    df_merged = df_actual.merge(df_rules, on=['Rule Name', 'ID'], suffixes=('_actual', '_rule'))

# Function to calculate the deviation based on the conditions
    def calculate_deviation(row):
        if row['Counts'] < 10:
            return 0.0   # changed  
        return (row['Actual'] - row['Mean Percentage']) / row['Standard Deviation']

    # Apply the deviation calculation function to each row
    df_merged['Deviation'] = df_merged.apply(calculate_deviation, axis=1)

    # Calculate the absolute z-score
    df_merged['Absolute Z-Score'] = df_merged['Deviation'].abs()#changed

    # Filter the columns to display in the final output
    df_output = df_merged[['Rule Number_rule', 'Rule Name', 'ID', 'Date', 'Counts', 'Actual', 'Minimum Percentage', 'Maximum Percentage', 'Mean Percentage', 'Standard Deviation', 'Deviation', 'Absolute Z-Score']]

    # Rename the 'Rule Number_rule' column to 'Rule Number'
    df_output.rename(columns={'Rule Number_rule': 'Rule Number'}, inplace=True)

    # Convert 'Date' column to pandas datetime format
    df_output['Date'] = pd.to_datetime(df_output['Date'])#changed

    # Group by 'Rule Name' and 'Date' and sum the z-scores for AM0 and AM1
    z_score_sum = df_output.groupby(['Rule Name', 'Date'])['Absolute Z-Score'].sum().reset_index()#changed
    z_score_sum.rename(columns={'Absolute Z-Score': 'Z-Score Sum'}, inplace=True)

    # Merge the z-score sum back into the output DataFrame
    df_output = df_output.merge(z_score_sum, on=['Rule Name', 'Date'], how='left')

    # Get the minimum date
    min_date = df_output['Date'].min()

    # Function to calculate the week, day number, and day name
    def get_week_day_name(date):
        days_since_min = (date - min_date).days
        week_number = days_since_min // 7 + 1
        day_number = days_since_min % 7 + 1
        day_name = date.strftime('%A')
        return week_number, day_number, day_name

    # Apply the function to create the 'Week', 'Day', and 'Day Name' columns
    df_output['Week'], df_output['Day'], df_output['Day Name'] = zip(*df_output['Date'].map(get_week_day_name))

    # Display the resulting DataFrame
    print(df_output)
    # Store the output DataFrame to a CSV file
    df_output.to_csv('DEVIATION_FINAL1_1.csv', index=False)

input_file='map1.csv'

algo_actual(input_file)
# algo_deviation_rule_input = 'Unimodel Library.csv'
# algo_deviation_actual_input = 'Actual.csv'
# algo_deviation(algo_deviation_rule_input, algo_deviation_actual_input)

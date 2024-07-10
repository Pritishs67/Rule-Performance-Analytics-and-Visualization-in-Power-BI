import pandas as pd

def UniModel(five_month_test_csv):
    df = pd.read_csv(five_month_test_csv)

# Get the column names from the DataFrame
    column_names = df.columns.tolist()

    # Create a dictionary to store the column mappings
    column_mapping = {}

    # Assign rules to the remaining columns starting from rule 1
    for idx, column_name in enumerate(column_names[4:], start=1):
        column_mapping[column_name] = f"{column_name} rule {idx}"

    # Rename the columns using the mapping
    df = df.rename(columns=column_mapping)



import pandas as pd

def map_columns_to_rules(file_path, output_file_path):
    # Read the CSV file into a DataFrame
    dataframe = pd.read_csv(file_path)

    # Iterate over each column and map '1' and '0' values
    for column in dataframe.columns[4:]:
        # Check if the column contains '1' or '0'
        if '1' in dataframe[column].values or 1 in dataframe[column].values :
            dataframe[column] = dataframe[column].replace({'1': 'AM1',1:'AM1'})
        if '0' in dataframe[column].values or 0 in dataframe[column].values:
            dataframe[column] = dataframe[column].replace({'0': 'AM0',0: 'AM0'})

    # Save the transformed DataFrame to a new CSV file
    dataframe.to_csv(output_file_path, index=False)



import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# function 2 of unimodel library
def Unimodel_file_create(map_file_input):
    df = pd.read_csv(map_file_input)
    df['createdOn'] = pd.to_datetime(df['createdOn']).dt.date

# Specify the rule columns
    rule_columns = df.columns[4:]

    # Create an empty DataFrame to store the statistics
    # statistics_df = pd.DataFrame(columns=['Rule Number', 'Rule Name', 'ID', 'Minimum Percentage', 'Maximum Percentage',
    #                                       'Mean Percentage', 'Standard Deviation'])
    statistics_df=[]

    # Define the ID mapping for 'AM0' and 'AM1'
    id_mapping = {0: 'AM0', 1: 'AM1'}

    rule_numbers = {}  # Dictionary to store the rule number for each column

    for column in rule_columns:
        # print(column)
        try:
            if column in rule_numbers:
                # Use the existing rule number if column name already encountered
                rule_number = rule_numbers[column]
                print(column)
            else:
                # Assign a new rule number for the column if it's encountered for the first time
                rule_number = len(rule_numbers) + 1
                rule_numbers[column] = rule_number

            # Group by 'createdOn' column and count zero and one occurrences
            column_counts = df.groupby('createdOn')[column].value_counts().unstack().fillna(0)

            # Calculate percentages for the column
            column_counts['Percentage_0'] = (column_counts['AM0'] / (column_counts['AM0'] + column_counts['AM1'])) * 100
            column_counts['Percentage_1'] = (column_counts['AM1'] / (column_counts['AM0'] + column_counts['AM1'])) * 100

            # Calculate minimum, maximum, mean, and standard deviation for the column
            min_percentage_0 = column_counts['Percentage_0'].min()
            max_percentage_0 = column_counts['Percentage_0'].max()
            mean_percentage_0 = column_counts['Percentage_0'].mean()
            std_percentage_0 = column_counts['Percentage_0'].std()

            min_percentage_1 = column_counts['Percentage_1'].min()
            max_percentage_1 = column_counts['Percentage_1'].max()
            mean_percentage_1 = column_counts['Percentage_1'].mean()
            std_percentage_1 = column_counts['Percentage_1'].std()

            # Append the statistics to the DataFrame
            # statistics_df = statistics_df.append({
            #     'Rule Number': rule_number,
            #     'Rule Name': column,
            #     'ID': id_mapping.get(0),
            #     'Minimum Percentage': min_percentage_0,
            #     'Maximum Percentage': max_percentage_0,
            #     'Mean Percentage': mean_percentage_0,
            #     'Standard Deviation': std_percentage_0
            # })
            # statistics_df = statistics_df.append({
            #     'Rule Number': rule_number,
            #     'Rule Name': column,
            #     'ID': id_mapping.get(1),
            #     'Minimum Percentage': min_percentage_1,
            #     'Maximum Percentage': max_percentage_1,
            #     'Mean Percentage': mean_percentage_1,
            #     'Standard Deviation': std_percentage_1
            # })
            statistics_df.append({
                'Rule Number': rule_number,
                'Rule Name': column,
                'ID': id_mapping.get(0),
                'Minimum Percentage': min_percentage_0,
                'Maximum Percentage': max_percentage_0,
                'Mean Percentage': mean_percentage_0,
                'Standard Deviation': std_percentage_0
            })
            statistics_df.append({
                'Rule Number': rule_number,
                'Rule Name': column,
                'ID': id_mapping.get(1),
                'Minimum Percentage': min_percentage_1,
                'Maximum Percentage': max_percentage_1,
                'Mean Percentage': mean_percentage_1,
                'Standard Deviation': std_percentage_1
            })

        except KeyError:
            print(f"Column '{column}' not found in the DataFrame.")
        except ZeroDivisionError:
            print(f"Unable to calculate percentages for column '{column}'. Division by zero error.")

    # Save the DataFrame to a CSV file
    statistics_df_final=pd.DataFrame(statistics_df)
    statistics_df_final.to_csv('Unimodel Library.csv', index=False)

    print("Statistics saved to CSV file!")

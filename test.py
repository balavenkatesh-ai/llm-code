import pandas as pd

def create_csv_with_title(filename, title):
    # Create a DataFrame for the first table
    data1 = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    }
    df1 = pd.DataFrame(data1)

    # Create a DataFrame for the second table
    data2 = {
        'Country': ['USA', 'Canada', 'UK'],
        'Language': ['English', 'French', 'English'],
        'Population': [328, 37, 66]
    }
    df2 = pd.DataFrame(data2)

    # Write the title and DataFrames to a CSV file
    with open(filename, 'w') as f:
        f.write(title + '\n\n')  # Write the title and leave one empty row
        
        # Write the first table
        for index, row in df1.iterrows():
            f.write(','.join(map(str, row.values)) + '\n')
        
        # Add an extra empty row between tables
        f.write('\n')
        
        # Write the second table
        for index, row in df2.iterrows():
            f.write(','.join(map(str, row.values)) + '\n')

def main():
    filename = 'example.csv'
    title = 'Table Title'

    # Create the CSV file with title and tables
    create_csv_with_title(filename, title)

if __name__ == "__main__":
    main()




# Determine the maximum number of columns
    max_columns = max(len(df1.columns), len(df2.columns))

    # Write the title and DataFrames to a CSV file
    with open(filename, 'w') as f:
        f.write(title + '\n\n')  # Write the title and leave one empty row
        
        # Write the first table
        for index, row in df1.iterrows():
            row_values = list(row.values) + [''] * (max_columns - len(df1.columns))
            f.write(','.join('"{0}"'.format(val) for val in row_values) + '\n')
        
        # Add an extra empty row between tables
        f.write('\n')
        
        # Write the second table
        for index, row in df2.iterrows():
            row_values = list(row.values) + [''] * (max_columns - len(df2.columns))
            f.write(','.join('"{0}"'.format(val) for val in row_values) + '\n')

    # Read the created CSV file back into a DataFrame
    df = pd.read_csv(filename, skiprows=2)  # Skip the title and empty row
    return df

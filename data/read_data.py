import pandas as pd

# Read the CSV file
df = pd.read_csv('data/companies.csv')

# Print the first 5 rows
print(df[['name', 'rating', 'review', 'company_type', 'Head_Quarters', 'Company_Age']].head())

# # Print all columns
# print(df.columns)

# # Print the shape of the dataframe
# print(df.shape)

# # Print the data types of the columns
# print(df.dtypes)

# # Print the null values
# print(df.isnull().sum())
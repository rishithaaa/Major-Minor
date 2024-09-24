import os
import io
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Set Conda environment path
conda_env_path = '/path/to/your/miniconda3/bin'
os.environ['PATH'] = f'{conda_env_path}/bin:{os.environ["PATH"]}'


# Install required packages
os.system('pip install pandas requests matplotlib seaborn')

# Reading data from the provided URL
data_url = "https://raw.githubusercontent.com/arora123/Data/master/emp-data.csv"
response = requests.get(data_url)

# Checking if the request was successful
if response.status_code == 200:
    # Importing the necessary libraries
    from io import StringIO

    # Reading the data
    data = pd.read_csv(io.StringIO(response.text))

    # Convert 'Salary' column to numeric, coerce errors to NaN
    data['Salary'] = pd.to_numeric(data['Salary'], errors='coerce')

    # Objectives
    # 1. How many Males/Females are there in the entire organization?
    gender_count = data['Gender'].value_counts()
    print("Gender Count in the Entire Organization:")
    print(gender_count)

    # 2. How many Males/Females are there in each department or for each location?
    gender_department_count = data.groupby(['Department', 'Gender']).size().unstack().fillna(0)
    print("\nGender Count in Each Department:")
    print(gender_department_count)

    # Check if 'Location' column exists before grouping
    if 'Location' in data.columns:
        gender_location_count = data.groupby(['Location', 'Gender']).size().unstack().fillna(0)
        print("\nGender Count in Each Location:")
        print(gender_location_count)

    # 3. For which department is the average Pay highest?
    # Handle NaN values by skipping them during the mean calculation
    highest_avg_pay_department = data.groupby('Department')['Salary'].mean().idxmax()
    print(f"\nDepartment with the Highest Average Pay: {highest_avg_pay_department}")

    # 4. For which location is the average Pay highest?
    # Check if 'Location' column exists before grouping
    if 'Location' in data.columns:
        highest_avg_pay_location = data.groupby('Location')['Salary'].mean(skipna=True).idxmax()
        print(f"\nLocation with the Highest Average Pay: {highest_avg_pay_location}")
    else:
        print("\n'Location' column not found in the dataset.")

    # 5. What percentage of employees received good & very good rating?
    # What about poor & very poor rating? and average rating?
    if 'Ratings' in data.columns:
        rating_counts = data['Ratings'].value_counts(normalize=True) * 100
        print("\nPercentage of Employees with Each Rating:")
        print(rating_counts)
    else:
        print("\n'Ratings' column not found in the dataset.")

    # 6. Compute gender pay gap for each department. Interpret
    gender_pay_gap_department = data.groupby(['Department', 'Gender'])['Salary'].mean().unstack()
    gender_pay_gap_department['Gender Pay Gap'] = (
        (gender_pay_gap_department['Female'] - gender_pay_gap_department['Male']) / gender_pay_gap_department['Male']
    ) * 100
    print("\nGender Pay Gap for Each Department:")
    print(gender_pay_gap_department[['Male', 'Female', 'Gender Pay Gap']])

    # 7. Compute gender pay gap for each location. Interpret
    if 'Location' in data.columns:
        gender_pay_gap_location = data.groupby(['Location', 'Gender'])['Salary'].mean().unstack()
        gender_pay_gap_location['Gender Pay Gap'] = (
            (gender_pay_gap_location['Female'] - gender_pay_gap_location['Male']) / gender_pay_gap_location['Male']
        ) * 100
        print("\nGender Pay Gap for Each Location:")
        print(gender_pay_gap_location[['Male', 'Female', 'Gender Pay Gap']])

    # Additional Exercises:
    # 1. Use visualization to understand & explore data
    sns.countplot(x='Gender', data=data)
    plt.title('Gender Distribution')
    plt.show()

    sns.scatterplot(x='Salary', y='Ratings', hue='Gender', data=data)
    plt.title('Salary vs Ratings by Gender')
    plt.show()

    # 2. Use statistical methods to explore the relationship/association between the variables
    # gender & location
    if 'Location' in data.columns:
        gender_location_association = pd.crosstab(data['Gender'], data['Location'])
        print("\nAssociation between Gender and Location:")
        print(gender_location_association)

    # gender & department
    gender_department_association = pd.crosstab(data['Gender'], data['Department'])
    print("\nAssociation between Gender and Department:")
    print(gender_department_association)

    # gender & rating
    if 'Ratings' in data.columns:
        gender_rating_association = pd.crosstab(data['Gender'], data['Ratings'])
        print("\nAssociation between Gender and Ratings:")
        print(gender_rating_association)

    # gender & salary
    gender_salary_association = data.groupby('Gender')['Salary'].describe()
    print("\nAssociation between Gender and Salary:")
    print(gender_salary_association)

    # location & salary
    if 'Location' in data.columns:
        location_salary_association = data.groupby('Location')['Salary'].describe()
        print("\nAssociation between Location and Salary:")
        print(location_salary_association)

    # department & salary
    department_salary_association = data.groupby('Department')['Salary'].describe()
    print("\nAssociation between Department and Salary:")
    print(department_salary_association)
else:
    print("Failed to retrieve data. Please check the data URL.")

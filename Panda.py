import numpy as np
import pandas as pd


def create_data():
    marks = np.array([78, 85, 62, 90, 74])
    names = ["Aman", "Riya", "Kunal", "Sneha", "Vikram"]

    data = {
        "Name": names,
        "Marks": marks
    }

    df = pd.DataFrame(data)
    return df


def analyze_data(df):
    print("\nStudent Data:")
    print(df)

    print("\nStatistics:")
    print("Average Marks:", np.mean(df["Marks"]))
    print("Highest Marks:", np.max(df["Marks"]))
    print("Lowest Marks:", np.min(df["Marks"]))


def add_result_column(df):
    df["Result"] = np.where(df["Marks"] >= 75, "Pass", "Fail")
    print("\nUpdated Data with Result:")
    print(df)


def main():
    df = create_data()
    analyze_data(df)
    add_result_column(df)


main()

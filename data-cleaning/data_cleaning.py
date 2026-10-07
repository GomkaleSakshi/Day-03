from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "dataset" / "employee_data.csv"
OUTPUT_FILE = PROJECT_ROOT / "dataset" / "cleaned_employee_data.csv"
NUMERIC_COLUMNS = ["Age", "Salary", "Experience", "Joining_Year", "Performance_Score"]


def main():
    data = pd.read_csv(INPUT_FILE)

    print("Raw dataset information")
    data.info()
    print("\nMissing values before cleaning")
    print(data.isna().sum())

    data["Employee_ID"] = data["Employee_ID"].astype("string").str.strip()

    for column in NUMERIC_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    invalid_value_counts = {
        "Age": int((data["Age"].notna() & ~data["Age"].between(18, 70)).sum()),
        "Salary": int((data["Salary"].notna() & (data["Salary"] <= 0)).sum()),
        "Experience": int((data["Experience"].notna() & (data["Experience"] < 0)).sum()),
        "Joining_Year": int((data["Joining_Year"].notna() & ~data["Joining_Year"].between(1980, 2026)).sum()),
        "Performance_Score": int((data["Performance_Score"].notna() & ~data["Performance_Score"].between(1, 5)).sum()),
    }
    print("\nInvalid values before cleaning")
    print(pd.Series(invalid_value_counts))

    data["Age"] = data["Age"].where(data["Age"].between(18, 70))
    data["Salary"] = data["Salary"].where(data["Salary"] > 0)
    data["Experience"] = data["Experience"].where(data["Experience"] >= 0)
    data["Joining_Year"] = data["Joining_Year"].where(data["Joining_Year"].between(1980, 2026))
    data["Performance_Score"] = data["Performance_Score"].where(data["Performance_Score"].between(1, 5))

    for column in ["Name", "Department", "Gender"]:
        data[column] = data[column].astype("string").str.strip()
        data[column] = data[column].replace("", pd.NA)

    data = data.dropna(subset=["Employee_ID"])
    duplicate_count = int(data.duplicated().sum())
    data = data.drop_duplicates()

    data["Age"] = data["Age"].fillna(data["Age"].median())
    data["Experience"] = data["Experience"].where(data["Experience"] <= data["Age"] - 18)
    data["Experience"] = data["Experience"].fillna(data["Experience"].median())
    data["Salary"] = data["Salary"].fillna(data["Salary"].median())
    data["Joining_Year"] = data["Joining_Year"].fillna(data["Joining_Year"].median()).round()
    data["Performance_Score"] = data["Performance_Score"].fillna(data["Performance_Score"].median()).round()
    data["Name"] = data["Name"].fillna("Unknown")

    for column in ["Department", "Gender"]:
        data[column] = data[column].fillna(data[column].mode().iloc[0])

    data["Employee_ID"] = data["Employee_ID"].astype(str)
    data["Age"] = data["Age"].round().astype(int)
    data["Salary"] = data["Salary"].round(2)
    data["Experience"] = data["Experience"].round().astype(int)
    data["Joining_Year"] = data["Joining_Year"].astype(int)
    data["Performance_Score"] = data["Performance_Score"].astype(int)

    data.to_csv(OUTPUT_FILE, index=False)

    print("\nMissing values after cleaning")
    print(data.isna().sum())
    print(f"\nDuplicate records removed: {duplicate_count}")
    print(f"Cleaned records saved: {len(data)}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

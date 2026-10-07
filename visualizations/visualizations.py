from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "dataset" / "cleaned_employee_data.csv"
OUTPUT_DIRECTORY = PROJECT_ROOT / "visualizations"


def save_figure(file_name):
    plt.tight_layout()
    plt.savefig(OUTPUT_DIRECTORY / file_name, dpi=150, bbox_inches="tight")
    plt.close()


def main():
    data = pd.read_csv(INPUT_FILE)

    department_counts = data["Department"].value_counts().sort_index()
    department_average_salary = data.groupby("Department")["Salary"].mean().sort_values(ascending=False)

    department_counts.plot(kind="bar", color="#287271")
    plt.title("Employees by Department")
    plt.xlabel("Department")
    plt.ylabel("Number of Employees")
    plt.xticks(rotation=30, ha="right")
    save_figure("department_employee_count.png")

    department_average_salary.plot(kind="bar", color="#e09f3e")
    plt.title("Average Salary by Department")
    plt.xlabel("Department")
    plt.ylabel("Average Salary ($)")
    plt.xticks(rotation=30, ha="right")
    save_figure("department_average_salary.png")

    plt.hist(data["Salary"], bins=10, color="#577590", edgecolor="white")
    plt.title("Salary Distribution")
    plt.xlabel("Salary ($)")
    plt.ylabel("Number of Employees")
    save_figure("salary_distribution.png")

    plt.hist(data["Age"], bins=10, color="#f28482", edgecolor="white")
    plt.title("Age Distribution")
    plt.xlabel("Age (years)")
    plt.ylabel("Number of Employees")
    save_figure("age_distribution.png")

    plt.scatter(data["Experience"], data["Salary"], color="#3a7d44", alpha=0.8)
    plt.title("Experience vs Salary")
    plt.xlabel("Experience (years)")
    plt.ylabel("Salary ($)")
    save_figure("experience_vs_salary.png")

    performance_counts = data["Performance_Score"].value_counts().sort_index()
    performance_counts.plot(kind="bar", color="#9b5de5")
    plt.title("Performance Score Distribution")
    plt.xlabel("Performance Score (1 to 5)")
    plt.ylabel("Number of Employees")
    plt.xticks(rotation=0)
    save_figure("performance_score_distribution.png")

    print(f"Six charts saved in: {OUTPUT_DIRECTORY}")


if __name__ == "__main__":
    main()

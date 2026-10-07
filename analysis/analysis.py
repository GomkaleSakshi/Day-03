from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "dataset" / "cleaned_employee_data.csv"
OUTPUT_FILE = PROJECT_ROOT / "analysis" / "analysis_results.txt"


def main():
    data = pd.read_csv(INPUT_FILE)

    department_counts = data["Department"].value_counts().sort_index()
    department_average_salary = data.groupby("Department")["Salary"].mean().sort_values(ascending=False)
    gender_counts = data["Gender"].value_counts().sort_index()
    performance_counts = data["Performance_Score"].value_counts().sort_index()
    experience_salary_correlation = data["Experience"].corr(data["Salary"])

    results = [
        "EMPLOYEE DATA ANALYSIS",
        "======================",
        f"Total employees: {len(data)}",
        f"Average salary: ${data['Salary'].mean():,.2f}",
        f"Highest salary: ${data['Salary'].max():,.2f}",
        f"Lowest salary: ${data['Salary'].min():,.2f}",
        f"Average age: {data['Age'].mean():.1f} years",
        f"Average experience: {data['Experience'].mean():.1f} years",
        "",
        "Department-wise employee count:",
        department_counts.to_string(),
        "",
        "Department-wise average salary:",
        department_average_salary.map(lambda amount: f"${amount:,.2f}").to_string(),
        "",
        "Gender-wise employee count:",
        gender_counts.to_string(),
        "",
        "Performance-score count:",
        performance_counts.to_string(),
        f"Average performance score: {data['Performance_Score'].mean():.2f} out of 5",
        "",
        f"Experience-salary correlation: {experience_salary_correlation:.2f}",
        "",
        "KEY FINDINGS",
        f"Largest department by employee count: {department_counts.idxmax()} ({department_counts.max()} employees).",
        f"Highest average salary by department: {department_average_salary.index[0]} (${department_average_salary.iloc[0]:,.2f}).",
    ]

    if experience_salary_correlation >= 0.5:
        correlation_finding = "Experience and salary have a strong positive relationship in this sample."
    elif experience_salary_correlation <= -0.5:
        correlation_finding = "Experience and salary have a strong negative relationship in this sample."
    else:
        correlation_finding = "Experience and salary have a weak relationship in this sample."

    results.append(correlation_finding)
    results.append("Correlation describes association and does not establish cause and effect.")

    report = "\n".join(results)
    print(report)
    OUTPUT_FILE.write_text(report + "\n", encoding="utf-8")
    print(f"\nAnalysis results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

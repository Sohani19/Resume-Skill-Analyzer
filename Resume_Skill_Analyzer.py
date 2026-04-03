import pandas as pd
import numpy as np
import os

# JOB SKILL DATABASE
# This dictionary stores job roles and their required skills

JOB_SKILLS = {
    "data analyst": ["python", "pandas", "numpy", "sql", "excel", "matplotlib"],
    "python developer": ["python", "oops", "file handling", "exception handling"],
    "web developer": ["html", "css", "javascript", "python"],
    "ai engineer": ["python", "numpy", "machine learning", "statistics"]
}


# FUNCTION TO SELECT JOB ROLE
def get_job_role():
    print("\nAvailable Job Roles:")
    
    # Display all job roles
    for role in JOB_SKILLS:
        print("-", role.title())

    # Keep asking until valid role is entered
    while True:
        role = input("\nEnter job role: ").strip().lower()
        if role in JOB_SKILLS:
            return role
        print("Invalid job role. Please select from the list.")


# FUNCTION TO GET USER SKILLS 
def get_student_skills():
    while True:
        skills_input = input("\nEnter your skills (comma separated): ")

        # Converting input into a clean list
        skills_list = [
            skill.strip().lower()
            for skill in skills_input.split(",")
            if skill.strip()
        ]

        if skills_list:
            return skills_list

        print("You must enter at least one skill.")


# RESUME ANALYSIS FUNCTION 
def analyze_resume(student_skills, job_role):
    required_skills = JOB_SKILLS[job_role]

    # Creating a DataFrame to compare skills
    analysis_df = pd.DataFrame({
        "Required Skill": required_skills,
        "Matched": [skill in student_skills for skill in required_skills]
    })

    matched_count = analysis_df["Matched"].sum()
    total_skills = len(required_skills)

    # Calculating match percentage
    match_percentage = np.round((matched_count / total_skills) * 100, 2)

    # Getting missing skills
    missing_skills = analysis_df[
        analysis_df["Matched"] == False
    ]["Required Skill"].tolist()

    return analysis_df, match_percentage, missing_skills


# SAVING RESULT TO CSV FILE
def save_to_csv(df, job_role, percentage, missing_skills):
    result_df = df.copy()

    result_df["Job Role"] = job_role
    result_df["Match Percentage"] = percentage
    result_df["Missing Skills"] = (
        ", ".join(missing_skills) if missing_skills else "None"
    )

    file_exists = os.path.exists("resume_analysis.csv")

    result_df.to_csv(
        "resume_analysis.csv",
        mode="a",
        index=False,
        header=not file_exists
    )


# MAIN FUNCTION 
def MainFunc():
    print("\n--- Resume Skill Analyzer ---")

    try:
        job_role = get_job_role()
        student_skills = get_student_skills()

        df, percentage, missing_skills = analyze_resume(
            student_skills, job_role
        )

        print("\nSkill Analysis:\n")
        print(df)

        print(f"\nSkill Match Percentage: {percentage}%")

        if missing_skills:
            print("\nMissing Skills:")
            for skill in missing_skills:
                print("-", skill)
        else:
            print("\nGreat! You have all required skills.")

        save_to_csv(df, job_role, percentage, missing_skills)
        print("\nResult saved to resume_analysis.csv")

    except Exception as error:
        print("An error occurred:", error)


# CALLING MAIN FUNCTION
MainFunc()
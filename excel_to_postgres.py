import pandas as pd
from sqlalchemy import create_engine

# Load the Excel file
excel_path = "data/Database_ContentIupdated.xlsx_jan.xlsx"
df = pd.read_excel(excel_path)

# Clean column names 
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]


column_mapping = {
    "clinical_trial_number": "clinical_trail_number", 
    "patient_number": "patient_id",
    "original_t_cell_sources": "origin_t_cell_sources",
    "partial_response_for_whole_study": "partial_response_for",
    "survival_post_6_months_for_whole_group": "survival_post_6_months",
    "best_reponse": "best_response"
}

df.rename(columns=column_mapping, inplace=True)

# all required DB columns are present
required_columns = [
    "sequence", "disease", "disease_description", "paper_number_for_record",
    "country_name_of_clinical_trial", "pubmed_id", "year", "title_of_the_paper",
    "clinical_trail_number", "patient_id", "sex", "age", "age_group", "car_t_design",
    "generation_of_car_receptor", "vector", "antigen", "transfection_method",
    "origin_t_cell_sources", "patient_inclusion_criteria", "patient_exclusion_criteria",
    "best_response", "partial_response_for", "stable_disease",
    "complete_response_for_the_whole_group", "no_response",
    "progressive_disease_after_one_month", "median_overall_survival",
    "survival_post_6_months", "number_of_previous_therapies"
]

missing = set(required_columns) - set(df.columns)
if missing:
    print("Missing columns in Excel after renaming:", missing)
    exit(1) 

for col in df.columns:
    df[col] = df[col].apply(lambda x: x[:255] if isinstance(x, str) and len(x) > 255 else x)

# # Fill missing values 
# df["patient_inclusion_criteria"] = df["patient_inclusion_criteria"].fillna("N/A")
# df["patient_exclusion_criteria"] = df["patient_exclusion_criteria"].fillna("N/A")
# df["best_response"] = df["best_response"].fillna("N/A")
# df["partial_response_for"] = df["partial_response_for"].fillna("N/A")
# #df["clinical_trials"] = df["clinical_trials"].fillna("N/A")
# df["stable_disease"] = df["stable_disease"].fillna("N/A")
# # df[""] = df[""].fillna("N/A")
# # df[""] = df[""].fillna("N/A")
 
# Fill all object (text) columns with "N/A"
df = df.fillna(value={col: "N/A" for col in df.select_dtypes(include='object').columns})

# Fill all numeric columns with -1 or 0 (whichever makes sense)
df = df.fillna(value={col: -1 for col in df.select_dtypes(include='number').columns})


engine = create_engine("postgresql+psycopg2://db_user:db_pass@localhost:5432/canimmdb")

# Feed data into the table
df.to_sql('clinical_trials', engine, if_exists='append', index=False)


print("Data imported successfully!")

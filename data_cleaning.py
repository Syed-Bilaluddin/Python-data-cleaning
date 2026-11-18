import re
import pandas as pd
def is_valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    return bool(re.match(pattern, email))

df = pd.read_csv("messy_data.csv")

original_records = len(df)

for column in ["Name", "Email", "City"]:
    df[column] = df[column].str.strip()

df["Name"] = df["Name"].str.title()
df["Email"] = df["Email"].str.lower()
df["City"] = df["City"].str.title()

duplicate_count = df.duplicated().sum()

df = df.drop_duplicates()

missing_count = (
    df["Name"].isna() |
    df["Email"].isna() |
    (df["Name"].fillna("").str.strip() == "") |
    (df["Email"].fillna("").str.strip() == "")
).sum()

df = df.dropna(subset=["Name", "Email"])
df = df[(df["Name"] != "") & (df["Email"] != "")]

df["Valid_Email"] = df["Email"].apply(is_valid_email)

invalid_email_count = (~df["Valid_Email"]).sum()

df["Monthly_Sales"] = pd.to_numeric(df["Monthly_Sales"], errors="coerce")

df["Needs_Review"] = df["Monthly_Sales"].isna()

df.to_csv("clean_data.csv", index=False)

print("=====CLEANING REPORT=====")
print("Original Records: ", original_records)
print("Duplicates found: ", duplicate_count)
print("Missing Name/Email: ", missing_count)
print("Invalid Email Counts: ", invalid_email_count)
print("Records needing review: ",df["Needs_Review"].sum())
print("Final Records: ",len(df))

print("=========================")

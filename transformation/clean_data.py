import pandas as pd

# Read JSON data
df = pd.read_json("raw_data/users.json")

print("Original Shape:", df.shape)

# Extract nested fields
df["city"] = df["address"].apply(lambda x: x["city"])
df["zipcode"] = df["address"].apply(lambda x: x["zipcode"])
df["company_name"] = df["company"].apply(lambda x: x["name"])

# Keep only required columns
cleaned_df = df[
    [
        "id",
        "name",
        "username",
        "email",
        "phone",
        "website",
        "city",
        "zipcode",
        "company_name",
    ]
]

# Remove duplicates
cleaned_df = cleaned_df.drop_duplicates()

# Remove missing values
cleaned_df = cleaned_df.dropna()

print("\nCleaned Data:")
print(cleaned_df.head())

# Save CSV
cleaned_df.to_csv("raw_data/cleaned_users.csv", index=False)

print("\n✅ Flattened data saved successfully!")
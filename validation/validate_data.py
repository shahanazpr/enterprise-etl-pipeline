import pandas as pd
from validation.user_model import User

# Read cleaned CSV
df = pd.read_csv("raw_data/cleaned_users.csv")

print("Validating records...\n")

valid_count = 0

for _, row in df.iterrows():
    user = User(**row.to_dict())
    valid_count += 1

print(f"✅ {valid_count} records validated successfully!")
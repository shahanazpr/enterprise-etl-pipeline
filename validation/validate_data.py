import pandas as pd
from pydantic import ValidationError
from validation.user_model import User
from utils.logger import logger

df = pd.read_csv("raw_data/cleaned_users.csv")

print("Validating records...\n")

valid_records = []
invalid_count = 0

for _, row in df.iterrows():
    try:
        user = User(**row.to_dict())
        valid_records.append(user)

    except ValidationError as e:
        invalid_count += 1
        logger.error(
            f"Validation failed for record ID {row.get('id', 'Unknown')}: {e}"
        )
        continue

logger.info(f"Valid records: {len(valid_records)}")
logger.info(f"Invalid records skipped: {invalid_count}")

print(f"✅ {len(valid_records)} records validated successfully!")
print(f"❌ {invalid_count} invalid records skipped.")
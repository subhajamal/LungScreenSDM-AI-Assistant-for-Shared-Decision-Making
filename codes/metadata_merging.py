import json
import shutil

# Paths
original_path = r"C:\Users\subha\Downloads\LungCancerChatbot\lung_metadata.json"
new_data_path = r"C:\Users\subha\Downloads\LungCancerChatbot\lung_metadata_web_fetched.json"
backup_path = r"C:\Users\subha\Downloads\LungCancerChatbot\lung_metadata_backup.json"

# Step 1: Load the original metadata
with open(original_path, "r", encoding="utf-8") as f:
    original_metadata = json.load(f)

# Step 2: Load the new web metadata
with open(new_data_path, "r", encoding="utf-8") as f:
    new_metadata = json.load(f)

# Step 3: Create a backup
shutil.copy(original_path, backup_path)
print(f"Backup saved as: {backup_path}")

# Step 4: Merge new entries
merged_metadata = original_metadata + new_metadata

# Step 5: Save back to the original file
with open(original_path, "w", encoding="utf-8") as f:
    json.dump(merged_metadata, f, indent=4, ensure_ascii=False)

print(f"Merged {len(new_metadata)} new entries into {original_path}")

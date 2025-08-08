import csv
import json
from typing import List, Dict

def save_labeled_dataset(features_list: List[Dict], labels_dict: Dict[int, int], output_path: str):
    """
    Merge extracted features with labels and save as CSV file.

    :param features_list: List of feature dictionaries with 'blockNumber' keys
    :param labels_dict: Dictionary mapping blockNumber -> label (int)
    :param output_path: File path for output CSV dataset
    """
    if not features_list:
        print("No features provided to save.")
        return

    # Prepare rows combining features and label
    rows = []
    for features in features_list:
        block_num = features['blockNumber']
        label = labels_dict.get(block_num, 0)  # default label=0 if unknown
        row = features.copy()
        row['label'] = label
        rows.append(row)

    # Write CSV - columns based on first features dict plus label
    fieldnames = list(features_list[0].keys()) + ['label']

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Training dataset saved to {output_path}")


# Example usage: Load existing features and labels, then save CSV

if __name__ == "__main__":
    # Example: Load features from a JSON file (replace with your actual data source)
    with open("../data/features.json", "r") as f:
        features_list = json.load(f)  # List of feature dicts

    # Example: Load labels from JSON (blockNumber -> label)
    with open("../data/labels.json", "r") as f:
        labels_dict = json.load(f)  # Dict with blockNumber keys as strings

    # Convert label keys to int because CSV expects numeric keys
    labels_dict = {int(k): v for k, v in labels_dict.items()}

    # Save combined dataset to CSV
    save_labeled_dataset(features_list, labels_dict, "../data/training_dataset.csv")

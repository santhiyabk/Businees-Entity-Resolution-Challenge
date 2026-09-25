import csv
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
TRAIN_DIR = BASE_DIR / "dataset" / "train"


def load_data(file_name, nrows=1000):
    file_path = TRAIN_DIR / file_name

    rows = []

    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        reader = csv.DictReader(file, delimiter="\t")

        for i, row in enumerate(reader):
            if i >= nrows:
                break
            rows.append(row)

    return rows


def normalize_name(value):
    if not value:
        return ""

    value = str(value).lower()

    replacements = {
        r"\bpvt\b": "private",
        r"\bltd\b": "limited",
        r"\bco\b": "company",
        r"\bcorp\b": "corporation",
        r"\binc\b": "incorporated"
    }

    for pattern, replacement in replacements.items():
        value = re.sub(pattern, replacement, value)

    value = re.sub(r"[^\w\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value


def normalize_address(value):
    if not value:
        return ""

    value = str(value).lower()

    replacements = {
        r"\brd\b": "road",
        r"\bst\b": "street",
        r"\bave\b": "avenue",
        r"\bblvd\b": "boulevard",
        r"\bhwy\b": "highway",
        r"\bln\b": "lane",
        r"\bdr\b": "drive"
    }

    for pattern, replacement in replacements.items():
        value = re.sub(pattern, replacement, value)

    value = re.sub(r"[^\w\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value


def preprocess_data(rows):

    for row in rows:

        row["business_name_normalized"] = normalize_name(
            row.get("business_name", "")
        )

        row["business_address_normalized"] = normalize_address(
            row.get("business_address", "")
        )

        row["country_normalized"] = (
            row.get("country", "").lower().strip()
        )

    return rows


if __name__ == "__main__":

    print("Loading training data...")

    source1 = load_data("train_source1.tsv")
    source2 = load_data("train_source2.tsv")
    source3 = load_data("train_source3.tsv")

    print("Source 1 rows:", len(source1))
    print("Source 2 rows:", len(source2))
    print("Source 3 rows:", len(source3))

    print("\nPreprocessing...")

    source1 = preprocess_data(source1)
    source2 = preprocess_data(source2)
    source3 = preprocess_data(source3)

    print("Preprocessing completed!")

    print("\nSample normalized data:")

    for row in source1[:5]:
        print(
            "Name:",
            row.get("business_name"),
            "->",
            row.get("business_name_normalized")
        )

        print(
            "Address:",
            row.get("business_address"),
            "->",
            row.get("business_address_normalized")
        )

        print()
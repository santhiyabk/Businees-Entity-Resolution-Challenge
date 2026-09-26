import csv
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
TRAIN_DIR = BASE_DIR / "dataset" / "train"
OUTPUT_DIR = BASE_DIR / "processed_data"

OUTPUT_DIR.mkdir(exist_ok=True)


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


def preprocess_file(input_file, output_file):

    print(f"\nProcessing: {input_file.name}")

    with open(
        input_file,
        "r",
        encoding="utf-8",
        errors="replace",
        newline=""
    ) as infile:

        reader = csv.DictReader(infile, delimiter="\t")

        fieldnames = list(reader.fieldnames)

        fieldnames.extend([
            "business_name_normalized",
            "business_address_normalized",
            "country_normalized"
        ])

        with open(
            output_file,
            "w",
            encoding="utf-8",
            newline=""
        ) as outfile:

            writer = csv.DictWriter(
                outfile,
                fieldnames=fieldnames,
                delimiter="\t"
            )

            writer.writeheader()

            count = 0

            for row in reader:

                row["business_name_normalized"] = normalize_name(
                    row.get("business_name", "")
                )

                row["business_address_normalized"] = normalize_address(
                    row.get("business_address", "")
                )

                row["country_normalized"] = (
                    row.get("country", "").lower().strip()
                )

                writer.writerow(row)

                count += 1

                if count % 100000 == 0:
                    print(f"  Processed {count:,} rows")

    print(f"Completed: {count:,} rows")


if __name__ == "__main__":

    print("======================================")
    print("Business Entity Resolution")
    print("Full Data Preprocessing")
    print("======================================")

    preprocess_file(
        TRAIN_DIR / "train_source1.tsv",
        OUTPUT_DIR / "source1_clean.tsv"
    )

    preprocess_file(
        TRAIN_DIR / "train_source2.tsv",
        OUTPUT_DIR / "source2_clean.tsv"
    )

    preprocess_file(
        TRAIN_DIR / "train_source3.tsv",
        OUTPUT_DIR / "source3_clean.tsv"
    )

    print("\n======================================")
    print("ALL PREPROCESSING COMPLETED!")
    print(f"Output folder: {OUTPUT_DIR}")
    print("======================================")
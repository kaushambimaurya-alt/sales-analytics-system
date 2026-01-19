import os
from datetime import datetime


def read_sales_file(file_name):
    """
    Reads the sales data file using safe encoding
    and a path relative to this script.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, file_name)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except UnicodeDecodeError:
        # Fallback encoding
        with open(file_path, "r", encoding="latin-1") as f:
            return f.readlines()


def clean_sales_data(lines):
    """
    Cleans and validates sales data
    """

    total_records = 0
    invalid_count = 0
    valid_records = []

    for line in lines:
        line = line.strip()

        # 1. Skip empty lines
        if not line:
            continue

        parts = line.split("|")

        # 2. Skip header row (case-insensitive)
        if parts[0].strip().lower() == "transactionid":
            continue

        # 3. Validate column count
        if len(parts) != 8:
            invalid_count += 1
            continue

        total_records += 1

        (
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ) = parts

        # 4. Validate transaction ID
        if not transaction_id.startswith("T"):
            invalid_count += 1
            continue

        # 5. Validate required fields
        if not customer_id.strip() or not region.strip():
            invalid_count += 1
            continue

        # 6. Validate date format (YYYY-MM-DD)
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            invalid_count += 1
            continue

        # 7. Clean numeric values
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            invalid_count += 1
            continue

        if quantity <= 0 or unit_price <= 0:
            invalid_count += 1
            continue

        # 8. Clean product name (trim spaces only)
        product_name = product_name.strip()

        # 9. Store valid record
        valid_records.append([
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ])

    return total_records, invalid_count, valid_records


# ------------------- RUN PROGRAM -------------------

if __name__ == "__main__":
    file_name = "sales_data.txt"

    try:
        lines = read_sales_file(file_name)
    except FileNotFoundError:
        print(f"ERROR: '{file_name}' not found in the data directory.")
        exit(1)

    total, invalid, valid_data = clean_sales_data(lines)

    print("Total records parsed:", total)
    print("Invalid records removed:", invalid)
    print("Valid records after cleaning:", len(valid_data))


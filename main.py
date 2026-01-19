
def read_sales_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return lines
    except Exception as e:
        print("Error reading file:", e)
        return []


def parse_transactions(lines):
    transactions = []
    invalid_count = 0

    # Remove completely empty lines
    clean_lines = [line for line in lines if line.strip()]

    print("Total lines in file:", len(clean_lines))

    # Skip header line
    for line in clean_lines[1:]:

        # Split using | and remove spaces
        parts = [p.strip() for p in line.strip().split("|")]

        # Must have exactly 8 columns
        if len(parts) != 8:
            invalid_count += 1
            continue

        try:
            quantity = int(parts[4])
            price = float(parts[5])

            transaction = {
                "transaction_id": parts[0],
                "date": parts[1],
                "product_id": parts[2],
                "product_name": parts[3],
                "quantity": quantity,
                "unit_price": price,
                "customer_id": parts[6],
                "region": parts[7],
                "amount": quantity * price
            }

            transactions.append(transaction)

        except Exception:
            invalid_count += 1

    return transactions, invalid_count


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):

    filtered = transactions

    if region:
        filtered = [t for t in filtered if t["region"].lower() == region.lower()]

    if min_amount is not None:
        filtered = [t for t in filtered if t["amount"] >= min_amount]

    if max_amount is not None:
        filtered = [t for t in filtered if t["amount"] <= max_amount]

    summary = {
        "total_transactions": len(transactions),
        "filtered_transactions": len(filtered),
        "total_sales": sum(t["amount"] for t in filtered)
    }

    return filtered, summary


def generate_report(transactions, summary):

    try:
        with open("sales_report.txt", "w", encoding="utf-8") as report:

            report.write("SALES REPORT\n")
            report.write("============================\n\n")

            report.write(f"Total Transactions: {summary['total_transactions']}\n")
            report.write(f"Filtered Transactions: {summary['filtered_transactions']}\n")
            report.write(f"Total Sales Amount: {summary['total_sales']}\n\n")

            report.write("Transaction Details:\n")
            report.write("----------------------------------\n")

            for t in transactions:
                report.write(
                    f"ID: {t['transaction_id']} | "
                    f"Product: {t['product_name']} | "
                    f"Region: {t['region']} | "
                    f"Amount: {t['amount']}\n"
                )

        print("\nReport generated successfully: sales_report.txt")

    except Exception as e:
        print("Error generating report:", e)


def main():

    print("Welcome to Sales Analytics System\n")

    filepath = "data/sales_data.txt"

    lines = read_sales_file(filepath)

    if not lines:
        print("No data found in file!")
        return

    transactions, invalid = parse_transactions(lines)

    print(f"Total valid transactions: {len(transactions)}")
    print(f"Invalid records skipped: {invalid}")

    regions = set(t["region"] for t in transactions)
    print("\nAvailable Regions:", regions)

    choice = input("\nDo you want to apply filters? (y/n):")

    region = None
    min_amount = None
    max_amount = None

    if choice.lower() == "y":

        region = input("Enter region to filter (or press enter to skip): ")
        if region.strip() == "":
            region = None

        try:
            min_amount_input = input("Enter minimum amount (or press enter to skip): ")
            min_amount = float(min_amount_input) if min_amount_input else None

            max_amount_input = input("Enter maximum amount (or press enter to skip): ")
            max_amount = float(max_amount_input) if max_amount_input else None

        except:
            print("Invalid amount input! Skipping amount filters.")

    filtered, summary = validate_and_filter(
        transactions, region, min_amount, max_amount
    )

    generate_report(filtered, summary)

if __name__ == "__main__":
 main()
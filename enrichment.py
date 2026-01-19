import os


def enrich_sales_data(transactions, product_mapping):

    enriched = []

    for t in transactions:

        new_t = t.copy()

        try:
            product_id = t.get("ProductID", "")
            numeric_id = int(product_id.replace("P", ""))
        except:
            numeric_id = None

        if numeric_id in product_mapping:
            api_info = product_mapping[numeric_id]

            new_t["API_Category"] = api_info.get("category")
            new_t["API_Brand"] = api_info.get("brand")
            new_t["API_Rating"] = api_info.get("rating")
            new_t["API_Match"] = True

        else:
            new_t["API_Category"] = None
            new_t["API_Brand"] = None
            new_t["API_Rating"] = None
            new_t["API_Match"] = False

        enriched.append(new_t)

    return enriched


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    header = [
        "TransactionID",
        "Date",
        "ProductID",
        "ProductName",
        "Quantity",
        "UnitPrice",
        "CustomerID",
        "Region",
        "API_Category",
        "API_Brand",
        "API_Rating",
        "API_Match"
    ]

    try:
        with open(filename, "w") as f:

            f.write("|".join(header) + "\n")

            for t in enriched_transactions:

                row = []

                for col in header:
                    value = t.get(col, "")

                    if value is None:
                        value = ""

                    row.append(str(value))

                f.write("|".join(row) + "\n")

        print("Enriched data saved successfully to:", filename)

    except Exception as e:
        print("Error saving enriched data:", e)


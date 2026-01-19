import requests


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            products = data.get("products", [])

            result = []

            for p in products:
                product_info = {
                    'id': p.get('id'),
                    'title': p.get('title'),
                    'category': p.get('category'),
                    'brand': p.get('brand'),
                    'price': p.get('price'),
                    'rating': p.get('rating')
                }
                result.append(product_info)

            print("Successfully fetched products from API")
            return result

        else:
            print("API request failed with status:", response.status_code)
            return []

    except Exception as e:
        print("Error connecting to API:", e)
        return []



def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """

    mapping = {}

    for product in api_products:

        product_id = product.get('id')

        mapping[product_id] = {
            'title': product.get('title'),
            'category': product.get('category'),
            'brand': product.get('brand'),
            'rating': product.get('rating')
        }

    return mapping



import os


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """

    enriched = []

    for t in transactions:

        new_t = t.copy()

        # Extract numeric ID from ProductID (e.g., P101 -> 101)
        try:
            product_id = t.get("ProductID", "")
            numeric_id = int(product_id.replace("P", ""))
        except:
            numeric_id = None

        # Enrich if mapping exists
        if numeric_id in product_mapping:
            api_info = product_mapping[numeric_id]

            new_t["API_Category"] = api_info.get("category")
            new_t["API_Brand"] = api_info.get("brand")
            new_t["API_Rating"] = api_info.get("rating")
            new_t["API_Match"] = True

        else:
            # Handle missing products
            new_t["API_Category"] = None
            new_t["API_Brand"] = None
            new_t["API_Rating"] = None
            new_t["API_Match"] = False

        enriched.append(new_t)

    return enriched



def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    """

    # Ensure data folder exists
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

            # Write header
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

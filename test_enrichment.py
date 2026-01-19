from utils.api_handler import fetch_all_products, create_product_mapping
from enrichment import enrich_sales_data, save_enriched_data


sample_transactions = [
    {
        'TransactionID': 'T001',
        'Date': '2024-12-01',
        'ProductID': 'P1',
        'ProductName': 'Sample Product',
        'Quantity': 2,
        'UnitPrice': 549,
        'CustomerID': 'C001',
        'Region': 'North'
    },
    {
        'TransactionID': 'T002',
        'Date': '2024-12-02',
        'ProductID': 'P999',
        'ProductName': 'Unknown',
        'Quantity': 1,
        'UnitPrice': 100,
        'CustomerID': 'C002',
        'Region': 'South'
    }
]


print("Fetching API Products...")
products = fetch_all_products()

mapping = create_product_mapping(products)

print("Enriching transactions...")

enriched = enrich_sales_data(sample_transactions, mapping)

for e in enriched:
    print(e)

print("\nSaving to file...")
save_enriched_data(enriched)

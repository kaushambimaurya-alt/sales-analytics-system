
# ================================
# Sales Summary Calculator
# utils/data_processor.py
# ================================

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    Returns: float
    """
    total_revenue = 0.0

    for tx in transactions:
        total_revenue += tx['Quantity'] * tx['UnitPrice']

    return total_revenue


def region_wise_sales(transactions):
    """
    Analyzes sales by region
    Returns: dictionary
    """
    region_data = {}
    grand_total = 0.0

    # Aggregate region data
    for tx in transactions:
        region = tx['Region']
        revenue = tx['Quantity'] * tx['UnitPrice']
        grand_total += revenue

        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_data[region]['total_sales'] += revenue
        region_data[region]['transaction_count'] += 1

    # Calculate percentage
    for region in region_data:
        region_data[region]['percentage'] = round(
            (region_data[region]['total_sales'] / grand_total) * 100, 2
        )

    # Sort by total_sales (descending)
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]['total_sales'],
            reverse=True
        )
    )

    return sorted_regions


def top_selling_products(transactions, n=5):
    """
    Finds top n products by quantity sold
    Returns: list of tuples
    """
    product_data = {}

    for tx in transactions:
        product = tx['ProductName']
        quantity = tx['Quantity']
        revenue = tx['Quantity'] * tx['UnitPrice']

        if product not in product_data:
            product_data[product] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_data[product]['quantity'] += quantity
        product_data[product]['revenue'] += revenue

    result = [
        (product, data['quantity'], data['revenue'])
        for product, data in product_data.items()
    ]

    # Sort by quantity sold
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    Returns: dictionary
    """
    customer_data = {}

    for tx in transactions:
        customer = tx['CustomerID']
        product = tx['ProductName']
        revenue = tx['Quantity'] * tx['UnitPrice']

        if customer not in customer_data:
            customer_data[customer] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }

        customer_data[customer]['total_spent'] += revenue
        customer_data[customer]['purchase_count'] += 1
        customer_data[customer]['products_bought'].add(product)

    # Final calculations
    for customer in customer_data:
        total = customer_data[customer]['total_spent']
        count = customer_data[customer]['purchase_count']

        customer_data[customer]['avg_order_value'] = round(total / count, 2)
        customer_data[customer]['products_bought'] = list(
            customer_data[customer]['products_bought']
        )

    # Sort by total_spent descending
    sorted_customers = dict(
        sorted(
            customer_data.items(),
            key=lambda x: x[1]['total_spent'],
            reverse=True
        )
    )

    return sorted_customers


def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    Returns: dictionary sorted by date
    """
    daily_data = {}

    for tx in transactions:
        date = tx['TransactionDate']
        revenue = tx['Quantity'] * tx['UnitPrice']
        customer = tx['CustomerID']

        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }

        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['unique_customers'].add(customer)

    # Convert set of unique_customers to count
    for date in daily_data:
        daily_data[date]['unique_customers'] = len(daily_data[date]['unique_customers'])

    # Sort by date
    sorted_daily_data = dict(sorted(daily_data.items()))

    return sorted_daily_data



def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    Returns: tuple (date, revenue, transaction_count)
    """
    daily_data = daily_sales_trend(transactions)

    peak_date = max(daily_data.items(), key=lambda x: x[1]['revenue'])

    date = peak_date[0]
    revenue = peak_date[1]['revenue']
    transaction_count = peak_date[1]['transaction_count']

    return (date, revenue, transaction_count)



def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    Returns: list of tuples
    """
    product_data = {}

    # Step 1: Aggregate product data
    for tx in transactions:
        product = tx['ProductName']
        quantity = tx['Quantity']
        revenue = quantity * tx['UnitPrice']

        if product not in product_data:
            product_data[product] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_data[product]['quantity'] += quantity
        product_data[product]['revenue'] += revenue

    # Step 2: Filter low performing products
    low_products = [
        (product, data['quantity'], data['revenue'])
        for product, data in product_data.items()
        if data['quantity'] < threshold
    ]

    # Step 3: Sort by TotalQuantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products

import csv
from pathlib import Path
import re

DATA_PATH = Path("data") / "electronics_sales.csv"


def read_sales(path=DATA_PATH):
    """Read the CSV with the csv module and return raw rows."""

    with open(path, mode="r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        rows = list(reader)

        print(f"Rows read: {len(rows)}")
        print(f"Columns found: {reader.fieldnames}")

    return rows


def parse_number(value):
    """Convert messy numeric strings into numbers safely."""


def convert_rows(rows):
    """Clean records and separate valid and skipped sales."""


def parse_number(value):
    """Convert a messy numeric string into a float, or return None."""

    if value is None:
        return None

    value = value.strip()

    if not value:
        return None

    # Handle number words that we can confidently interpret
    word_numbers = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5
    }

    if value.lower() in word_numbers:
        return float(word_numbers[value.lower()])

    # Remove the currency label
    value = value.upper().replace("KES", "").strip()

    # Remove thousands separators
    value = value.replace(",", "")

    # Only accept properly formatted positive or negative numeric strings
    if not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", value):
        return None

    try:
        return float(value)

    except ValueError:
        return None

    # print(parse_number("two"))
    # print(parse_number("38,999"))
    # print(parse_number("KES 18999"))
    # print(parse_number("N/A"))
    # print(parse_number(""))
    # print(parse_number("abc"))


def convert_rows(rows):
    """Clean sales records and separate valid and skipped rows."""

    clean_rows = []
    skipped_rows = []

    for row in rows:

        # Convert quantity and unit price
        quantity = parse_number(row["quantity"])
        unit_price = parse_number(row["unit_price_kes"])

        reasons = []

        # Validate quantity
        if quantity is None:
            reasons.append("Invalid or missing quantity")

        elif quantity <= 0:
            reasons.append("Quantity must be positive")

        elif not quantity.is_integer():
            reasons.append("Quantity must be a whole number")

        # Validate unit price
        if unit_price is None:
            reasons.append("Invalid or missing unit price")

        elif unit_price <= 0:
            reasons.append("Unit price must be positive")

        # Skip records with any validation problems
        if reasons:
            skipped = row.copy()
            skipped["reason"] = "; ".join(reasons)

            skipped_rows.append(skipped)
            continue

        # Create a clean copy of the original record
        clean_row = row.copy()

        clean_row["quantity"] = int(quantity)
        clean_row["unit_price_kes"] = unit_price

        # Calculate transaction revenue
        clean_row["revenue"] = clean_row["quantity"] * unit_price

        clean_rows.append(clean_row)

    return clean_rows, skipped_rows



def total_revenue(rows):
    """Calculate the total revenue from all valid transactions."""

    total = 0

    for row in rows:
        total += row["revenue"]

    return total


def revenue_by(rows, field):
    """Calculate total revenue grouped by a specified column."""

    totals = {}

    for row in rows:

        key = row[field]

        if key in totals:
            totals[key] += row["revenue"]

        else:
            totals[key] = row["revenue"]

    return totals


def top_n(totals, n=3):
    """Return the n highest (product, revenue) pairs."""

    ranked = sorted(
        totals.items(),
        key=lambda item: (-item[1], item[0])
    )

    return ranked[:n]


def high_value(rows, threshold):
    """Return transactions whose revenue meets or exceeds the threshold."""

    return [
        row for row in rows
        if row["revenue"] >= threshold
    ]


def mean(values):
    """Calculate the arithmetic mean."""

    if not values:
        raise ValueError("Cannot calculate mean of an empty list.")

    return sum(values) / len(values)


def median(values):
    """Calculate the median of a list of numbers."""

    if not values:
        raise ValueError("Cannot calculate median of an empty list.")

    sorted_values = sorted(values)

    n = len(sorted_values)

    middle = n // 2

    if n % 2 == 1:
        return sorted_values[middle]

    else:
        return (
            sorted_values[middle - 1] +
            sorted_values[middle]
        ) / 2


def minimum_maximum(values):
    """Return the minimum and maximum values without min() or max()."""

    if not values:
        raise ValueError(
            "Cannot calculate minimum and maximum of an empty list."
        )

    minimum = values[0]
    maximum = values[0]

    for value in values:

        if value < minimum:
            minimum = value

        if value > maximum:
            maximum = value

    return minimum, maximum



def verify_with_pandas(path, my_results):
    """Recompute headline numbers with pandas and compare results."""

    import math
    import pandas as pd

    # Read all columns as strings to preserve the original values
    df = pd.read_csv(path, dtype=str, keep_default_na=False)

    # Apply the same cleaning function used in our pure Python analysis
    df["quantity"] = df["quantity"].apply(parse_number)
    df["unit_price_kes"] = df["unit_price_kes"].apply(parse_number)

    # Keep only valid transactions
    valid = (
        df["quantity"].notna()
        & df["unit_price_kes"].notna()
        & (df["quantity"] > 0)
        & (df["quantity"] % 1 == 0)
        & (df["unit_price_kes"] > 0)
    )

    df = df.loc[valid].copy()

    # Convert quantity to integer and calculate revenue
    df["quantity"] = df["quantity"].astype(int)

    df["revenue"] = (
        df["quantity"] * df["unit_price_kes"]
    )

    # Recalculate headline results using pandas
    pandas_total = df["revenue"].sum()

    pandas_products = (
        df.groupby("product")["revenue"]
        .sum()
        .to_dict()
    )

    pandas_top3 = sorted(
        pandas_products.items(),
        key=lambda item: (-item[1], item[0])
    )[:3]

    pandas_mean = df["revenue"].mean()
    pandas_median = df["revenue"].median()

    # Compare floating-point results with a small tolerance
    def matches(a, b):
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=0.01)

    # 1. Total revenue
    total_match = matches(
        my_results["total_revenue"],
        pandas_total
    )

    print("\n=== pandas verification ===")

    if total_match:
        print("Total revenue      : MATCH")
    else:
        print(
            f"Total revenue      : MISMATCH "
            f"(pure={my_results['total_revenue']:.2f}, "
            f"pandas={pandas_total:.2f})"
        )

    # 2. Revenue by product
    product_match = (
        my_results["product_totals"].keys()
        == pandas_products.keys()
        and all(
            matches(my_results["product_totals"][product], amount)
            for product, amount in pandas_products.items()
        )
    )

    if product_match:
        print("Revenue by product : MATCH")
    else:
        print("Revenue by product : MISMATCH")
        print("Pure Python:", my_results["product_totals"])
        print("Pandas:", pandas_products)

    # 3. Top three products
    top3_match = (
        len(my_results["top3"]) == len(pandas_top3)
        and all(
            product_a == product_b
            and matches(revenue_a, revenue_b)
            for (product_a, revenue_a), (product_b, revenue_b)
            in zip(my_results["top3"], pandas_top3)
        )
    )

    if top3_match:
        print("Top 3              : MATCH")
    else:
        print("Top 3              : MISMATCH")
        print("Pure Python:", my_results["top3"])
        print("Pandas:", pandas_top3)

    # 4. Mean and median
    statistics_match = (
        matches(my_results["mean"], pandas_mean)
        and matches(my_results["median"], pandas_median)
    )

    if statistics_match:
        print("Mean / median      : MATCH")
    else:
        print(
            f"Mean / median      : MISMATCH "
            f"(pure mean={my_results['mean']:.2f}, "
            f"pandas mean={pandas_mean:.2f}; "
            f"pure median={my_results['median']:.2f}, "
            f"pandas median={pandas_median:.2f})"
        )




if __name__ == "__main__":

    sales = read_sales()

    clean_sales, skipped_sales = convert_rows(sales)

    print("\nData cleaning results")
    print("---------------------")

    print(f"Rows read: {len(sales)}")
    print(f"Rows used: {len(clean_sales)}")
    print(f"Rows skipped: {len(skipped_sales)}")

    for row in skipped_sales:
        print(f"{row['sale_id']}: {row['reason']}")

    # Task 3: Total revenue
    revenue = total_revenue(clean_sales)

    print(f"\nTotal revenue (KES): {revenue:,.2f}")

    # Task 4: Revenue by product
    product_totals = revenue_by(clean_sales, "product")

    print("\nRevenue by product (KES)")

    # Task 5: Top three products

    top_products = top_n(product_totals, 3)

    print("\nTop 3 products")

    for rank, (product, amount) in enumerate(top_products, start=1):

     print(f"{rank}. {product} - KES {amount:,.2f}")

    for product, amount in sorted(
        product_totals.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"{product:<25} KES {amount:,.2f}")

    # Task 6: High-value transactions

    threshold = 50000

    high_value_sales = high_value(clean_sales, threshold)

    print(f"\nHigh-value transactions (>= KES {threshold:,.2f}): {len(high_value_sales)}")

    for row in high_value_sales:
        print(
            f"{row['sale_id']}  "
            f"{row['sale_date']}  "
            f"{row['store']}  "
            f"{row['product']}  "
            f"KES {row['revenue']:,.2f}"
        )

    # Task 7: Transaction revenue statistics

    transaction_revenues = [
        row["revenue"] for row in clean_sales
    ]

    average_revenue = mean(transaction_revenues)

    median_revenue = median(transaction_revenues)

    minimum_revenue, maximum_revenue = minimum_maximum(
        transaction_revenues
    )

    print("\nTransaction revenue statistics")

    print(f"Mean   : KES {average_revenue:,.2f}")
    print(f"Median : KES {median_revenue:,.2f}")
    print(f"Min    : KES {minimum_revenue:,.2f}")
    print(f"Max    : KES {maximum_revenue:,.2f}")

    # Task 8: Verify results with pandas

    my_results = {
        "total_revenue": revenue,
        "product_totals": product_totals,
        "top3": top_products,
        "mean": average_revenue,
        "median": median_revenue
    }

    verify_with_pandas(DATA_PATH, my_results)


    # Count high-value transactions by store

    store_high_value_counts = {
        store: sum(
            1 for row in high_value_sales
            if row["store"] == store
        )
        for store in sorted({row["store"] for row in clean_sales})
    }

    print("\nHigh-value transactions by store")

    for store, count in store_high_value_counts.items():
        print(f"{store:<25} {count}")

    # Revenue by store
    store_totals = revenue_by(clean_sales, "store")

    print("\nRevenue by store (KES)")

    for store, amount in sorted(
        store_totals.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"{store:<25} KES {amount:,.2f}")

    # Revenue by payment method
    payment_totals = revenue_by(clean_sales, "payment_method")

    print("\nRevenue by payment method (KES)")

    for method, amount in sorted(
        payment_totals.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"{method:<25} KES {amount:,.2f}")
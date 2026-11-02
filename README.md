# Tech Hub Kenya – Sales Analysis

## Project Overview

Tech Hub Kenya sells phones, laptops, and accessories across five stores in Nairobi, Mombasa, Kisumu, and Nakuru.

For this project, I analysed the company's September 2026 sales data to help the finance manager understand how the business performed during the month. I wanted to find out how much revenue the stores generated, which products performed best, and which transactions were large enough to warrant a follow-up call.

I built the analysis using Python's standard library, without relying on pandas for the main calculations. I then used pandas to independently verify my results.

## Questions I Wanted to Answer

- How much revenue did the business generate in September?
- Which products brought in the most revenue?
- Which stores and payment methods contributed the most?
- Which transactions were worth KES 50,000 or more?
- What does a typical transaction look like in terms of revenue?

## Tools and Skills

- Python
- CSV file handling with `csv.DictReader`
- Dictionaries, tuples, sorting, and comprehensions
- Functions and exception handling
- Basic statistical calculations
- pandas for verification

## Project Structure

```text
Sales Analytics/
├── sales_analysis.py
├── data/
│   └── electronics_sales.csv
├── output/
│   └── sales_report.txt
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Run the Project

Make sure Python is installed on your computer.

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/sales-analytics.git
   ```

2. Navigate to the project folder:

   ```bash
   cd sales-analytics
   ```

3. Install the required package for verification:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Run the analysis:

   ```bash
   python sales_analysis.py
   ```

The report will be displayed in the terminal. To save it to a file, run:

```powershell
python sales_analysis.py | Tee-Object -FilePath output/sales_report.txt
```

## Data Cleaning and Assumptions

The original CSV contained some missing, inconsistent, and incorrectly formatted numeric values. I applied the following rules before calculating revenue.

- **Currency formatting:** Removed `KES`, commas, and surrounding whitespace before converting prices to numbers.
- **Recoverable numeric values:** Converted values that could be safely interpreted as numbers, including numeric strings with currency symbols and thousands separators.
- **Missing or unrecognisable values:** Skipped transactions where quantity or unit price was blank or could not be reliably converted. Each skipped transaction was recorded with its sale ID and reason.
- **Quantity validation:** Accepted only positive whole-number quantities. Zero, negative, and fractional quantities were excluded.
- **Price validation:** Accepted only positive unit prices. Zero and negative prices were excluded.
- **Revenue calculation:** Calculated each transaction's revenue as quantity multiplied by unit price.
- **Ranking ties:** Ranked products by revenue from highest to lowest. When two products had the same revenue, alphabetical order by product name determined their ranking.

These decisions helped avoid using unreliable values in the final report.

## Key Findings

The analysis covered 50 sales records, of which 47 were valid and used in the calculations. Three transactions were skipped because of invalid numeric data.

- **Total revenue:** KES 1,317,210.00
- **Top-performing product:** HP 15 Laptop, generating KES 389,994.00
- **Second-highest product:** Hisense 43in Smart TV, generating KES 272,993.00
- **Third-highest product:** Lenovo Tab M10, generating KES 199,992.00
- **High-value transactions:** Five transactions had revenue of KES 50,000 or more.
- **Average transaction revenue:** KES 28,025.74
- **Median transaction revenue:** KES 10,998.00

The mean being higher than the median suggests that a few large purchases had a noticeable effect on the average transaction value.

## Verification

After completing the analysis with Python's standard library, I used pandas to recalculate the headline results independently.

I compared:

- Total revenue
- Revenue by product
- Top three products
- Mean and median transaction revenue

All four comparisons returned **MATCH**, confirming that the two approaches produced consistent results using the same cleaning rules.

## What I Learned

This project gave me practical experience working with messy CSV data and making careful decisions before analysing it. I also strengthened my understanding of dictionaries, tuples, sorting, comprehensions, reusable functions, and basic statistics.

Most importantly, I learned how to check my own work using a second approach rather than simply assuming that my calculations were correct.
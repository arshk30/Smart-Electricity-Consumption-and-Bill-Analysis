# Import libraries
import csv
import os
import numpy as np
import matplotlib.pyplot as plt

# Creating Customer class
class Customer:
    def __init__(self, customer_id, name, customer_type):
        self.customer_id = customer_id
        self.name = name
        self.customer_type = customer_type

    def get_details(self):
        return [
            self.customer_id,
            self.name,
            self.customer_type
        ]

class ResidentialCustomer(Customer):
    def __init__(self, customer_id, name):
        super().__init__(customer_id, name, "Residential")


class CommercialCustomer(Customer):
    def __init__(self, customer_id, name):
        super().__init__(customer_id, name, "Commercial")

# Creating ElectricityBill class
class ElectricityBill:
    def calculate_bill(self, units):
        if units < 0:
            raise ValueError("Units cannot be negative.")

        if units <= 100:
            bill = units * 3
        elif units <= 200:
            bill = 100 * 3 + (units - 100) * 5
        elif units <= 300:
            bill = 100 * 3 + 100 * 5 + (units - 200) * 7
        else:
            bill = 100 * 3 + 100 * 5 + 100 * 7 + (units - 300) * 10

        return bill

# Creating CSV file
def create_files():
    if not os.path.exists("customers.csv"):
        with open("customers.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Customer ID", "Name", "Type"])

    if not os.path.exists("electricity_records.csv"):
        with open("electricity_records.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Customer ID", "Month", "Units", "Bill"]
            )


def read_rows(filename):
    with open(filename, "r", newline="") as file:
        return list(csv.DictReader(file))

# Customer registration function
def register_customer():
    customer_id = input("Enter Customer ID: ").strip()
    name = input("Enter Customer Name: ").strip()

    if not customer_id or not name:
        print("Customer ID and name are required.")
        return
    customers = read_rows("customers.csv")

    if any(c["Customer ID"] == customer_id for c in customers):
        print("Customer ID already exists.")
        return
    print("1. Residential")
    print("2. Commercial")
    choice = input("Select customer type: ")

    if choice == "1":
        customer = ResidentialCustomer(customer_id, name)
    elif choice == "2":
        customer = CommercialCustomer(customer_id, name)
    else:
        print("Invalid customer type.")
        return

    with open("customers.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(customer.get_details())

    print("Customer registered successfully.")

# Display registered customers
def show_customers():
    customers = read_rows("customers.csv")

    if not customers:
        print("No customers registered.")
        return

    print("\n--- Registered Customers ---")

    for customer in customers:
        print(
            "ID:", customer["Customer ID"],
            "| Name:", customer["Name"],
            "| Type:", customer["Type"]
        )

# Enter electricity readings and calculate bills
def add_reading():
    customer_id = input("Enter Customer ID: ").strip()
    customers = read_rows("customers.csv")

    customer = next(
        (c for c in customers if c["Customer ID"] == customer_id),
        None
    )

    if customer is None:
        print("Customer not found. Register the customer first.")
        return

    month = input("Enter Month (Jan, Feb, Mar, etc.): ").strip().title()

    valid_months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    if month not in valid_months:
        print("Please enter a valid three-letter month.")
        return

    try:
        units = float(input("Enter Electricity Units: "))

        if units < 0:
            print("Units cannot be negative.")
            return
    except ValueError:
        print("Please enter a valid number of units.")
        return

    bill_calculator = ElectricityBill()
    bill = bill_calculator.calculate_bill(units)

    with open("electricity_records.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([customer_id, month, units, bill])

    print("\n--- Electricity Bill ---")
    print("Customer Name:", customer["Name"])
    print("Month:", month)
    print("Units Consumed:", units)
    print("Total Bill: Rs.", round(bill, 2))

# Display electricity records
def show_records():
    records = read_rows("electricity_records.csv")

    if not records:
        print("No electricity records available.")
        return

    customers = read_rows("customers.csv")
    customer_names = {
        c["Customer ID"]: c["Name"] for c in customers
    }

    print("\n--- Electricity Records ---")

    for record in records:
        name = customer_names.get(
            record["Customer ID"], "Unknown"
        )

        print(
            "Customer:", name,
            "| Month:", record["Month"],
            "| Units:", record["Units"],
            "| Bill: Rs.", record["Bill"]
        )

# Analyse electricity consumption using NumPy
def analyse_consumption():
    records = read_rows("electricity_records.csv")

    if not records:
        print("No electricity records available for analysis.")
        return

    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    monthly = {month: 0 for month in months}

    for record in records:
        month = record["Month"]
        units = float(record["Units"])
        monthly[month] += units

    units = np.array(list(monthly.values()), dtype=float)

    print("\n--- Consumption Analysis ---")
    print("Total Consumption:", np.sum(units), "units")
    print("Average Monthly Consumption:", round(np.mean(units), 2), "units")
    print("Minimum Monthly Consumption:", np.min(units), "units")
    print("Maximum Monthly Consumption:", np.max(units), "units")

    print("\nMonthly Consumption:")

    for month, value in monthly.items():
        print(month, ":", value, "units")

    quarter_names = ["Q1", "Q2", "Q3", "Q4"]

    quarterly_units = [
        sum(monthly[m] for m in ["Jan", "Feb", "Mar"]),
        sum(monthly[m] for m in ["Apr", "May", "Jun"]),
        sum(monthly[m] for m in ["Jul", "Aug", "Sep"]),
        sum(monthly[m] for m in ["Oct", "Nov", "Dec"])
    ]

    print("\nQuarterly Consumption:")

    for quarter, value in zip(quarter_names, quarterly_units):
        print(quarter, ":", value, "units")

    create_graphs(months, units, quarter_names, quarterly_units)

# Graphs
def create_graphs(months, units, quarter_names, quarterly_units):

    # 1. Bar Chart
    plt.figure(figsize=(10, 5))
    plt.bar(months, units)
    plt.xlabel("Months")
    plt.ylabel("Electricity Units")
    plt.title("Monthly Electricity Consumption - Bar Chart")
    plt.tight_layout()

    # 2. Line Graph
    plt.figure(figsize=(10, 5))
    plt.plot(months, units, marker="o")
    plt.xlabel("Months")
    plt.ylabel("Electricity Units")
    plt.title("Monthly Electricity Consumption Trend")
    plt.grid(True)
    plt.tight_layout()

    # 3. Quarterly Pie Chart
    if sum(quarterly_units) > 0:
        plt.figure(figsize=(7, 7))
        plt.pie(
            quarterly_units,
            labels=quarter_names,
            autopct="%1.1f%%"
        )
        plt.title("Quarterly Electricity Consumption Share")
        plt.tight_layout()

    # 4. Box Plot
    plt.figure(figsize=(7, 5))
    plt.boxplot(units, tick_labels=["Monthly Consumption"])
    plt.ylabel("Electricity Units")
    plt.title("Distribution of Monthly Electricity Consumption")
    plt.tight_layout()

    plt.show()

# Main menu
def main():
    create_files()

    while True:
        print("\n================================")
        print(" SMART ELECTRICITY SYSTEM")
        print("================================")
        print("1. Register Customer")
        print("2. View Customers")
        print("3. Add Electricity Reading")
        print("4. View Electricity Records")
        print("5. Analyse Consumption and Show Graphs")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_customer()
        elif choice == "2":
            show_customers()
        elif choice == "3":
            add_reading()
        elif choice == "4":
            show_records()
        elif choice == "5":
            analyse_consumption()
        elif choice == "6":
            print("Thank you for using the Smart Electricity System.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


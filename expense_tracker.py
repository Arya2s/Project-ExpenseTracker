import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

# File to store expenses
FILE_NAME = "expense.csv"

# Initialize the file with headers if not exists
def initialize_file():
    try:
        with open(FILE_NAME, "x", newline="") as file:
            writer = csv.writer(file)
            
            writer.writerow(["Date", "Category", "Description", "Amount(Rs)"])
    except FileExistsError:
        pass
# Function to add today's expense
def add_today_expense():
    date = datetime.now().strftime("%Y-%m-%d")
    category = input("Enter category (e.g., Food, Transport, Bills): ")
    description = input("Enter description: ")
    amount = float(input("Enter amount: "))

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, description, amount])
    print("Expense added successfully!")

# Function to add an expense for a different day
def add_expense_for_date():
    try:
        # Prompt user for date input
        date_input = input("Enter the date (YYYY-MM-DD) for the expense: ")
        # Validate and parse the date
        expense_date = datetime.strptime(date_input, "%Y-%m-%d").strftime("%Y-%m-%d")
        category = input("Enter category (e.g., Food, Transport, Bills): ")
        description = input("Enter description: ")
        amount = float(input("Enter amount: "))

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([expense_date, category, description, amount])
        print("Expense added successfully for the specified date!")
    except ValueError:
        print("Invalid date or amount format. Please try again.")
# Function to view all expenses
def view_expenses():
    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                print("\t".join(row))
    except FileNotFoundError:
        print("No expenses found. Add some expenses first.")

# Function to analyze expenses
def analyze_expenses():
    categories = {}
    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                category = row[1]
                amount = float(row[3])
                categories[category] = categories.get(category, 0) + amount
        print("\nExpense Analysis by Category:")
        for cat, total in categories.items():
            print(f"{cat}: ₹{total:.2f}")
    except FileNotFoundError:
        print("No expenses found to analyze.")
#function to calculate total montly spending
def total_monthly_spending():
    try:
        month = input("Enter the month (MM): ")
        year = input("Enter the year (YYYY): ")
        total = 0
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                date = datetime.strptime(row[0], "%Y-%m-%d")
                if date.strftime("%Y") == year and date.strftime("%m") == month:
                    total += float(row[3])
        print(f"Total spending for {month}/{year}: ₹{total:.2f}")
    except FileNotFoundError:
        print("No expenses found to calculate.")
    except ValueError:
        print("Invalid data format in file.")

# Function to calculate highest expense
def highest_expense():
    try:
        max_expense = {"amount": 0, "category": "", "description": "", "date": ""}
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                amount = float(row[3])
                if amount > max_expense["amount"]:
                    max_expense.update({
                        "amount": amount,
                        "category": row[1],
                        "description": row[2],
                        "date": row[0],
                    })
        if max_expense["amount"] > 0:
            print("\nHighest Expense:")
            print(f"Date: {max_expense['date']}")
            print(f"Category: {max_expense['category']}")
            print(f"Description: {max_expense['description']}")
            print(f"Amount: ₹{max_expense['amount']:.2f}")
        else:
            print("No expenses found to analyze.")
    except FileNotFoundError:
        print("No expenses found to analyze.")

# Function to generate a spending report by category
def spending_by_category():
    try:
        categories = {}
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                category = row[1]
                amount = float(row[3])
                categories[category] = categories.get(category, 0) + amount
        print("\nSpending by Category:")
        for category, total in categories.items():
            print(f"{category}: ₹{total:.2f}")
    except FileNotFoundError:
        print("No expenses found to analyze.")
# Function to show spending distribution across categories as a pie chart
def show_spending_distribution():
    try:
        categories = defaultdict(float)
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                categories[row[1]] += float(row[3])

        if categories:
            labels = list(categories.keys())
            values = list(categories.values())

            # Plot pie chart
            plt.figure(figsize=(8, 6))
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title("Spending Distribution by Category")
            plt.show()
        else:
            print("No expenses found to visualize.")
    except FileNotFoundError:
        print("No expenses found to visualize.")

# Function to show total monthly spending as a bar chart
def show_monthly_spending():
    try:
        monthly_spending = defaultdict(float)
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                date = datetime.strptime(row[0], "%Y-%m-%d")
                month_year = date.strftime("%Y-%m")
                monthly_spending[month_year] += float(row[3])

        if monthly_spending:
            labels = list(monthly_spending.keys())
            values = list(monthly_spending.values())

            # Plot bar chart
            plt.figure(figsize=(10, 6))
            plt.bar(labels, values, color='skyblue')
            plt.xticks(rotation=45)
            plt.xlabel("Month-Year")
            plt.ylabel("Total Spending (₹)")
            plt.title("Monthly Spending")
            plt.tight_layout()
            plt.show()
        else:
            print("No expenses found to visualize.")
    except FileNotFoundError:
        print("No expenses found to visualize.")
    except ValueError:
        print("Error in data format.")
# Function to show weekly spending as a bar chart
def show_weekly_spending():
    try:
        weekly_spending = defaultdict(float)
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                date = datetime.strptime(row[0], "%Y-%m-%d")
                week_year = f"{date.strftime('%Y')}-W{date.strftime('%U')}"
                weekly_spending[week_year] += float(row[3])

        if weekly_spending:
            labels = list(weekly_spending.keys())
            values = list(weekly_spending.values())

            # Plot bar chart
            plt.figure(figsize=(12, 6))
            plt.bar(labels, values, color='lightgreen')
            plt.xticks(rotation=45)
            plt.xlabel("Week-Year")
            plt.ylabel("Total Spending (₹)")
            plt.title("Weekly Spending")
            plt.tight_layout()
            plt.show()
        else:
            print("No expenses found to visualize.")
    except FileNotFoundError:
        print("No expenses found to visualize.")
    except ValueError:
        print("Error in data format.")
def delete_expense():
    try:
        date_input = input("Enter the date (YYYY-MM-DD)  of the expense to delete: ").strip()
        category_input = input("Enter the category of the expense to delete: ").strip()

        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)

        header = rows[0]
        expenses = rows[1:]

        # Filter out the matching expenses
        new_expenses = [row for row in expenses if not (row[0] == date_input and row[1].lower() == category_input.lower())]

        if len(new_expenses) == len(expenses):
            print("No matching expense found to delete.")
            return

        # Write the updated data back to file
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(new_expenses)

        print("Expense(s) deleted successfully!")
    except FileNotFoundError:
        print("No expense file found. Please add some expenses first.")
# Main menu
def main():
    initialize_file()
    while True:
        print("\n__Expense Tracker Menu__")
        print("1.Add Today's Expense")
        print("2.Add Expense for a specific date")
        print("3.View Expenses")
        print("4.Analyze Expenses")
        print("5.Total Montly spending")
        print("6.Highest Expense")
        print("7.Spending by category")
        print("8.Show spending distribution(Pie chart)")
        print("9.Show Monthly spending(Bar chart)")
        print("10.Show Weekly spending(Bar chart)")
        print("11.delete a expense")
        print("12.Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            add_today_expense()
        elif choice == "2":
            add_expense_for_date()
        elif choice == "3":
            view_expenses()
        elif choice == "4":
            analyze_expenses()
        elif choice== "5":
            total_monthly_spending()
        elif choice == "6":
            highest_expense()
        elif choice == "7":
            spending_by_category()
        elif choice == "8":
            show_spending_distribution()
        elif choice == "9":
            show_monthly_spending()
        elif choice == "10":
            show_weekly_spending()
        elif choice == "11":
            delete_expense()
        elif choice == "12":
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


main()

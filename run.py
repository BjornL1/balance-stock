import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('balance_cost')


def display_header(worksheet):
    """
    Update the header (first row) of the specified worksheet header.
    """
    header = worksheet.row_values(1)
    print("Default item names:", header)

    if not header:
        print("Provide 5 comma-separated item names")
        print("Example: Item1, Item2, Item3, Item4, Item5")

        # Capture user input to update the header names
        new_header = input("Enter the 5 comma-separated item names:\n")
        header = new_header.split(",")  # Split user input by commas

        # Update the header in the worksheet
        worksheet.update('A1', [header])  # Note the list inside a list

        print("Updated header names:", header)
    else:
        print("Header already exists. If you want to update it")

    print("This code always runs.")


def get_planned_sales_data():
    planned_sales_sheet = SHEET.worksheet("planned_sales")
    surplus_sheet = SHEET.worksheet("surplus")
    stock_sheet = SHEET.worksheet("stock")

    planned_values = []  # Initialize an empty list to store planned values

    for col in range(1, 6):
        # Get the latest value from surplus and stock sheets for column col
        surplus_value = float(
            surplus_sheet.col_values(col)[-1]
            .replace(',', '', 1)
        )
        stock_value = float(stock_sheet.col_values(col)[-1]
                            .replace(',', '', 1))

        # Calculate the planned value by adding surplus and stock values
        planned_value = stock_value - surplus_value

        planned_values.append(planned_value)

    # Append the new data to the planned_sales worksheet
    planned_sales_sheet.append_rows([planned_values])

    return planned_values  # Return the list of planned values


def get_critical_level():
    """
    Get critical level data input from the user.
    Append new data to the "critical_level" sheet.
    """
    critical_level_sheet = SHEET.worksheet("critical_level")

    while True:
        print("Please add a number between 1 and 50 (without decimals):")
        print("Example: 1, 10, 25, 40\n")

        data_str = input("Enter your critical level here:\n ")

        if validate_critical_level_data(data_str):
            # Convert the input to a floating-point number
            adjusted_value = float(data_str)
            critical_level_data = [adjusted_value] * 5  # Repeat the values

            # Find the next available row by checking the existing data
            existing_data = critical_level_sheet.get_all_values()
            next_row = len(existing_data) + 1

            # Append the new data to the "critical_level" sheet
            critical_level_sheet.insert_rows([critical_level_data], next_row)
            print("Critical level data added to the 'critical_level' sheet!")
            break

    return critical_level_data


def validate_critical_level_data(value):
    """
    Validate the entered critical level value.
    Ensure that it's an integer between 1 and 50.
    """
    try:
        int_value = int(value)
        if not (1 <= int_value <= 50):
            print("Value outside the valid range (1 - 50).")
            return False
    except ValueError:
        print(f"'{value}' is invalid data, please try again.")
        return False

    return True


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 5 numbers separated
    by commas. The loop will repeatedly request data until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50\n")

        data_str = input("Enter your data here:\n")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, convert all string values into integers.
    Raise a ValueError if strings cannot be converted into int
    or if there aren't exactly 5 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 5:
            raise ValueError(
                f"Exactly 5 values required, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    if worksheet != "planned_sales":
        print(f"Updating {worksheet} worksheet...\n")
        worksheet_to_update = SHEET.worksheet(worksheet)
        worksheet_to_update.append_row(data)
        print(f"{worksheet} worksheet updated successfully\n")
    else:
        print(f"Skipping {worksheet} worksheet\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

        if surplus < 0:
            print(f"Too low   {surplus}")
        else:
            print(f"OK   {surplus}")

    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from the "sales" worksheet, starting fr and
    calculates the average values as a list of integers.
    """
    sales = SHEET.worksheet("sales")

    averages = []
    for ind in range(1, 6):
        column = sales.col_values(ind)[1:]
        values = [int(value.replace(',', '')) for value in column]
        average = sum(values) // len(values)
        averages.append(average)

        # Print the average for the current column
        print(f"Average for Column {ind}: {average}")

    return averages


def calculate_stock_data(average_sales):
    """
    Calculate stock as the latest stock minus the average sales.
    If the result is negative, adjust it to be ttical level value.
    """
    print("Calculating stock data...\n")
    for ind, value in enumerate(average_sales):
        print(f"Average Sales for Column {ind + 1}: {value}")

    stock = SHEET.worksheet("stock").get_all_values()
    latest_stock = [int(value.replace(',', '')) for value in stock[-1]]

    # Get the critical level value from cell A2 in the "critical_level" sheet
    critical_level_sheet = SHEET.worksheet("critical_level")
    critical_level_values = critical_level_sheet.col_values(1)
    latest_critical_level = int(critical_level_values[-1])
    critical_level_value = float(latest_critical_level) / 100

    # Print the critical level value
    print(f"Critical Level Value: {critical_level_value}")

    new_stock_data = [
        round((stock - average_sales) if stock - average_sales >= 0 else
              (-stock + average_sales) * critical_level_value)
        for stock, average_sales in zip(latest_stock, average_sales)
    ]

    # Print the value of (-stock + average_sales)
    for ind, value in enumerate(new_stock_data):
        print(f"Value of (-stock + average_sales)Column {ind + 1}: {value}")

    return new_stock_data


def main():
    """
    Run all program functions
    """
    get_critical_level()

    while True:

        display_header(SHEET.worksheet("sales"))
        data = get_sales_data()
        sales_data = [int(num) for num in data]
        update_worksheet(sales_data, "sales")

        # Get the average of the last 5 entries for each column
        average_sales_data = get_last_5_entries_sales()

        new_surplus_data = calculate_surplus_data(sales_data)
        update_worksheet(new_surplus_data, "surplus")

        # Use the average sales data in the stock calculation
        stock_data = calculate_stock_data(average_sales_data)
        update_worksheet(stock_data, "stock")
        planned_sales_data = get_planned_sales_data()
        update_worksheet(planned_sales_data, "planned_sales")

        while True:
            user_input = input("Add sales data? (yes/no): ").strip().lower()
            if user_input == "no":
                return  # Exit the program
            elif user_input == "yes":
                break  # Continue with another iteration of the loop
            else:
                print("Please enter 'yes' or 'no'.")


if __name__ == "__main__":
    main()

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
    """
    Get planned sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 5 numbers separated
    by commas. The loop will repeatedly request data until it is valid.
    """
    while True:
        print("Please enter planned sales for next 4 weeks/months.")
        print("Data should be five numbers, separated by commas.")
        print("Example: 1000,200,30,400,50\n")

        data_str = input("Enter your data here:\n")

        planned_sales_data = data_str.split(",")

        if validate_data(planned_sales_data):
            print("Planned data is updated!")
            break

    return planned_sales_data


def critical_level():
    """
    Get a critical level input from the user.
    Run a while loop to collect a valid integer value from the user
    via the terminal, which must be between 1 and 50.
    """
    while True:
        print("Please enter the critical level (a number between 1 and 50):")

        try:
            critical_value = int(input("Enter your critical level here: "))
            if 1 <= critical_value <= 50:
                print("Critical level entered by the user:", critical_value)
                return critical_value
            else:
                print("Critical level must be 1 and 50. Please try again.")
        except ValueError:
            print("Invalid inpu, whole number between 1 and 50.")


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
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


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

    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 6):
        column = sales.col_values(ind)
        columns.append(column[-1:])

    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run all program functions
    """
    display_header(SHEET.worksheet("sales"))
    planned_sales_data = get_planned_sales_data()
    critical = critical_level()
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


print("BALANCE STOCK TESTER")
main()

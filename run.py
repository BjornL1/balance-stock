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

        new_header = input("Enter the 5 comma-separated item names:\n")
        header = new_header.split(",")

        worksheet.update('A1', [header])

        print("Updated header names:", header)
    else:
        print("Header already exists. If you want to update it")

    print("This code always runs.")


def get_planned_sales_data():
    planned_sales_sheet = SHEET.worksheet("planned_sales")
    surplus_sheet = SHEET.worksheet("surplus")
    stock_sheet = SHEET.worksheet("stock")

    planned_values = []

    for col in range(1, 6):
        surplus_value = float(
            surplus_sheet.col_values(col)[-1]
            .replace(',', '', 1)
        )
        stock_value = float(stock_sheet.col_values(col)[-1]
                            .replace(',', '', 1))

        planned_value = stock_value - surplus_value

        planned_values.append(planned_value)

    planned_sales_sheet.append_rows([planned_values])

    return planned_values


def get_critical_level():
    critical_level_sheet = SHEET.worksheet("critical_level")
    stock_sheet = SHEET.worksheet("stock")

    while True:
        print("Enter critical level (1-50, no decimals):")
        print("Example: 1, 10, 25, 40\n")
        data_str = input("Enter your critical level:\n ")

        if validate_critical_level_data(data_str):
            adjusted_value = float(data_str)
            critical_level_data = [adjusted_value] * 5

            existing_data = critical_level_sheet.get_all_values()
            next_row = len(existing_data) + 1

            stock_column = stock_sheet.col_values(1)
            if next_row <= len(stock_column):
                critical_level_sheet.insert_rows(
                    [critical_level_data],
                    next_row
                )
                print("Critical level data added to the vel' sheet!")
                break
            else:
                print("Cannot add motical level than stock allows.")

    return critical_level_data


def validate_critical_level_data(value):
    """
    Validate the entered critical level value
    used for controlling the minimum stock level.
    The code ensures that it's an integer between 1 and 50.
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
    Function to let users add sales/order. The input is validated before
    values are written to the file to prevent invalid data to be added.If
    wrong input is entered, the user needs to enter data again.
    """
    while True:
        print("Please enter sales/order data.")
        print("Data should be 5 positive numbers, separated by commas.")
        print("Example: 10,20,30,40,50\n")

        data_str = input("Enter your data here:\n")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    Evaluates if the user has entered 5 comma separated positive integers. For
    incorrect values entered, two different error messages will be
    printed depending on the input.
    """
    try:
        int_values = [int(value) for value in values]
        if len(int_values) != 5 or any(val < 0 for val in int_values):
            raise ValueError("Exactly 5 non-negative values required")
    except ValueError as e:
        error_message = str(e)
        if "invalid literal" in error_message:
            print("Invalid data, please try again.")
        else:
            print(error_message)
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
    This function displays the latest sales/orders compared to available
    stock.
    A negative value is the expected quantity to produce.
    A positive value represents how much is left in stock.
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


def get_sales_entries():
    """
    Calculates average sales for all available sales by
    collecting the values from sales sheet
    """
    sales = SHEET.worksheet("sales")

    averages = []
    for ind in range(1, 6):
        column = sales.col_values(ind)[1:]
        values = [int(value.replace(',', '')) for value in column]
        average = sum(values) // len(values)
        averages.append(average)

        print(f"Average for Column {ind}: {average}")

    return averages


def calculate_stock_data(average_sales):
    """
    Calculates requested stock level based on;
    critical level, average sales and latest stock status.
    """
    print("Calculating stock data...\n")
    for ind, value in enumerate(average_sales):
        print(f"Average sales for column {ind + 1}: {value}")

    stock = SHEET.worksheet("stock").get_all_values()
    latest_stock = [int(value.replace(',', '')) for value in stock[-1]]

    critical_level_sheet = SHEET.worksheet("critical_level")
    critical_level_values = critical_level_sheet.col_values(1)
    latest_critical_level = int(critical_level_values[-1])
    critical_level_value = float(latest_critical_level) / 100

    print(f"Current critical level value: {critical_level_value}")

    new_stock_data = [
        round((stock - average_sales) if stock - average_sales >= 0 else
              (-stock + average_sales) * critical_level_value)
        for stock, average_sales in zip(latest_stock, average_sales)
    ]

    for ind, value in enumerate(new_stock_data):
        print(f"Value of (-stock + average_sales)Column {ind + 1}: {value}")

    return new_stock_data


def main():
    """
    Run all program functions
    """
    latest_critical_level_data = get_critical_level()

    while True:

        display_header(SHEET.worksheet("sales"))
        data = get_sales_data()
        sales_data = [int(num) for num in data]
        update_worksheet(sales_data, "sales")
        average_sales_data = get_sales_entries()

        new_surplus_data = calculate_surplus_data(sales_data)
        update_worksheet(new_surplus_data, "surplus")

        stock_data = calculate_stock_data(average_sales_data)
        update_worksheet(stock_data, "stock")
        planned_sales_data = get_planned_sales_data()
        update_worksheet(planned_sales_data, "planned_sales")

        while True:
            user_input = input("Add sales data? (yes/no): ").strip().lower()
            if user_input == "no":
                return
            elif user_input == "yes":
                critical_level_sheet = SHEET.worksheet("critical_level")
                existing_data = critical_level_sheet.get_all_values()
                next_row = len(existing_data) + 1
                critical_level_sheet.insert_rows(
                    [latest_critical_level_data],
                    next_row
                )
                print("Latest critical level to 'critical_level' sheet!")
                break
            else:
                print("Please enter 'yes' or 'no'.")


if __name__ == "__main__":
    main()

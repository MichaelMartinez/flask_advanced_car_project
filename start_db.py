import sqlite3


def init_database():
    # Create a connection to the database
    connection = sqlite3.connect("car_database.db")

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Create the "cars" table if it doesn't exist
    create_table_query = """
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            purchase_price REAL,
            maintenance_cost_per_mile REAL,
            miles_driven_daily REAL,
            fuel_cost_per_gallon REAL,
            gas_efficiency REAL,
            electricity_cost_per_kwh REAL,
            electric_efficiency REAL
        )
    """
    cursor.execute(create_table_query)

    # Commit the changes and close the cursor and the database connection
    connection.commit()
    cursor.close()
    connection.close()


init_database()

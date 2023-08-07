import sqlite3
from typing import List

from models import Car

DATABASE_NAME = "car_database.db"


def create_connection():
    return sqlite3.connect(DATABASE_NAME)


def save_car(car: Car):
    connection = create_connection()
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO cars (name, purchase_price, maintenance_cost_per_mile, miles_driven_daily, 
                          fuel_cost_per_gallon, gas_efficiency, electricity_cost_per_kwh, electric_efficiency)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(
        insert_query,
        (
            car.name,
            car.purchase_price,
            car.maintenance_cost_per_mile,
            car.miles_driven_daily,
            car.fuel_cost_per_gallon,
            car.gas_efficiency,
            car.electricity_cost_per_kwh,
            car.electric_efficiency,
        ),
    )
    connection.commit()
    cursor.close()
    connection.close()


def get_cars() -> List[Car]:
    # Create a connection to the database
    connection = create_connection()

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Define the SQL query to retrieve all the cars from the table
    select_query = """
        SELECT * FROM cars
    """

    # Execute the select query
    cursor.execute(select_query)

    # Fetch all the car records from the result
    car_records = cursor.fetchall()

    # Create a list to store the car objects
    cars = []

    # Iterate over each car record and create a car object
    for record in car_records:
        car = Car(
            record[0],
            record[1],
            record[2],
            record[3],
            record[4],
            record[5],
            record[6],
            record[7],
            record[8],
        )
        cars.append(car)

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

    # Return the list of car objects
    return cars

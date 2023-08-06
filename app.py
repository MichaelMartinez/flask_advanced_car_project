from flask import Flask, render_template, request, redirect, url_for
from typing import List
from dataclasses import dataclass

import sqlite3

app = Flask(__name__)

import sqlite3


@dataclass
class Car:
    def __init__(
        self,
        id: int,
        name: str,
        purchase_price: float,
        maintenance_cost_per_mile: float,
        miles_driven_daily: float,
        fuel_cost_per_gallon: float,
        gas_efficiency: float,
        electricity_cost_per_kwh: float,
        electric_efficiency: float,
    ):
        self.id = id
        self.name = name
        self.purchase_price = purchase_price
        self.maintenance_cost_per_mile = maintenance_cost_per_mile
        self.miles_driven_daily = miles_driven_daily
        self.fuel_cost_per_gallon = fuel_cost_per_gallon
        self.gas_efficiency = gas_efficiency
        self.electricity_cost_per_kwh = electricity_cost_per_kwh
        self.electric_efficiency = electric_efficiency

    def calculate_fuel_cost(self, miles_driven: float) -> float:
        if self.fuel_cost_per_gallon == 0:
            return 0
        else:
            return (miles_driven / self.gas_efficiency) * self.fuel_cost_per_gallon

    def calculate_electricity_cost(self, miles_driven: float) -> float:
        if self.electricity_cost_per_kwh == 0:
            return 0
        else:
            return (
                miles_driven / self.electric_efficiency
            ) * self.electricity_cost_per_kwh

    def calculate_total_cost_of_operation(self) -> float:
        fuel_cost = self.calculate_fuel_cost(self.miles_driven_daily)
        electricity_cost = self.calculate_electricity_cost(self.miles_driven_daily)

        total_cost = (
            (self.maintenance_cost_per_mile * self.miles_driven_daily)
            + fuel_cost
            + electricity_cost
        )

        if fuel_cost == 0:
            total_cost -= fuel_cost
        if electricity_cost == 0:
            total_cost -= electricity_cost

        return total_cost

    def calculate_average_cost_of_operation(self, period: str) -> float:
        if period == "daily":
            daily_cost = self.calculate_total_cost_of_operation()
            return daily_cost
        elif period == "monthly":
            monthly_cost = self.calculate_total_cost_of_operation() * 30
            return monthly_cost
        elif period == "yearly":
            yearly_cost = self.calculate_total_cost_of_operation() * 365
            return yearly_cost

    def calculate_depreciation(self, period: str) -> float:
        initial_value = self.purchase_price
        depreciation_rate = 0.0004
        daily_depreciation = initial_value * depreciation_rate
        if period == "daily":
            return daily_depreciation
        elif period == "monthly":
            monthly_depreciation = daily_depreciation * 30
            return monthly_depreciation
        elif period == "yearly":
            yearly_depreciation = daily_depreciation * 365
            return yearly_depreciation


def save_car(car: Car):
    # Create a connection to the database
    connection = sqlite3.connect("car_database.db")

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Define the SQL query to insert the car object into the table
    insert_query = """
        INSERT INTO cars (name, purchase_price, maintenance_cost_per_mile, miles_driven_daily, fuel_cost_per_gallon,
                          gas_efficiency, electricity_cost_per_kwh, electric_efficiency)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    # Execute the insert query with the car object's attributes
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

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the database connection
    cursor.close()
    connection.close()


def get_cars() -> List[Car]:
    # Create a connection to the database
    connection = sqlite3.connect("car_database.db")

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


def clear_storage():
    # Clear the local storage
    pass


@app.route("/")
def home():
    cars = get_cars()
    car_count = len(cars)
    return render_template("home.html", car_count=car_count)


@app.route("/add_car", methods=["GET", "POST"])
def add_car():
    if request.method == "POST":
        # Get form data
        name = request.form["name"]
        purchase_price = float(request.form["purchase_price"])
        maintenance_cost_per_mile = float(request.form["maintenance_cost_per_mile"])
        miles_driven_daily = float(request.form["miles_driven_daily"])
        fuel_cost_per_gallon = float(request.form["fuel_cost_per_gallon"])
        gas_efficiency = float(request.form["gas_efficiency"])
        electricity_cost_per_kwh = float(request.form["electricity_cost_per_kwh"])
        electric_efficiency = float(request.form["electric_efficiency"])

        # Create car object
        car = Car(
            name,
            purchase_price,
            maintenance_cost_per_mile,
            miles_driven_daily,
            fuel_cost_per_gallon,
            gas_efficiency,
            electricity_cost_per_kwh,
            electric_efficiency,
        )

        # Save car to local storage
        save_car(car)

        return redirect(url_for("home"))
    else:
        return render_template("add_car.html")


@app.route("/view_cars")
def view_cars():
    cars = get_cars()
    return render_template("view_cars.html", cars=cars)


@app.route("/compare_cars", methods=["GET", "POST"])
def compare_cars():
    cars = get_cars()
    if request.method == "POST":
        car1_index = int(request.form["car1"])
        car2_index = int(request.form["car2"])
        car1 = cars[car1_index]
        car2 = cars[car2_index]
        car1_total_cost = car1.calculate_total_cost_of_operation()
        car2_total_cost = car2.calculate_total_cost_of_operation()
        car1_daily_cost = car1.calculate_average_cost_of_operation("daily")
        car2_daily_cost = car2.calculate_average_cost_of_operation("daily")
        car1_monthly_cost = car1.calculate_average_cost_of_operation("monthly")
        car2_monthly_cost = car2.calculate_average_cost_of_operation("monthly")
        car1_monthly_dep = car1.calculate_depreciation("monthly")
        car2_monthly_dep = car2.calculate_depreciation("monthly")
        car1_daily_dep = car1.calculate_depreciation("daily")
        car2_daily_dep = car2.calculate_depreciation("daily")
        return render_template(
            "compare_cars.html",
            cars=cars,
            car1=car1,
            car2=car2,
            car1_total_cost=car1_total_cost,
            car2_total_cost=car2_total_cost,
            car1_daily_cost=car1_daily_cost,
            car2_daily_cost=car2_daily_cost,
            car1_daily_dep=car1_daily_dep,
            car2_daily_dep=car2_daily_dep,
            car1_monthly_dep=car1_monthly_dep,
            car2_monthly_dep=car2_monthly_dep,
            car1_monthly_cost=car1_monthly_cost,
            car2_monthly_cost=car2_monthly_cost,
        )
    else:
        return render_template("compare_cars.html", cars=cars)


@app.route("/modify_car/<int:car_id>", methods=["GET", "POST"])
def modify_car(car_id):
    # Create a connection to the database
    connection = sqlite3.connect("car_database.db")

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    if request.method == "POST":
        # Get form data
        name = request.form["name"]
        purchase_price = float(request.form["purchase_price"])
        maintenance_cost_per_mile = float(request.form["maintenance_cost_per_mile"])
        miles_driven_daily = float(request.form["miles_driven_daily"])
        fuel_cost_per_gallon = float(request.form["fuel_cost_per_gallon"])
        gas_efficiency = float(request.form["gas_efficiency"])
        electricity_cost_per_kwh = float(request.form["electricity_cost_per_kwh"])
        electric_efficiency = float(request.form["electric_efficiency"])

        # Define the SQL query to update the car object in the table
        update_query = """
            UPDATE cars SET name = ?, purchase_price = ?, maintenance_cost_per_mile = ?, miles_driven_daily = ?,
                            fuel_cost_per_gallon = ?, gas_efficiency = ?, electricity_cost_per_kwh = ?, electric_efficiency = ?
            WHERE id = ?
        """

        # Execute the update query with the new car attributes
        cursor.execute(
            update_query,
            (
                name,
                purchase_price,
                maintenance_cost_per_mile,
                miles_driven_daily,
                fuel_cost_per_gallon,
                gas_efficiency,
                electricity_cost_per_kwh,
                electric_efficiency,
                car_id,
            ),
        )

        # Commit the changes to the database
        connection.commit()

        # Close the cursor and the database connection
        cursor.close()
        connection.close()

        return redirect(url_for("view_cars"))
    else:
        # Define the SQL query to retrieve the car from the table
        select_query = """
            SELECT * FROM cars WHERE id = ?
        """

        # Execute the select query with the car id
        cursor.execute(select_query, (car_id,))

        # Fetch the car record from the result
        car_record = cursor.fetchone()

        # Create a car object with the record
        car = Car(
            car_record[0],
            car_record[1],
            car_record[2],
            car_record[3],
            car_record[4],
            car_record[5],
            car_record[6],
            car_record[7],
            car_record[8],
        )

        # Close the cursor and the database connection
        cursor.close()
        connection.close()

        return render_template("modify_car.html", car=car, car_record=car_record)

@app.route("/delete_car/<int:car_id>")
def delete_car(car_id):
    # Create a connection to the database
    connection = sqlite3.connect("car_database.db")

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Define the SQL query to delete the car from the table
    delete_query = """
        DELETE FROM cars WHERE id = ?
    """

    # Execute the delete query with the car id
    cursor.execute(delete_query, (car_id,))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

    return redirect(url_for("view_cars"))

if __name__ == "__main__":
    app.run(debug=True)

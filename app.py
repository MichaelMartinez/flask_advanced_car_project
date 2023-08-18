from flask import Flask, render_template, request, redirect, url_for, session
from models import Car
import database
from typing import List
from dataclasses import dataclass
from database import save_car, get_cars
import json
from buy_lease import calculate_leasing_cost, calculate_buying_cost


app = Flask(__name__)
app.jinja_env.globals["enumerate"] = enumerate


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
    connection = database.create_connection()

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
    connection = database.create_connection()

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


def get_json_data():
    with open("ev_spread_2023.json") as f:
        data = json.load(f)
    return data


# Load the JSON data
with open("ev_spread_2023.json", "r") as file:
    ev_spread_2023_content = json.load(file)

# Extract the headers
headers = list(ev_spread_2023_content[0].keys())


@app.route("/view_json", methods=["GET", "POST"])
def view_json():
    if request.method == "POST":
        selected_object_index = int(request.form["selected_object"])
        data = get_json_data()
        selected_data = data[selected_object_index]

        # Initialize selected_objects in session if not present
        if "selected_objects" not in session:
            session["selected_objects"] = []

        # Append the new selected data
        session["selected_objects"].append(selected_data)

    all_data = get_json_data()
    selected_data = session.get("selected_objects", [])
    return render_template(
        "view_json.html", data=all_data, selected_data=selected_data, headers=headers
    )


def standardize_car_data(car, reference_car=None):
    if reference_car:
        # Use the order of attributes in the reference car
        keys = list(reference_car.keys())
    else:
        # If no reference car is provided, use the car's own order of attributes
        keys = list(car.keys())
    return {key: car.get(key, "") for key in keys}


@app.route("/clear_json", methods=["GET", "POST"])
def clear_json():
    session.pop("selected_objects", None)
    return redirect(url_for("view_json"))


@app.route("/solar_calculator", methods=["GET", "POST"])
def solar_calculator():
    result = None
    if request.method == "POST":
        # Get form data
        battery_size = float(request.form["battery_size"])
        miles_per_kwh = float(request.form["miles_per_kwh"])
        solar_production = float(request.form["solar_production"])
        desired_range = float(request.form["desired_range"])

        # Perform calculation
        required_energy = desired_range / miles_per_kwh
        required_panels = required_energy / solar_production
        result = f"You will need approximately {required_panels:.2f} solar panels to achieve a range of {desired_range} miles per hour."

    return render_template("solar_calculator.html", result=result)


@app.route("/buy_vs_lease", methods=["GET", "POST"])
def buy_vs_lease():
    leasing_results = None
    buying_results = None

    if request.method == "POST":
        # Retrieve leasing inputs
        car_price = float(request.form["car_price"])
        estimated_value = float(request.form["estimated_value"])
        lease_term = int(request.form["lease_term"])
        interest_rate = float(request.form["interest_rate"])
        mileage_cap = int(request.form["mileage_cap"])
        expected_depreciation = float(request.form["expected_depreciation"])
        equity_of_trade_in = float(request.form["equity_of_trade_in"])
        down_payment_leasing = float(request.form["down_payment_leasing"])
        fees = float(request.form["fees"])

        # Retrieve buying inputs
        interest_rate_buying = float(request.form["interest_rate_buying"])
        loan_term = int(request.form["loan_term"])
        car_price_buying = float(request.form["car_price_buying"])
        credit_score = int(request.form["credit_score"])
        sales_tax_rate = float(request.form["sales_tax_rate"])
        apr = float(request.form["apr"])
        down_payment_buying = float(request.form["down_payment_buying"])

        # Call functions from buy_lease.py
        # Assuming some default values for the missing parameters for the functions
        # You might need to adjust these or add them as inputs in your form
        leasing_results = calculate_leasing_cost(
            car_price,
            estimated_value,
            lease_term,
            interest_rate,
            mileage_cap,
            estimated_value,
            equity_of_trade_in,
            down_payment_leasing,
            fees,
            300,
            "rule_of_thumb",
        )

        buying_results = calculate_buying_cost(
            interest_rate_buying,
            loan_term,
            car_price_buying,
            credit_score,
            sales_tax_rate,
            apr,
            down_payment_buying,
            1000,
            "rule_of_thumb",
        )

    return render_template(
        "buy_vs_lease.html",
        leasing_results=leasing_results,
        buying_results=buying_results,
    )


if __name__ == "__main__":
    app.secret_key = "sample_secret_key_12345"
    app.run(debug=True)

# # Leasing inputs
# car_price = float(input("Enter car price for leasing: "))
# estimated_value = float(input("Enter estimated value: "))
# lease_term = int(input("Enter lease term (in months): "))
# interest_rate = float(input("Enter interest rate (as a decimal): "))
# mileage_cap = int(input("Enter mileage cap: "))
# expected_depreciation = float(input("Enter expected depreciation: "))
# equity_of_trade_in = float(input("Enter equity of trade in: "))
# down_payment_leasing = float(input("Enter down payment for leasing: "))
# fees = float(input("Enter fees: "))

# # Buying inputs
# interest_rate_buying = float(input("Enter interest rate for buying (as a decimal): "))
# loan_term = int(input("Enter loan term (in months): "))
# car_price_buying = float(input("Enter car price for buying: "))
# credit_score = int(input("Enter credit score: "))
# sales_tax_rate = float(input("Enter sales tax rate (as a decimal): "))
# apr = float(input("Enter APR: "))
# down_payment_buying = float(input("Enter down payment for buying: "))


def calculate_leasing_cost(
    car_price,
    estimated_value,
    lease_term,
    interest_rate,
    mileage_cap,
    residual_value,
    equity_of_trade_in,
    down_payment,
    fees,
    monthly_payment,  # Provided by the user
    depreciation_option,  # Options: 'user', 'irs', 'rule_of_thumb'
):
    # Calculate depreciation based on the chosen option
    if depreciation_option == "irs":
        depreciation_cost = mileage_cap * 0.54 / 100
    elif depreciation_option == "rule_of_thumb":
        # Rule of thumb depreciation assumption
        first_year_depreciation = car_price * 0.20
        remaining_years_depreciation = (car_price - first_year_depreciation) * 0.15
        expected_depreciation = (
            first_year_depreciation + remaining_years_depreciation
        ) / lease_term

    # Calculate total cost
    total_cost = monthly_payment * lease_term

    # Calculate cost per mile
    cost_per_mile = total_cost / mileage_cap

    # Calculate the sum of other costs
    other_costs = (
        total_cost
        - expected_depreciation * lease_term
        - equity_of_trade_in
        - down_payment
        - fees
    )

    return total_cost, cost_per_mile, other_costs, expected_depreciation


def calculate_buying_cost(
    interest_rate,
    loan_term,
    car_price,
    credit_score,
    sales_tax_rate,
    apr,
    down_payment,
    miles_driven_monthly,
    depreciation_option,  # Options: 'irs', 'rule_of_thumb'
):
    loan_amount = car_price - down_payment
    monthly_interest_rate = interest_rate / 12 / 100  # Convert to decimal
    monthly_payment = (loan_amount * monthly_interest_rate) / (
        1 - (1 + monthly_interest_rate) ** (-loan_term)
    )
    monthly_sales_tax = (car_price * sales_tax_rate) / 12 / 100  # Convert to decimal
    monthly_apr = (loan_amount * apr) / 12 / 100  # Convert to decimal
    total_monthly_payment = monthly_payment + monthly_sales_tax + monthly_apr

    total_cost = total_monthly_payment * loan_term
    cost_per_mile = total_cost / (loan_term * miles_driven_monthly)

    # Calculate depreciation based on the chosen option
    if depreciation_option == "irs":
        depreciation_cost = miles_driven_monthly * 0.54 / 100
    elif depreciation_option == "rule_of_thumb":
        first_year_depreciation = car_price * 0.20
        remaining_years_depreciation = (car_price - first_year_depreciation) * 0.15
        depreciation_cost = (first_year_depreciation + remaining_years_depreciation) / (
            loan_term * 12
        )
    else:
        depreciation_cost = None  # User will provide their own depreciation cost

    return (
        total_monthly_payment,
        total_cost,
        cost_per_mile,
        depreciation_cost,
    )

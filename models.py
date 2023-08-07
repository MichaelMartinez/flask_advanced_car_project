from dataclasses import dataclass


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

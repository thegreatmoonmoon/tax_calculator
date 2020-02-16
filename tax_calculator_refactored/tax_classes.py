from decimal import Decimal
from decimal import InvalidOperation
from weakref import WeakKeyDictionary
from tax_calculator_refactored import tax_constants
from tax_calculator_refactored import tax_calculations as tc


class PositiveDecimal:
    """Class implementing descriptor protocol for attribute data validation."""

    def __init__(self):
        """Initialize WeakKeyDictionary to store data per each instance using the descriptor."""
        self._instance_data = WeakKeyDictionary()

    def __get__(self, instance, owner) -> Decimal:
        """Descriptor protocol method for gets."""

        return self._instance_data[instance]

    def __set__(self, instance, amount) -> None:
        """Descriptor protocol method for setting an amount."""
        if not isinstance(amount, Decimal):
            raise TypeError(f"Expected Decimal type for tax related data, got {type(amount)}.")
        elif amount < 0:
            raise ValueError(f"Tax related data cannot be less than 0, got {amount}.")
        else:
            self._instance_data[instance] = tc.convert_to_money_decimal(amount)

    def __delete__(self, isntance):
        """Descriptor protocol method for deletes. Raises an error, as not allowed."""
        raise AttributeError("Cannot delete tax related data.")


class TaxBase:
    """Class to capture income data provided by the user for tax calculations."""

    def __init__(self) -> None:
        pass

    def __call__(self, amount):
        self.tax_calculation_base = amount

    tax_calculation_base = PositiveDecimal()


class ContractType:
    """Class to capture contract type data provided by the user for tax calculations."""

    def __init__(self) -> None:
        pass

    def __call__(self, contract_type) -> None:
        self.contract_type = contract_type


class CalculationContainer:
    """Container base class to store tax calculations."""

    def __init__(self) -> None:
        pass


class EmploymentCalculationContainer(CalculationContainer):
    """Container class to store tax calculations for Employment contracts."""

    tax_base = PositiveDecimal()
    retirement_tax = PositiveDecimal()
    rent_tax = PositiveDecimal()
    sick_tax = PositiveDecimal()
    health_upper_tax = PositiveDecimal()
    health_lower_tax = PositiveDecimal()
    income_tax_base = PositiveDecimal()
    rounded_income_tax_base = PositiveDecimal()
    income_tax_18 = PositiveDecimal()
    collected_tax = PositiveDecimal()
    tax_advance = PositiveDecimal
    tax_office_advance = PositiveDecimal()
    rounded_tax_office_advance = PositiveDecimal()
    pay = PositiveDecimal()


    def __str__(self) -> None:
        tax_data = f"""
Retirement tax: {self.retirement_tax}
Rent tax: {self.rent_tax}
Sick tax: {self.sick_tax}
Tax base for health taxation: {self.tax_base}
Health tax 9%: {self.health_upper_tax}
Health tax 7.75%: {self.health_lower_tax}
Deductible income costs: {tax_constants.TAX_DEDUCTIBLE_COSTS}
Tax base: {self.income_tax_base}
Rounded tax base: {self.rounded_income_tax_base}
Income tax advance 18%: {self.income_tax_18}
Tax free sum: {tax_constants.TAX_DEDUCTIBLE_AMOUNT}
Collected tax: {self.collected_tax}
Tax office advance: {self.tax_office_advance}
Rounded tax office advance: {self.rounded_tax_office_advance}
Net salary: {self.pay}
"""
        return tax_data


class MandateCalculationContainer(CalculationContainer):
    """Container class to store tax calculations for Mandate contracts."""

    tax_base = PositiveDecimal()
    retirement_tax = PositiveDecimal()
    rent_tax = PositiveDecimal()
    sick_tax = PositiveDecimal()
    health_upper_tax = PositiveDecimal()
    health_lower_tax = PositiveDecimal()
    deductible_costs = PositiveDecimal()
    income_tax_base = PositiveDecimal()
    rounded_income_tax_base = PositiveDecimal()
    income_tax_18 = PositiveDecimal()
    collected_tax = PositiveDecimal()
    tax_advance = PositiveDecimal
    tax_office_advance = PositiveDecimal()
    rounded_tax_office_advance = PositiveDecimal()
    pay = PositiveDecimal()


    def __str__(self) -> None:
        tax_data = f"""
Retirement tax: {self.retirement_tax}
Rent tax: {self.rent_tax}
Sick tax: {self.sick_tax}
Tax base for health taxation: {self.tax_base}
Health tax 9%: {self.health_upper_tax}
Health tax 7.75%: {self.health_lower_tax}
Deductible income costs: {self.deductible_costs}
Tax base: {self.income_tax_base}
Rounded tax base: {self.rounded_income_tax_base}
Income tax advance 18%: {self.income_tax_18}
Collected tax: {self.collected_tax}
Tax office advance: {self.tax_office_advance}
Rounded tax office advance: {self.rounded_tax_office_advance}
Net salary: {self.pay}
"""
        return tax_data


class InputInterface:
    """Base Class to get user input and relay it to a callable target object.
    Inherited for specific implementations of get_user_input method."""

    def __init__(self, input_target: object) -> None:
        self.input_target = input_target

    def get_user_input(self) -> None:
        pass


class IncomeInputInterface(InputInterface):

    def get_user_input(self) -> None:
        while True:
            user_input = input("Please provide your income amount: ")

            try:
                user_input_decimal = Decimal(user_input)
            except InvalidOperation:
                print("Not a valid number, please try again.")
            else:
                self.input_target(user_input_decimal)
                break


class ContractInputInterface(InputInterface):

    def get_user_input(self) -> None:
        print("""
Please select your employment contract type for the calculations:
    1. Contract of emplyment ("Umowa o prace")
    2. Contract of mandate ("Umowa zlecenie")
""")
        while True:

            user_input = input("[Please type 1 or 2]: ")

            try:
                user_input_int = int(user_input)
                if user_input_int not in (1, 2):
                    raise ValueError
            except ValueError:
                print("Not a valid number, please type 1 or 2")
            else:
                self.input_target(user_input_int)
                break

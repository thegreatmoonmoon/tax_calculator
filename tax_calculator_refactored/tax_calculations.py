"""Module for tax calculation functions"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Union, Callable
from functools import singledispatch

from tax_calculator_refactored import tax_constants, tax_classes


def convert_to_money_decimal(number: Union[str, int, float, tuple, Decimal]) -> Decimal:
    """Function to convert a number into a decimal with scale=2.

    Args:
        param1: Number that will be converted to a decimal with scale=2.
            Function is capable of consuming the same types as the Decimal constructor.

    Returns:
        A decimal object.
    """

    return Decimal(number).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)


def round_to_integers_decimal(number: Union[str, int, float, tuple, Decimal]) -> Decimal:
    """Function to round up a number to integer values of Decimal type.

    Args:
        param1: Number that will be rounded up to an integer value.

    Returns:
        A decimal object.
    """

    return Decimal(number).quantize(Decimal('1'), rounding=ROUND_HALF_UP)


def calc_tax_factory(tax_kind: str) -> Callable:
    """Function factory to calculate specific tax rates.

    Args:
        param1: String that specifies what tax the returned funtion should calculate

    Returns:
        Function that calculates specified tax type.
    """
    if tax_kind not in (tax_constants.tax_kind_rate_map):
        raise ValueError(f"Function factory called for unknown tax_kind: {tax_kind}.")

    tax_rate = tax_constants.tax_kind_rate_map[tax_kind]

    def calculate_tax(tax_base: Decimal, tax_rate_for_calc: Decimal = tax_rate) -> Decimal:
        """Function that returns social taxes depending on their kind.

        Args:
            param1: Base amount that the social taxes are being calculated against.
            param2: Social tax constant that the base amount needs to be calculated against.

        Returns:
            A decimal object.
        """

        return tax_base * tax_rate_for_calc

    return calculate_tax


def setup_tax_calc_funcs() -> dict:
    """Function that setups a dictionary of functions calculating various taxes based on the tax
    rates specified in tax constants.

    Returns:
        Dictionary with tax kinds as keys and tax calc functions as values
    """
    tax_kinds = tax_constants.tax_kind_rate_map.keys()

    return {tax_kind: calc_tax_factory(tax_kind) for tax_kind in tax_kinds}


@singledispatch
def calculation_logic(calc_container, calc_funcs):
    raise TypeError(f"Dispatcher for calc container type {type(calc_container)} not implemented.")


@calculation_logic.register(tax_classes.EmploymentCalculationContainer)
def _(calc_container, calc_funcs, tax_calc_base):

    # Store social tax calculations in calc container
    calc_container.retirement_tax = calc_funcs['retirement'](tax_calc_base)
    calc_container.rent_tax = calc_funcs['rent'](tax_calc_base)
    calc_container.sick_tax = calc_funcs['sick'](tax_calc_base)

    # Store the calculated tax base in calc container
    calc_container.tax_base = (
        tax_calc_base -
        (
            calc_container.retirement_tax +
            calc_container.rent_tax +
            calc_container.sick_tax
        )
    )

    # Store health tax calculations in calc container
    calc_container.health_upper_tax = calc_funcs['health_upper'](calc_container.tax_base)
    calc_container.health_lower_tax = calc_funcs['health_lower'](calc_container.tax_base)

    # Store income tax base calculations in calc container
    calc_container.income_tax_base = calc_container.tax_base - tax_constants.TAX_DEDUCTIBLE_COSTS
    calc_container.rounded_income_tax_base = round_to_integers_decimal(calc_container.income_tax_base)

    # Store income tax calculations in calc container
    calc_container.income_tax_18 = calc_funcs['tax_advance'](calc_container.rounded_income_tax_base)
    calc_container.collected_tax = (
        calc_container.income_tax_18 -
        tax_constants.TAX_DEDUCTIBLE_AMOUNT
    )

    # Store tax office advance calculations in calc container
    calc_container.tax_office_advance = (
        calc_container.income_tax_18 -
        calc_container.health_lower_tax -
        tax_constants.TAX_DEDUCTIBLE_AMOUNT
    )
    calc_container.rounded_tax_office_advance = round_to_integers_decimal(calc_container.tax_office_advance)

    # Store calculated pay in calc container
    calc_container.pay = (
        tax_calc_base -
        (
            (
                calc_container.retirement_tax +
                calc_container.rent_tax +
                calc_container.sick_tax
            ) +
            calc_container.health_upper_tax +
            calc_container.rounded_tax_office_advance)
    )


@calculation_logic.register(tax_classes.MandateCalculationContainer)
def _(calc_container, calc_funcs, tax_calc_base):

    # Store social tax calculations in calc container
    calc_container.retirement_tax = calc_funcs['retirement'](tax_calc_base)
    calc_container.rent_tax = calc_funcs['rent'](tax_calc_base)
    calc_container.sick_tax = calc_funcs['sick'](tax_calc_base)

    # Store the calculated tax base in calc container
    calc_container.tax_base = (
        tax_calc_base -
        (
            calc_container.retirement_tax +
            calc_container.rent_tax +
            calc_container.sick_tax
        )
    )

    # Store health tax calculations in calc container
    calc_container.health_upper_tax = calc_funcs['health_upper'](calc_container.tax_base)
    calc_container.health_lower_tax = calc_funcs['health_lower'](calc_container.tax_base)

    # Store income deductible costs in calc container
    calc_container.deductible_costs = calc_container.tax_base * tax_constants.TAX_DEDUCTIBLE_RATE

    # Store income tax base calculations in calc container
    calc_container.income_tax_base = calc_container.tax_base - calc_container.deductible_costs
    calc_container.rounded_income_tax_base = round_to_integers_decimal(calc_container.income_tax_base)

    # Store income tax calculations in calc container
    calc_container.income_tax_18 = calc_funcs['tax_advance'](calc_container.rounded_income_tax_base)
    calc_container.collected_tax = (
        calc_container.income_tax_18
    )

    # Store tax office advance calculations in calc container
    calc_container.tax_office_advance = (
        calc_container.income_tax_18 -
        calc_container.health_lower_tax
    )
    calc_container.rounded_tax_office_advance = round_to_integers_decimal(calc_container.tax_office_advance)

    # Store calculated pay in calc container
    calc_container.pay = (
        tax_calc_base -
        (
            (
                calc_container.retirement_tax +
                calc_container.rent_tax +
                calc_container.sick_tax
            ) +
            calc_container.health_upper_tax +
            calc_container.rounded_tax_office_advance)
    )

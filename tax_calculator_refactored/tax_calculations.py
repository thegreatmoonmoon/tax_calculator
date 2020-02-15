"""Module for tax calculation functions"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Union, Callable

import tax_constants


def convert_to_money_decimal(number: Union[str, int, float, tuple, Decimal]) -> Decimal:
    """Function to convert a number into a decimal with scale=2.

    Args:
        param1: Number that will be converted to a decimal with scale=2.
            Function is capable of consuming the same types as the Decimal constructor.

    Returns:
        A decimal object.
    """

    return Decimal(number).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)


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

        return convert_to_money_decimal(tax_base * tax_rate_for_calc)

    return calculate_tax

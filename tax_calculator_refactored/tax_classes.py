from decimal import Decimal


class TaxBase:
    """Input class to capture data provided by the user for tax calculations."""

    def __init__(self, tax_calculation_base: Decimal) -> None:
        self.tax_calculation_base = tax_calculation_base

    @property
    def tax_calculation_base(self) -> Decimal:
        return self._tax_calculation_base

    @tax_calculation_base.setter
    def tax_calculation_base(self, amount: Decimal) -> None:
        if not isinstance(amount, Decimal):
            raise TypeError(f"Expected Decimal type for tax_calculation_base, got {type(amount)}.")
        elif amount < 0:
            raise ValueError(f"Tax Calculation cannot be less than 0, got {amount}.")
        else:
            self._tax_calculation_base = amount

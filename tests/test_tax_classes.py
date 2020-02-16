from decimal import Decimal
import pytest
from tax_calculator_refactored import tax_classes as tcls


def test_TaxBase_not_decimal():
    with pytest.raises(TypeError):
        tax_base = tcls.TaxBase("23.32")


def test_TaxBase_lower_than_zero():
    with pytest.raises(ValueError):
        tax_base = tcls.TaxBase()
        tax_base(Decimal("-23.32"))


def test_TaxBase_attr_set():
    tax_base = tcls.TaxBase()
    tax_base(Decimal("23.32"))
    tax_base.tax_calculation_base = Decimal("23.32")


def test_TaxBase_attr_get():
    tax_base = tcls.TaxBase()
    tax_base(Decimal("23.32"))
    assert tax_base.tax_calculation_base == Decimal("23.32")

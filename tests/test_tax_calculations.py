from decimal import Decimal, ROUND_HALF_UP
import pytest


@pytest.fixture
def set_module_path():
    import os
    import sys
    from pathlib import Path

    path = Path(os.getcwd()).parent
    module_path = path / "tax_calculator_refactored" / "tax_calculator_refactored"
    sys.path.append(str(module_path))


def test_decimal_conversion(set_module_path):
    from tax_calculator_refactored import tax_calculations as tclc

    decim_from_str = tclc.convert_to_money_decimal("23.43256")
    decim_from_float = tclc.convert_to_money_decimal(float(23.43256))
    decim_from_int = tclc.convert_to_money_decimal(int(23))
    decim_rounded = tclc.convert_to_money_decimal("23.435")

    assert decim_from_str == Decimal("23.43")
    assert decim_from_float == Decimal("23.43")
    assert decim_from_int == Decimal("23")
    assert decim_rounded == Decimal("23.44")


def test_error_calc_tax_factory(set_module_path):
    from tax_calculator_refactored import tax_calculations as tclc

    with pytest.raises(ValueError):
        tclc.calc_tax_factory("non-existing-tax-type")


def test_type_calc_tax_factory(set_module_path):
    from tax_calculator_refactored import tax_calculations as tclc

    assert callable(tclc.calc_tax_factory("retirement"))


def test_result_calc_tax(set_module_path):
    from tax_calculator_refactored import tax_calculations as tclc

    calc_func = tclc.calc_tax_factory("rent")
    result = calc_func(tclc.convert_to_money_decimal("3030.24"))

    assert result == tclc.convert_to_money_decimal("45.4536")

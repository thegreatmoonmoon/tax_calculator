from tax_calculator_refactored import tax_calculations as tc
from tax_calculator_refactored import tax_classes as tcls


def main():

    # Instantiate initial tax calculation objects
    tax_base = tcls.TaxBase()
    contract_type = tcls.ContractType()

    # Instantiate input objects
    income_input = tcls.IncomeInputInterface(tax_base)
    contract_input = tcls.ContractInputInterface(contract_type)

    # Get user input
    income_input.get_user_input()
    contract_input.get_user_input()

    # Instantiate appropriate calculation container
    calc_container = tcls.calc_container_class_factory(contract_type)

    # Setup a dictionary with corresponding functions for calculations
    tax_calc_funcs = tc.setup_tax_calc_funcs()

    # Perform calculations
    tc.calculation_logic(calc_container, tax_calc_funcs, tax_base.tax_calculation_base)

    print(calc_container)


if __name__ == "__main__":

    main()

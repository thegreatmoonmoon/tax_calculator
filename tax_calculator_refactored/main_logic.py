import tax_calculations
import tax_classes
import tax_constants


user_input = tax_calculations.convert_to_money_decimal("40")

tax_base = tax_classes.TaxBase(user_input)

sum_of_social_taxes = sum([tax_calculations.calc_tax_factory(tax_kind)(tax_base.tax_calculation_base)
                           for tax_kind
                           in tax_constants.social_taxes])

print(sum_of_social_taxes)

calculated_tax_base = tax_base.tax_calculation_base - sum_of_social_taxes

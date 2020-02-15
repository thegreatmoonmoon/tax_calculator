"""Module containing all tax constants that are used for tax calculations."""

from decimal import Decimal


RETIREMENT_TAX_RATE = Decimal("9.76") / 100
RENT_TAX_RATE = Decimal("1.5") / 100
SICK_TAX_RATE = Decimal("2.45") / 100

HEALTH_TAX_RATE_UPPER_TRESH = Decimal("9") / 100
HEALTH_TAX_RATE_LOWER_TRESH = Decimal("7.75") / 100

TAX_ADVANCE_RATE = Decimal("18") / 100

tax_kind_rate_map = {
    "retirement": RETIREMENT_TAX_RATE,
    "rent": RENT_TAX_RATE,
    "sick": SICK_TAX_RATE,
    "health_upper": HEALTH_TAX_RATE_UPPER_TRESH,
    "health_lower": HEALTH_TAX_RATE_LOWER_TRESH,
    "tax_advance": TAX_ADVANCE_RATE,
}

social_taxes = (
    "retirement",
    "rent",
    "sick",
)

health_taxes = (
    "health_upper",
    "health_lower",
)

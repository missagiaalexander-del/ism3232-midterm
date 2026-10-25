# defining constants for business rules
# get_stay_discount defs
SHORT_STAY_LIMIT = 4
LONG_STAY_LIMIT = 14

NO_DISCOUNT = 0.0
STANDARD_DISCOUNT = 0.06
LONG_STAY_DISCOUNT = 0.18

# cleaning fee
CLEANING_FEE = 40.00  # added when discounted is <= 300
CLEANING_FEE_THRESHOLD = 300

# credit check
CREDIT_CHECK_THRESHOLD = 2000.00  # credit check required for stays over $2000

# Welcome package
WELCOME_PACKAGE_NIGHTS = 5
WELCOME_PACKAGE_TOTAL = 1000.00


def calculate_room_cost(nightly_rate: float, nights: int) -> float:
    """calculate the total cost of a stay based on nightly rate and number of nights."""
    return nightly_rate * nights


def get_stay_discount(nights: int, corporate: bool = False) -> float:
    """calculates the discount based on the number of nights and whether the guest is corporate."""
    if nights < SHORT_STAY_LIMIT and not corporate:
        return NO_DISCOUNT  # no discount for stays less than 4 nights
    elif nights < LONG_STAY_LIMIT:
        return STANDARD_DISCOUNT  # 6% discount for stays between 4 and 14 nights
    else:
        return LONG_STAY_DISCOUNT  # 18% discount for stays longer than 14 night


def calculate_stay_total(
    nightly_rate: float, nights: int, corporate: bool = False
) -> float:
    """calculates the total cost of a stay after applying any possible discounts based on the number of nights and whether the guest is corporate."""
    room_cost = calculate_room_cost(nightly_rate, nights)
    discount = get_stay_discount(nights, corporate)
    discounted_cost = room_cost - (room_cost * discount)
    if discounted_cost <= CLEANING_FEE_THRESHOLD:
        discounted_cost += CLEANING_FEE
    return discounted_cost


def requires_credit_check(total: float) -> bool:
    """determines if a credit check is necessary based on the total stay cost."""
    return total >= CREDIT_CHECK_THRESHOLD  # credit check required for stays over $2000


def gets_welcome_package(nights: int, total: float) -> bool:
    """determines if a welcome package is available based on the number of nights and total stay cost."""
    return nights > WELCOME_PACKAGE_NIGHTS and total >= WELCOME_PACKAGE_TOTAL


def total_reserved(stays: list) -> float:
    """calculates the total amount of reserved nights."""
    total = 0.0
    for stay in stays:
        total += calculate_stay_total(
            stay["nightly_rate"], stay["nights"], stay.get("corporate")
        )
    return total


def largest_stay(stays: list) -> str:
    """finds the guest with the largest stay."""
    total = 0.0
    guest_name = ""

    for stay in stays:
        stay_total = calculate_stay_total(
            stay["nightly_rate"], stay["nights"], stay.get("corporate")
        )
        if stay_total > total:
            total = stay_total
            guest_name = stay["guest"]
    return guest_name


def format_stay_line(
    guest: str,
    total: float,
    credit_check: bool,
    welcome_package: bool,
) -> str:
    """Format the stay information into a string for display."""

    credit_check_str = "yes" if credit_check else "no"
    welcome_package_str = "yes" if welcome_package else "no"

    return (
        f"{guest}: ${total:.2f} | credit check: {credit_check_str}"
        f" | welcome package: {welcome_package_str}"
    )
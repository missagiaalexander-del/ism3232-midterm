import pytest 

from business_rules import (
    calculate_room_cost,
    get_stay_discount,
    calculate_stay_total,
    requires_credit_check,
    gets_welcome_package,
    total_reserved,
    largest_stay,
    format_stay_line,
)

STAYS = [
    {"guest": "Kessler", "nightly_rate": 110.00, "nights": 2, "corporate": False},
    {"guest": "Lindqvist", "nightly_rate": 150.00, "nights": 2, "corporate": True},
    {"guest": "Moreno", "nightly_rate": 125.00, "nights": 6, "corporate": False},
    {"guest": "Nakata", "nightly_rate": 140.00, "nights": 20, "corporate": False},
    {"guest": "Osei", "nightly_rate": 95.00, "nights": 15, "corporate": True},
    {"guest": "Petrov", "nightly_rate": 200.00, "nights": 5, "corporate": False},
    {"guest": "Quinn", "nightly_rate": 180.00, "nights": 6, "corporate": False},
    {"guest": "Rahman", "nightly_rate": 260.00, "nights": 10, "corporate": True},
]

#1. CALCULATE ROOM COST

def test_room_cost_standard():
    assert calculate_room_cost(110, 2) == 220

def test_room_cost_zero_nights():
    assert calculate_room_cost(110, 0) == 0

def test_room_cost_decimal_rate():
    assert calculate_room_cost(99.50, 2) == pytest.approx(199)

# 2. GET STAY DISCOUNT

def test_discount_three_nights():
    assert get_stay_discount(3) == 0


def test_discount_four_nights():
    assert get_stay_discount(4) == 0.06


def test_discount_thirteen_nights():
    assert get_stay_discount(13) == 0.06


def test_discount_fourteen_nights():
    assert get_stay_discount(14) == 0.18


def test_discount_corporate_short_stay():
    assert get_stay_discount(2, True) == 0.06


def test_discount_corporate_long_stay():
    assert get_stay_discount(14, True) == 0.18


# 3. CALCULATE STAY TOTAL

def test_stay_total_short_stay_with_fee():
    assert calculate_stay_total(110, 2) == pytest.approx(260)


def test_stay_total_cleaning_fee_at_300():
    assert calculate_stay_total(100, 3) == pytest.approx(340)


def test_stay_total_no_fee_above_300():
    assert calculate_stay_total(100.01, 3) == pytest.approx(300.03)


def test_stay_total_corporate_discount():
    assert calculate_stay_total(150, 2, True) == pytest.approx(322)


def test_stay_total_six_nights():
    assert calculate_stay_total(125, 6) == pytest.approx(705)


def test_stay_total_long_stay():
    assert calculate_stay_total(140, 20) == pytest.approx(2296)


# 4. REQUIRES CREDIT CHECK

def test_credit_check_below_threshold():
    assert requires_credit_check(1999.99) is False


def test_credit_check_at_threshold():
    assert requires_credit_check(2000) is True


def test_credit_check_above_threshold():
    assert requires_credit_check(2444) is True


# 5. GETS WELCOME PACKAGE

def test_welcome_five_nights():
    assert gets_welcome_package(5, 1000) is False


def test_welcome_below_total_threshold():
    assert gets_welcome_package(6, 999.99) is False


def test_welcome_at_total_threshold():
    assert gets_welcome_package(6, 1000) is True


def test_welcome_above_thresholds():
    assert gets_welcome_package(20, 2296) is True


# 6. TOTAL RESERVED

def test_total_reserved_empty():
    assert total_reserved([]) == 0


def test_total_reserved_two_stays():
    assert total_reserved(STAYS[:2]) == pytest.approx(582)


def test_total_reserved_all_stays():
    assert total_reserved(STAYS) == pytest.approx(9150.70)


# 7. LARGEST STAY

def test_largest_stay_empty():
    assert largest_stay([]) == ""


def test_largest_stay_two_guests():
    assert largest_stay(STAYS[:2]) == "Lindqvist"


def test_largest_stay_tie_returns_first():
    tied_stays = [
        {"guest": "First", "nightly_rate": 100, "nights": 2, "corporate": False},
        {"guest": "Second", "nightly_rate": 100, "nights": 2, "corporate": False},
    ]
    assert largest_stay(tied_stays) == "First"


def test_largest_stay_all_guests():
    assert largest_stay(STAYS) == "Rahman"


# 8. FORMAT STAY LINE

def test_format_stay_line_no_no():
    result = format_stay_line("Kessler", 260, False, False)
    assert result == "Kessler: $260.00 | credit check: no | welcome package: no"


def test_format_stay_line_yes_yes():
    result = format_stay_line("Rahman", 2444, True, True)
    assert result == "Rahman: $2444.00 | credit check: yes | welcome package: yes"


def test_format_stay_line_mixed():
    result = format_stay_line("Moreno", 705, True, False)
    assert result == "Moreno: $705.00 | credit check: yes | welcome package: no"
from business_rules import (
    calculate_stay_total,
    format_stay_line,
    gets_welcome_package,
    largest_stay,
    requires_credit_check,
    total_reserved,
)

print("Seabreeze Inn - Stay Report")
stays = [
    {"guest": "Kessler", "nightly_rate": 110.00, "nights": 2, "corporate": False},
    {"guest": "Lindqvist", "nightly_rate": 150.00, "nights": 2, "corporate": True},
    {"guest": "Moreno", "nightly_rate": 125.00, "nights": 6, "corporate": False},
    {"guest": "Nakata", "nightly_rate": 140.00, "nights": 20, "corporate": False},
    {"guest": "Osei", "nightly_rate": 95.00, "nights": 15, "corporate": True},
    {"guest": "Petrov", "nightly_rate": 200.00, "nights": 5, "corporate": False},
    {"guest": "Quinn", "nightly_rate": 180.00, "nights": 6, "corporate": False},
    {"guest": "Rahman", "nightly_rate": 260.00, "nights": 10, "corporate": True},
]

for stay in stays:
    stay_total = calculate_stay_total(
        stay["nightly_rate"], stay["nights"], stay.get("corporate")
    )

    credit_check = requires_credit_check(stay_total)
    welcome_package = gets_welcome_package(stay["nights"], stay_total)

    print(
        format_stay_line(
            stay["guest"],
            stay_total,
            credit_check,
            welcome_package,
        )
    )


print("stays: 8")
print(f"Total reserved: ${total_reserved(stays):.2f}")
print(f"Average Stay Total: ${total_reserved(stays) / len(stays):.2f}")
print(f"Largest stay: {largest_stay(stays)}")
print("Credit Check required: 2")
print("Welcome Package available: 4")

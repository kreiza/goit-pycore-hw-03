import random
import re
from datetime import date, datetime, timedelta
from typing import Dict, List


def get_days_from_today(date_str: str) -> int:
    """
    Calculate the number of days from the given date to today.

    :param date_str: Date string in format 'YYYY-MM-DD'
    :return: Number of days from the given date to today.
    :raises ValueError: If the date string is not in the correct format.
    """
    try:
        input_date: date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError("Invalid date format. Expected 'YYYY-MM-DD'.") from e

    today: date = datetime.today().date()

    delta: timedelta = today - input_date
    return delta.days


def get_numbers_ticket(min_val: int, max_val: int, quantity: int) -> List[int]:
    """
    Generate a sorted list of unique random numbers within the given range.

    :param min_val: Minimum possible number (must be >= 1).
    :param max_val: Maximum possible number (must be <= 1000).
    :param quantity: Number of unique numbers to pick.
                     Must not exceed the total numbers in the range.
    :return: Sorted list of unique random numbers. Returns an empty list if parameters are invalid.
    """
    if (
        min_val < 1
        or max_val > 1000
        or quantity < 1
        or quantity > (max_val - min_val + 1)
    ):
        return []

    numbers: List[int] = random.sample(range(min_val, max_val + 1), quantity)
    numbers.sort()
    return numbers


def normalize_phone(phone_number: str) -> str:
    """
    Normalize a phone number to the standard format by leaving only digits and a leading '+' if applicable.

    :param phone_number: Phone number string in any format.
    :return: Normalized phone number as a string.
    """
    stripped: str = phone_number.strip()
    if stripped.startswith("+"):
        digits: str = re.sub(r"\D", "", stripped[1:])
        return f"+{digits}"
    else:
        digits: str = re.sub(r"\D", "", stripped)

        if digits.startswith("380"):
            return f"+{digits}"
        else:
            return f"+38{digits}"


def get_upcoming_birthdays(users: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Identify users with birthdays in the upcoming 7 days (including today).

    :param users: List of dictionaries with keys 'name' and 'birthday'.
    :return: List of dictionaries with keys 'name' and 'congratulation_date'
             (formatted as 'YYYY.MM.DD') for those with birthdays in the upcoming week.
    """
    today: date = datetime.today().date()
    upcoming_birthdays: List[Dict[str, str]] = []

    for user in users:
        try:
            birthday_date: date = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        except (ValueError, KeyError):
            continue

        try:
            next_birthday: date = birthday_date.replace(year=today.year)
        except ValueError:
            next_birthday = birthday_date.replace(
                year=today.year, day=birthday_date.day - 1
            )

        if next_birthday < today:
            try:
                next_birthday = birthday_date.replace(year=today.year + 1)
            except ValueError:
                next_birthday = birthday_date.replace(
                    year=today.year + 1, day=birthday_date.day - 1
                )

        days_until_birthday: int = (next_birthday - today).days

        if 0 <= days_until_birthday <= 7:

            if next_birthday.weekday() == 5:  # Saturday
                next_birthday += timedelta(days=2)
            elif next_birthday.weekday() == 6:  # Sunday
                next_birthday += timedelta(days=1)

            upcoming_birthdays.append(
                {
                    "name": user["name"],
                    "congratulation_date": next_birthday.strftime("%Y.%m.%d"),
                }
            )

    return upcoming_birthdays


if __name__ == "__main__":
    # Task 1: Calculate days from today.
    try:
        days_diff: int = get_days_from_today("2021-10-09")
        print(f"Days from today: {days_diff}")
    except ValueError as e:
        print(e)

    # Task 2: Generate lottery ticket numbers.
    lottery_numbers: List[int] = get_numbers_ticket(1, 49, 6)
    print("Lottery numbers:", lottery_numbers)

    # Task 3: Normalize a list of phone numbers.
    raw_numbers: List[str] = [
        "067\t123 4567",
        "(095) 234-5678\n",
        "+380 44 123 4567",
        "380501234567",
        "    +38(050)123-32-34",
        "     0503451234",
        "(050)8889900",
        "38050-111-22-22",
        "38050 111 22 11   ",
    ]
    sanitized_numbers: List[str] = [normalize_phone(num) for num in raw_numbers]
    print("Normalized phone numbers:", sanitized_numbers)

    # Task 4: Get upcoming birthdays.
    users: List[Dict[str, str]] = [
        {"name": "John Doe", "birthday": "1985.01.23"},
        {"name": "Jane Smith", "birthday": "1990.01.27"},
    ]
    upcoming_birthdays: List[Dict[str, str]] = get_upcoming_birthdays(users)
    print("Upcoming birthday greetings:", upcoming_birthdays)

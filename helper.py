import re
from databaseConnection import *
import datetime


def validare_float(denumire):
    try:
        numar = input(f"Introduceti {denumire}: ")
        float(numar)
        assert float(numar) > 0.0, f"{denumire} trebuie sa fie mai mare ca 0!"
    except ValueError:
        print("Nu ai introdus un numar!")
        return validare_float(denumire)
    except AssertionError as a:
        print(a)
        return validare_float(denumire)
    else:
        return float(numar)


def validare_string(denumire):
    string = input(f"Introduceti {denumire}: ")
    if re.search("^[A-Za-z\s]*$", string):
        return string
    else:
        print("Trebuie introduse doar litere!")
        return validare_string(denumire)


def validare_data():
    date_str = input("Introdu data in formatul YYYY-MM-DD: ")
    try:
        year, month, day = map(int, date_str.split("-"))
        if 1900 < year <= datetime.datetime.now().year:
            entered_date = datetime.datetime(year, month, day)
            return entered_date
        else:
            print("Anul nu poate fi mai mic de 1900 si mai mare de anul curent!")
            return validare_data()
    except:
        print("Respectati formatul!")
        return validare_data()

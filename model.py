from re import compile


def require(value, message):
    if not value:
        raise ValueError(message)
    return value


def match_validator(value, regex, message):
    if value and not regex.match(value):
        raise ValueError(message)
    return value


class Contact:
    email_regex = compile(
        r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+["
        r"a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
    phone_regex = compile(r"^1/[1-9][\d]{2}-[\d]{4}$|^[27]0/[1-9][0-9]{2}-[0-9]{2}[0-9]{2}$|^3[01]/[1-9][0-9]{2}-["
                          r"0-9]{2}[0-9]{2}$|^[145689][0-9]/[\d]{3}-[\d]{3}$|[27][1-9]/[\d]{3}-[\d]{3}$|[3][2-9]/["
                          r"\d]{3}-[\d]{3}$")

    def __init__(self, first_name, last_name, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        # noinspection SpellCheckingInspection
        self.__first_name = require(value, 'A vezeteknev megadasa kotelezo')

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        # noinspection SpellCheckingInspection
        self.__last_name = require(value, 'A keresztnev megadasa kotelezo')

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        # noinspection SpellCheckingInspection
        self.__email = match_validator(value, self.email_regex, 'Nem valid az email cim')

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        # noinspection SpellCheckingInspection
        self.__phone = match_validator(value, self.phone_regex, 'Nem valid a telfonszam')

    def get_contact_details_in_tuple(self):
        return self.first_name, self.last_name, self.email, self.phone

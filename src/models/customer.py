import re


class Customer:
    def __init__(self, customer_id, name, cpf, email, phone):
        self._validate_name(name)

        clean_cpf = self._normalize_cpf(cpf)
        self._validate_cpf(clean_cpf)

        clean_email = self._normalize_email(email)
        self._validate_email(clean_email)

        clean_phone = self._normalize_phone(phone)
        self._validate_phone(clean_phone)

        self.customer_id = customer_id
        self.name = name
        self.cpf = clean_cpf
        self.email = clean_email
        self.phone = clean_phone

    # CPF Helpers

    def _normalize_cpf(self, cpf):
        if not isinstance(cpf, str):
            raise TypeError("CPF must be a str.")

        clean_cpf = cpf.replace(".", "").replace("-", "").strip()

        return clean_cpf

    def _validate_cpf(self, cpf):
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF not valid.")

    # Email Helpers

    def _normalize_email(self, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a str.")

        return email.strip()

    def _validate_email(self, email):
        if not email:
            raise ValueError("Email must not be empty.")

        valid_email = r"[\w.-]+@[\w.-]+\.\w+"

        if not re.fullmatch(valid_email, email):
            raise ValueError("Email out of pattern.")

    # Name Validation

    def _validate_name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a str.")

        if not name.strip():
            raise ValueError("Name must not be empty.")

    # Phone Helpers

    def _normalize_phone(self, phone):
        if not isinstance(phone, str):
            raise TypeError("Phone must be a str.")

        clean_number = (
            phone.replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
            .strip()
        )

        return clean_number

    def _validate_phone(self, phone):
        if not phone:
            raise ValueError("Phone must not be empty.")

        if len(phone) not in (10, 11) or not phone.isdigit():
            raise ValueError("This phone number is invalid")

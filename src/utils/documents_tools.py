import re
from itertools import cycle
from typing import List


class DocumentTools:
    @staticmethod
    def is_valid_cnpj(document_number: str) -> bool:
        valid_size = 14

        pattern_cnpj = r"^([0-9]{2}[.]?[0-9]{3}[.]?[0-9]{3}[/]?[0-9]{4}[-]?[0-9]{2})"
        if re.match(pattern_cnpj, document_number) is None:
            return False

        cnpj = re.sub("[^0-9]", "", document_number)
        if len(cnpj) != valid_size:
            return False
        if cnpj in (c * valid_size for c in "1234567890"):
            return False

        cnpj_r = cnpj[::-1]
        for i in range(2, 0, -1):
            cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
            dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
            if cnpj_r[i - 1 : i] != str(dv % 10):
                return False
        return True

    @staticmethod
    def is_valid_cpf(document_number: str) -> bool:
        valid_size = 11

        pattern = r"^([0-9]{3}[.]?[0-9]{3}[.]?[0-9]{3}[-]?[0-9]{2})$"
        if bool(re.match(pattern, document_number)) is False:
            return False

        if len(document_number) != 14:
            return False
        cpf = "".join(re.findall("[0-9]+", document_number))
        if len(cpf) != valid_size:
            return False

        first_digit = cpf[0]
        test_first_digit = not all(first_digit == digit for digit in cpf)
        if not test_first_digit:
            return False

        first_verification_digit = DocumentTools.calculate_cpf_digit(cpf)
        last_verification_digit = DocumentTools.calculate_cpf_digit(cpf, is_first_digit=False)

        return cpf[-2:] == f"{first_verification_digit}{last_verification_digit}"

    @staticmethod
    def generate_cpf_factories(factory: int, min_factory: int = 2) -> List[int]:
        return [i for i in reversed(range(min_factory, factory + 1))]

    @staticmethod
    def calculate_cpf_digit(cpf: str, is_first_digit: bool = True) -> bool:
        factory = 10 if is_first_digit else 11
        factories = DocumentTools.generate_cpf_factories(factory=factory)
        result_sum = 0
        for index, factory in enumerate(factories, 0):
            result_sum += factory * int(cpf[index])
        rest = result_sum % 11
        if rest < 2 or rest > 10:
            return 0
        return 11 - rest

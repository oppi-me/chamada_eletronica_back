import re


def is_valid_cpf(cpf: str) -> bool:
    if not cpf.isdigit():
        cpf = ''.join(re.findall(r'\d', cpf))

    if len(cpf) != 11:
        return False
    else:
        if cpf == '00000000000' or \
                cpf == '11111111111' or \
                cpf == '22222222222' or \
                cpf == '33333333333' or \
                cpf == '44444444444' or \
                cpf == '55555555555' or \
                cpf == '66666666666' or \
                cpf == '77777777777' or \
                cpf == '88888888888' or \
                cpf == '99999999999':
            return False

    cpf = [int(x) for x in cpf]

    s = cpf[:9]

    s.append(_gen(s))
    s.append(_gen(s))

    return s == cpf[:]


def is_valid_mac_address(mac_address: str) -> bool:
    pattern = r'^([0-9A-Fa-f]{2}[:\-.]?){5}[0-9A-Fa-f]{2}$'
    return bool(re.match(pattern, mac_address))


def normalize_mac_address(mac_address: str) -> str:
    for r in ['.', '-', ':']:
        mac_address = mac_address.replace(r, '')

    mac_address = re.findall(r'(.{2})', mac_address)

    mac_address = ':'.join(mac_address)

    return mac_address


def sanitize(string: str) -> str:
    for r in ['.', '-', ':']:
        string = string.replace(r, '')
    return string


def _gen(cpf):
    """Gera o próximo dígito do número de CPF
    """
    res = []
    for i, a in enumerate(cpf):
        b = len(cpf) + 1 - i
        res.append(b * a)

    res = sum(res) % 11

    if res > 1:
        return 11 - res
    else:
        return 0

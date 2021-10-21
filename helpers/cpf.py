import re


def isValid(cpf: str) -> bool:
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
    s.append(__gen(s))
    s.append(__gen(s))
    return s == cpf[:]


def __gen(cpf):
    res = []
    for i, a in enumerate(cpf):
        b = len(cpf) + 1 - i
        res.append(b * a)

    res = sum(res) % 11

    if res > 1:
        return 11 - res
    else:
        return 0

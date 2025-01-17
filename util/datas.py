from datetime import datetime

def diferenca_meses(ini: datetime, fim: datetime) -> int:
    '''Retorna a diferença entre as duas datas ignorando os dias.'''
    anos = fim.year - ini.year
    meses = anos*12 + fim.month-ini.month
    return meses

def mes(indice: int) -> str:
    '''Converte um índice de mês (1-12) para o nome do mês.'''
    if indice == 1:
        return 'jan'
    elif indice == 2:
        return 'fev'
    elif indice == 3:
        return 'mar'
    elif indice == 4:
        return 'abr'
    elif indice == 5:
        return 'maio'
    elif indice == 6:
        return 'jun'
    elif indice == 7:
        return 'jul'
    elif indice == 8:
        return 'ago'
    elif indice == 9:
        return 'set'
    elif indice == 10:
        return 'out'
    elif indice == 11:
        return 'nov'
    elif indice == 12:
        return 'dez'
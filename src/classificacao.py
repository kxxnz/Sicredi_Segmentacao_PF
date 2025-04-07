
def classificar_pf(renda, investimento):
    if renda <= 2000:
        return 'PF I'
    elif 2000 < renda <= 4000:
        return 'PF II'
    elif (4000 < renda <= 10000) or (investimento >= 100000):
        return 'PF III'
    elif renda > 10000 or investimento >= 250000:
        return 'PF IV'
    else:
        return 'Indefinido'

def definir_canal(segmento):
    if segmento in ['PF I', 'PF II']:
        return 'Digital'
    elif segmento in ['PF III', 'PF IV']:
        return 'Agência'
    else:
        return 'Indefinido'

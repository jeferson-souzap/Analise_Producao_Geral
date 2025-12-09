



#FUNÇÕES
def formatar_brl(valor):
    #Formata um valor numérico (R$)
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")



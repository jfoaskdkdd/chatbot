
import re
import csv

# Função para ler e processar a lista em formato de tabela

def ler_lista_tabela(texto):
    # Não usada mais, agora leitura é do CSV
    return []

# Função para validar campos obrigatórios

def validar_campos(contatos):
    validos = []
    faltando = []
    for c in contatos:
        if c['nome'] and c['numero']:
            validos.append(c)
        else:
            faltando.append(c)
    print(f"Entradas válidas: {len(validos)} | Faltando nome/numero: {len(faltando)}")
    if faltando:
        print("Entradas removidas por falta de nome ou número:")
        for c in faltando:
            print(c)
    return validos

# Função para filtrar apenas celulares

def is_celular(numero):
    numero_limpo = re.sub(r'\D', '', numero)
    return re.match(r'^55\d{2}9\d{8}$', numero_limpo)

def title_case_nome(nome):
    return ' '.join([w.capitalize() for w in re.split(r'\s+', nome.strip())])

def filtrar_celulares(contatos):
    celulares = []
    removidos = []
    for c in contatos:
        numero_limpo = re.sub(r'\D', '', c['numero'])
        if numero_limpo.startswith('55'):
            pass
        elif numero_limpo.startswith('0') and len(numero_limpo) >= 12:
            numero_limpo = '55' + numero_limpo[1:]
        elif len(numero_limpo) == 11:
            numero_limpo = '55' + numero_limpo
        c['numero'] = numero_limpo
        nome_normalizado = title_case_nome(c['nome'])
        if is_celular(numero_limpo):
            celulares.append({'nome': nome_normalizado, 'numero': numero_limpo, 'site': c.get('site', '')})
        else:
            removidos.append({'nome': nome_normalizado, 'numero': c['numero'], 'site': c.get('site', '')})
    print(f"Celulares válidos: {len(celulares)} | Removidos (fixos/inválidos): {len(removidos)}")
    if removidos:
        print("Removidos (fixos/inválidos):")
        for c in removidos:
            print(c)
    return celulares

# Função principal


# Nova função para processar task1.csv e exportar para processarchecker.csv
def processar_task1_csv():
    print("--- Lendo task1.csv ---")
    contatos = []
    with open('task1.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nome = row.get('name', '').strip()
            site = row.get('website', '').strip()
            numero = row.get('phone', '').strip()
            contatos.append({'nome': nome, 'numero': numero, 'site': site})
    print(f"Total de linhas lidas: {len(contatos)}")
    print("--- Validando campos ---")
    contatos_validos = validar_campos(contatos)
    print("--- Filtrando celulares ---")
    celulares = filtrar_celulares(contatos_validos)
    print("--- Salvando resultado ---")
    with open('processarchecker.csv', 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['name', 'website', 'phone']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in celulares:
            writer.writerow({'name': c['nome'], 'website': c['site'], 'phone': c['numero']})
    print(f"Lista pronta para checker: processarchecker.csv ({len(celulares)} contatos)")
    return celulares

# Exemplo de uso
if __name__ == "__main__":
    processar_task1_csv()

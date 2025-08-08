import re
import csv

GOOGLE_FIELDS = [
    'First Name', 'Middle Name', 'Last Name', 'Phonetic First Name', 'Phonetic Middle Name', 'Phonetic Last Name',
    'Name Prefix', 'Name Suffix', 'Nickname', 'File As', 'Organization Name', 'Organization Title',
    'Organization Department', 'Birthday', 'Notes', 'Photo', 'Labels',
    'Phone 1 - Label', 'Phone 1 - Value', 'Custom Field 1 - Label', 'Custom Field 1 - Value'
]

def title_case_nome(nome):
    # Remove espaços extras e coloca cada palavra com a primeira letra maiúscula
    return ' '.join([w.capitalize() for w in re.split(r'\s+', nome.strip())])

def split_nome(nome):
    partes = nome.split()
    if not partes:
        return '', '', ''
    if len(partes) == 1:
        return partes[0], '', ''
    if len(partes) == 2:
        return partes[0], '', partes[1]
    # 3 ou mais partes: First, Middle, Last
    return partes[0], ' '.join(partes[1:-1]), partes[-1]

def ler_lista_tabela(texto):
    linhas = texto.strip().split('\n')
    contatos = []
    for idx, linha in enumerate(linhas, 1):
        partes = re.split(r'\t+|\s{2,}', linha.strip())
        if len(partes) == 2:
            nome, numero = partes
        elif len(partes) == 1:
            nome, numero = partes[0], ''
        else:
            nome, numero = '', ''
        contatos.append({'nome': nome.strip(), 'numero': numero.strip()})
    return contatos

def validar_campos(contatos):
    validos = []
    for c in contatos:
        if c['nome'] and c['numero']:
            validos.append(c)
    return validos

def is_celular(numero):
    numero_limpo = re.sub(r'\D', '', numero)
    return re.match(r'^55\d{2}9\d{8}$', numero_limpo)

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
        if is_celular(numero_limpo):
            celulares.append({'nome': c['nome'], 'numero': numero_limpo})
        else:
            removidos.append({'nome': c['nome'], 'numero': c['numero']})
    print(f"Celulares válidos: {len(celulares)} | Removidos (fixos/inválidos): {len(removidos)}")
    if removidos:
        print("Removidos (fixos/inválidos):")
        for c in removidos:
            print(c)
    return celulares

def exportar_para_csv_google_v2(contatos, arquivo_csv):
    with open(arquivo_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=GOOGLE_FIELDS)
        writer.writeheader()
        for c in contatos:
            nome_normalizado = title_case_nome(c['nome'])
            first, middle, last = split_nome(nome_normalizado)
            row = {k: '' for k in GOOGLE_FIELDS}
            row['First Name'] = first
            row['Middle Name'] = middle
            row['Last Name'] = last
            row['Labels'] = '* myContacts'
            row['Phone 1 - Label'] = 'Mobile'
            row['Phone 1 - Value'] = f'+{c["numero"]}'
            writer.writerow(row)
    print(f'Exportado para {arquivo_csv} no modelo Google Contatos (com nomes normalizados).')

def processar_lista_para_google_csv_v2(arquivo_lista, arquivo_csv):
    with open(arquivo_lista, 'r', encoding='utf-8') as f:
        texto = f.read()
    contatos = ler_lista_tabela(texto)
    contatos_validos = validar_campos(contatos)
    celulares = filtrar_celulares(contatos_validos)
    exportar_para_csv_google_v2(celulares, arquivo_csv)

if __name__ == "__main__":
    processar_lista_para_google_csv_v2('lista.txt', 'contatos_google.csv')

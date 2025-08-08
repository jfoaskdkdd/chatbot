import json
import csv

# Campos do Google Contacts conforme formatocerto.csv
GOOGLE_FIELDS = [
    'First Name','Middle Name','Last Name','Phonetic First Name','Phonetic Middle Name','Phonetic Last Name',
    'Name Prefix','Name Suffix','Nickname','File As','Organization Name','Organization Title','Organization Department',
    'Birthday','Notes','Photo','Labels','Phone 1 - Label','Phone 1 - Value','Custom Field 1 - Label','Custom Field 1 - Value'
]

def main():
    with open('contatos_filtrados.json', encoding='utf-8') as f:
        contatos = json.load(f)
    with open('google.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=GOOGLE_FIELDS)
        writer.writeheader()
        for c in contatos:
            row = {field: '' for field in GOOGLE_FIELDS}
            row['First Name'] = c['nome']
            row['Phone 1 - Value'] = c['numero']
            row['Phone 1 - Label'] = 'Mobile'
            row['Labels'] = '* myContacts'
            writer.writerow(row)
    print('Exportação concluída: google.csv')

if __name__ == '__main__':
    main()

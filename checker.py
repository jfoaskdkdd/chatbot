import requests
import csv
import time
import json
import re

# Lista de domínios de agregadores/redes sociais/encurtadores
AGREGADORES = [
    'instagram.com', 'facebook.com', 'wa.me', 'whatsapp.com', 'linktr.ee', 'beacons.ai', 'canva.site',
    'bit.ly', 'bio.site', 'youtube.com', 'tiktok.com', 'cutt.ly', 'l.instagram.com', 'shre.ink',
    'campsite.bio', 'about.me', 'carrd.co', 'taplink.cc', 'direct.me', 'linkme.bio', 'linkbio.co',
    'linkin.bio', 'lnk.bio', 'linkpop.com', 'linktree', 'tr.ee', 'bio.link', 'linkfly.to',
    'meadd.com', 'vk.com', 'twitter.com', 'x.com', 'snapchat.com', 'pinterest.com', 'tumblr.com',
    'reddit.com', 'medium.com', 'soundcloud.com', 'spotify.com', 'deezer.com', 'apple.com',
    'google.com', 'maps.app.goo.gl', 'goo.gl', 'forms.gle', 'sites.google.com', 'pages.app',
    'notion.site', 'notion.so', 'substack.com', 'mailchi.mp', 'tinyurl.com', 'getresponse.com',
    'rdstation.com', 'hotmart.com', 'sympla.com.br', 'eventbrite.com', 'eventbrite.com.br',
    'eventos.gupy.io', 'even3.com.br', 'eventials.com', 'zoom.us', 'meet.google.com', 'teams.microsoft.com',
    'skype.com', 'discord.gg', 'discord.com', 'telegram.me', 't.me', 'patreon.com', 'apoia.se',
    'pix.com.br', 'pagseguro.uol.com.br', 'mercadopago.com.br', 'paypal.com', 'pag.ae', 'nubank.com.br',
    'picpay.com', 'ifood.com.br', 'rappi.com.br', 'ubereats.com', '99app.com', 'airbnb.com',
    'booking.com', 'expedia.com', 'tripadvisor.com', 'linkedin.com', 'jobs.gupy.io', 'indeed.com',
    'glassdoor.com', 'infojobs.com.br', 'catho.com.br', 'vagas.com.br', 'bion.bio', 'linkr.bio',
    'linke.to', 'linktr.ee', 'linktree', 'bio.site', 'bio.link', 'linkfly.to', 'linkpop.com',
    'linkin.bio', 'lnk.bio', 'linkbio.co', 'linkme.bio', 'direct.me', 'taplink.cc', 'carrd.co',
    'about.me', 'campsite.bio', 'shre.ink', 'l.instagram.com', 'cutt.ly', 'tr.ee', 'meadd.com',
    'vk.com', 'x.com', 'twitter.com', 'snapchat.com', 'pinterest.com', 'tumblr.com', 'reddit.com',
    'medium.com', 'soundcloud.com', 'spotify.com', 'deezer.com', 'apple.com', 'google.com',
    'maps.app.goo.gl', 'goo.gl', 'forms.gle', 'sites.google.com', 'pages.app', 'notion.site',
    'notion.so', 'substack.com', 'mailchi.mp', 'tinyurl.com', 'getresponse.com', 'rdstation.com',
    'hotmart.com', 'sympla.com.br', 'eventbrite.com', 'eventbrite.com.br', 'eventos.gupy.io',
    'even3.com.br', 'eventials.com', 'zoom.us', 'meet.google.com', 'teams.microsoft.com', 'skype.com',
    'discord.gg', 'discord.com', 'telegram.me', 't.me', 'patreon.com', 'apoia.se', 'pix.com.br',
    'pagseguro.uol.com.br', 'mercadopago.com.br', 'paypal.com', 'pag.ae', 'nubank.com.br', 'picpay.com',
    'ifood.com.br', 'rappi.com.br', 'ubereats.com', '99app.com', 'airbnb.com', 'booking.com',
    'expedia.com', 'tripadvisor.com', 'linkedin.com', 'jobs.gupy.io', 'indeed.com', 'glassdoor.com',
    'infojobs.com.br', 'catho.com.br', 'vagas.com.br', 'bion.bio', 'linkr.bio', 'linke.to'
]


# --- ETAPA 1: Filtragem de celulares válidos ---
def is_celular(numero):
    numero_limpo = re.sub(r'\D', '', numero)
    return re.match(r'^55\d{2}9\d{8}$', numero_limpo)

def title_case_nome(nome):
    return ' '.join([w.capitalize() for w in re.split(r'\s+', nome.strip())])

def filtrar_celulares_task1():
    print("[1/3] Lendo e filtrando task1.csv...")
    contatos = []
    with open('task1.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nome = row.get('name', '').strip()
            site = row.get('website', '').strip()
            numero = row.get('phone', '').strip()
            numero_limpo = re.sub(r'\D', '', numero)
            if numero_limpo.startswith('55'):
                pass
            elif numero_limpo.startswith('0') and len(numero_limpo) >= 12:
                numero_limpo = '55' + numero_limpo[1:]
            elif len(numero_limpo) == 11:
                numero_limpo = '55' + numero_limpo
            nome_normalizado = title_case_nome(nome)
            contatos.append({'nome': nome_normalizado, 'numero': numero_limpo, 'site': site})
    # Valida campos obrigatórios
    validos = [c for c in contatos if c['nome'] and c['numero']]
    faltando = [c for c in contatos if not (c['nome'] and c['numero'])]
    print(f"Entradas válidas: {len(validos)} | Faltando nome/numero: {len(faltando)}")
    # Filtra apenas celulares
    celulares = [c for c in validos if is_celular(c['numero'])]
    removidos = [c for c in validos if not is_celular(c['numero'])]
    print(f"Celulares válidos: {len(celulares)} | Removidos (fixos/inválidos): {len(removidos)}")
    if removidos:
        print("Removidos (fixos/inválidos):")
        for c in removidos:
            print(c)
    # Exporta para processarchecker.csv
    with open('processarchecker.csv', 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['name', 'website', 'phone']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in celulares:
            writer.writerow({'name': c['nome'], 'website': c['site'], 'phone': c['numero']})
    print(f"[1/3] Lista pronta para análise de sites: processarchecker.csv ({len(celulares)} contatos)")
    return celulares

# --- ETAPA 2: Análise dos sites e exportações ---
def tipo_site(url):
    if not url or url.strip() == '':
        return 'sem site'
    url_lower = url.lower()
    for agg in AGREGADORES:
        if agg in url_lower:
            return 'agregador/social'
    if url_lower.startswith('http'):
        return 'site próprio'
    return 'outro'

def checar_status(url):
    if not url or url.strip() == '':
        return ''
    try:
        resp = requests.head(url, timeout=7, allow_redirects=True)
        if resp.status_code >= 400:
            return f'OFF ({resp.status_code})'
        return 'ON'
    except Exception as e:
        try:
            resp = requests.get(url, timeout=7, allow_redirects=True)
            if resp.status_code >= 400:
                return f'OFF ({resp.status_code})'
            return 'ON'
        except Exception as e2:
            return 'OFF'

def analisar_sites_e_exportar():
    print("[2/3] Analisando sites e exportando resultados...")
    with open('processarchecker.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    results = []
    for row in rows:
        nome = row['name']
        url = row['website']
        numero = row['phone']
        tipo = tipo_site(url)
        status = checar_status(url) if tipo == 'site próprio' else ('' if tipo == 'sem site' else 'ON')
        results.append({
            'name': nome,
            'phone': numero,
            'website': url,
            'tipo_site': tipo,
            'status': status
        })
        print(f"{nome} | {numero} | {url} | {tipo} | {status}")
        time.sleep(0.5)
    # Exporta contatos sem site, site off ou agregador/social (filtrados.csv)
    export_filtrados = [r for r in results if r['tipo_site'] in ['sem site', 'agregador/social'] or (r['tipo_site'] == 'site próprio' and r['status'] != 'ON')]
    with open('filtrados.csv', 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['name', 'phone', 'website', 'tipo_site', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in export_filtrados:
            writer.writerow(r)
    # Exporta no formato Google Contacts (google.csv) igual ao formatocerto.csv
    google_fields = [
        'First Name','Middle Name','Last Name','Phonetic First Name','Phonetic Middle Name','Phonetic Last Name',
        'Name Prefix','Name Suffix','Nickname','File As','Organization Name','Organization Title','Organization Department',
        'Birthday','Notes','Photo','Labels','Phone 1 - Label','Phone 1 - Value','Custom Field 1 - Label','Custom Field 1 - Value'
    ]
    with open('google.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=google_fields)
        writer.writeheader()
        for r in export_filtrados:
            # Preencher apenas First Name e Phone 1 - Value, o resto vazio
            row = {field: '' for field in google_fields}
            row['First Name'] = r['name']
            row['Phone 1 - Value'] = r['phone']
            row['Phone 1 - Label'] = 'Mobile'
            row['Labels'] = '* myContacts'
            writer.writerow(row)
    # Exporta contatos_filtrados.json no formato [{'nome':..., 'numero':...}]
    contatos_json = [
        {'nome': r['name'], 'numero': r['phone']}
        for r in export_filtrados if r['name'] and r['phone']
    ]
    with open('contatos_filtrados.json', 'w', encoding='utf-8') as f:
        json.dump(contatos_json, f, ensure_ascii=False, indent=2)
    print("[3/3] Exportações concluídas!")

# --- FLUXO PRINCIPAL ---
if __name__ == "__main__":
    filtrar_celulares_task1()
    analisar_sites_e_exportar()
    print('Finalizado!')

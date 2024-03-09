from bs4 import BeautifulSoup
import requests
from googlesearch import search

link = 'https://labrescue.pl/porady/szczury/co-jedza-szczury/'

# Pobieranie strony z linku
response = requests.get(link)

# Zapisywanie strony do pliku strona_labrescue.html
if response.status_code == 200:
    with open('strona_labrescue.html', 'w') as file:
        file.write(response.text)

# Wczytywanie zawartości strony HTML
with open('strona_labrescue.html', 'r') as file:
    html_page = file.read()

# Utworzenie obiektu BeautifulSoup
soup = BeautifulSoup(html_page, 'html.parser')

# Odczytanie tytułu strony
page_title = soup.title.string

# Odczytanie nagłówków h2
headers_h2 = soup.find_all('h2')
for el in headers_h2:
    print(el.string)
#    for url in search(el.string, stop=10):
#        print(url)

# Odczytanie pierwszego akapitu strony
akapit_wstep = soup.find('div', class_='entry-content').find('span')


# Odczytanie przedostatniego akapitu strony
podtytul_zakazane = soup.find('h2', string = headers_h2[-2].string)
if podtytul_zakazane:
    akapit_zakazane = podtytul_zakazane.find_next_sibling('p')
    if akapit_zakazane:
        lista_zakazanych = akapit_zakazane.find_next_sibling('ul')


# Odczytanie ostatniego akapitu strony
podtytul_dieta = soup.find('h2', string = headers_h2[-1].string)
if podtytul_dieta:
    akapit_podsumowanie = podtytul_dieta.find_next_sibling('p')
    if akapit_podsumowanie:
        lista_pokarmow = akapit_podsumowanie.find_next_sibling('ul')

with open('index.md', 'w', encoding='utf-8') as file:
    file.write('# ' + page_title + '\n')
    file.write(akapit_wstep.text + '\n')
    file.write('## ' + "Dieta" + '\n')
    if lista_pokarmow:
        for el in lista_pokarmow.find_all('li'):
            tag = el.find('strong')
            if tag:
                file.write('* **' + tag.text.strip() + '**')
                file.write(el.text.replace(tag.text, '') + '\n')
    file.write('## ' + podtytul_zakazane.text + '\n')
    file.write(akapit_zakazane.text + '\n')
    if lista_zakazanych:
        for el in lista_pokarmow.find_all('li'):
            file.write('*' + el.text + '\n')


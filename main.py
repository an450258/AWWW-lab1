from bs4 import BeautifulSoup
import requests
from duckduckgo_search import DDGS

link = 'https://labrescue.pl/porady/szczury/co-jedza-szczury/'
image = 'https://labrescue.pl/wp-content/uploads/2023/06/Grafiki-na-strone-1.webp'


def read_page(url):
    # Pobieranie strony z linku
    response = requests.get(link)

    # Zapisywanie strony do pliku strona_labrescue.html
    with open('strona_labrescue.html', 'w') as file:
        file.write(response.text)

    # Wczytywanie zawartości strony HTML
    with open('strona_labrescue.html', 'r') as file:
        return file.read()


def md_link(tag):
    return "[" + tag.strip() + "]" + "(" + tag.replace(" ","") + ".html)"


def md_h1_title(text):
    return '# ' + text + '\n'


def md_h2_title(text):
    return '## ' + text + '\n'


def md_image(img):
    return "![[Image not loaded]](" + img + ")\n\n"


def md_source(source):
    return "Źródło: [" + source + "](" + source + ")\n\n"


# Wyniki wyszukiwania z dodaniem frazy "extra"
def save_search_result(file, tag, extra):
    tag_extra = DDGS().text(tag.text + " " + extra, max_results=2)
    file.write(md_h2_title(tag.text + " - " + extra))
    for el in tag_extra:
        file.write("* " + el['title'] + '\n')
        file.write(md_link(el['href']) + "\n\n")


def create_duckduckgo_subpage(tag):
    with open(tag.text.replace(" ","") + ".md", 'w', encoding='utf-8') as file:

        file.write(md_h1_title(tag.text))
        tag_image = DDGS().images(tag.text, max_results=1)[0]
        file.write(md_image(tag_image['image']))
        file.write(md_source(tag_image['url']))

        save_search_result(file, tag, "gryzonie")
        save_search_result(file, tag, "zdrowie")
        save_search_result(file, tag, "przepisy")
        save_search_result(file, tag, "zakupy")


def create_main_page(first_title, first_paragraph, first_list, second_title, second_paragraph, second_list):
    with open('index.md', 'w', encoding='utf-8') as file:

        file.write(md_h1_title(first_title.string))

        file.write(md_source(link))

        file.write(md_image(image))

        file.write(first_paragraph.text + '\n')

        file.write('\n' + md_h2_title("Dieta"))
        for el in first_list.find_all('li'):
            tag = el.find('strong')
            file.write('* **' + md_link(tag.text) + '**')
            file.write(el.text.replace(tag.text, '') + '\n')
            create_duckduckgo_subpage(tag)

        file.write('\n' + md_h1_title(second_title.text))
        file.write(second_paragraph.text.strip() + '\n')
        second_list = second_list.find_all('li')
        second_list.pop(0)
        for el in second_list:
            file.write('* ' + el.text + '\n')


if __name__ == "__main__":
    html_page = read_page(link)

    # Utworzenie obiektu BeautifulSoup
    soup = BeautifulSoup(html_page, 'html.parser')

    # Odczytanie tytułu strony
    page_title = soup.title

    # Odczytanie nagłówków h2
    headers_h2 = soup.find_all('h2')

    # Odczytanie pierwszego akapitu strony
    akapit_wstep = soup.find('div', class_='entry-content').find('span')

    # Odczytanie przedostatniego akapitu strony
    podtytul_zakazane = soup.find('h2', string=headers_h2[-2].string)
    if podtytul_zakazane:
        akapit_zakazane = podtytul_zakazane.find_next_sibling('p')
        if akapit_zakazane:
            lista_zakazane = akapit_zakazane.find_next_sibling('ul')

    # Odczytanie ostatniego akapitu strony
    podtytul_dieta = soup.find('h2', string=headers_h2[-1].string)
    if podtytul_dieta:
        akapit_dieta = podtytul_dieta.find_next_sibling('p')
        if akapit_dieta:
            lista_dieta = akapit_dieta.find_next_sibling('ul')

    # Utworzenie pliku z główną stroną
    create_main_page(page_title, akapit_wstep, lista_dieta, podtytul_zakazane, akapit_zakazane, lista_zakazane)



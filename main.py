# основные импорты
import requests
from bs4 import BeautifulSoup

st_accept = "text/html"
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"

# формируем хеш заголовков
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}

def start_scrapping(url) -> None:
    req = requests.get(url, headers=headers)
    # считываем текст HTML-документа
    src = req.text
    
    soup = BeautifulSoup(src, 'lxml') # достали последние игры
    games = soup.find('div',
                    {'class':'r-table r-only-mobile-5 performances-overview',
                     }).descendants

    for i in games:
        all_statics = i.text
        print(f'{all_statics}')


if __name__ == '__main__': # бест-практис... ю ноу?
    url = 'https://ru.dotabuff.com/players/249237243'
    start_scrapping(url=url)

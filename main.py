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
    soup = BeautifulSoup(req.text, 'lxml') # достали последние игры
    games = soup.find('div', 
                      class_='performances-overview')

    for stats in games:
        hero = stats.find('div', class_='r-fluid').find('a').find('img').get('alt')
        kda = stats.find('span', class_='kda-record').text
        lvl = stats.find('div', class_='tw-rounded-tl-sm').text
        match_result = stats.find('div', class_='r-match-result').find('a', class_=['won', 'lost']).text
        
        print(hero, kda, lvl, match_result)


if __name__ == '__main__': # бест-практис... ю ноу?
    url = 'https://ru.dotabuff.com/players/249237243'
    start_scrapping(url=url)

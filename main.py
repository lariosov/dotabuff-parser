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
    
    clear_stats = {}

    for stats in games:
        hero = stats.find('div', class_='r-fluid').find('a').find('img').get('alt')
        kda = stats.find('span', class_='kda-record').text
        lvl = stats.find('div', class_='tw-rounded-tl-sm').text
        match_result = stats.find('div', class_='r-match-result').find('a', class_=['won', 'lost']).text
        game_mode = stats.find('div', 
                          class_='r-fluid r-175 r-text-only r-first').find('div', 
                                                                           class_='r-body').find('div',
                                                                                                 class_='subtext').text
    
        clear_stats[hero] = {
            'kda': kda,
            'game_mode': game_mode,
            'lvl': lvl,
            'match_result': match_result
        }
        
    return clear_stats


if __name__ == '__main__': # бест-практис... ю ноу?
    url = 'https://ru.dotabuff.com/players/249237243'
    print(start_scrapping(url=url))

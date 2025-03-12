# основные импорты
import requests
from bs4 import BeautifulSoup

st_accept = "text/html"
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"

# формируем хеш заголовков
headers = {"Accept": st_accept, "User-Agent": st_useragent}


def start_scrapping(id) -> int:
    url = f"https://ru.dotabuff.com/players/{id}"
    req = requests.get(url, headers=headers)

    # считываем текст HTML-документа
    soup = BeautifulSoup(req.text, "lxml")  # достали последние игры
    games = soup.find("div", class_="performances-overview")

    clear_stats = {}

    for stats in games:
        try:
            hero = stats.find("div", class_="r-fluid").find("a").find("img").get("alt")
            kda = stats.find("span", class_="kda-record").text
            lvl = stats.find("div", class_="tw-rounded-tl-sm").text
            match_result = (
            stats.find("div", class_="r-match-result")
            .find("a", class_=["won", "lost"])
            .text
            )
            game_mode = (
            stats.find("div", class_="r-first")
            .find("div", class_="r-body")
            .find("div", class_="subtext")
            .text
            )
            game_link = (
            stats.find("div", class_="r-match-result")
            .find("a", class_=["won", "lost"])
            .get("href")
            )
            date = stats.find("div", class_="r-match-result").find("time").text
            avg_rate = stats.find("div", class_="subtext").text
            role = (
                stats.find("span", class_="subtext icons")
                .find("i", "role-icon")
                .get("title")
            )
            lane = (
                stats.find("span", class_="subtext icons")
                .find("i", "lane-icon")
                .get("title")
            )
            duration = stats.find("div", class_="r-duration").find("div", "r-body").text

            url = f"https://ru.dotabuff.com{game_link}"
            r = requests.get(url, headers=headers)

            # считываем текст HTML-документа
            soup = BeautifulSoup(r.text, "lxml")  # достали последние игры
            hero_stats = soup.find("tr", class_=f"player-{id}")

            net_worth = hero_stats.find("td",
                            class_="color-stat-gold").text
            last_hits = (hero_stats
                        .find("td",
                        class_="tf-r r-tab r-group-2 cell-minor")
                        .text
                        )
            denied = (hero_stats
                      .find("td",
                            class_="tf-pl r-tab r-group-2 cell-minor")
                            .text
                    )
            damage = (hero_stats
                      .find("td",
                      class_="tf-r r-tab r-group-3 cell-minor")
                      .text
                      )
            tower_dmg = (hero_stats
                     .find_all("td",
                           class_="tf-r r-tab r-group-3 cell-minor")[2].text
                    )

        except:
            role = "Нет информации"
            lane = "Нет информации"
            net_worth = "Нет информации"

        clear_stats[game_link] = {
            "hero": hero,
            "kda": kda,
            "game_mode": game_mode,
            "lvl": lvl,
            "match_result": match_result,
            "date": date,
            "avg_rate": avg_rate,
            "role": role,
            "lane": lane,
            "duration": duration,
            "net_worth": net_worth,
            "last_hits": last_hits,
            "denied": denied,
            "damage": damage,
            "tower_dmg": tower_dmg,
        }

    return clear_stats


if __name__ == "__main__":  # бест-практис... ю ноу?
    print(start_scrapping(id=249237243))

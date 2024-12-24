# dotabuff-parser
Маленький парсер, который будет парсить страницу с персональными последними играми на DotaBuff.  
Нужен этот парсер для работы в совокупности с TelegramBot, чтобы создать бота, через которого можно удобно чекнуть профиль друга и его последние игры.  
  
# dotabuff-parser API
Доступные виды запросов:
> GET

## GET /api/profile
Принимает в себя одну переменную `id` типа `int`


Переменной `id` являются цифры из открытого профиля DotaBuff.  
>Например: https://ru.dotabuff.com/players/249237243 , где переменная id == 249237243

API доступен по пути:
> http://lariosov.online/api/profile?id=249237243


API возвращает значения в виде:  
```{"/matches/8069331759":{"hero":"Arc Warden","kda":"17/5/15","game_mode":"All Pick","lvl":"24","match_result":"Победа","date":"06.12.2024","avg_rate":"Герой I","role":"Ключевая роль","lane":"Средняя линия","duration":"31:08"}```

![изображение](https://github.com/user-attachments/assets/5f13caa8-660d-4fb4-ace2-a05f51de8292)

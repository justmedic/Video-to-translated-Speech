Один из первых поих проектов. Переводит видео по ссылке с ютуба Video to Sond (пока только en -> ru)

Вставляешь ссылку на видео с ютуба, выбираешь голос озвучки и ждешь. Распознавание речи ресурсоемкая задача так что компик может напрячься. В среднем перевод занимает 20% от длины видео. В конце создает файл перевода.

ПЕРЕД ЗАПУСКОМ НЕ ЗАБУДЬТЕ СКАЧАТЬ УТИЛИТЫ С ГУГЛ ДИСКА

Копировать
```
git clone https://github.com/justmedic/VtS/
```
Заходим на гугл диск, скачиваем все и разархивируем в директории проекта (где лежит файл main.py)

```
https://drive.google.com/drive/folders/1L3LFyS5dK-NZZwVfwnl2hwWn0tlPj6SO?usp=sharing
```

Когда все установилось, запускаем через докер (некоторые библиотеки очень объемные, так что загрузка будет долгой)
```
docker build -t video-to-sound-app .
docker run video-to-sound-app

```


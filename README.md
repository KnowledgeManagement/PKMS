# PKMS
## Tool for Personal Knowledge Management System
For now it's a handy tool for uploading to YandexDisk or dowloding from it. It's both either telegram bot and console script. 
## OAuthCode for YandexDisk
You should have a Yandex account to work this out.
First of all you have to go via [link](https://oauth.yandex.ru) and create an app. Choose the following settings:

<img width="591" alt="Снимок экрана 2022-07-29 в 23 09 39" src="https://user-images.githubusercontent.com/62376752/181835983-cee96db5-0319-4670-8171-ce60be06a7c4.png">
<img width="641" alt="Снимок экрана 2022-07-29 в 22 51 01" src="https://user-images.githubusercontent.com/62376752/181833681-f46eb342-cf0d-42ef-b4ce-c3ae1fb89788.png">

After creation open page of this app and find ClientId and copy it. 
To finally get OAuthCode go follow the link (change appid with your ClientId)
```
https://oauth.yandex.ru/authorize?response_type=token&client_id=<appid>
```
## Telegram bot
His tag - https://t.me/PKMS_bot

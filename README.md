# Запуск приложения

Для запуска приложения используется

```bash
sudo docker-compose up
```
При запуске приложения создаётся два пользователя, с токеном админа и пользователя

Чтобы получить токен админа

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/auth/jwt/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin%40mail.com&password=admin'

{"access_token":"X982ZKPeFESRV35kyxePucT8KWnzvHRGMA0-AXqzHXM","token_type":"bearer"}
```

Чтобы получить токен пользователя

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/auth/jwt/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=user%40mail.com&password=user'

{"access_token":"KMhWr_GVMVwRqQa8866PQkXDELhbitty1klhc7FG6Rc-AXqzHXM","token_type":"bearer"}
```

При выполнении запросов к роутам необходимо указывать токен в заголовках.

Пример добавления тэга

```bash

curl -X 'POST' \
  'http://0.0.0.0:8000/tag' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer xXmSGkj2NP39HMIp8a6MykDI2GTmVD-03rJO5ZjLL2k' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string"
}'

{
  "name": "string"
}
```

Информацию о других роутах(после запуска приложения) можно просмотреть по адресу
http://0.0.0.0:8000/docs

# Тестирование

Перед E2E тестированием получения банера, необходимо перезапустить контейнеры, поскольку для теста нужна чистая база.
```bash 
sudo docker-compose up --force-recreate
```

После чего запускаем приложение

Дальше необходимо настроить и актировать виртуальное окружение
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt 
cd tests/
pytest
```
После выполнения теста в базе будут тестовые значения, поэтому необходимо снова перезагрузить приложение.




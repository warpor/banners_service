# Вопросы и пояснения
1. По описанию из задачи не было ясно, нужно ли создавать отдельные сущности в базе для тэгов и фичей.
- С одной стороны, в API указаны методы только для работы с баннером.
- С другой стороны, из дополнительных условий следует, что API можно менять "Измените API таким образом".

  
Из строчки задания "Тег — это сущность для обозначения группы пользователей", решил, что нужно завести сущность для тега и фичи в базе.

Таким образом, модель `Banner` зависит от `Tag` и `Feature`, и перед добавлением баннера, необходимо добавить объекты `Tag` и `Feature` в Бд.
`Tag` и `Feature` имеют одно поле `name`, которое является уникальным.  
`Banner` связан с `Tag` через модель `BannerTag`, которая реализует связь многие-ко-многим


2. Два вида доступа реализовал через Oauth авторизацию, с помощью библиотеки [fastapi_users](https://fastapi-users.github.io/fastapi-users/10.1/).
Соответственно, токен сначала необходимо сформировать, сохранить в базе и получить(возвращается уникальный токен), это делается с помощью следующего метода.

```
curl -X 'POST' \
  'http://0.0.0.0:8000/auth/jwt/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin%40mail.com&password=admin'
```
В ответе вернется токен админа
```bash
{
  "access_token": "pPZF5w9sNGDF-oJFyN6JH1qYd0Eo7LhjGkS9MOXk3oM",
  "token_type": "bearer"
}
```

Таким образом, при отправке запросов, информацию о токене нужно указывать в хедере следующим образом.

```bash
...
  -H 'Authorization: Bearer {token}'
...
```
где `{token}` - это поле `access_token` из ответа получения токена

Для получения токена пользователя
```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/auth/jwt/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=user%40mail.com&password=user'
```

Дальше по описанию `{admin-toke}` - токен админа, `{user-token}` - токен пользователя.

3. При попытке создать/изменить баннер с набором feature_id и tags_id, которые уже существует, возвращается 400 статус с телом ответа
```bash
{
  "detail": "Некорректные данные"
}
```

4. Для просмотра добавленных фичей и тегов, можно воспользоваться подключением к базе.

При запущенном приложении
```bash
psql -h localhost -p 5455 -U warpor -d banners
```
Пароль для подключения `123`.

Получение фичей
```sql
select * from features;
```

Получение тэгов
```sql
select * from tags;
```

Получение тэгов баннеров
```sql
select * from banners_tags;
```
# Запуск приложения

Для запуска приложения используется

```bash
sudo docker-compose up
```

При запуске приложения создаётся два пользователя, с правом доступа админа и пользователя.  
Данные админа `admin@mail.com:admin`  
Данные пользователя `user@mail.com:user`  

После запуска приложения все методы доступны по адресу http://0.0.0.0:8000/docs.  

# Обращение к методам через CURL
- Получить токен админа

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/auth/jwt/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin%40mail.com&password=admin'

{"access_token":"X982ZKPeFESRV35kyxePucT8KWnzvHRGMA0-AXqzHXM","token_type":"bearer"}
```

- Получить токен пользователя

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/auth/jwt/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=user%40mail.com&password=user'

{"access_token":"KMhWr_GVMVwRqQa8866PQkXDELhbitty1klhc7FG6Rc-AXqzHXM","token_type":"bearer"}
```

- Добавить тэг

```bash

curl -X 'POST' \
  'http://0.0.0.0:8000/tag' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer {admin-token}' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string"
}'

{
  "name": "string"
}
```

- Добавить фичу

```bash

curl -X 'POST' \
  'http://0.0.0.0:8000/feature' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer {admin-token}' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string"
}'

{
  "name": "string"
}
```

- Добавить баннер

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/banner' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer {admin-token}' \
  -H 'Content-Type: application/json' \
  -d '{
  "feature_id": 1,
  "content": {"some": "test"},
  "is_active": true,
  "tag_ids": [
    1
  ]
}'

{
  "id": 1
}
```

- Обновить баннер

```bash
curl -X 'PATCH' \
  'http://0.0.0.0:8000/banner/3' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer {admin-token}' \
  -H 'Content-Type: application/json' \
  -d '{
  "is_active": false
}'

{
  "id": 1
}
```

- Получить банер

```bash
curl -X 'GET' \
  'http://0.0.0.0:8000/user_banner?tag_id=1&feature_id=1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer {admin-token/user-token}'

{
  "content": {
    "some": "test"
  }
}
```

- Удалить банер

```bash
curl -X 'DELETE' \
  'http://0.0.0.0:8000/banner/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer {admin-token}'

{
  "description": "Баннер успешно удалён",
  "headers": null,
  "content": null,
  "links": null,
  "status_code": 204
}
```

Более подробную информацию о роутах можно просмотреть по адресу
http://0.0.0.0:8000/docs

# Тестирование

Поскольку для создания `Banner` необходимо иметь в базе `Feature` и `Tag`, для тестирования E2E получения банера, сначала необходимо добавить в базу эти две сущности.  
Таким образом, проводится тестирование 4 методов.
1. Тест на создание фичи
2. Тест на создание тэга
3. Тест на создание баннера
4. Тест на получение баннера

Поэтому перед тестированием необходимо иметь чистую базу.  
Пересоздаём контейнеры
```bash 
sudo docker-compose up --force-recreate
```

Дальше необходимо настроить и актировать виртуальное окружение.  
Выполняется из корня проекта
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt 
cd tests/
pytest
```




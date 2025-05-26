![image](https://github.com/user-attachments/assets/fbd5a48c-6f35-47d6-90ec-14c32baa6470)  

Инструкция для запуска:  
```
git clone https://github.com/mikle305/TestTask_LeaderboardDjango

# НЕ ПРОПУСТИТЕ!!! 
# Дублируйте .env.template и переименуйте его в .env

pip install poetry
poetry update
docker compose up -d --force-recreate

# Создадим супер юзера с логином admin и паролем admin и получим для него токен авторизации
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell 
python manage.py drf_create_token admin

# Добавляем 11 результатов для соревнования some_competition, сценария some_scenario, с пользователем admin и еще 10 рандомами:
python test.py create_results 11 admin some_competition some_scenario

# Запрос к /results/results/get-competition-result/
# Подставьте вместо <your_auth_token> токен авторизации полученный в шагах ранее
# Пользователь с правами администратора можешь получать данные по любому имени пользователя
# Обычный пользователь сможет получать только лидерборд по своему user_name
python test.py get_results some_competition admin some_scenario <your_auth_token>

# Если понадобится можете удалить все результаты сгенерированные ранее
python test.py delete_results
```

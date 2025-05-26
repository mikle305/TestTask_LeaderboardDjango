import random
import string
import http.client
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")

import django

django.setup()

from leaderboard.models import CompetitionResult
from common.env_settings import env_settings


connection = http.client.HTTPConnection(f"127.0.0.1:{env_settings.app.backend_port}")


def random_string(n: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=n))


def create_results(count: int, main_user_name: str, competition: str, scenario: str) -> None:
    if count < 1:
        print("Количество юзеров должно быть 1 или больше")
        return

    commands = ["team1", "team2", "team3"]
    room_ids = ["room1", "room2"]
    flight_time_min = 5.0
    flight_time_max = 20.0
    objs = []
    for i in range(count):
        objs.append(
            CompetitionResult(
                competition=competition,
                room_id=random.choice(room_ids),
                command_name=random.choice(commands),
                user_name=main_user_name if i == 0 else random_string(8),
                scenario=scenario,
                flight_time=round(random.uniform(flight_time_min, flight_time_max), 2),
                false_start=False,
            )
        )
    CompetitionResult.objects.bulk_create(objs)
    print(f"✅ Добавлено {count} рандомных результатов.")


def get_results(competition: str, user_name: str, scenario: str, auth_token: str) -> None:
    payload = {
        "competition": competition,
        "user_name": user_name,
        "scenario": scenario,
    }

    headers = {
        "Authorization": f"Token {auth_token}",
        "Content-Type": "application/json",
    }
    connection.request("POST", "/results/results/get-competition-result/", body=json.dumps(payload), headers=headers)
    response = connection.getresponse()
    data = response.read().decode()

    if response.status == 200:
        parsed = json.loads(data)
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    else:
        print(f"Ошибка {response.status}: {data}")


def delete_results() -> None:
    CompetitionResult.objects.all().delete()
    print("✅ Все результаты удалены из БД.")


def print_usage() -> None:
    print("Использование:")
    print("  python test.py create_results <count> <main_user_name> <competition> <scenario>")
    print("  python test.py get_results <competition> <user_name> <scenario> <auth_token>")
    print("  python test.py delete_results")
    sys.exit(1)


def main() -> None:
    if len(sys.argv) < 2:
        print_usage()
    cmd = sys.argv[1]
    if cmd == "create_results":
        if len(sys.argv) != 6:
            print_usage()
        _, _, count, main_user_name, competition, scenario = sys.argv
        create_results(int(count), main_user_name, competition, scenario)
    elif cmd == "get_results":
        if len(sys.argv) != 6:
            print_usage()
        _, _, competition, user_name, scenario, auth_token = sys.argv
        get_results(competition, user_name, scenario, auth_token)
    elif cmd == "delete_results":
        delete_results()
    else:
        print_usage()


if __name__ == "__main__":
    main()

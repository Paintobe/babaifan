import json

from django_redis import get_redis_connection


def checkNum(phone):
    redis_cli = get_redis_connection('cart')
    dataall = redis_cli.get(f'cart-{phone}')
    dataall = json.loads(dataall)
    num = 0
    for id,dic in dataall.items():
        num += int(dic['num'])
    # print(num)
    return num


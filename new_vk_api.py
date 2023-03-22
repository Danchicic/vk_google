import requests
import time
import datetime

today = datetime.date.today()
token = 'vk1.a.J4JNwE0KNXLPpteH7ONBfTQIPsYe6DB4ZfwXLQUfs8oRx_IJRyVFK_5BGjHiKvHYrUjy4BGgrLseyNq-Sx02WaCmXoZCszF7VMcM2KZK0vxUQUqvZAuvBAtAafoUrk8PKmUYAWF9vXQ35sgRFTVOz8K5NGZpTaG7d_qZT9wwtD1fVAerVXfv6NGzbFNw9qNu0D2euVOpvdP4myuM9eygJw'
names_by_ids = {}


def _get_clients() -> list:
    response = requests.post('https://api.vk.com/method/ads.getClients', params={
        'access_token': 'vk1.a.J4JNwE0KNXLPpteH7ONBfTQIPsYe6DB4ZfwXLQUfs8oRx_IJRyVFK_5BGjHiKvHYrUjy4BGgrLseyNq-Sx02WaCmXoZCszF7VMcM2KZK0vxUQUqvZAuvBAtAafoUrk8PKmUYAWF9vXQ35sgRFTVOz8K5NGZpTaG7d_qZT9wwtD1fVAerVXfv6NGzbFNw9qNu0D2euVOpvdP4myuM9eygJw',
        'account_id': 1900015976,
        'v': 5.131,
    })
    s = response.json()
    ids = []
    for el in s['response']:
        ids.append(int(el['id']))
    return ids


def _get_ads():
    data = []

    # all_clients_ids = _get_camp()
    ids = _get_clients()
    for i in range(len(ids)):
        if i % 2 == 0:
            time.sleep(1.01)
        response = requests.post('https://api.vk.com/method/ads.getAds', params={
            'access_token': 'vk1.a.J4JNwE0KNXLPpteH7ONBfTQIPsYe6DB4ZfwXLQUfs8oRx_IJRyVFK_5BGjHiKvHYrUjy4BGgrLseyNq-Sx02WaCmXoZCszF7VMcM2KZK0vxUQUqvZAuvBAtAafoUrk8PKmUYAWF9vXQ35sgRFTVOz8K5NGZpTaG7d_qZT9wwtD1fVAerVXfv6NGzbFNw9qNu0D2euVOpvdP4myuM9eygJw',
            'account_id': 1900015976,
            'client_id': ids[i],
            'v': 5.131,
        })
        data.append(response.json())
    return data


def parce(data: list) -> list:
    ads_list = []
    for el in data:
        for ej in el['response']:
            ads_list.append(int(ej['id']))
    return ads_list


def get_messages():
    targets_today = []
    all_ads: list = _get_ads()
    ads_list = parce(all_ads)
    data: list = []

    for i in range(len(ads_list)):
        if i % 2 == 0:
            time.sleep(1.01)
        response = requests.post('https://api.vk.com/method/ads.getStatistics', params={
            'access_token': 'vk1.a.J4JNwE0KNXLPpteH7ONBfTQIPsYe6DB4ZfwXLQUfs8oRx_IJRyVFK_5BGjHiKvHYrUjy4BGgrLseyNq-Sx02WaCmXoZCszF7VMcM2KZK0vxUQUqvZAuvBAtAafoUrk8PKmUYAWF9vXQ35sgRFTVOz8K5NGZpTaG7d_qZT9wwtD1fVAerVXfv6NGzbFNw9qNu0D2euVOpvdP4myuM9eygJw',
            'account_id': 1900015976,
            'ids_type': 'ad',
            'ids': ads_list[i],
            'period': 'day',
            'date_from': today,
            'date_to': 0,
            'v': 5.131,
        })
        data.append(response.json())

    ids: list = []
    names: list = []

    for el in all_ads:
        stats = el['response']
        for ej in stats:
            ids.append(ej['id'])
            names.append(ej['name'])

    ds = dict(zip(ids, names))
    for el in data:
        for ej in el['response']:
            status = ej['stats']
            for elem in status:
                try:
                    count_messages = elem['message_sends_by_any_user']
                except:
                    count_messages = 0
                try:
                    spent_money = elem['spent']
                except:
                    spent_money = 0

                targets_today.append(
                    {
                        'Артикул': ds[ej["id"]],
                        'Кол-во сообщений за день': count_messages,
                        'Потрачено за день': spent_money
                    }
                )
    tg = []
    for el in set(names):
        all_cost = 0
        all_msg = 0
        for ej in targets_today:
            if ej['Артикул'] == el:
                all_cost += float(ej['Потрачено за день'])
                all_msg += int(ej['Кол-во сообщений за день'])
        tg.append({
            'Артикул': el,
            'Кол-во сообщений за день': all_msg,
            'Потрачено за день': all_cost
        })

    return tg


if __name__ == '__main__':
    print(get_messages())

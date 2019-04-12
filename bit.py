import requests
import os
import argparse
from dotenv import load_dotenv
load_dotenv()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_link', nargs=1)
    return parser


def create_bitlink(link):

    bitlink_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    payload = {
        'long_url': link,
        'group_id': '',
        'domain': 'bit.ly',
        'title': 'python',
    }

    response = requests.post(bitlink_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def get_summary_clicks(bitlink):

    sum_bitlink_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(bitlink[7:])
    payload = {
        'unit': 'month',
        'units': -1,
    }

    response = requests.get(sum_bitlink_url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(link):
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(link[7:])
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
    return False


if __name__ == '__main__':

    token = os.getenv('TOKEN')
    client_url = 'https://api-ssl.bitly.com/v4/user'
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    recommendation = 'Check the entered data'

    parser = create_parser()
    namespace = parser.parse_args()
    user_link = namespace.user_link[0]

    if is_bitlink(user_link):
        try:
            print(get_summary_clicks(user_link))
        except requests.exceptions.HTTPError as error:

            exit("Can't get data from server:\n{0}\n{1}".format(error, recommendation))
    else:
        try:
            print(create_bitlink(user_link))
        except requests.exceptions.HTTPError as error:
            exit("Can't get data from server:\n{0}\n{1}".format(error, recommendation))

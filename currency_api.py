
import logging

from urllib.request import Request, urlopen, urlretrieve
from urllib.parse import quote

import json
import re

logger = logging.getLogger('bot_log')


def update_rates():

    try:
        with urlopen(
                Request('https://poe.ninja/api/data/currencyoverview?league=Delirium&type=Currency',
                        headers={'User-Agent': 'Mozilla/5.0'})) as url:
            return json.loads(url.read().decode())
        # print(rate_data)
    except Exception as exception:
        logger.error(
            "Could not fetch rates update from API: {}".format(exception))

    return None


def download_img_url(url, name):

    match = re.search("\.(jpg|png|jpeg)", url)

    if not match:
        logger.error(
            "Could not find image extension or Is not image: {}".format(url))
        raise Exception

    file_name = "{}.{}".format(name, match.group(1))
    urlretrieve(url, file_name)

    return file_name


if __name__ == '__main__':
    json_data = update_rates()

    # print(json.dumps(json_data, indent=4, sort_keys=True))

    logger.setLevel(level=logging.DEBUG)

    console_log = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
    console_log.setFormatter(formatter)
    logger.addHandler(console_log)

    for currency in json_data['currencyDetails']:

        url = currency['icon']
        url = re.sub(' ', '%20', url)

        name = currency['name']
        name = re.sub(" ", "_", name)
        name = re.sub("'s", "", name)
        name = name.lower()

        logger.debug("name: {}".format(name))
        file_name = download_img_url(
            url, 'assets/new_currency_templates/' + name)

        logger.debug("Downloaded {} into {}".format(url, file_name))

''' generate currency classes python file '''

from urllib.request import Request, urlopen, urlretrieve
from urllib.parse import quote

import json
import logging
import re

logger = logging.getLogger(__name__)


def get_items_poe_ninja():

    try:
        with urlopen(
                Request('https://poe.ninja/api/data/currencyoverview?league=Delirium&type=Currency',
                        headers={'User-Agent': 'Mozilla/5.0'})) as url:
            return json.loads(url.read().decode())
    except Exception as exception:
        logger.error(
            "Could not fetch from API: {}".format(exception))

    return None


def get_item_poe_wiki(item_name):

    logger.info("Fetching POE WIKI infor for: {}".format(item_name))

    item_name = re.sub(" ", "%20", item_name)

    url = 'https://pathofexile.gamepedia.com/api.php?action=cargoquery&' + \
        'tables=items,stackables&' + \
        'join%20on=items._PageName=stackables._PageName&' + \
        'fields=stackables.stack_size,items.name,items.size_x,items.size_y&' + \
        'where=items.name="{}"&' + \
        'format=json'

    url = url.format(item_name)

    try:
        with urlopen(
                Request(url, headers={'User-Agent': 'Mozilla/5.0'})) as url:
            return json.loads(url.read().decode())
    except Exception as exception:
        logger.error(
            "Could not fetch from API: {}".format(exception))

    return None


def download_img_url(url, name):

    match = re.search("\.(jpg|png|jpeg)", url)

    if not match:
        logger.error(
            "Could not find image extension or Is not image: {}".format(url))
        raise Exception

    file_name = "{}.{}".format(name, match.group(1))

    logger.info("Downloading image: {}".format(url))
    # urlretrieve(url, file_name)

    return file_name


def main():
    ''' Donwload the currency images that will be used for template matching '''

    json_data = get_items_poe_ninja()

    data = {}
    commented = {}

    for currency in json_data['currencyDetails']:

        # Internal name
        name = currency['name']
        name = re.sub(" ", "_", name)
        name = re.sub("'s", "", name)
        name = name.lower()

        # Class Name
        class_name = currency['name']
        class_name = re.sub("'s", "", class_name)
        class_name = re.sub("-", "", class_name)
        class_name = re.sub(r'\b(\w)', r'\1'.upper(), class_name)
        class_name = re.sub(' ', '', class_name)

        # Pretty name
        pretty_name = currency['name']

        # Possible regex describing name
        regex = pretty_name

        url = currency['icon']
        url = re.sub(' ', '%20', url)

        # Path to the currency template
        template_path = download_img_url(
            url, '../assets/new_currency_templates/' + name)

        template_path = re.sub("\.\.\/", "", template_path)

        wiki_data = get_item_poe_wiki(pretty_name)

        tgt = None
        if wiki_data['cargoquery'][0]['title']['stack size'] == "":
            tgt = commented
        else:
            tgt = data

        tgt[pretty_name] = {}
        tgt[pretty_name]['pretty_name'] = pretty_name
        tgt[pretty_name]['class_name'] = class_name
        tgt[pretty_name]['name'] = name
        tgt[pretty_name]['regex'] = regex
        tgt[pretty_name]['template_path'] = template_path

        # Stack size missing
        # Skip this item // Comment it
        tgt[pretty_name]['stack_size'] = wiki_data['cargoquery'][0]['title']['stack size']
        tgt[pretty_name]['size_x'] = wiki_data['cargoquery'][0]['title']['size x']
        tgt[pretty_name]['size_y'] = wiki_data['cargoquery'][0]['title']['size y']

    text = HEADER
    curr_list = []
    for d in data:
        print(data[d]['class_name'])

        curr_list += [data[d]['class_name']]

        text += CLASS_TEMPLATE.format(
            data[d]['class_name'],
            data[d]['pretty_name'],
            data[d]['name'],
            data[d]['pretty_name'],
            data[d]['stack_size'],
            data[d]['regex'],
            data[d]['template_path'],
            data[d]["size_x"],
            data[d]["size_y"])

    all_curr = "CURRENCY_LIST = [ \n\t" + ",\n\t".join(curr_list) + "\n]"

    text += all_curr

    for d in commented:
        print(commented[d]['class_name'])
        temp = CLASS_TEMPLATE.format(
            commented[d]['class_name'],
            commented[d]['pretty_name'],
            commented[d]['name'],
            commented[d]['pretty_name'],
            commented[d]['stack_size'],
            commented[d]['regex'],
            commented[d]['template_path'],
            commented[d]["size_x"],
            commented[d]["size_y"])

        text += re.sub(r'(.*)', r'#\1', temp)

    with open("currency.py", "w") as f:
        f.write(text)


CLASS_TEMPLATE = """
class {}(Currency):
    ''' {} '''

    name = "{}"
    pretty_name = "{}"
    stack_size = {}
    regex = "{}"
    template_path = "{}"
    size_x = {}
    size_y = {}

"""


HEADER = """
''' Currencies '''

class CurrencyStack():
    ''' Stack of Currceny '''

    def __init__(self, curr, ammount):
        self.curr = curr
        self.ammount = ammount

    def __str__(self):
        return "Stack of {} {}".format(self.ammount, self.curr.pretty_name)


class Currency():
    ''' Currencies class '''

    name = None
    pretty_name = None
    stack_size = None
    regex = None
    template_path = None
    size_x = 0
    size_y = 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.pretty_name
"""

if __name__ == '__main__':

    logger.setLevel(level=logging.DEBUG)

    console_log = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
    console_log.setFormatter(formatter)
    logger.addHandler(console_log)

    main()

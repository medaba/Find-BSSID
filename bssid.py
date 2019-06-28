#!/usr/bin/env python3

import sys
import requests
import xml.etree.ElementTree as et
import webbrowser
import pyperclip
from fire import Fire


def get_bssid():
    """Получает BSSID из командной строки, или из буфера обмена.
       Возвращает BSSID без знаков препинания
    """
    if len(sys.argv) > 1:
        bssid = sys.argv[1]
    else:
        bssid = pyperclip.paste()

    bssid = bssid.replace(':','')
    bssid = bssid.replace('-','')
    bssid = bssid.replace(' ','')

    return bssid


def get_coordinates():
    """Делает запрос к maps.yandex и передает в нем полученный BSSID.
       Возвращает координаты этой точки, либо 'Not found' в случае неудачи
       """
    bssid = get_bssid()
    resp = requests.get(f'http://mobile.maps.yandex.net/cellid_location/?clid=-1&lac=-1&cellid=-1&operatorid=null&countrycode=null&signalstrength=-1&wifinetworks={bssid}:-65&app')
    error = resp.text.find('error')

    if error > 0:
        sys.exit('Not found')
    else:
        xml = et.fromstring(resp.text)
        latitude = (xml.find('./coordinates').attrib['latitude'])
        longitude = (xml.find('./coordinates').attrib['longitude'])

    return f'{latitude},{longitude}'


def open_map(mapit=True):
    if mapit:
        webbrowser.open(f'https://maps.yandex.ru/?text={get_coordinates()}')
    else:
        print(get_coordinates())



if __name__ == '__main__':
   Fire(open_map)


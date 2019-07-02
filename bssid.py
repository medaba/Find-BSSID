#!/usr/bin/env python3

import sys
import requests
import xml.etree.ElementTree as et
import webbrowser
import pyperclip
from fire import Fire


def get_bssid(bssid=None):
    """
    Принимает BSSID в качестве аргумента, а если его там нет ->
    Извлекает BSSID из командной строки, или из буфера обмена. ->
    Возвращает строку с BSSID без знаков препинания
    """
    if bssid == None:
        if len(sys.argv) > 1:
            bssid = sys.argv[1]
        else:
            bssid = pyperclip.paste()

    bssid = bssid.replace(':','')
    bssid = bssid.replace('-','')
    bssid = bssid.replace(' ','')

    return bssid


def get_coordinates(bssid=None):
    """
    Делает запрос к maps.yandex и передает ему полученный BSSID.
    Возвращает координаты этой точки, либо 'Not found' в случае неудачи
    """
    bssid = get_bssid(bssid)
    r = requests.get(f'http://mobile.maps.yandex.net/cellid_location/?clid=-1&lac=-1&cellid=-1&operatorid=null&countrycode=null&signalstrength=-1&wifinetworks={bssid}:-65&app')
    error = r.text.find('error')

    if error > 0:
        return 'Not found'
    else:
        xml = et.fromstring(r.text)
        latitude = (xml.find('./coordinates').attrib['latitude'])
        longitude = (xml.find('./coordinates').attrib['longitude'])

    return f'{latitude},{longitude}'


def get_coords_list(bssid_list):
    """
    Принимает список bssid
    Пытается найти эти адреса
    В случае успеха добавляет координаты в словарь
    Возвращает словарь вида 'bssid': 'latitude,longitude'
    """
    coords = {}

    for x in bssid_list:
        check_bssid = get_coordinates(x)

        if check_bssid == 'Not found':
            continue
        else:
            coords[x] = check_bssid

    return coords


def open_map(bssid=None):
    coordinates = get_coordinates(bssid)
    if coordinates != 'Not found':
        webbrowser.open(f'https://maps.yandex.ru/?text={coordinates}')
        print(coordinates)
    else:
        print(coordinates)



def main(mapit=True):

    if mapit:
        open_map()
    else:
        print(get_coordinates())

    crds = get_coords_list(['20:4E:7F:E0:89:F8',
                            '00:22:B0:F3:B9:D9',
                            '00:4F:62:2D:D5:2C',
                            'B0:48:7A:AB:FB:88',
                            'A0:63:91:6F:1C:E7'])

    print(crds)



if __name__ == '__main__':
   Fire(main)


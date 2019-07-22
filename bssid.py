#!/usr/bin/env python3

import sys
import requests
import xml.etree.ElementTree as et
import webbrowser
import pyperclip
from fire import Fire


def get_bssid(bssid=None):
    """Принимает BSSID в качестве аргумента, а если его там нет ->
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
    """Делает запрос к maps.yandex и передает ему полученный BSSID.
       Возвращает координаты этой точки, либо 'Not found' в случае неудачи
       """
    bssid = get_bssid(bssid)
    r = requests.get(f'http://mobile.maps.yandex.net/cellid_location/?clid=-1&lac=-1&cellid=-1&operatorid=null&countrycode=null&signalstrength=-1&wifinetworks={bssid}:-65&app')

    if "error" in r.text:
        return 'Not found'
    else:
        xml = et.fromstring(r.text)
        latitude = (xml.find('./coordinates').attrib['latitude'])
        longitude = (xml.find('./coordinates').attrib['longitude'])

    return f'{latitude},{longitude}'


def get_coords_dict(bssid_list):
    """Принимает список bssid
       Пытается найти эти адреса
       В случае успеха добавляет координаты в словарь
       Возвращает словарь вида 'bssid': 'latitude,longitude'
       """
    coords = {}

    for bssid in bssid_list:
        checked = get_coordinates(bssid)

        if checked == 'Not found':
            continue
        else:
            coords[bssid] = checked

    return coords


def open_map(bssid=None):
    """Принимает BSSID
       Передает его далее для поиска координат
       В случае успеха открывает в браузере карту с данными координатами
       """
    coordinates = get_coordinates(bssid)
    if coordinates != 'Not found':
        webbrowser.open(f'https://maps.yandex.ru/?text={coordinates}')
    else:
        return coordinates



def main():

    # open_map('C8:3A:35:3E:95:18')
    print(get_coords_dict(['C8:3A:35:3E:95:18']))



if __name__ == '__main__':
   Fire(main)

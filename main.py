import requests
import time
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# from random import choice


def get_google_links(url, useragent=None, proxy=None):
    """Функция принимает адрес с дорк запросом
    и возвращает список с урл страниц"""

    r = requests.get(url, headers=useragent, proxies=proxy, timeout=5)  # передаем значения юзе аг. и прокси
    print('Google', r.status_code)  # получаем статус код от гугла
    if 'ничего не найдено' in r.text:
        print('В гугле больше нет ссылок  для поиска')  # вызываем исключение если нет страниц больше
        raise Exception
    else:
        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.find_all('div', class_='kCrYT')
        urls = []
        for i in title:
            try:  # конструкция для отлова исключений
                links = i.find('a').get('href')  # ищем все ссылки и методом get достем их из href
                links = 'https://www.google.ru' + links  # корректно оформляем ссылку
                urls.append(links)  # добавляем найденную ссылку в список

            except AttributeError:  # игнорируем самую частую ошибку 'NoneType'
                continue

            except Exception as e:  # ловим возможные другие исключения
                print('Google error: ', e)  # печатаем ошибку и причину ошибки/исключения
                continue  # если происходит исключение продолжить цикл пропустив итерацию

        for el in urls:  # в цикле обработать запись
            with open('BigDataDork.txt', 'a', encoding='utf-8', errors='ignore') as file:
                file.writelines(el + '\n')  # записываем в каждую строчку/линию
                print(el)  # выводим на экран элементы из списка urls
        return urls  # возвращаем список url


def get_file(url, useragent=None, proxy=None):
    """Функция переходит по url и получает содержимое (текст)"""
    try:  # с отработкой исключений
        requests.packages.urllib3.disable_warnings()  # отключаем проверку безопасности (проблемы с сертификатом)
        r = requests.get(url, headers=useragent, proxies=proxy, verify=False, timeout=30)  # получаем содерж страницы
        print(str(url[35:55]), r.status_code)  # выводим часть адреса url и статус запроса
        return r.text.strip()  # возвращаем текст из url адреса
    except Exception as e:  # отработка исключений
        print('Get text from site error: ', e)  # печатаем инфу об исключениях
        empty = ''
        return empty  # возвращам пустой файл для записи если что то не так


def save_pages(file_object):
    """Функция сохранения конечных данных в файл"""
    with open('BigData.txt', 'a', encoding='utf-8', errors='ignore') as f:
        f.write(file_object)


def main():
    dorks = ['https://www.google.ru/search?q=ext:txt+intext:%22%40gmail.com%22+intext:%22password%22+after:2000'
             '&newwindow=1&hl=ru-UA&gbv=1&ei=6x3OX8XrLceFrwT7jK3gBA&start=',
             'https://image.google.ge/search?q=allintext:%40gmail.com+filetype:log&gbv=1&ei=QK1LYIj5GsX0kgXuibSgDg&start=']  # урл с дорк запросом в гугле
    last_url = '0'  # для корректности адреса
    # TODO: сделать чтоб брал из файла дорки
    # useragents = open("useragent.txt").read().split('\n')  # читаем юзер агенты из файла и форм-ем список из них
    # proxies = open("proxy.txt").read().split('\n')  # тоже самое с прокси серверами

    for dork in dorks:
        # отчет со страницы (n)
        # продолжать цикл пока не достигнем (n30)
        # useragent = {'User-Agent': choice(useragents)}  # с помощью рандома выбираем юз.агент оформляем в словарь
        # proxy = {'http': 'http://' + choice(proxies)}  # тоже самое с прокси серверами

        # print(useragent, '\n', proxy)
        page_number = 1
        while page_number != 3000:
            url_gen = dork + str(page_number) + last_url

            print(url_gen)
            print('Ждем 70 sec')
            time.sleep(7)
            try:
                lists_url = get_google_links(url_gen)
                for url in lists_url:
                    save_pages(get_file(url))
                page_number += 1
            except Exception as e:
                print(e)
                page_number = 1
        continue


if __name__ == '__main__':
    main()

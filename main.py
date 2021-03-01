import requests
import time
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# from random import choice


#     first_url = "https://www.google.ru/search?q=ext:txt+intext:%22%40gmail.com%22+intext:%22password%22+after:2000" \
#                 "&newwindow=1&hl=ru-UA&gbv=1&ei=6x3OX8XrLceFrwT7jK3gBA&start="

def get_google_links(url, useragent=None, proxy=None):  # по умолчанию юзер агент и прокси равны None
    """Функция принимает адрес с дорк запросом
    и возвращает список с урл страниц"""

    r = requests.get(url, headers=useragent, proxies=proxy, timeout=5)  # передаем значения юзе аг. и прокси
    print('Google', r.status_code)  # получаем статус код от гугла

    soup = BeautifulSoup(r.text, 'lxml')  # создаем экземпляр класса bs4 передаем значение r.text и указываем парсер
    title = soup.find_all('div', class_='kCrYT')  # создаем переменную и передаем область поиска (find_all -> [])
    urls = []  # создаем пустой список урлов
    for i in title:  # в цикле обрабатываем поиск
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
        with open('BigDataDork.txt', 'a') as file:  # создаем файл для записи
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
    with open('BigData.txt', 'a') as f:
        f.write(file_object)


def main():
    first_url = "https://www.google.ru/search?q=filetype:txt+intext:password+after:2010+intext:%22+%22%40gmail.com%22" \
                "%20%22+|+%40yahoo.com+|+%40hotmail.com&newwindow=1&gbv=1&start="  # урл с дорк запросом в гугле
    last_url = '0' # элемент для построения урл

    # useragents = open("useragent.txt").read().split('\n')  # читаем юзер агенты из файла и форм-ем список из них
    # proxies = open("proxy.txt").read().split('\n')  # тоже самое с прокси серверами

    page_number = 1  # отчет со страницы (n)
    while page_number != 3000:  # продолжать цикл пока не достигнем (n30)
        # useragent = {'User-Agent': choice(useragents)}  # с помощью рандома выбираем юз.агент оформляем в словарь
        # proxy = {'http': 'http://' + choice(proxies)}  # тоже самое с прокси серверами

        # print(useragent, '\n', proxy)  # выводим какой выбран прокси и юзер агент

        url_gen = first_url + str(page_number) + last_url  # формируем урл с начальной страницей

        print(url_gen)  # печатаем полученнную страницу
        print('waiting 70 sec')
        time.sleep(70)  # ждем 60 сек (гугл очень привередлив и выдает 429)

        for url in get_google_links(url_gen):  # в цикле скармливаем полученную урл с доркой, нашей ф-ции
            save_pages(get_file(url))  # сохраняем результат
        page_number += 1  # прибавляем к счетчику единицу


if __name__ == '__main__':
    main()

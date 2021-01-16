TOKEN=''


import requests
import os
HEADERS = {
        "Authorization":f"OAuth {TOKEN}"
    }

def getting_name_dir():
    """Вводим имя новой папке на Яндекс диске"""
    active1 = True
    while active1:
        new_yandex_dir = input(
            "Ведите имя нового или существующего каталога в Яндекс диск, для копирования туда файлов с жеского диска компьютьера: ")
        new_yandex_dir = new_yandex_dir.strip()


        new_yandex_dir = new_yandex_dir.split(' ')

        if (len(new_yandex_dir) > 1 or  len(new_yandex_dir[0]) ==0):
            print('Вы ввели имя с ошибкой, повторите')
            continue
        else:
            return new_yandex_dir[0]


new_dir=getting_name_dir()

# В этом блоке проверяем существуетли каталог new_dir
# dir = True - такой каталог существует уже, dir=False - не существует
try:

    response = requests.get(
        "https://cloud-api.yandex.net/v1/disk/resources",
        params={
            "path": new_dir,  # Запись c именем

        },
        headers=HEADERS
    )
    response.raise_for_status()
    answer = response.json()['_embedded']['path']
    print("Такой каталого уже существует")
    dir=True

except:

    print("Такого каталога еще не существует, и он будет создан!")
    dir=False



#Если каталога не существует dir==False, то создаем его в яндекс Диске в корне
if dir==False:
    response = requests.put(
        "https://cloud-api.yandex.net/v1/disk/resources",
        params={
            "path": new_dir,  # Запись c именем

        },
        headers=HEADERS
    )
    response.raise_for_status()
    answer = response.json()
    print("Создан каталог", answer)


#Вводим путь на файл на компьютере
active = True
while active:
    url_new = input(r"Введите ссылку на файл на фашем компьютере типа c:\my_folder\file.txt, или 'q' для выхода: ")
    if url_new == 'q' or url_new == 'Q':
        print("Вы вышли из программы! Всего доброго!")
        break
    #Проверяем существует ли файл
    if os.path.exists(url_new) == True:
        file_name=os.path.basename(url_new) #берем от пути  - название файла

        A=[new_dir, file_name]


        url_yandex_disk='/'.join(A)
        response = requests.get(
            "https://cloud-api.yandex.net/v1/disk/resources/upload",
            params={
                # "path": file_name_urel,  # Запись c именем
                "path": url_yandex_disk,  # Запись c именем
                "overwrite": 'true'  # Атрибут перезаписи файла
            },
            headers=HEADERS
        )
        response.raise_for_status()
        href = response.json()['href']
        print("href", href)


        print("url_new", url_new)

        with open(url_new, 'rb') as f:
            upload_response = requests.put(href, files={"file": f})
            upload_response.raise_for_status()
            print("Файл на ядекс диск загружен успешно")
    else:
        print("Такого файла не существует, попробуйте заново ввести:")
        continue


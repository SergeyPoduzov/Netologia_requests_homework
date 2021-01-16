import requests
import os
#Сылка на АПИ
link ="https://superheroapi.com/api"
# https://superheroapi.com/api/2619421814940190/149
heroes = [] #это будет список героев
id_heroes = [149,332, 655] # initial ids heroes От сюда https://superheroapi.com/ids.html - взал ID  вручном режиме

IMG_DIR = 'images'# папка чтобы сохранить картинки героев
if os.path.isdir(IMG_DIR) == False:
    os.mkdir(IMG_DIR)

token = 2619421814940190

class Hero:
    """Класс героев"""
    def __init__(self, id, name):
        self.id=id
        self.name=name
        self.clever=0
        self.image=""

    def getting_clever(self, clever_num):
        """Добавление Ума"""
        self.clever +=int(clever_num)
    def getting_image(self, image):
        if (type(image)==str):
            self.image=image

    def __str__(self):
        txt=""
        txt +="Имя героя: " + self.name + ", его ум: " + str(self.clever) + " баллов."
        return txt

def adding_to_Heroes(hero):
    """Функция добавления героя к героям"""
    heroes.append(hero)

def find_clever_hero(heroes):
    """Функция поиска самого умного героя"""
    list_clever_hero=[]
    max_clever = 0
    for hero in heroes:
        if hero.clever>max_clever:
            max_clever=hero.clever
            list_clever_hero=[]
            list_clever_hero.append(hero)
        elif hero.intelligence==max_clever:
            list_clever_hero.append(hero)
    return list_clever_hero

for hero in id_heroes:
    A=[link, str(token),str(hero)]
    new_path="/".join(A)


    response = requests.get(
        new_path,
    )
    data_name=response.json()["name"]
    data_intelligence = response.json()["powerstats"]["intelligence"]
    data_img_url=response.json()["image"]["url"]


    new_hero=Hero(hero, data_name)
    new_hero.getting_clever(data_intelligence)
    heroes.append( new_hero)

    new_hero.getting_image(data_img_url)

    img_response = requests.get(new_hero.image)
    img_response.raise_for_status()

    img_name = new_hero.image.split("/")[-1]
    print( new_hero)
    # wb - запись бацтовых данных
    with open(os.path.join(IMG_DIR, img_name), 'wb') as f:
        f.write(img_response.content)


#Нахождение самого умного героя
heroes_clever=find_clever_hero(heroes)
print("Самые умные герои: ")
for hero in heroes_clever:
    print(hero)
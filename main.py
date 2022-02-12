import os
import pygame
import requests


def geo_search(search):
    geocoder_request = \
        f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b" \
        f"&geocode={search}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym = toponym["Point"]["pos"]
        return toponym
    else:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")


def exitt():
    try:
        os.remove('map.png')
    except Exception:
        pass
    exit()


def update(addr):
    response = requests.get(
        f"http://static-maps.yandex.ru/1.x/?ll={geo_search(addr).replace(' ', ',')}"
        f"&spn={scale},{scale}&l=map")
    if response:
        with open("map.png", "wb") as f:
            f.write(response.content)
    else:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        exitt()


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    pygame.display.set_caption('Большая задача по Maps API. Часть №1')
    clock = pygame.time.Clock()
    while True:
        clock.tick(33)
        update(address)
        screen.blit(pygame.image.load("map.png"), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitt()
        pygame.display.flip()


if __name__ == "__main__":
    address = 'Новосибирск'
    scale = 0.1
    main()

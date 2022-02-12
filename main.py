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
    pos = [float(i) for i in geo_search(addr).split(' ')]
    pos[0] += x
    pos[1] += y
    pos = ','.join([str(i) for i in pos])
    response = requests.get(
        f"http://static-maps.yandex.ru/1.x/?ll={pos}"
        f"&spn={scale},{scale}&l=map")
    if response:
        with open("map.png", "wb") as f:
            f.write(response.content)
    else:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        exitt()


def main():
    global scale, x, y
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    pygame.display.set_caption('Большая задача по Maps API. Часть №3')
    clock = pygame.time.Clock()
    update(address)
    while True:
        ch = False
        clock.tick(33)
        screen.blit(pygame.image.load("map.png"), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitt()
            if event.type == pygame.KEYDOWN:
                # print(scale)
                if event.key == pygame.K_PAGEUP:
                    if 2 > scale > 0.3:
                        scale += 0.1
                        ch = True
                    elif scale < 0.3:
                        scale += 0.01
                        ch = True
                    elif 50 > scale > 2:
                        scale += 1
                        ch = True
                elif event.key == pygame.K_PAGEDOWN:
                    if 0.03 < scale < 0.5:
                        scale -= 0.01
                        ch = True
                    elif 0.03 > scale > 0.01:
                        scale -= 0.005
                        ch = True
                    elif 0.5 < scale < 2:
                        scale -= 0.05
                        ch = True
                    elif scale > 2:
                        scale -= 1
                        ch = True
                if event.key == pygame.K_UP:
                    if -90 <= y + scale <= 90:
                        y += scale
                        ch = True
                elif event.key == pygame.K_LEFT:
                    if -180 <= x - scale * 2 <= 180:
                        x -= scale * 2
                        ch = True
                elif event.key == pygame.K_DOWN:
                    if -90 <= y - scale <= 90:
                        y -= scale
                        ch = True
                elif event.key == pygame.K_RIGHT:
                    if -180 <= x + scale * 2 <= 180:
                        x += scale * 2
                        ch = True
        if ch:
            update(address)
        pygame.display.flip()


if __name__ == "__main__":
    x = y = 0
    address = 'Новосибирск'
    scale = 0.1
    main()

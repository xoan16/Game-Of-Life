import pygame
from mapped import mapping
import math
from time import process_time
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (20,90)

xsize = 1500
ysize = 700
pygame.init()
screen = pygame.display.set_mode((xsize, ysize))
screen.fill((0, 0, 0))
mapping.size(xsize, ysize)
mapping.resetable = False
mapping.first = 2
mapping.camera = ((50, 50))
i = 1
speed = 100
pause = True
font = pygame.font.Font(None, 30)
gen = 0

main_list = [(0, -1), (0, 0), (0, 1)]
dead_list = [(0, -1), (0, 0), (0, 1)]
points_list = [3, 3, 3]
# for x in range(100):
#     for y in range(100):
#         main_list.append((x, y))


xcelda = 100
ycelda = 100

def dis(p1, a1):
    return math.sqrt((p1[0] - a1[0])**2 + (p1[1] - a1[1])**2)

def drawer(a, b, mouse):
    alpha = mapping.unmap(pygame.mouse.get_pos())[0] // xcelda * xcelda + xcelda * a
    beta = mapping.unmap(pygame.mouse.get_pos())[1] // ycelda * ycelda + ycelda * b

    threshold = 300

    if dis(mapping.unmap(mouse), (alpha, beta)) >= threshold:
        factor = 0
    else:
        factor = (threshold - dis(mapping.unmap(mouse), (alpha, beta))) / threshold

    pygame.draw.circle(screen, (round(255 * factor), round(255 * factor), round(255 * factor)), mapping.map((alpha, beta)), mapping.esc(5))

def UI():
    pygame.draw.line(screen, (255, 255, 255), (20, 20), (100, 20), 2)
    pygame.draw.line(screen, (255, 255, 255), (20, 20), (20, 100), 2)
    pygame.draw.line(screen, (255, 255, 255), (xsize - 20, 20), (xsize - 100, 20), 2)
    pygame.draw.line(screen, (255, 255, 255), (xsize - 20, 20), (xsize - 20, 100), 2)
    pygame.draw.line(screen, (255, 255, 255), (20, ysize - 20), (100, ysize - 20), 2)
    pygame.draw.line(screen, (255, 255, 255), (20, ysize - 20), (20, ysize - 100), 2)
    pygame.draw.line(screen, (255, 255, 255), (xsize - 20, ysize - 20), (xsize - 100, ysize - 20), 2)
    pygame.draw.line(screen, (255, 255, 255), (xsize - 20, ysize - 20), (xsize - 20, ysize - 100), 2)
    pygame.draw.circle(screen, (255, 255, 255), mapping.map((50, 50)), mapping.esc(20), mapping.esc(4))
    screen.blit(font.render("cells: " + str(len(main_list)), True, (255, 255, 255)), (40, ysize - 50))
    screen.blit(font.render("generation: " + str(gen), True, (255, 255, 255)), (40, ysize - 75))
    screen.blit(font.render("camera pos: " + str((round(mapping.camera[0]) - 50, round(mapping.camera[1]) - 50)), True, (255, 255, 255)), (xsize // 2 - 80, ysize - 50))
    screen.blit(font.render("zoom: " + str(round(mapping.zoom, 3)), True, (255, 255, 255)), (xsize // 2 - 80, ysize - 75))
    screen.blit(font.render("speed of simulation: " + str(speed), True, (255, 255, 255)), (40, 40))
    getPos = pygame.mouse.get_pos()
    coords = mapping.unmap(getPos)
    alpha = mapping.unmap(getPos)[0] // xcelda * xcelda + 10
    beta = mapping.unmap(getPos)[1] // ycelda * ycelda + 10
    tuple = mapping.map((alpha, beta))
    pygame.draw.rect(screen, (100, 100, 100), (tuple[0], tuple[1], mapping.esc(80), mapping.esc(80)), 1)
    screen.blit(font.render("   " + str((round(coords[0] // xcelda), round(coords[1] // ycelda))), True, (255, 255, 255)), getPos)


def render(alpha):
    alpha = mapping.map((alpha[0]*xcelda + 10, alpha[1]*ycelda + 10))
    pygame.draw.rect(screen, (255, 255, 255), (alpha[0], alpha[1], mapping.esc(xcelda*0.8), mapping.esc(ycelda*0.8)), 3)

def render2(alph, beta):
    alph = mapping.map((alph[0]*xcelda + 10, alph[1]*ycelda + 10))
    if beta <= 4:
        pygame.draw.rect(screen, (0, 0, round((255 // 9) * beta)), (alph[0], alph[1], mapping.esc(xcelda*0.8), mapping.esc(ycelda*0.8)))
    else:
        pygame.draw.rect(screen, (round((255 // 9) * beta), 0, 0), (alph[0], alph[1], mapping.esc(xcelda*0.8), mapping.esc(ycelda*0.8)))

def shadow_engine(mean_list):
    k_list = []
    for x in mean_list:
        k_list.append(x)
    leng = len(k_list)
    points = [0] * leng

    for z in range(leng):
        a = k_list[z][0]
        b = k_list[z][1]
        for x in range(-1, 2):
            for y in range(-1, 2):
                try:
                    points[k_list.index((a + x, b + y))] += 1
                except ValueError:
                    k_list.append((a + x, b + y))
                    points.append(1)

    return k_list, points

def main_engine(mean_list, points, leng): #score = 45
    second_list = []

    for c in range(len(points)):
        if points[c] == 3 or points[c] == 4 and c < leng:
            second_list.append(mean_list[c])


    return second_list

g = process_time()

while True:
    # if gen < 2: # only for benchmarking

    if i%speed == 0:
        main_list = main_engine(dead_list, points_list, len(main_list))
        gen += 1
        i = 1

    if i%speed == speed // 2:
        dead_list, points_list = shadow_engine(main_list)

    for a in range(len(dead_list)):
        render2(dead_list[a], points_list[a])

    # for a in main_list:
    #     render(a)

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        pause = True
    if pygame.key.get_pressed()[pygame.K_RETURN]:
        pause = False
    if pygame.key.get_pressed()[pygame.K_r]:
        pause = True
        main_list = [(0, -1), (0, 0), (0, 1)]
        dead_list = [(0, -1), (0, 0), (0, 1)]
        points_list = [3, 3, 3]
        mapping.postzoom = 1
        mapping.camera = ((50, 50))
        gen = 0

    if pygame.mouse.get_pressed()[0]:
        coords = mapping.unmap(pygame.mouse.get_pos())
        if not (coords[0] // xcelda, coords[1] // ycelda) in main_list:
            main_list.append((coords[0] // xcelda, coords[1] // ycelda))
            dead_list.append((coords[0] // xcelda, coords[1] // ycelda))
            points_list.append(3)

    if pygame.mouse.get_pressed()[2]:
        coords = mapping.unmap(pygame.mouse.get_pos())
        if (coords[0] // xcelda, coords[1] // ycelda) in main_list:
            main_list.remove((coords[0] // xcelda, coords[1] // ycelda))
        if (coords[0] // xcelda, coords[1] // ycelda) in dead_list:
            points_list.pop(dead_list.index((coords[0] // xcelda, coords[1] // ycelda)))
            dead_list.remove((coords[0] // xcelda, coords[1] // ycelda))


    if pause:
        for x in range(-2, 4):
            for y in range(-2, 4):
                drawer(x, y, pygame.mouse.get_pos())
                UI()


    mapping.loop()
    pygame.display.flip()
    screen.fill((0, 0, 0))
    if pause: i += 0
    else: i += 1
    # else: break

time = (process_time() - g) / 100

print("score = " + str(round(1/time, 2)*10))

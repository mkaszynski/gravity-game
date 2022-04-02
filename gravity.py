"""
Simple gravity simulator.

Run with python gravity.py

Controls:
    - "w" : Increase mass of new objects to be placed
    - "s" : Decrease mass of new objects to be placed
    - "Left click" : Place an object
    - "Right click" : Remove an object

"""

import random

import pygame

pygame.init()


def add_line(screen, text, x, y):
    # used to print the status of the variables
    text = font.render(text, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text, text_rect)


font = pygame.font.Font("freesansbold.ttf", 32)


def distance(pos1, pos2):
    """Calculate the distance between two 2d points."""
    x = (pos2[0] - pos1[0]) ** 2
    y = (pos2[1] - pos1[1]) ** 2
    return (x + y) ** 0.5


INIT_VEL_FAC = 3

pause = False

GRAVITY_CONST = 0.0005
MAX_OBJECTS = 150

time2 = 2022

mass = 1

# Set up the drawing window
x_width, y_width = 1200, 650
screen = pygame.display.set_mode([x_width, y_width])
dire = ""

MIN_VAL = 1

clock = pygame.time.Clock()

# these are the gravitational objects
objects = []

# optionally initialize with random objects
# for i in range(0, 100):
#     objects.append([random.random()*650, random.random()*650, random.random()*2*INIT_VEL_FAC - INIT_VEL_FAC, random.random()*2*INIT_VEL_FAC - INIT_VEL_FAC, 1, (random.random()*255, (random.random()*255, (random.random()*255)])


# Run until the user asks to quit
running = True
while running:

    pygame.event.poll()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_p]:
        pause = True
    if keys[pygame.K_o]:
        pause = False

    # global center of gravity
    sum1 = 1e-5
    add1 = 1e-5
    sum2 = 1e-5
    cg = (sum1 / add1, sum2 / add1)

    # increase or decrease mass if w or s is held
    if keys[pygame.K_w]:
        mass += 0.1
    if keys[pygame.K_s]:
        mass -= 0.1

    time2 += 0.05

    if mass < 1:
        mass = 1

    mouse_held = pygame.mouse.get_pressed()
    mx, my = pygame.mouse.get_pos()

    # Remove an object when the right mouse button is held down
    if mouse_held[2]:
        # loop through all objects and check if within 20 pixels
        for i in objects:
            if (
                i[0] > (mx + cg[0] - x_width // 2) - 10
                and i[0] < (mx + cg[0] - x_width // 2) + 10
            ):
                if (
                    i[1] > (my + cg[0] - y_width // 2) - 10
                    and i[1] < (my + cg[0] - y_width // 2) + 10
                ):
                    objects.remove(i)

    # Add an object when the left mouse button is held down
    if mouse_held[0]:
        objects.append(
            [
                mx + cg[0] - x_width // 2,  # x position
                my + cg[1] - y_width // 2,  # y position
                0,  # x velocity
                0,  # y velocity
                mass,  # mass
                random.random() * 255,  # red
                random.random() * 255,  # green
                random.random() * 255,  # blue
            ]
        )

    if not pause:
        for i, obj_a in enumerate(objects):
            for obj_b in objects:

                # skip if self
                if obj_a is obj_b:
                    continue

                xdist = obj_b[0] - obj_a[0]

                if abs(xdist) < MIN_VAL:
                    if xdist < 0:
                        xdist = -MIN_VAL
                    else:
                        xdist = MIN_VAL

                ydist = obj_b[1] - obj_a[1]
                if abs(ydist) < MIN_VAL:
                    if ydist < 0:
                        ydist = -MIN_VAL
                    else:
                        ydist = MIN_VAL

                # compute force of gravity in x direction
                x_gravity = (
                    obj_a[4] * obj_b[4] * GRAVITY_CONST * (xdist) ** -2
                    + obj_a[4] * GRAVITY_CONST
                )
                if xdist < 0:
                    obj_b[2] += x_gravity
                else:
                    obj_b[2] -= x_gravity

                # compute force of gravity in y direction
                y_gravity = (
                    obj_a[4] * obj_b[4] * GRAVITY_CONST * (ydist) ** -2
                    + obj_a[4] * GRAVITY_CONST
                )
                if ydist < 0:
                    obj_b[3] += y_gravity
                else:
                    obj_b[3] -= y_gravity

        for i in objects:
            sum1 += i[0]
            add1 += i[4]
            sum2 += i[1]

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if len(objects) > MAX_OBJECTS:
            objects.remove(random.choice(objects))

        # Fill the background with black
        screen.fill((0, 0, 0))
        add_line(screen, f"mass {mass:.0f}", 0, 0)

        # update the position from velocity
        for g in objects:
            g[0] += g[2]  # x
            g[1] += g[3]  # y

            # objects.append((g[0] + g[2]*0.01, g[1] - g[3]*0.01, g[2], g[3], g[4]))
        # print(len(objects))

        # for o in objects:
        #     if o[0] > 600:
        #         o[0] = 600
        #         o[2]*=-1
        #     if o[0] < 0:
        #         o[0] = 0
        #         o[2]*=-1
        #     if o[1] > 600:
        #         o[1] = 600
        #         o[3]*=-1
        #     if o[1] < 0:
        #         o[1] = 0
        #         o[3]*=-1

        # for x in objects:
        #     for y in objects:
        #         dis = distance((x[0], x[1]), (y[0], y[1]))
        #         if x[0] == y[0] and x[1] == y[1]:
        #             if x in objects:
        #                 objects.remove(x)
        #             if y in objects:
        #                 objects.remove(y)
        #             objects.append([x[0], x[1], 0, 0, (x[4] + y[4])*0.501])

    for u in objects:
        debris = pygame.Rect(
            u[0] - cg[0] + x_width // 2, u[1] - cg[1] + y_width // 2, u[4] * 2, u[4] * 2
        )
        pygame.draw.rect(screen, (u[5], u[6], u[7]), debris)

    clock.tick(60)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

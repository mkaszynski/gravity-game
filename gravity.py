"""
Simple gravity simulator.

Run with python gravity.py

Controls:
    - "w" : Increase mass of new objects to be placed
    - "s" : Decrease mass of new objects to be placed
    - "Left click" : Place an object
    - "Right click" : Remove an object

TODO:
- Add argsparse done
- fix moving camera ?
- fix drift

"""

import random

import argparse

import pygame

def sum_of_list(l):
  total = 0
  for val in l:
    total = total + val
  return total

parser = argparse.ArgumentParser(description="femorph")

parser.add_argument(
    "--add_objects", help="at the start add random particles", action="store_true"
)

args = parser.parse_args()


def add_line(font, screen, text, x, y):
    # used to print the status of the variables
    text = font.render(text, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text, text_rect)


def distance(pos1, pos2):
    """Calculate the distance between two 2d points."""
    x = (pos2[0] - pos1[0]) ** 2
    y = (pos2[1] - pos1[1]) ** 2
    return (x + y) ** 0.5


INIT_VEL_FAC = 1
GRAVITY_CONST = 0.0005
MAX_OBJECTS = 150
MIN_VAL = 1



# Run until the user asks to quit
def main():

    # initialize pygame and the font
    pygame.init()
    font = pygame.font.Font("freesansbold.ttf", 32)
    clock = pygame.time.Clock()

    pause = False
    time2 = 2022

    # Set up the drawing window
    x_width, y_width = 1200, 650
    screen = pygame.display.set_mode([x_width, y_width])
    # these are the gravitational objects
    objects = []
    
    mean = [[600], [325]]
    
    # optionally initialize with random objects
    if args.add_objects:
        for i in range(0, 100):
            objects.append([random.random()*650, random.random()*650, random.random()*2*INIT_VEL_FAC - INIT_VEL_FAC, random.random()*2*INIT_VEL_FAC - INIT_VEL_FAC, 1, random.random()*255, random.random()*255, random.random()*255])
    mass = 1

    running = True
    while running:

        pygame.event.poll()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_p]:
            pause = True
        if keys[pygame.K_o]:
            pause = False

        # global center of gravity
        sum1 = 1
        add1 = 1
        sum2 = 1
        cg = (sum_of_list(mean[0])/len(mean[0]), sum_of_list(mean[1])/len(mean[1]))
        
        # increase or decrease mass if w or s is held
        if keys[pygame.K_w]:
            mass += 0.1
        if keys[pygame.K_s]:
            mass -= 0.1

        time2 += 0.05

        if mass < 1:
            mass = 1
        
        for i in objects:
            mean[0].append(i[0])
            mean[1].append(i[1])

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
                        i[1] > (my + cg[1] - y_width // 2) - 10
                        and i[1] < (my + cg[1] - y_width // 2) + 10
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
            add_line(font, screen, f"mass {mass:.0f}", 0, 0)

            # update the position from velocity
            for g in objects:
                g[0] += g[2]  # x
                g[1] += g[3]  # y

        for u in objects:
            debris = pygame.Rect(
                u[0] - cg[0] + x_width // 2, u[1] - cg[1] + y_width // 2, u[4] * 2, u[4] * 2
            )
            pygame.draw.rect(screen, (u[5], u[6], u[7]), debris)

        clock.tick(60)

        # Flip the display
        pygame.display.flip()
        
        if mean == [[600], [325]]:
            mean = [[600], [325]]

    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':
    main()

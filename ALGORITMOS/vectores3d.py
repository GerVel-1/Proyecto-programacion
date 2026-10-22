import pygame, math

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

cubo = [(-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1),
        (-1,-1, 1), (1,-1, 1), (1,1, 1), (-1,1, 1)]

aristas = [(0,1),(1,2),(2,3),(3,0),
           (4,5),(5,6),(6,7),(7,4),
           (0,4),(1,5),(2,6),(3,7)]

ax = ay = az = 0.0
tz = 5

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    k = pygame.key.get_pressed()
    if k[pygame.K_LEFT]:  ay -= 0.03
    if k[pygame.K_RIGHT]: ay += 0.03
    if k[pygame.K_UP]:    ax -= 0.03
    if k[pygame.K_DOWN]:  ax += 0.03
    if k[pygame.K_q]:     az -= 0.03
    if k[pygame.K_e]:     az += 0.03
    if k[pygame.K_w]:     tz -= 0.05
    if k[pygame.K_s]:     tz += 0.05

    puntos2d = []
    for x, y, z in cubo:
        y, z = y*math.cos(ax) - z*math.sin(ax), y*math.sin(ax) + z*math.cos(ax)
        x, z = x*math.cos(ay) - z*math.sin(ay), x*math.sin(ay) + z*math.cos(ay)
        x, y = x*math.cos(az) - y*math.sin(az), x*math.sin(az) + y*math.cos(az)
        z += tz
        f = 300 / z
        puntos2d.append((300 + x*f, 300 + y*f))

    screen.fill((25, 25, 30))
    for i, j in aristas:
        pygame.draw.line(screen, (0, 200, 255), puntos2d[i], puntos2d[j], 2)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
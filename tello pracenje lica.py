import pygame
import cv2
from djitellopy import Tello

pygame.init()

tello = Tello()

tello.connect()

print(tello.get_battery())

tello.set_speed(20)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_pos = None
tracking = False

img = tello.get_frame_read().frame

cameraWin = pygame.display.set_mode((960, 720))

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:  # Naredba za uzletanje na tipku "t"
                tello.takeoff()
            elif event.key == pygame.K_l:  # Naredba za sletanje na tipku "l"
                tello.land()
            elif event.key == pygame.K_f:
                tracking = not tracking
            elif event.key == pygame.K_r:  # Rotacija u smeru kazaljke na satu na tipku "r"
                tello.rotate_clockwise(45)
            elif event.key == pygame.K_g:  # Rotacija u suprotnom smeru od kazaljke na satu na tipku "g"
                tello.rotate_counter_clockwise(45)
            elif event.key == pygame.K_q:  # Kretanje drona gore na tipku "q"
                tello.move_up(30)
            elif event.key == pygame.K_e:  # Kretanje drona dole na tipku "e"
                tello.move_down(30)
            elif event.key == pygame.K_a:  # Kretanje drona u levo na tipku "a"
                tello.move_left(30)
            elif event.key == pygame.K_d:  # Kretanje drona u desno na tipku "d"
                tello.move_right(30)
            elif event.key == pygame.K_w:  # Kretanje drona napred na tipku "w"
                tello.move_forward(30)
            elif event.key == pygame.K_s:  # Kretanje drona nazad na tipku "s"
                tello.move_back(30)
            elif event.key == pygame.K_UP:  # Salto unapred na tipku strelica na gore
                tello.flip_forward()
            elif event.key == pygame.K_DOWN:  # Salto unazad na tipku strelica na dole
                tello.flip_back()
            elif event.key == pygame.K_LEFT:  # Salto u levo na tipku leva strelica
                tello.flip_left()
            elif event.key == pygame.K_RIGHT:  # Salto u desno na tipku desna strelica
                tello.flip_right()

    if tracking:
        img = tello.get_frame_read().frame
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            face_pos = faces[0]

        if face_pos is not None:
            face_center = (face_pos[0] + face_pos[2] / 2, face_pos[1] + face_pos[3] / 2)
            img_center = (960 / 2, 720 / 2)

            cv2.rectangle(img, (face_pos[0], face_pos[1]), (face_pos[0] + face_pos[2], face_pos[1] + face_pos[3]), (0, 255, 0), 2)

            x = face_center[0] - img_center[0]
            y = face_center[1] - img_center[1]
            z = 0

            speed = int(20 * abs(x) / 480)

            speed = min(speed, 50)

            if abs(x) > 20:
                if x < 0:
                    tello.send_rc_control(-speed, 0, 0, 0)
                else:
                    tello.send_rc_control(speed, 0, 0, 0)

                if abs(y) > 20:
                    if y < 0:
                        tello.send_rc_control(0, speed, 0, 0)
                    else:
                        tello.send_rc_control(0, -speed, 0, 0)

            else:
                tello.send_rc_control(0, 0, 0, 0)

img = tello.get_frame_read().frame
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = pygame.surfarray.make_surface(img)
cameraWin.blit(img, (0, 0))

pygame.display.update()

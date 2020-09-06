# Import 'kivy.core.text' must be called in entry point script
# before import of cv2 to initialize Kivy's text provider.
# This fixes crash on app exit.

import kivy.core.text
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
import face_recognition
import cv2


class KCamera(Image):

    def __init__(self, **kwargs):
        super(KCamera, self).__init__(**kwargs)
        self.capture = None

    def start(self, capture, fps=30):
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule_interval(self.update)
        self.capture = None

    def update(self, dt):

        global prev_y1
        global prev_x1
        global prev_y2
        global prev_x2
        global vel
        global squarepart
        global currentx
        global currenty

        # print(f'{currentx, currenty} loooooooool')
        # print(root.ids.squarepart.pos)

        return_value, frame = self.capture.read()

        if return_value:

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)

            if len(face_locations) >= 1:

                y1, x1, y2, x2 = face_locations[0]


                if y1 - prev_y1 < 0:
                    currenty += vel

                # if  updated y position higher than previous x position go up

                if y1 - prev_y1 > 0:
                    currenty -= vel

                squarepart.pos[1] = currenty
                prev_y1, prev_x1, prev_y2, prev_x2 = y1, x1, y2, x2





            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()
                texture.flip_horizontal()
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()







class QrtestHome(BoxLayout):

    def init_qrtest(self):
        global capture
        global prev_y1
        global prev_x1
        global prev_y2
        global prev_x2
        global vel
        global squarepart
        global currentx
        global currenty

        prev_y1, prev_x1, prev_y2, prev_x2 = 0,0,0,0
        vel = 50

        squarepart = self.ids.squarepart
        currentx = squarepart.pos[0]
        currenty = squarepart.pos[1]
        print(currentx, currenty)
        capture = cv2.VideoCapture(0)
        self.ids.qrcam.start(capture)




class qrtestApp(App):

    def build(self):
        homeWin = QrtestHome()
        homeWin.init_qrtest()

        return homeWin

    def on_stop(self):
        global capture
        if capture:
            capture.release()
            capture = None

qrtestApp().run()
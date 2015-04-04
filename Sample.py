################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################
import sys
sys.path.insert(0, "./lib")
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from PIL import Image
import ctypes
from flask import Flask, render_template, Response
import StringIO

from camera import Camera

# flask app
app = Flask(__name__)

# global image stream
current_image = StringIO.StringIO()

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def gen_frame():
    while True:
        frame = current_image.getvalue()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # return Response(gen_frame(),
                    # mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

class SampleListener(Leap.Listener):

    def __init__(self):
        Leap.Listener.__init__(self)
        self.last_image = False;

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_images(self, controller):
        global current_image

        if (self.last_image + 1 < time.time()):
            image = controller.images[0]
            imagedata = ctypes.cast(image.data.cast().__long__(), ctypes.POINTER(image.width*image.height*ctypes.c_ubyte)).contents
            image_object = Image.frombuffer("L", (image.width, image.height), imagedata, "raw", "L", 0, 1)
            # image_object.save(current_image, "JPEG");
            image_object.save("1.jpg", "JPEG");
            print "Got Image"
            self.last_image = time.time()
            # controller.remove_listener(self);
        

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Startup the flask app
    app.run(host='0.0.0.0', debug=True)

    # when the flask app is killed, remove the listener
    controller.remove_listener(listener)

    # # Keep this process running until Enter is pressed
    # print "Press Enter to quit..."
    # try:
    #     sys.stdin.readline()
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     # Remove the sample listener when done
    #     controller.remove_listener(listener)


if __name__ == "__main__":
    main()

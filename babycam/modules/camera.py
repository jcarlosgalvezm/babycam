import time
import threading
from PIL import Image, ImageChops
from io import BytesIO
import numpy as np
from .notifications import Notify
import logging
import io
import time
import picamera

try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class CameraEvent(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """
    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    thread = None  # background thread that reads frames from camera
    th_motion = None  # background thread that detects motion
    frame = None  # current frame is stored here by background thread
    last_frame = None  # lastframe is stored here by background thread
    last_access = 0  # time of last client access to the camera
    event = CameraEvent()
    logger = logging.getLogger('BabyCam')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    def __init__(self):
        """Start the background camera thread if it isn't running yet."""
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()

            # start background frame thread
            BaseCamera.thread = threading.Thread(target=self._thread)
            BaseCamera.thread.start()

            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)

    @staticmethod
    def get_frame():
        """Return the current camera frame."""
        BaseCamera.last_access = time.time()

        # wait for a signal from the camera thread
        BaseCamera.event.wait()
        BaseCamera.event.clear()

        return BaseCamera.frame

    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            camera.resolution = (1920, 1080)
            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            for item in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        th_motion = threading.Thread()
        for frame in frames_iterator:
            BaseCamera.last_frame = BaseCamera.frame
            BaseCamera.frame = frame
            if th_motion.is_alive() is False:
                th_motion = threading.Thread(target=BaseCamera.motion, args=(BaseCamera.last_frame, BaseCamera.frame,))
                th_motion.start()
            BaseCamera.event.set()  # send signal to client
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break
        BaseCamera.thread = None

    @staticmethod
    def image_entropy(img):
        w, h = img.size
        a = np.array(img.convert('RGB')).reshape((w*h, 3))
        h, e = np.histogramdd(a, bins=(16,)*3, range=((0, 256),)*3)
        prob = h/np.sum(h)  # normalize
        prob = prob[prob > 0]  # remove zeros
        return -np.sum(prob*np.log2(prob))

    @staticmethod
    def motion(lastframe, currentframe):

        try:
            lf = Image.open(BytesIO(lastframe))
            cf = Image.open(BytesIO(currentframe))

            img = ImageChops.difference(cf, lf)
            if BaseCamera.image_entropy(img) > 0.09:
                print('Lucia se mueve')
                Notify.notify()
        except Exception as e:
            print(e)
            return

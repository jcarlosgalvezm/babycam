from instapush import Instapush, App
import time


class Notify(object):

    def __init__(self):
        pass

    @staticmethod
    def notify():
        app = App(appid='59e0f493a4c48a96c0d2736a', secret='b641a88dc13e74bad108186d69b767de')
        app.notify(event_name='BabyCam', trackers={'Baby': 'Lucia'})
        time.sleep(600)

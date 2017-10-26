from instapush import Instapush, App
import time


class Notify(object):

    def __init__(self):
        pass
    
    @staticmethod
    def readcfg():
        with open('config.yml', 'r', enconding='utf-8') as yml:
            cfg = yaml.safe_load(yml)

        return cfg['usercfg']['babyname'], cfg['usercfg']['appid'], cfg['usercfg']['secret']

    @staticmethod
    def notify():
        babyname, appid, secret = Notify.readcfg()
        app = App(appid=appid, secret=secret)
        app.notify(event_name='BabyCam', trackers={'Baby': babyname})
        time.sleep(600)

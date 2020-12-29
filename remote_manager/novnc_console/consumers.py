from channels.generic.websocket import WebsocketConsumer
import threading
import time
import numpy as np
import cv2
from vncdotool import api
from pathlib import Path
from .models import VNCSession
from datetime import datetime
import subprocess


class VNCRecorder:
    def __init__(self, output, host, fps, password):
        self.client = api.connect(host, password=password)
        self.client.refreshScreen(False)
        videodims = self.client.screen.size
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.frame = fps
        self.output = output
        self.video = cv2.VideoWriter(self.output, fourcc, fps, videodims)
        self.signal = True

    def record(self):
        while self.signal:
            start = time.time()
            for i in range(0, self.frame):
                self.client.refreshScreen(False)
                imtemp = self.client.screen.copy()
                self.video.write(cv2.cvtColor(np.array(imtemp), cv2.COLOR_RGB2BGR))
            stop = time.time()
            elapse = stop - start
            if elapse < 1:
                time.sleep(1 - elapse)
        else:
            self.video.release()
            self.client.disconnect()
            try:
                target_path = self.output.replace('media/temp/', 'media/record/', 1)
                Path('/'.join(target_path.split('/')[:-1])).mkdir(parents=True, exist_ok=True)
                subprocess.run(['ffmpeg', '-i', self.output, target_path])
            except:
                pass
            finally:
                pass

    def stop(self):
        self.signal = False


class ThreadRecording:
    def __init__(self, vnc, user):
        self.vnc = vnc
        self.user = user
        self.thread = threading.Thread(target=self.recording)
        self.thread.start()

    def end(self):
        self.recorder.stop()

    def recording(self):
        dir = 'media/temp/%s/%s/' % (self.vnc.id, self.user.username)
        Path(dir).mkdir(parents=True, exist_ok=True)
        dt = datetime.now()
        filename = dir + dt.strftime('%Y%m%d%H%M%S') + '.mp4'
        vnc_server = '%s:%s' % (self.vnc.ip4_addr, self.vnc.vnc_display)
        self.recorder = VNCRecorder(filename, vnc_server, 10, self.vnc.password)
        self.recorder.record()


class RecordConsumer(WebsocketConsumer):
    def connect(self):
        vnc = VNCSession.objects.get(id=self.scope['url_route']['kwargs']['name'])
        self.accept()
        self.test = ThreadRecording(vnc, self.scope['user'])

    def disconnect(self, close_code):
        self.test.end()

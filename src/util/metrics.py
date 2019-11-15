from .constants import REQUEST_NUM, LATENCY, DATA_TRANSFER
from .repeatedTimer import RepeatedTimer
from datetime import datetime
from time import sleep
import threading

class Metrics:
    def __init__(self,pid):
        self._metrics = {}
        self.initMetric()
        self._file = f"metrics/{pid}.metr"
        self._rt = threading.Thread(target=self.emit_fixed_rate)
        self._rt.setDaemon(True)
        self._rt.start()

    def initMetric(self):
        self._metrics[REQUEST_NUM] = 0
        self._metrics[LATENCY] = 0
        self._metrics[DATA_TRANSFER] = 0
    
    def addOne(self, metricName):
        self._metrics[metricName] += 1

    def addValue(self, metricName, value):
        self._metrics[metricName] += value
    
    def emit_fixed_rate(self):
        while True:
            self.emit()
            try:
                sleep(1)
            except:
                pass


    def emit(self):
        try:
            with open(self._file,'a') as fr:
                now = datetime.now()
                fr.write ("\nTime: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
                for k,v in self._metrics.items():
                    fr.write(k + ": \t" + str(v) + "\n")
                self.initMetric()
        except IOError as e:
            print(e)
            

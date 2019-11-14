# with open("testread",'r',encoding="utf-8") as target:
#     print(target.read())
# import schedule
# import time 

# def test():
#     print('Hello, World!')

# def sched_job():
#     schedule.every(1).seconds.do(test)
#     return schedule.CancelJob

# sched_job()

# while True:
#     schedule.run_pending()
#     time.sleep(1)

from threading import Timer
from time import sleep

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def hello(name):
    print("Hello %s!" % name)

def test():
    timer = RepeatedTimer(1, hello, "world")
    try:
        sleep(5) # your long-running job goes here...
    finally:
        # timer.stop() #÷
        pass
test()
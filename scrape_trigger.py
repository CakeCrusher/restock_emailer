import os
import datetime as dt
from threading import Timer
import time
        
# time to start
START_TIME = dt.datetime(2021, 5, 22, 19, 11)
# how often it iterates
ITERATE_SECONDS = 60
# determines the potential inaccuracy (in seconds) of when the cycle begins
# (0.0 < inaccuracy < START_TIME_PRECISION)
START_TIME_PRECISION = 0.1

# makes datetime more readable
def readable(_dt):
    return _dt.strftime("%d/%m/%Y %H:%M:%S")


# task to be performed on every trigger
def task():
    os.system('scrapy crawl stock_status -o availability.jsonlines')

old_trigger = None
next_trigger = None

# begins the cycle
def task_runner():
    global old_trigger
    global next_trigger

    timedelta = dt.timedelta(seconds=ITERATE_SECONDS)
    next_trigger = old_trigger + timedelta

    print(f'Triggered at: {readable(dt.datetime.now())}')
    print(f'Next trigger at: {readable(dt.datetime.now() + timedelta)}')

    delta_seconds = (next_trigger - old_trigger).total_seconds()
    Timer(delta_seconds, task_runner, ()).start()

    task()


# checks every START_TIME_PRECISION to start the timer on the earliest START_TIME
while True:
    now = dt.datetime.now()
    if now.minute == START_TIME.minute:
        old_trigger = dt.datetime.now()
        print(f'Began at: {dt.datetime.now()}')
        task_runner()
        break
    else:
        print('waiting...')
        time.sleep(START_TIME_PRECISION)
""" Timer Class """

import time

class Error(Exception):
    """ Base class for Timer Exceptions """
    pass

class TimerStartError(Error):
    def __init__(self, message):
        self.message = message

class TimerEndError(Error):
    def __init__(self, message):
        self.message = message

class Timer:
    def __init__(self, text="The task took a time of: {:0.6f} seconds"):
        """ Init the variables """
        self.start_time = None
        self.text = text
    
    def start(self):
        """ Start a new timer """
        try:
            if self.start_time is not None:
                raise TimerStartError("Timer is running. Use .stop() to stop it")

            self.start_time = time.perf_counter()

        except TimerStartError as tse:
            print()
            print(tse.message)
            exit(0)

    def stop(self):
        """ Stop the timer, and report the elapsed time """
        try:
            if self.start_time is None:
                raise TimerEndError("Timer is not running. Use .start() to start it")

            elapsed_time = time.perf_counter() - self.start_time
            self.start_time = None
        
            print(self.text.format(elapsed_time))

        except TimerEndError as tee:
            print()
            print(tee.message)
            exit(0)

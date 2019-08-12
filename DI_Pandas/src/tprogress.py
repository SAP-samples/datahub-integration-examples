
import time
import logging

# logs time progress of program

######## Utility
class progress :
    def __init__(self,max_num=1,step_size=1,freq=1) :
        self.inc = -1
        self.freq = freq
        self.step_size = step_size
        self.max = max_num
        self.time_start = time.time()
        self.time_last = self.time_start
        self.time_end_projected = time.time()
        self.strtime_end_projected = time.strftime("%H:%M:%S", time.localtime(self.time_end_projected))

        self.plogger = logging.getLogger('tprogress')
        self.plogger.setLevel(logging.INFO)

        self.plogger.debug("Start time: " + time.strftime('{%Y-%m-%d %H:%M:%S}'))

    # called within a loop to state past time and projected end time
    def monitor(self):
        self.inc += 1
        if self.inc % self.freq == 0:
            time_taken = time.time() - self.time_start
            if self.inc != 0 :
                self.time_end_projected = time_taken / (self.inc*self.step_size) * self.max + self.time_start
                self.strtime_end_projected = time.strftime("%H:%M:%S", time.localtime(self.time_end_projected))
            time_hour, time_min, time_sec = self.timestamp(time_taken)
            prog = int(round((self.inc*self.step_size*100)/self.max))
            time_str = "{0:3d}% : {1:3.0f} s ({2:3.0f}:{3:2.0f}:{4:3.1f}) End:{5}".format(prog,time_taken,time_hour, time_min, time_sec,self.strtime_end_projected)
            self.plogger.info("Monitor: " + time_str)

    # called to get time since last called
    def elapsed_time (self,info_str="",print_info=False) :
        info_str = "Elapsed Time :" if not info_str else info_str
        time_taken = time.time() - self.time_start
        time_taken_last = time.time() - self.time_last
        time_hour, time_min, time_sec = self.timestamp(time_taken)
        tstr = "Time past since last stop {:.3f}s (total time: {:3.0f}:{:2.0f}:{:3.1f})".format((time_taken - time_taken_last), time_hour, time_min, time_sec)
        if print_info :
            self.plogger.info(info_str + tstr)
        self.time_last = time.time()
        return tstr

    def timestamp(self,time_taken):
        time_hour, rest = divmod(time_taken, 3600)
        time_min, time_sec = divmod(rest, 60)
        return time_hour, time_min, time_sec

    def get_start_time(self):
        return time.strftime("%H:%M:%S", time.localtime(self.time_start))
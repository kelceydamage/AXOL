<<<<<<< HEAD


import logging, random, operator, datetime, sys
from threading import Thread, Event, Lock

class Task(object):
    def __init__(self, name, start_time, calc_next_time, time_interval, func):
        """
        Initialize a Task.

        Arguments:
        name            - Name of task.
        start_time      - First time for task to run
        calc_next_time  - Function to calculate the time of next run,
                          gets one argument, the last run time as a datetime.
                          Returns None when task should no longer be run
        func            - A function to run
        """
        self.time_interval = time_interval
        self.name = name
        self.start_time = start_time
        print '%%%%%%%%%%%%%%%%%%%%%%%%%'
        print 'START TIME:',start_time
        self.scheduled_time = start_time
        print 'SCHED TIME',self.scheduled_time
        self.calc_next_time = calc_next_time
        self.func = func
        self.halt_flag = Event()

    def run(self):
        logging.debug("Running %s task, scheduled at: %s" % (self.name, self.scheduled_time,))

        print 'FUNC ##########################'
        print self.func
        print 'FUNC ##########################'

        if not self.halt_flag.isSet():
            try:
                try:

                    print 'KKKKKKKKKKKKKKKKKKKKKKKK'
                    print self.func
                    print self.func()
                    self.func()
                except:
                    raise
            finally:
                print self.scheduled_time
                print self.time_interval
                self.scheduled_time = self.calc_next_time(int(self.time_interval))
                print self.scheduled_time
                logging.debug("Scheduled next run of %s for: %s" % (self.name, self.scheduled_time,))

    def halt(self):
        self.halt_flag.set()

class Scheduler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)

        self.tasks = {}
        self.tasks_lock = Lock()
        self.halt_flag = Event()
        self.nonempty = Event()

    def schedule(self, name, start_time, calc_next_time, time_interval, func):
        task = Task(name, start_time, calc_next_time, time_interval, func)
        receipt = self.schedule_task(task)
        return receipt

    def schedule_task(self, task):
        receipt = random.random()

        self.tasks_lock.acquire()
        self.tasks[receipt] = task
        self.nonempty.set()
        self.tasks_lock.release()

        return receipt

    def list(self):
        return self.tasks

    def drop(self, task_receipt):
        self.tasks_lock.acquire()
        try:
            self.tasks[task_receipt].halt()
            del self.tasks[task_receipt]
            if len(self.tasks)==0:
                self.nonempty.clear()
        except KeyError:
            print 'INVALID TASK RECEIPT'
            logging.error('Invalid task receipt: %s' % (task_receipt,))
        self.tasks_lock.release()

    def halt(self):


        # Drop all active tasks
        #map(self.drop, self.tasks.keys())
        for key in self.tasks.keys():
            self.drop([key])
        print self.tasks.keys()
        self.halt_flag.set()
        # Exit the thread to kill the scheduler
        #sys.exit()

    def __find_next_task(self):
        self.tasks_lock.acquire()
        items = self.tasks.items()
        by_time = lambda x: operator.getitem(x, 1).scheduled_time
        items.sort(key=by_time)
        try:
            receipt = items[0][0]
        except Exception, e:
            receipt = None
        self.tasks_lock.release()
        return receipt

    def run(self):
        while 1:
            receipt = self.__find_next_task()
            if receipt != None:
                task_time = self.tasks[receipt].scheduled_time
                print '$$$$$$$$$$$$$$$$$$$$$'
                print self.tasks[receipt].name
                print 'Task Time:',task_time
                print 'Date Time:',datetime.datetime.now()
                if task_time < datetime.datetime.now():
                    print '11111111111111111'
                    time_to_wait = datetime.timedelta(seconds=int(self.tasks[receipt].time_interval))
                else:
                    print '22222222222222222'
                    time_to_wait = task_time - datetime.datetime.now()
                #time_to_wait = datetime.datetime.now() - task_time
                print 'TTW:',time_to_wait
                secs_to_wait = 0.
                # Check if time to wait is in the future
                print 'DELTA:',datetime.timedelta()
                print 'STW:',time_to_wait.seconds
                if time_to_wait > datetime.timedelta():
                    secs_to_wait = time_to_wait.seconds
                print "Next task is %s in %s seconds" % (self.tasks[receipt].name, time_to_wait,)
                logging.debug("Next task is %s in %s seconds" % (self.tasks[receipt].name, time_to_wait,))
                self.halt_flag.wait(secs_to_wait)
                try:
                    try:
                        self.tasks_lock.acquire()
                        task = self.tasks[receipt]
                        logging.debug("Running %s..." % (task.name,))
                        print '########## RUN ####################'
                        task.run()
                    finally:
                        self.tasks_lock.release()
                except Exception, e:
                    logging.exception(e)
                    logging.debug( self.tasks )
            else:
                self.nonempty.wait()

def every_x_secs(x):
    """
    Returns a function that will generate a datetime object that is x seconds
    in the future from a given argument.
    """
    return lambda last: last + datetime.timedelta(seconds=x)

def every_x_mins(x):
    """
    Returns a function that will generate a datetime object that is x minutes
    in the future from a given argument.
    """
    return lambda last: last + datetime.timedelta(minutes=x)

def daily_at(time):
    """
    Returns a function that will generate a datetime object that is one day
    in the future from a datetime argument combined with 'time'.
    """
    return lambda last: datetime.datetime.combine(last + datetime.timedelta(days=1), time)

class RunUntilSuccess(object):
    """
    Provide control flow for a procedure.
    Run procedure until it throws no exceptions or exhausts
    its number of attempts.
    """
    def __init__(self, func, num_tries=10):
        self.func = func
        self.num_tries = num_tries

    def __call__(self):
        try_count = 0
        is_success = False
        while not is_success and try_count < self.num_tries:
            try_count += 1
            try:
                self.func()
                is_success = True
            except Exception, e:  # Some exception occurred, try again
                logging.exception(e)
                logging.error("Task failed on try #%s" % (try_count,))
                continue

        if is_success:
            logging.info("Task %s was run successfully." % (self.func.__name__,))
        else:
            logging.error("Success was not achieved!")

class RunOnce(object):
    """
    Provide control flow for a procedure.
    Run procedure until it is stopped
    """
    def __init__(self, func, args=None):
        self.func = func
        self.args = args

    def __call__(self):
        try:
            if self.args is None:
                self.func()
            else:
                self.func(self.args)
        except Exception, e:  # Some exception occurred, try again
            logging.exception(e)
            logging.error("Task failed: %s" % (e))


=======


import logging, random, operator, datetime, sys
from threading import Thread, Event, Lock

class Task(object):
    def __init__(self, name, start_time, calc_next_time, time_interval, func):
        """
        Initialize a Task.

        Arguments:
        name            - Name of task.
        start_time      - First time for task to run
        calc_next_time  - Function to calculate the time of next run,
                          gets one argument, the last run time as a datetime.
                          Returns None when task should no longer be run
        func            - A function to run
        """
        self.time_interval = time_interval
        self.name = name
        self.start_time = start_time
        print '%%%%%%%%%%%%%%%%%%%%%%%%%'
        print 'START TIME:',start_time
        self.scheduled_time = start_time
        print 'SCHED TIME',self.scheduled_time
        self.calc_next_time = calc_next_time
        self.func = func
        self.halt_flag = Event()

    def run(self):
        logging.debug("Running %s task, scheduled at: %s" % (self.name, self.scheduled_time,))

        print 'FUNC ##########################'
        print self.func
        print 'FUNC ##########################'

        if not self.halt_flag.isSet():
            try:
                try:

                    print 'KKKKKKKKKKKKKKKKKKKKKKKK'
                    print self.func
                    print self.func()
                    self.func()
                except:
                    raise
            finally:
                print self.scheduled_time
                print self.time_interval
                self.scheduled_time = self.calc_next_time(int(self.time_interval))
                print self.scheduled_time
                logging.debug("Scheduled next run of %s for: %s" % (self.name, self.scheduled_time,))

    def halt(self):
        self.halt_flag.set()

class Scheduler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)

        self.tasks = {}
        self.tasks_lock = Lock()
        self.halt_flag = Event()
        self.nonempty = Event()

    def schedule(self, name, start_time, calc_next_time, time_interval, func):
        task = Task(name, start_time, calc_next_time, time_interval, func)
        receipt = self.schedule_task(task)
        return receipt

    def schedule_task(self, task):
        receipt = random.random()

        self.tasks_lock.acquire()
        self.tasks[receipt] = task
        self.nonempty.set()
        self.tasks_lock.release()

        return receipt

    def list(self):
        return self.tasks

    def drop(self, task_receipt):
        self.tasks_lock.acquire()
        try:
            self.tasks[task_receipt].halt()
            del self.tasks[task_receipt]
            if len(self.tasks)==0:
                self.nonempty.clear()
        except KeyError:
            print 'INVALID TASK RECEIPT'
            logging.error('Invalid task receipt: %s' % (task_receipt,))
        self.tasks_lock.release()

    def halt(self):


        # Drop all active tasks
        #map(self.drop, self.tasks.keys())
        for key in self.tasks.keys():
            self.drop([key])
        print self.tasks.keys()
        self.halt_flag.set()
        # Exit the thread to kill the scheduler
        #sys.exit()

    def __find_next_task(self):
        self.tasks_lock.acquire()
        items = self.tasks.items()
        by_time = lambda x: operator.getitem(x, 1).scheduled_time
        items.sort(key=by_time)
        try:
            receipt = items[0][0]
        except Exception, e:
            receipt = None
        self.tasks_lock.release()
        return receipt

    def run(self):
        while 1:
            receipt = self.__find_next_task()
            if receipt != None:
                task_time = self.tasks[receipt].scheduled_time
                print '$$$$$$$$$$$$$$$$$$$$$'
                print self.tasks[receipt].name
                print 'Task Time:',task_time
                print 'Date Time:',datetime.datetime.now()
                if task_time < datetime.datetime.now():
                    print '11111111111111111'
                    time_to_wait = datetime.timedelta(seconds=int(self.tasks[receipt].time_interval))
                else:
                    print '22222222222222222'
                    time_to_wait = task_time - datetime.datetime.now()
                #time_to_wait = datetime.datetime.now() - task_time
                print 'TTW:',time_to_wait
                secs_to_wait = 0.
                # Check if time to wait is in the future
                print 'DELTA:',datetime.timedelta()
                print 'STW:',time_to_wait.seconds
                if time_to_wait > datetime.timedelta():
                    secs_to_wait = time_to_wait.seconds
                print "Next task is %s in %s seconds" % (self.tasks[receipt].name, time_to_wait,)
                logging.debug("Next task is %s in %s seconds" % (self.tasks[receipt].name, time_to_wait,))
                self.halt_flag.wait(secs_to_wait)
                try:
                    try:
                        self.tasks_lock.acquire()
                        task = self.tasks[receipt]
                        logging.debug("Running %s..." % (task.name,))
                        print '########## RUN ####################'
                        task.run()
                    finally:
                        self.tasks_lock.release()
                except Exception, e:
                    logging.exception(e)
                    logging.debug( self.tasks )
            else:
                self.nonempty.wait()

def every_x_secs(x):
    """
    Returns a function that will generate a datetime object that is x seconds
    in the future from a given argument.
    """
    return lambda last: last + datetime.timedelta(seconds=x)

def every_x_mins(x):
    """
    Returns a function that will generate a datetime object that is x minutes
    in the future from a given argument.
    """
    return lambda last: last + datetime.timedelta(minutes=x)

def daily_at(time):
    """
    Returns a function that will generate a datetime object that is one day
    in the future from a datetime argument combined with 'time'.
    """
    return lambda last: datetime.datetime.combine(last + datetime.timedelta(days=1), time)

class RunUntilSuccess(object):
    """
    Provide control flow for a procedure.
    Run procedure until it throws no exceptions or exhausts
    its number of attempts.
    """
    def __init__(self, func, num_tries=10):
        self.func = func
        self.num_tries = num_tries

    def __call__(self):
        try_count = 0
        is_success = False
        while not is_success and try_count < self.num_tries:
            try_count += 1
            try:
                self.func()
                is_success = True
            except Exception, e:  # Some exception occurred, try again
                logging.exception(e)
                logging.error("Task failed on try #%s" % (try_count,))
                continue

        if is_success:
            logging.info("Task %s was run successfully." % (self.func.__name__,))
        else:
            logging.error("Success was not achieved!")

class RunOnce(object):
    """
    Provide control flow for a procedure.
    Run procedure until it is stopped
    """
    def __init__(self, func, args=None):
        self.func = func
        self.args = args

    def __call__(self):
        try:
            if self.args is None:
                self.func()
            else:
                self.func(self.args)
        except Exception, e:  # Some exception occurred, try again
            logging.exception(e)
            logging.error("Task failed: %s" % (e))


>>>>>>> 0dce5d2808d53f11fb56e83c23403662414b1209

from abc import ABC, abstractmethod
from functools import total_ordering
import threading
import subprocess
import gc

@total_ordering
class Event(ABC):
    
    classmap = {}
    objcount = 0

    @classmethod
    def registerSubclass(cls,key,func):
        cls.classmap[key] = func

    @classmethod
    def makeEvent(cls,mrs,list):
        try:
            action, type, *args = list
        except:
            print(f"'{list}' too short to be an action")
            return None
        if action != 'action':
            print(f"'{action}' is not 'action', in '{list}'")
            return None
        if type not in cls.classmap:
            print(f"'{type} is not a registered action type, in '{list}'")
            return None
        #print("EVMEV",type,args)
        return cls.classmap[type](mrs,type,*args)

    def __init__(self,mrs,name):
        self.mrs = mrs
        self.name = name
        self.sched = None
        Event.objcount += 1
        self.objnum = Event.objcount

    def __lt__(self, other):
        return self.objnum < other.objnum

    def __str__(self):
        return str(self.__class__.__module__) + "." + str(self.__class__.__name__) + "" + str(self.__dict__)

    def __repr__(self):
        return "EVT:"+"DONG"

    @abstractmethod
    def run(self,eq,now,dead):
        pass

    
# class DimScreenEvent(Event):
#     def __init__(self,mrs,name):
#         super().__init__(mrs,name)
#         self.brightness = -1    # Current brightness unset
#         self.delay = 60*60      # default seconds til dim
        
#     def reschedule(self):
#         self.mrs.scheduleEvent(self.delay,self) # one hour on
        
#     def wake(self):
#         self.reschedule();
#         self.setBrightnessPercent(30)

#     def run(self,eq,now,dead):
#         self.setBrightnessPercent(0)
#         delta = now - dead
#         print(f'{dead} executed at {now} delay {delta}')
#         start = eq.now()
#         n = gc.collect()
#         end = eq.now()
#         gctime = end - start
#         print(f'{n} objects collected in {gctime}')

#     def setBrightnessPercent(self,pct):
#         if self.brightness != pct: 
#             print(f'brightness to {pct}')
#             self.brightness = pct
#             decks = self.mrs.decks 
#             decks.setAllDecksBrightness(pct)


class ClockEvent(Event):

    def run(self,eq,now,dead):
        delta = now - dead
        print(f'{dead} executed at {now} delay {delta}')
        then = int(now/10)*10+10
        eq.runAt(then,self)

class ThreadEvent(Event):

    @abstractmethod
    def threadRun(self,eq,now,dead):
        pass

    def run(self,eq,now,dead):
        worker = self.threadRun
        def catch(eq,now,dead):
            try:
                #print("LKASLKDAOAART",self,now)
                worker(eq,now,dead)
                #print("FDDDAAANLKASLKDAOAART",self,now,dead)
            except Exception as e:
                print("ZTNDKGOGN",self,e)
        thread = threading.Thread(target=catch,args=(eq,now,dead))
        thread.start()

class SleepEvent(ThreadEvent):
    def threadRun(self,eq,now,dead):
        print("SLEEPEV "+str(now))
        eq.sleep(4)
        print("SLEEPEZ "+str(eq.now()))
        eq.runIn(3,self)
        
class ShellEvent(ThreadEvent):

    Event.registerSubclass('shell',lambda mrs,type,*args: ShellEvent(mrs,type,*args))

    def __init__(self,mrs,name,*args):
        super().__init__(mrs,name)
        #print(args)
        self.args = args
        
    def threadRun(self,eq,now,dead):
        cmd = self.args[0]
        cmda = cmd.split()
        prog = cmda[0]
        rprog = self.mrs.resolveProgram(prog)
        if rprog is None:
            print(f"WARNING: NO EXECUTABLE '{prog}' FOUND; '{cmd}' IGNORED")
            return
        if rprog != prog:
            cmda[0] = rprog
            cmd = " ".join(cmda)

        print("SHELL",cmd)
        comp=subprocess.run(cmd,shell=True, capture_output=True)
        if comp.returncode != 0:
            print("WARNING:",comp.args,"exited",comp.returncode)
            print("STDOUT:",comp.stdout)
            print("STDERR:",comp.stderr)


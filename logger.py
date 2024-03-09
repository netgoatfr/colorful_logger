
import datetime
import traceback
from colorama import Fore, Style, init as __init
import sys
__init()

class BaseStream:
    def __init__(self,file=sys.stdout):
        self.file = file
class ErrStream(BaseStream):
    def __init__(self):
        super().__init__(sys.stderr)


DEFAULT_FORMAT = "[{h} {m} {s}] [{root}] [{level}]: {content}"

class Logger:
    def __init__(self, name:str = "Logger",level:str = "debug",/,*, stream=BaseStream, format = DEFAULT_FORMAT, colored=True):
        self.root = name
        self._format = format
        self._colored = colored
        self._stream = stream
        self.set_level(level)
        
    def set_level(self,lvl):
        self._level = lvl.lower()[0]
        mapping = dict(d=0,i=1,w=2,e=3,f=4)
        self._enabled = ["debug","info","warn","error","fatal"][mapping:]
    @property
    def _time(self):
        return datetime.datetime.now()
    
    def info(self,txt):
        time = self._time
        if self._colored:print(Fore.LIGHTGREEN_EX+Style.BRIGHT+self._format.format(h=time.hour,m=time.minute,s=time.second,root=self.root,level="INFO",content=txt)+Style.RESET_ALL,file=self._stream.file)
        else:print(self._format.format(h=time.hour,m=time.minute,s=time.second,root=self.root,level="INFO",content=txt),file=self._stream.file)

    def debug(self,txt):
        if "debug" not in self._enabled:return
        time = self._time
        if self._colored:print(Fore.LIGHTBLUE_EX+Style.BRIGHT+self._format.format(h=time.hour,m=time.minute,s=time.second,root=self.root,level="DEBUG",content=txt)+Style.RESET_ALL,file=self._stream.file)
        else:print(self._format.format(h=time.hour,m=time.minute,s=time.second,root=self.root,level="DEBUG",content=txt),file=self._stream.file)

    def warn(self,txt):
        if "warn" not in self._enabled:return
        time = self._time
        if self._colored:print(Fore.YELLOW+Style.BRIGHT+self._format.format(h=time.hour,m=time.minute,s=time.second,root=self.root,level="WARN",content=txt)+Style.RESET_ALL,file=self._stream.file)
        else:print(self._format.format(h=time.hour,m=time.minute,s=time.second,root=self.root,level="WARN",content=txt),file=self._stream.file)


    def error(self,txt):
        if "error" not in self._enabled:return
        time = self._time
        if self._colored:print(Fore.LIGHTRED_EX+Style.BRIGHT+self._format.format(h=time.hour,m=time.minute,s=time.second,root=self.root,level="ERROR",content=txt)+Style.RESET_ALL,file=self._stream.file)
        else:print(self._format.format(h=time.hour,m=time.minute,s=time.second,root=self.root,level="ERROR",content=txt),file=self._stream.file)

    def fatal(self,txt):
        if "fatal" not in self._enabled:return
        time = self._time
        if self._colored:print(Fore.RED+Style.BRIGHT+self._format.format(h=time.hour,m=time.minute,s=time.second,root=self.root,level="FATAL",content=txt)+Style.RESET_ALL,file=self._stream.file)
        else:print(self._format.format(h=time.hour,m=time.minute,s=time.second,root=self.root,level="FATAL",content=txt),file=self._stream.file)
    critical = fatal # To enable compat from other logging modules
        
    def report_exception(self,e:BaseException):
        self.lock.acquire()
        self._before_log(str(e))
        lines = traceback.format_exception(e)
        for line in lines:
            if self.colored_output:print(Fore.RED+Style.BRIGHT+"["+self._time+"]"+" ["+self.root+"] [EXCEPTION]: "+line+Style.RESET_ALL,file=self.file)
            else:print("["+self._time+"]"+" ["+self.root+"] [EXCEPTION]: "+line,file=self.file)
        self._after_log(str(e)) 
        self.lock.release()

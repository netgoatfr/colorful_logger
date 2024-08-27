import datetime
import types
import typing
import traceback
from colorama import Fore, Style, init as __init
import sys
__init()

DEFAULT_FORMAT = "[{h}:{m}:{s}] [{root}] [{level}]: {content}"

class Logger:
    def __init__(self, name:str = "Logger",level:str = "debug",/,*, stream:typing.TextIO = sys.stdout, format:str = DEFAULT_FORMAT, colored:bool=True,_prefix:str=""):
        '''
        # Create a Logger element:

        @name: the name that will be printed out. Is shown as the root in the output.

        @level: the logging level, should be "debug", "info", "warn", "error" or "fatal"
        > A level indicate the logger to ignore every call higher than a specifc level
        > For example, a logger with a level of "error" won't print debug, log, and warn calls.
        > Can be modified using logger.set_level(<level>)
        
        ## Positionals Arguments:
        @stream: the stream used to print the data. can be an opened file, or an object.
        
        @format: the logging format, which is by default to "[{h}:{m}:{s}] [{root}] [{level}]: {content}"
        - Availables format attributes (case-sensitive): [h]our, [m]inutes, [s]econds, m[i]liseconds, [d]ays, [M]onths, [y]ears, root, level, content
        
        @colored: enable or not colorful output.

        the @_prefix args should not be touched.
        '''
        self._root = name
        self._childs:list[Logger] = [] # This might be a bad idea. As it might use a lot of memory, but it's needed if a parent want to rename itself
        self._format = format
        self._colored = colored
        self._stream = stream
        self.set_level(level)
        self._prefix = _prefix
        
    @property
    def root(self):return self._prefix + self._root
    @root.setter
    def root(self,name):self._root = self._prefix + self._root

    def get_child(self,name:str):
        d = Logger(name,self._level,stream=self._stream,format=self._format,colored=self._colored,_prefix=self.root + "/")
        self._childs.append(d)
        return d
    def get_instance(self,name:str):
        d = Logger(name,self._level,stream=self._stream,format=self._format,colored=self._colored,_prefix=self.root + "#")
        self._childs.append(d)
        return d
    def get_sub(self,name:str):
        d = Logger(name,self._level,stream=self._stream,format=self._format,colored=self._colored,_prefix=self.root + ".")
        self._childs.append(d)
        return d

    def set_level(self,lvl:str):
        """
        Change the level of the logger
        """
        self._level = lvl.lower()[0] # Get the first letter of the level
        mapping = dict(d=0,i=1,w=2,e=3,f=4)
        self._enabled = ["debug","info","warn","error","fatal"][mapping[self._level]:]# Get which level will print out.
        for i in self._childs:
            i.set_level(lvl)
    @property
    def _time(self):
        return datetime.datetime.now()

    def hamburger(self,*a):
        hamburger = [('\n', 1), (' ', 36), ('▓', 32), (' ', 36), ('\n', 1), (' ', 32), ('▓', 4), ('▒', 32), ('▓', 4), (' ', 32), ('\n', 1), (' ', 28), ('▓', 4), ('▒', 40), ('▓', 4), (' ', 28), ('\n', 1), (' ', 24), ('▓', 4), ('▒', 48), ('▓', 4), (' ', 24), ('\n', 1), (' ', 20), ('▓', 4), ('▒', 14), (' ', 2), ('▒', 12), (' ', 2), ('▒', 26), ('▓', 4), (' ', 20), ('\n', 1), (' ', 18), ('▓', 2), ('▒', 50), (' ', 2), ('▒', 12), ('▓', 2), (' ', 18), ('\n', 1), (' ', 16), ('▓', 2), ('▒', 68), ('▓', 2), (' ', 16), ('\n', 1), (' ', 14), ('▓', 2), ('▒', 14), (' ', 2), ('▒', 14), (' ', 2), ('▒', 40), ('▓', 2), (' ', 14), ('\n', 1), (' ', 14), ('▓', 2), ('▒', 4), ('▓', 2), ('▒', 66), ('▓', 2), (' ', 14), ('\n', 1), (' ', 12), ('▓', 2), ('▒', 42), (' ', 2), ('▒', 32), ('▓', 2), (' ', 12), ('\n', 1), (' ', 12), ('▓', 2), ('▒', 56), (' ', 2), ('▒', 18), ('▓', 2), (' ', 12), ('\n', 1), (' ', 10), ('▓', 2), ('▒', 2), ('▓', 2), ('▒', 20), (' ', 2), ('▒', 54), ('▓', 2), (' ', 10), ('\n', 1), (' ', 8), ('▓', 4), ('▒', 8), (' ', 2), ('▒', 72), ('▓', 2), (' ', 8), ('\n', 1), (' ', 8), ('▓', 4), ('▒', 2), ('▓', 2), ('▒', 4), ('▓', 2), ('▒', 2), ('▓', 2), ('▒', 28), (' ', 2), ('▒', 38), ('▓', 2), (' ', 8), ('\n', 1), (' ', 8), ('▓', 2), ('▒', 6), ('▓', 2), ('▒', 76), ('▓', 2), (' ', 8), ('\n', 1), (' ', 8), ('▓', 88), (' ', 8), ('\n', 1), (' ', 6), ('▓', 2), ('▒', 16), ('▓', 2), ('▒', 28), ('▓', 2), ('▒', 40), ('▓', 6), (' ', 2), ('\n', 1), (' ', 2), ('▓', 4), ('▒', 4), ('▓', 2), ('▒', 18), ('▓', 2), ('▒', 6), ('▓', 2), ('▒', 22), ('▓', 2), ('▒', 10), ('▓', 2), ('▒', 4), ('▓', 2), ('▒', 4), ('▓', 10), ('▒', 6), ('▓', 2), ('\n', 1), (' ', 2), ('▓', 2), ('▒', 6), ('▓', 22), ('▒', 12), ('▓', 24), ('▒', 4), ('▓', 2), ('▒', 8), ('▓', 4), ('▒', 8), ('▓', 4), ('▒', 4), ('▓', 2), ('\n', 1), (' ', 2), ('▓', 8), ('▒', 22), ('▓', 12), ('▒', 24), ('▓', 2), ('▒', 8), ('▓', 4), ('▒', 14), ('▓', 6), (' ', 2), ('\n', 1), (' ', 2), ('░', 6), ('▒', 88), ('░', 6), (' ', 2), ('\n', 1), (' ', 8), ('▓', 62), ('█', 8), ('▓', 18), (' ', 8), ('\n', 1), (' ', 6), ('▓', 92), (' ', 6), ('\n', 1), (' ', 6), ('▓', 2), ('▒', 88), ('▓', 2), (' ', 6), ('\n', 1), (' ', 6), ('░', 2), ('▓', 88), ('░', 2), (' ', 6), ('\n', 1), (' ', 6), ('▒', 6), ('░', 78), ('▒', 4), ('█', 2), (' ', 8), ('\n', 1), (' ', 4), ('█', 10), ('░', 76), ('█', 8), (' ', 6), ('\n', 1), (' ', 4), ('█', 4), ('▓', 12), ('░', 64), ('▓', 10), ('█', 4), (' ', 6), ('\n', 1), (' ', 4), ('█', 4), ('▓', 2), ('█', 2), ('▓', 10), ('█', 2), ('▓', 2), ('░', 54), ('▓', 2), ('█', 2), ('▓', 8), ('█', 6), (' ', 6), ('\n', 1), (' ', 4), ('█', 4), ('▓', 2), ('█', 2), ('▓', 2), ('█', 2), ('▓', 18), ('░', 38), ('▓', 22), ('█', 4), (' ', 6), ('\n', 1), (' ', 4), ('█', 4), ('▓', 4), ('█', 2), ('▓', 4), ('█', 2), ('▓', 20), ('░', 26), ('▓', 22), ('█', 2), ('▓', 4), ('█', 4), (' ', 6), ('\n', 1), (' ', 4), ('█', 4), ('▓', 14), ('█', 2), ('▓', 24), ('░', 10), ('▓', 22), ('█', 2), ('▓', 8), ('█', 2), ('▓', 2), ('█', 4), (' ', 6), ('\n', 1), (' ', 4), ('█', 4), ('▓', 6), ('█', 2), ('▓', 10), ('█', 2), ('▓', 58), ('█', 2), ('▓', 6), ('█', 4), (' ', 6), ('\n', 1), (' ', 4), ('░', 2), ('█', 90), ('░', 2), (' ', 6), ('\n', 1), (' ', 6), ('░', 2), ('▓', 4), ('▒', 80), ('▓', 4), (' ', 8), ('\n', 1), (' ', 8), ('▓', 2), ('▒', 2), ('▓', 2), ('▒', 2), ('▓', 2), ('▒', 2), ('▓', 2), ('▒', 58), ('▓', 2), ('▒', 4), ('▓', 2), ('▒', 6), ('▓', 2), (' ', 8), ('\n', 1), (' ', 8), ('▓', 2), ('▒', 66), ('▓', 2), ('▒', 12), ('▓', 2), ('▒', 2), ('▓', 2), (' ', 8), ('\n', 1), (' ', 8), ('▓', 2), ('▒', 4), ('▓', 2), ('▒', 2), ('▓', 2), ('▒', 62), ('▓', 2), ('▒', 8), ('▓', 4), (' ', 8), ('\n', 1), (' ', 8), ('▓', 4), ('▒', 10), ('▓', 2), ('▒', 52), ('▓', 2), ('▒', 10), ('▓', 2), ('▒', 2), ('▓', 4), (' ', 8), ('\n', 1), (' ', 10), ('▓', 84), (' ', 10), ('\n', 1)]
        hamburger = "".join(x*y for x,y in hamburger)
        if self._colored:print(Fore.LIGHTMAGENTA_EX+Style.BRIGHT+self._formated("HAMBURGER","HAMBURGER !!!")+Style.RESET_ALL,file=self._stream)
        else:print(self._formated("HAMBURGER","HAMBURGER !!!"),file=self._stream)
        if self._colored:print(Fore.LIGHTMAGENTA_EX+Style.BRIGHT+self._formated("HAMBURGER",hamburger),Style.RESET_ALL,file=self._stream)
        else:print(self._formated("HAMBURGER",hamburger),file=self._stream)
    def _formated(self,lvl,content):
        return self._format.format(h=self._time.hour,
                                    m=self._time.minute,
                                    s=self._time.second,
                                    d=self._time.day,
                                    M=self._time.month,
                                    y=self._time.year,
                                    i=self._time.microsecond/1000,
                                    root=self.root,
                                    level=lvl,
                                    content=content)
    
    
    def info(self,txt):
        if "info" not in self._enabled:return
        if self._colored:print(Fore.LIGHTGREEN_EX+Style.BRIGHT+self._formated("INFO",txt)+Style.RESET_ALL,file=self._stream)
        else:print(self._formated("INFO",txt),file=self._stream)

    def debug(self,txt):
        if "debug" not in self._enabled:return
        if self._colored:print(Fore.LIGHTBLUE_EX+Style.BRIGHT+self._formated("DEBUG",txt)+Style.RESET_ALL,file=self._stream)
        else:print(self._formated("DEBUG",txt),file=self._stream)

    def warn(self,txt):
        if "warn" not in self._enabled:return
        if self._colored:print(Fore.YELLOW+Style.BRIGHT+self._formated("WARN",txt)+Style.RESET_ALL,file=self._stream)
        else:print(self._formated("WARN",txt),file=self._stream)
    warning = warn # To enable compat from other logging modules

    def error(self,txt,exc_info=None):
        if "error" not in self._enabled:return
        if self._colored:print(Fore.LIGHTRED_EX+Style.BRIGHT+self._formated("ERROR",txt)+Style.RESET_ALL,file=self._stream)
        else:print(self._formated("ERROR",txt),file=self._stream)
        if exc_info:
            self.report_exception(exc_info)
    def fatal(self,txt):
        if "fatal" not in self._enabled:return
        if self._colored:print(Fore.RED+Style.BRIGHT+self._formated("FATAL",txt)+Style.RESET_ALL,file=self._stream)
        else:print(self._formated("FATAL",txt),file=self._stream)
    critical = fatal # To enable compat from other logging modules

    def report_exception(self,e:BaseException | tuple[Exception,Exception,types.TracebackType]):
        if isinstance(e,BaseException):
            lines = traceback.format_exception(e)
        else:
            if not isinstance(e,tuple) or len(e) != 3 or not isinstance(e[2],types.TracebackType):
                raise ValueError("This tuple (%s) is not a valid exc_info" % e) 
            lines = traceback.format_tb(e[2])
            lines.append(str(e[1].__class__.__name__)+ ": "+str(e[1]))
        for line in lines:
            line = line.strip("\n ")
            if self._colored:print(Fore.RED+Style.BRIGHT+self._formated("EXCEPTION",line)+Style.RESET_ALL,file=self._stream)
            else:print(self._formated("EXCEPTION",line),file=self._stream)
    exception = report_exception # To enable compat from other logging modules

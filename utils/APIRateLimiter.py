import os
import sys
from pathlib import Path
import json
import time
import threading
import copy
from flask import request


class __RateLimiter:
    __isfileopen :bool = False
    __samplefile = Path(sys.modules['__main__'].__file__).stem

    def __init__(self,filename=__samplefile,filetype="json",folder=""):
        self.thread_running = False
        self.filename=filename 
        self.filetype=filetype  
        self.Data=dict()
        self.CurrentFile=None
        self.lock = threading.RLock()
        self.stop_event = threading.Event()
        self.fullpath=os.path.join(folder, f"{filename}.{filetype}")
        self.Validopen=self.__Fileopener()
        

        pass
    def API_RL(self,IP_Adrs:str,Cleaning=False,
               CooldownTime=20,AllowedFreq=8,CleaningFreq=80,ResetTime=8
               )->int:
        # if isinstance(ipaddress,str):
        #     self.ip=int(ipaddress.ip_address(IP_Adrs))
        # else:print("Here")
        #     self.ip=IP_Adrs
        self.Metrics={
            "CooldownTime":CooldownTime,
            "AllowedFreq":AllowedFreq,
           
                 }
        # background_thread = threading.Thread(target=self.hehe, args=(start_val,), daemon=True)
        if Cleaning and not self.thread_running:
            self.thread_running=True
            BackgroundThread=threading.Thread(
            
                target=self.__ipcleaner,
                args=(CleaningFreq,ResetTime,),
                daemon=False)
            BackgroundThread.start()
            
        return self.__Validator(ip=IP_Adrs)
    def __Fileopener(self)->int:
        if getattr(self, "__isfileopen", False):
            return 0
        data=dict()
        fullpath=self.fullpath
        try:
            with open (fullpath,'r') as File:
                try:
                    self.CurrentFile = open(fullpath, 'r+')
                    self.Data=json.load(File)
                    self.__isfileopen=True
                    return 1
                except  json.JSONDecodeError as error:
                    return 0

                except FileNotFoundError as Fnf:

                    return self.__Filedumper(operation=0)
        except FileNotFoundError as Fnf:
                self.CurrentFile=open(fullpath, 'w')
                # print("HAHHA")
                # json.dump({},self.CurrentFile,indent=4)
                return 1
            # return self.__Filedumper(operation=0)

        except FileExistsError as FEE:

             return 0
        except Exception as error:
 
            print(error)
            return 0
    def __Filedumper(self,operation=0,Data=None)->int:
        # print(Data)
        # if msg is not None: print(msg[0])
        try:  
            with self.lock:
                # if msg is not None: print(msg[1])    
                fullpath=self.fullpath
                flag=0
                
                if Data is None:
                    Data={}
                if self.CurrentFile is None:
                    self.CurrentFile = open(fullpath, 'w')    
                try:
                    self.CurrentFile.seek(0)
                    json.dump(Data,self.CurrentFile,indent=4)
                    self.CurrentFile.truncate()
                    self.CurrentFile.flush()
                    flag=1
                    
                except Exception as e:
                    try :
                        with open("LOg..txt",'a') as file:
                            record=f"{time.time()}:Error is {e}\n"
                            file.write(record)
                            
                        flag=0
                    except Exception as err:
                        flag=0

                if operation==1:               
                        self.CurrentFile.close()
                        self.__isfileopen=False
                        return 1
                else:
                    self.__isfileopen=True
                    return flag
        except Exception as e:
            print("HEHEH")

            
                            
        pass           
    def __Validator(self,ip:int)->int:

            currenttime=int(time.time())
            error=False
            flag=1
            with self.lock:  
                try:
                    lastseen=currenttime-self.Data[ip]["LastSeenTime"]
                except KeyError:

                    self.Data[ip]={
                        # "WaitTime":0,
                        "WaitStamp":0,
                        "LastSeenTime":currenttime,
                        "Visits":1   
                    }
                    error=True
                self.Data[ip]["LastSeenTime"]=currenttime
                if  error is False:
                    if lastseen>self.Metrics["CooldownTime"]:
                            # self.Data[ip]["WaitTime"]=0
                            self.Data[ip]["WaitStamp"]=0
                            self.Data[ip]["Visits"]=1
                            flag= 1
                    else:
                        Datacopy=copy.deepcopy(self.Data)
                        self.Data[ip],flag=  self.__RecentVists(Data=Datacopy[ip],CrnTime=currenttime)

                self.__Filedumper(Data=self.Data)                    
                return (flag or error)   
    def __RecentVists(self,Data,CrnTime)->tuple: #Solution For DeadLock
        

        if Data["Visits"]<=self.Metrics["AllowedFreq"]:
            Data["WaitStamp"]=0
            Data["Visits"]+=1
            return (Data,1)
        # timetowait=0
        if Data["WaitStamp"]==0:
            Data["WaitStamp"]=CrnTime+self.Metrics["CooldownTime"]
            Data["Visits"]+=1
            return (Data,self.Metrics["CooldownTime"])
        else:
            timetosend=Data["WaitStamp"]-CrnTime
            Data["Visits"]+=1
            if timetosend<=0:
                Data["WaitStamp"]=0
                Data["Visits"]=0
                timetosend=1
            
            return (Data,timetosend)        
    def __ipcleaner(self,ClnFrq=100,restlimit=80):
        
        self.thread_running=True
        CleanData={}
        while not self.stop_event.is_set():
            # print("Inside the Loop")
            self.stop_event.wait(ClnFrq)
            if self.stop_event.is_set():
                break
            with self.lock:
                # print("Inside the Lock")
                currenttime=int(time.time())
                # Keystodelete=[]
                changes=False
                CleanData=self.Data.copy()
                keys=list(CleanData.keys())
                for ip in keys:
                    # print("Checking IPs")
                    # print("Key here")
                    if(currenttime-CleanData[ip]["LastSeenTime"]>restlimit):
                        # print("BYEEE")
                        # Keystodelete.append(ip)
                        # print("Found IP")
                        changes=True
                        try:
                            del CleanData[ip]
                        except Exception as e:
                            print(e)
                if changes is True:
                    # print("Bye IPPPP")
                    self.Data=CleanData
                    self.__Filedumper(Data=self.Data)
                    changes=False
                # print("Sleep")

            # print("Loop End")
            time.sleep(ClnFrq)
        self.thread_running = False 
                    


    # def API_RL(self,IP_Adrs:str,Cleaning=False,
    #            CooldownTime=20,AllowedFreq=8,CleaningFreq=80,ResetTime=8
    #            )->int:


__Filename = Path(sys.modules['__main__'].__file__).stem if hasattr(sys.modules['__main__'], '__file__') else "log"
__root_dir = Path(__file__).resolve().parent.parent
__FolderPath = __root_dir / "logs" / "API"

_LIMITER_CACHE = {}
def __RL(IP_Adrs:str,Cleaning=False,
                CooldownTime=20,AllowedFreq=8,CleaningFreq=80,ResetTime=8,Filename=None,Folder=None)->int:
    # global __RateL
    # print(__Filename)
    # if ((Filename!=__Filename)or (Folder!=__FolderPath)):
    Filename = Filename or __Filename
    Folder = Folder or __FolderPath
    cache_key = (Filename, Folder)
    if cache_key not in _LIMITER_CACHE:
        _LIMITER_CACHE[cache_key] = __RateLimiter(filename=Filename, folder=Folder)
    # __RateL = __RateLimiter(filename=Filename, folder=Folder)

    
    return (_LIMITER_CACHE[cache_key].API_RL(IP_Adrs=IP_Adrs,Cleaning=Cleaning,
               CooldownTime=CooldownTime,AllowedFreq=AllowedFreq,CleaningFreq=CleaningFreq,ResetTime=ResetTime))
    


def RequiredRateLimiter(Cleaning=False,
                CooldownTime=20,AllowedFreq=8,CleaningFreq=80,ResetTime=8,Filename=None,Folder=None,FileType=".json"):
        # target_folder = FolderPath if FolderPath is not None else __FolderPath
        def Decorator(Func):
            def Wrapper(*args,**kwargs):
                return  Func(*args, **kwargs)  #if this is to complicated  FEZ
                Ip=request.remote_addr
                # Ip="12"
                Filename=Func.__name__
                # print(Filename)
                # CoolDown=__RL(IP_Adrs=Ip,*args,**kwargs)
                CoolDown= __RL(IP_Adrs=Ip,Cleaning=Cleaning,Filename=Filename,Folder=Folder,
               CooldownTime=CooldownTime,AllowedFreq=AllowedFreq,CleaningFreq=CleaningFreq,ResetTime=ResetTime)
                if CoolDown==1:
                    return Func(*args, **kwargs)
                else:
                    return f"Rate limit exceeded. Please wait {CoolDown} Secs.", 429 
                
            return Wrapper
        return Decorator



           
if __name__=="__main__":

    t=__RateLimiter()
    v=t.API_RL("127.0.0.2",Cleaning=True,CleaningFreq=1,CooldownTime=7)
    print(v)

            
        





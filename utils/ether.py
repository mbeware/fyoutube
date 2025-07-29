from  multiprocessing import SimpleQueue
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

#ether : a simple communication device
#etherbus : the link between every processes
#nugget : objet being shared

from typing import NewType,  Any,  Callable



Timestamp= NewType('Timestamp', float)
def ether_now()->Timestamp:
    return Timestamp(datetime.now().timestamp())

Payload_type = Enum('Payload_type', 'PAYLOAD MESSAGE VIDEO_INFO CHANNEL_INFO STATUS WILD', start=100)
Action = Enum('Action','DOWNLOAD LISTVIDEO LISTRSS LISTPLAYLIST DELETE SEND GET UPDATE REGISTER UNREGISTER',start=200)
State = Enum('State','ALIVE SUSPENDED EXPIRED PROCESSED', start=300)

@dataclass
class Ether_Payload:
    code:str

@dataclass
class Ether_Message(Ether_Payload):
    message:str
    type:str

@dataclass
class Ether_VideoInfo(Ether_Payload):
    video_url:str
    channel:str
    action:Action

@dataclass
class Ether_ChannelInfo(Ether_Payload):
    channel_url:str
    channel:str
    action:Action

@dataclass
class Ether_Status(Ether_Payload):
    code:str
    action:Action
    extra:Any

@dataclass
class Ether_Wild(Ether_Payload):
    info_about_extra:str
    extra:Any


@dataclass
class Nugget:
    type:Payload_type
    source:str
    sent:Timestamp
    state:State
    read:dict[str,Timestamp]={}
    dest:str|None=None
    payload:Ether_ChannelInfo|Ether_Message|Ether_Status|Ether_Payload|Ether_VideoInfo|Ether_Wild|None=None
    

etherbus:SimpleQueue[Nugget] = SimpleQueue()


starting_nugget=Nugget(type=Payload_type.STATUS,source="init",dest="ether_loop",sent=ether_now(),state=State.ALIVE)
etherbus.put(starting_nugget)

registered_ethernauts:dict[str,Callable[[Nugget],None]]={}

ETHER_TIMEOUT = 600

def ether_loop():
    me = 'ether_loop'
    while True:
        cnugget=etherbus.get()
        
        if cnugget.state in (State.EXPIRED, State.PROCESSED):
            continue 
        if cnugget.dest == me:
            if cnugget.source=="init": #proof of live token
                pass # we will just update the time and put it back on the bus.
            elif cnugget.type == Payload_type.STATUS:
                sn=Nugget(type=Payload_type.STATUS,source=cnugget.source,sent=cnugget.sent,state=cnugget.state,read=cnugget.read,dest=cnugget.dest,payload=cnugget.payload)
                if sn.payload.action:Action == Action.REGISTER:

#                    registered_ethernauts[pl.extra.dest]=pl.extra.callback[[Nugget],None]


        if cnugget.dest in registered_ethernauts:
            registered_ethernauts[cnugget.dest](cnugget)
            cnugget.state=State.PROCESSED

        if ether_now()-cnugget.sent > ETHER_TIMEOUT:
            cnugget.state = State.EXPIRED
            

        #we put back the nugget for now//    
        cnugget.read[me]=ether_now()
        etherbus.put(cnugget)




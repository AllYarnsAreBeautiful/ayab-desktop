# -*- coding: utf-8 -*-
# This file is part of AYAB.
#
#    AYAB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AYAB is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AYAB.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2022 Marcus Hoose (eKnitter.com)

import threading
import socket
from time import sleep

# Port for UDP
localPort = 12345
broadcast = ("255.255.255.255", 12345)

queueLock = threading.Lock()

class UDPThread(threading.Thread):
   def __init__(self) -> None:
      threading.Thread.__init__(self)                              
      self.exitFlag = False
      self.__sockUDP = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
      self.__sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
      self.__sockUDP.settimeout(0.1)
      self.__sockUDP.setblocking(False)
      self.__hostname = socket.gethostname()
      self.__ip_addresses = socket.gethostbyname_ex('localhost')
      self.__ip_address = "0.0.0.0"
      self.addresslist = list()

   def run(self):
      #print("Starting ")
      self.__sockUDP.bind((self.__ip_address ,localPort))
      
      Run = True
      while Run:
         try:
            dataadress = self.__sockUDP.recvfrom(250)
            #print("Recive")
            adress = dataadress[1][0]
            if not(adress in self.__ip_addresses[2]) and not(adress in self.addresslist):
               queueLock.acquire(1)
               self.addresslist.append(adress)
               queueLock.release()
         except:
            sleep(1)
         queueLock.acquire(1)
         Run = not self.exitFlag         
         queueLock.release()
         #print("RUN = ",Run)
         
      #print("Exiting")
      self.__sockUDP.close()
      del(self.__sockUDP)
      self.__sockUDP = None
      return

   def stop(self):
      #print("Stoping")      
      queueLock.acquire(1)
      self.exitFlag = True
      queueLock.release()

   def getIPlist(self):
      #print("GetList")
      result = list()
      if queueLock.acquire(True,0.1):
         result.extend(self.addresslist)
         queueLock.release()
      return result

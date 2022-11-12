import pandas as pd
import numpy as np
import functools as ft
import itertools as it
from abc import ABC, abstractmethod
from BaseReport import Tools

""" 
 Want to get practice on decorators 
 
i want thesde objects to hold thier own record of Reports and to log it
{what reports, 
what table they store form the db },
 and have connect to a database.

 intializing a  obj with create a baseReport based on the User. 

 this is a start of full app - will need to figure out the details 

 will need to modularize 

"""
class Users(ABC): 
    
    def __init__(self):
        self.id
        self.name
        self.pm 
        self.projects
        self.rate

    #class attributes    

    def __str__(self):
        info = "The name"+ name + "n\ id:" + self.id + "n\ id:"+ self.id
        return "The Name"+self.name
        
    numofreports = 0; 

    @abstractmethod
    def idSelf():
        pass

    @property
    def getPMs(self):
        return self.pm

    @property
    def setPMs(self, link):
        pass

    @classmethod
    def countProducedReports():
        pass 

    




class Accountant(Users):

    def __new___(cls):
        print("__new__ magic method is called")
        inst = object.__new___(cls)
        return inst

    def __init__(self,name):
        super().__init__()
        self.name = name


  

    def getReports():
        pass




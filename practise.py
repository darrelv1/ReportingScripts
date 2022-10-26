import pandas as pd
from abc import ABC

class Parent(ABC):

    def __init__(self,name, age, occupation):
        self.name = name
        self.age = age
        self.occupation = occupation

    def traits (self, passdown):
        if passdown:
            print("Parents pass down thier traits to thier offspring")
            print(self.name)
            print(self.age)
            print(self.occupation)
            print("\n")

    def testing(self):
        print("it's working")


class child(Parent):


    def __init__(self):
        self.asldkfj= "l;kfjas;dlkfja;slkdjf;klasjd;flkjasd;lfkj"
        

    def traits(self, passdown):
        return super().traits(passdown)
    

    
  #  def __init__(self):
  #      super().__init__("Darrel Valdiviezo", 40,"Software Developer")

    




Me = child()
Me.traits(True)
Me.testing()


from abc import abstractmethod, ABC




class Reporttools(ABC):


    @abstractmethod
    def printer(cls, link, df_dictionary):
        pass
    


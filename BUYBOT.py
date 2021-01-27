from abc import ABC, abstractmethod

# Abstract class BUYBOT
# Used as a template for AMZN_BOT, BSTBUY_BOT
class BUY_BOT(ABC) : 
    @abstractmethod
    def setup(self) : 
        pass

    @abstractmethod
    def check_in_stock(self) :
        pass

    @abstractmethod
    def add_to_cart(self) :  
        pass

    @abstractmethod
    def checkout(self) : 
        pass

    @abstractmethod
    def close(self) : 
        pass
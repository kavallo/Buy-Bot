from AMZN import AMZN_BOT
from selenium import webdriver 
import os

DRIVER_PATH = os.getcwd() + "\\chromedriver.exe"
WEB_DRIVER = webdriver.Chrome(DRIVER_PATH)

# ------------------------------------------
# Main 


AMAZON = AMZN_BOT(WEB_DRIVER) 
AMAZON.setup()
AMAZON.add_to_cart()
AMAZON.checkout()
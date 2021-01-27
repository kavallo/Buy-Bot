from AMZN import AMZN_BOT
from BSTBUY import BSTBUY_BOT
from NEWEGG import NEWEGG_BOT
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import asyncio
import threading
import time
import os

load_dotenv() 

# ------------------------------------------
# Webdriver setup

# Webdriver Options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

AMZN_DRIVER_PATH = os.getcwd() + "\\chromedriver\\amazon_driver.exe"
BSTBUY_DRIVER_PATH = os.getcwd() + "\\chromedriver\\bstbuy_driver.exe"
AMAZON = AMZN_BOT(webdriver.Chrome(AMZN_DRIVER_PATH, options=chrome_options))
BESTBUY = BSTBUY_BOT(webdriver.Chrome(BSTBUY_DRIVER_PATH, options=chrome_options))

# ------------------------------------------
# Functions

# Perform setup for BstBuy & Amzn bots
async def setup() : 
    AMZN_SETUP = setup_loop.create_task(AMAZON.setup())
    BB_SETUP = setup_loop.create_task(BESTBUY.setup())
    await asyncio.wait([AMZN_SETUP, BB_SETUP])

# Checks if the product is in stock 
def stock_check() :
    # Loop until product is in stock 
    while (True) :
        AMZN_STOCK = AMAZON.check_in_stock()
        BB_STOCK = BESTBUY.check_in_stock()
        # If Amzn product is in stock
        if (AMZN_STOCK) : 
            AMAZON.add_to_cart()
            BESTBUY.close()
            return True
        # If BstBuy product is in stock 
        elif (BB_STOCK) : 
            BESTBUY.add_to_cart()
            AMAZON.close()
            return False
        # If neither are in stock, sleep 
        else : 
            print("Sleeping " + os.getenv("page_refresh_timer") + " seconds...")
            time.sleep(int(os.getenv("page_refresh_timer")))
            
# ------------------------------------------
# Main

# Setup 
setup_loop = asyncio.get_event_loop()
setup_loop.run_until_complete(setup())

# Stock checking
check = stock_check()

# Checkout
if (check) : 
    AMAZON.checkout()
else : 
    BESTBUY.checkout()
from AMZN import AMZN_BOT
from BSTBUY import BSTBUY_BOT
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import threading
import time
import os

load_dotenv() 
USE_AMZN = os.getenv("USE_AMZN")
USE_BSTBUY = os.getenv("USE_BSTBUY")

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
def setup() :
    # If "USE_AMZN" setting is set to True in .env file
    if(USE_AMZN) :
        AMZN_SETUP_THREAD = threading.Thread(target=AMAZON.setup())
        AMZN_SETUP_THREAD.start()
    else :
        AMAZON.close()
        print("[AMAZON] Bot not in use. To fix, change settings in .env file")
    
    # If "USE_BSTBUY" setting is set to True in .env file
    if(USE_BSTBUY) :
        BSTBUY_SETUP_THREAD = threading.Thread(target=BESTBUY.setup())
        BSTBUY_SETUP_THREAD.start()
    else : 
        BESTBUY.close()
        print("[BESTBUY] Bot not in use. To fix, change settings in .env file")
    # If both bots are set to False in .env file
    if ((not USE_AMZN) and (not USE_BSTBUY)) :
        print("Both bots set to \"False\" in .env file. Exiting...")
        exit()
    # Join setup threads 
    AMZN_SETUP_THREAD.join() 
    BSTBUY_SETUP_THREAD.join()
    
# Checks if the product is in stock 
# Returns boolean based on which bot has the item in stock
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

# Runs setup, checks if the item is in stock, then purchases product 
def main() : 
    setup()
    check = stock_check()
    if (check) : 
        AMAZON.checkout()
    else : 
        BESTBUY.checkout()

# -------------------------
# Run 

main() 
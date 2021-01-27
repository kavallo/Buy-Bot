from BUYBOT import BUY_BOT
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from dotenv import load_dotenv
import asyncio
import time 
import os

load_dotenv() 

#---------------------------------------------------------------------------
# CSS Selectors used in BSTBUY_BOT

SURVEY_POPUP = "#survey_invite_no"
USER_SEL = "#fld-e"
PASS_SEL = "#fld-p1"
ADD_TO_CART = "button.btn-primary:nth-child(1)"
ALT_GO_TO_CART = ".cart-link > img:nth-child(1)"
CHECKOUT = ".btn-lg"

#---------------------------------------------------------------------------
# CLASS - BSTBUY_BOT

class BSTBUY_BOT(BUY_BOT) : 
    # Constructor
    def __init__(self, web_driver) : 
        self.driver = web_driver
    
    # Open browser and login to best buy account
    async def setup(self) : 
        self.driver.get(os.getenv("BSTBUY_PRODUCT_URL"))
        print("Opening Best Buy browser...")
        await asyncio.sleep(1)
        if self.driver.find_elements_by_css_selector(SURVEY_POPUP) :
            self.driver.find_element_by_css_selector(SURVEY_POPUP).click()

    # Checks if product is in stock. Used in add_to_cart method
    def check_in_stock(self) :
        self.driver.refresh()
        time.sleep(1)
        if self.driver.find_elements_by_css_selector(ADD_TO_CART) : 
            return True 
        else :
            print("[BESTBUY] Product not in stock")
            return False

    # Adds item to cart. Utilizes check_in_stock method & refreshes page
    def add_to_cart(self) :  
        print("[BESTBUY] Item is in stock! Adding to cart...")
        # Add product to cart
        self.driver.find_element_by_css_selector(ADD_TO_CART).click()

    # Purchasing Process
    def checkout(self) : 
        time.sleep(1)
        # Refreshes page, then goes to cart (Avoids edge cases involving pop ups)
        self.driver.refresh() 
        time.sleep(1) 
        self.driver.find_element_by_css_selector(ALT_GO_TO_CART).click()

        # Continue with checkout     
        time.sleep(2)
        print("[BESTBUY] Proceeding to checkout")
        self.driver.find_element_by_css_selector(CHECKOUT).click()

        # Sign-in Process  - Username
        print("[BESTBUY] Signing in...")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, USER_SEL)))
        self.driver.find_element_by_css_selector(USER_SEL).click()
        user_logon = self.driver.find_element_by_css_selector(USER_SEL)
        user_logon.send_keys(os.getenv("BSTBUY_EMAIL"))
        time.sleep(1) 

        # Sign-in Process  - Password
        self.driver.find_element_by_css_selector(PASS_SEL).click()
        user_logon = self.driver.find_element_by_css_selector(PASS_SEL)
        user_logon.send_keys(os.getenv("BSTBUY_PASS"))
        time.sleep(1) 
        user_logon.send_keys(Keys.RETURN)
        print("[BEST BUY] Sign in success!")

        # Purchase 
        self.driver.find_element_by_css_selector(CHECKOUT).click()

    # Exit webdriver session
    def close(self) : 
        self.driver.quit()
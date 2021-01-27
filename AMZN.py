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
# CSS Selectors used in AMZN_BOT
AMZN_SIGN_IN = "#nav-signin-tooltip > a:nth-child(1) > span:nth-child(1)"
USER_SEL = "#ap_email"
PASS_SEL = "#ap_password"
ADD_TO_CART = "#add-to-cart-button"
NO_INSURANCE = "#siNoCoverage-announce"
NO_INSURANCE_2 = "#attachSiNoCoverage-announce"
NO_INSURANCE_CHECKOUT = "#attach-sidesheet-checkout-button > span > input"
REG_CHECKOUT = "#hlb-ptc-btn-native"
GO_TO_CART = "#nav-cart-count"
PURCHASE = "#bottomSubmitOrderButtonId > span > input"

#---------------------------------------------------------------------------
# CLASS - AMZN_BOT

class AMZN_BOT(BUY_BOT) : 
    # Constructor
    def __init__(self, web_driver) : 
        self.driver = web_driver
    
    # Open and login to amazon account
    async def setup(self) : 
        self.driver.get(os.getenv("AMZN_PRODUCT_URL"))
        print("Opening Amazon browser...")

        # Wait for sign in button to appear, then click 
        await asyncio.sleep(1) 
        signin = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, AMZN_SIGN_IN)))
        self.driver.find_element_by_css_selector(AMZN_SIGN_IN).click() 

        # Sign-in Process  - Username
        print("[Amazon] Signing in...")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, USER_SEL)))
        self.driver.find_element_by_css_selector(USER_SEL).click()
        user_logon = self.driver.find_element_by_css_selector(USER_SEL)
        user_logon.send_keys(os.getenv("AMZN_EMAIL"))
        await asyncio.sleep(2) 
        user_logon.send_keys(Keys.RETURN)

        # Sign-in Process  - Password
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, PASS_SEL)))
        self.driver.find_element_by_css_selector(PASS_SEL).click()
        user_logon = self.driver.find_element_by_css_selector(PASS_SEL)
        user_logon.send_keys(os.getenv("AMZN_PASS"))
        await asyncio.sleep(2) 
        user_logon.send_keys(Keys.RETURN)
        print("[AMAZON] Sign in success!")
    
    # Checks if product is in stock. Used in add_to_cart method
    def check_in_stock(self) :
        self.driver.refresh()
        time.sleep(1)
        if self.driver.find_elements_by_css_selector(ADD_TO_CART) : 
            return True 
        else :
            print("[AMAZON] Product not in stock")
            return False

    # Adds item to cart. Utilizes check_in_stock method & refreshes page
    def add_to_cart(self) :  
        print("[AMAZON] Item is in stock! Adding to cart...")
        # Add product to cart
        self.driver.find_element_by_css_selector(ADD_TO_CART).click()

    # Purchasing Process
    def checkout(self) : 
        time.sleep(2)
        # If Insurance coverage plan pops up after adding to cart, click "No thanks" button
        if (self.driver.find_elements_by_css_selector(NO_INSURANCE)) : 
            self.driver.find_element_by_css_selector(NO_INSURANCE).click()
            time.sleep(2) 
            # Click on checkout button (in popup menu)
            if (self.driver.find_elements_by_css_selector(NO_INSURANCE_CHECKOUT)) :
                self.driver.find_element_by_css_selector(NO_INSURANCE_CHECKOUT).click()
            else : 
                self.driver.find_element_by_css_selector(REG_CHECKOUT).click()
        # If alternate insurance pop up shows, 
        elif (self.driver.find_elements_by_css_selector(NO_INSURANCE_2)) : 
            self.driver.find_element_by_css_selector(NO_INSURANCE_2).click()
            time.sleep(2) 
            # Click on checkout button (in popup menu)
            self.driver.find_element_by_css_selector(NO_INSURANCE_CHECKOUT).click()

        # Else if pop up menu comes up (w/ no insurance option)
        elif (self.driver.find_elements_by_css_selector(NO_INSURANCE_CHECKOUT)) : 
            time.sleep(2) 
            # Click on checkout button (in popup menu)
            self.driver.find_element_by_css_selector(NO_INSURANCE_CHECKOUT).click()

        # Else perform regular checkout 
        else : 
            self.driver.find_element_by_css_selector(REG_CHECKOUT).click()
        
        print("[AMAZON] Proceeding to checkout")
        time.sleep(1)
        # Purchase 
        self.driver.find_element_by_css_selector(PURCHASE).click()

    # Exit webdriver session 
    def close(self) : 
        self.driver.quit()
from BUYBOT import BUY_BOT
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from dotenv import load_dotenv
import time 
import os

load_dotenv() 

#---------------------------------------------------------------------------
# CSS Selectors used in AMZN_BOT
AMZN_SIGN_IN = "#nav-signin-tooltip > a:nth-child(1) > span:nth-child(1)"
USER_SEL = "#ap_email"
PASS_SEL = "#ap_password"
ADD_TO_CART = "#add-to-cart-button"
NO_INSURANCE = "#attachSiNoCoverage-announce"
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
    def setup(self) : 
        self.driver.get(os.getenv("AMZN_PRODUCT_URL"))
        print("Opening Amazon browser...")

        # Wait for sign in button to appear, then click 
        time.sleep(1) 
        signin = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, AMZN_SIGN_IN)))
        self.driver.find_element_by_css_selector(AMZN_SIGN_IN).click() 

        # Sign-in Process  - Username
        print("Amazon - Signing in...")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, USER_SEL)))
        self.driver.find_element_by_css_selector(USER_SEL).click()
        user_logon = self.driver.find_element_by_css_selector(USER_SEL)
        user_logon.send_keys(os.getenv("AMZN_EMAIL"))
        time.sleep(2) 
        user_logon.send_keys(Keys.RETURN)

        # Sign-in Process  - Password
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, PASS_SEL)))
        self.driver.find_element_by_css_selector(PASS_SEL).click()
        user_logon = self.driver.find_element_by_css_selector(PASS_SEL)
        user_logon.send_keys(os.getenv("AMZN_PASS"))
        time.sleep(2) 
        user_logon.send_keys(Keys.RETURN)
        print("Sign in success!")
    
    # Checks if product is in stock. Used in add_to_cart method
    def check_in_stock(self) :
        time.sleep(2) 
        try : 
            is_in_stock = self.driver.find_element_by_css_selector(ADD_TO_CART)
            return (is_in_stock.is_displayed())
        except : #TODO Find out specific error name to catch  
            return False

    # Adds item to cart. Utilizes check_in_stock method & refreshes page
    def add_to_cart(self) :  
        # Check if in stock. If !in_Stock: wait, then refresh page & check again
        in_Stock = self.check_in_stock()
        while(not in_Stock) : 
            print("(AMAZON) Product not in stock. Sleeping " + os.getenv("page_refresh_timer") + " seconds.")
            time.sleep(int(os.getenv("page_refresh_timer")))
            self.driver.refresh()
            in_Stock = self.check_in_stock()
        print("(AMAZON) Item is in stock! Adding to cart...")
        # If product is in stock, click on "add to cart" button
        self.driver.find_element_by_css_selector(ADD_TO_CART).click()

    # Purchasing Process
    def checkout(self) : 
        time.sleep(2)
        # If Insurance coverage plan pops up after adding to cart, click "No thanks" button
        try :  
            self.driver.find_element_by_css_selector(NO_INSURANCE) 
            self.driver.find_element_by_css_selector(NO_INSURANCE).click()
            time.sleep(2) # Sleep 2s
            # Click on checkout button (exclusive to insurance pop-up)
            self.driver.find_element_by_css_selector(NO_INSURANCE_CHECKOUT).click()

        # If insurance coverage pop-up doesn't show, add to cart & check out
        except : #TODO Find out specific error name to catch 
            self.driver.find_element_by_css_selector(REG_CHECKOUT).click()
        print("Proceeding to checkout")
        time.sleep(1) 

        # Purchase 
        # IMPORTANT: NEXT LINE COMMENTED OUT FOR TESTING -- UNCOMMENT TO PURCHASE ITEM
        # self.driver.find_element_by_css_selector(PURCHASE).click()
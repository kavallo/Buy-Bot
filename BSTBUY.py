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
# CSS Selectors used in BSTBUY_BOT
BB_LOGIN_DROPDOWN = "#header-block > div.header-large > div.fullbleed-wrapper > div > nav.utility-navigation\
                     > ul > li:nth-child(1) > button > div.gvpHeadicon.drop-arrow-icon.flyBtn > svg"
BB_SIGN_IN = ".lam-signIn__button"
USER_SEL = "#fld-e"
PASS_SEL = "#fld-p1"
ADD_TO_CART = "button.btn-primary:nth-child(1)"
ALT_GO_TO_CART = ".cart-link > img:nth-child(1)"
CHECKOUT = ".btn-lg"
PURCHASE = "#checkoutApp > div.page-spinner.page-spinner--out > div:nth-child(1) > div.checkout.large-view.fast-track\
            > main > div.checkout__container.checkout__container-fast-track > div.checkout__col.checkout__col--primary\
            > div > div.checkout-panel.contact-card > div.contact-card__order-button > div > button"

#---------------------------------------------------------------------------
# CLASS - BSTBUY_BOT

class BSTBUY_BOT(BUY_BOT) : 
    # Constructor
    def __init__(self, web_driver) : 
        self.driver = web_driver
    
    # Open browser and login to best buy account
    def setup(self) : 
        self.driver.get(os.getenv("BSTBUY_PRODUCT_URL"))
        print("Opening Best Buy browser...")
        time.sleep(1)
        # Wait for account dropdown to appear, then click on sign in  
        self.driver.find_element_by_css_selector(BB_LOGIN_DROPDOWN).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, BB_SIGN_IN)))
        self.driver.find_element_by_css_selector(BB_SIGN_IN).click()

        # Sign-in Process  - Username
        print("Best Buy - Signing in...")
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
        print("Sign in success!")

    # Checks if product is in stock. Used in add_to_cart method
    def check_in_stock(self) :
        time.sleep(2) 
        if self.driver.find_elements_by_css_selector(ADD_TO_CART) : 
            return True 
        else :
            return False

    # Adds item to cart. Utilizes check_in_stock method & refreshes page
    def add_to_cart(self) :  
        # Check if in stock. If !in_Stock: wait, then refresh page & check again
        in_Stock = self.check_in_stock()
        while(not in_Stock) : 
            print("(BESTBUY) Product not in stock. Sleeping " + os.getenv("page_refresh_timer") + " seconds.")
            time.sleep(int(os.getenv("page_refresh_timer")))
            self.driver.refresh()
            in_Stock = self.check_in_stock()
        print("(BESTBUY) Item is in stock! Adding to cart...")
        # If product is in stock, click on "add to cart" button
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
        print("(BESTBUY) Proceeding to checkout")
        self.driver.find_element_by_css_selector(CHECKOUT).click()
        
        # TODO -- There's an edge case where an additional pop up comes up right before
        # checkout. Haven't been able to recreate it, but if I see it again I'll add a workaround 
        # for it
        
        # Purchase 
        # IMPORTANT: NEXT LINE COMMENTED OUT FOR TESTING -- UNCOMMENT TO PURCHASE ITEM
        # self.driver.find_element_by_xpath(PURCHASE).click()
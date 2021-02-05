# Buy-Bot

A script made in Python 3.9.1 that automates the purchasing process of any item on Best Buy or Amazon. Used as a tool to get high in demand products in the hands of consumers, and saves you the time and stress of worrying when a product will be in stock for you to purchase it.

## Installing & Running

1. Download the latest version of Python from [here](https://www.python.org/downloads/). Make sure that you add Python to your PATH.
2. Download the latest version of Google Chrome from [here](https://www.google.com/chrome/)
3. Download this project
   - The webdrivers provided work **only** with Google Chrome version 88. If you're using a different version of Chome, download two of the appropriate webdrivers [here](https://chromedriver.chromium.org/downloads). Rename one webdriver amazon_driver.exe and the other bstbuy_driver.exe, and place both files in the chromedriver folder.    
4. Run setup.bat
5. Edit settings in the [.env](.env) file
6. Start the bot by running start.bat in this project's root directory **or** by typing the following in a terminal:
   - **`python main.py`**

## Common Questions

### Why does Buy-Bot stop after reaching a prompt for 2FA authentication when logging in to my account?
   - Buy-Bot isn't built to handle 2FA. If you receive a prompt from Amazon or Best Buy that an authentication email / text has been sent, verify that you're logging in then restart the bot.

### Why does Buy-Bot stop after reaching the checkout page?
   - Buy-Bot **does not** handle your address or credit card information, so please make sure that your default name, address, payment method, and shipping method are already set in your Best Buy or Amazon account. The "Place your order" button should be visible during checkout.

## License and copyright

© 2021 Jay J Patel
Licensed under the [Apache License](LICENSE)

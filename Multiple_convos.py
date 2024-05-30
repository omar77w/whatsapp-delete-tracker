import sys
import ctypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

import time

options = Options()
"""
Adding a profile allows you to save cookies and skip scanning QR Code every time you run the program.
Look here for more details: https://medium.com/@stevedep/send-whatsapp-messages-with-python-selenium-on-odroid-using-firefox-d50c6e3f697e
"""
#options.add_argument('-profile')
#options.add_argument('C:\\Users\\USER\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\pfg80jo8.python profile')

driver = webdriver.Firefox(options=options)    #For Chrome, replace "Firefox" with "Chrome"

driver.get("https://web.whatsapp.com")

try:
    print("Please log into WhatsApp...\n")
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, "side"))) #You have 120 seconds to login
except:
    print("You did not log in. Session timed out.")
    driver.quit()
    sys.exit(1)

print("Logged in! Loading messages...")

try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.x10l6tqk.xh8yej3.x1g42fcv")))
except:
    print("Loading messages timed out.")
    driver.quit()
    sys.exit(1)

time.sleep(20) #Wait ~20 seconds for conversations to load
print("Scanning...")

convos = driver.find_elements(By.CLASS_NAME, "_ak8q")  #List of conversations' page elements
users = {}

#First scan of all convos:
for convo in convos[1:]:   #Start from 1 to skip "Archive"
    if convo not in users:
        users[convo.text] = [0,0,0,0]    #Initialize 4 list items. These will store the scans and number of deleted messages, before and after.

    driver.execute_script("arguments[0].scrollIntoView();", convo)
    convo.click()

    #Scan conversations and store in dict1
    dict1 = set()
    texts = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
    dels = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw") #The number of messages that say "This message has been deleted"
    for i in texts:
        dict1.add(i.text)
    #Scroll up to load more messages
    for i in range(3):
        driver.find_element(By.TAG_NAME, ('body')).send_keys(Keys.PAGE_UP)
        texts2 = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
        dels2 = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw")
        for j in texts2:
            if j not in dict1:
                dict1.add(j.text)
        for j in dels2:
            if j not in dels:
                dels.append(j)

    users[convo.text][0] = dict1
    users[convo.text][2] = len(dels)

    if convos.index(convo) == 1:
        searchbar_item = convo.text


# Second scan of all conversations
while True:
    #Go to top of chat list:
    searchbar = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div[1]")
    for i in searchbar_item:
        searchbar.send_keys(i)
    for i in searchbar_item:
        searchbar.send_keys(Keys.BACKSPACE)
    time.sleep(0.1)

    for user in users:
        loc = driver.find_element(By.XPATH, "//*[contains(text(),'"+user+"')]")
        driver.execute_script("arguments[0].scrollIntoView();", loc)
        loc.click()

        dict2 = set()
        texts = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
        dels = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw")
        for i in texts:
            dict2.add(i.text)
        #Scroll up to load more messages
        for i in range(3):
            driver.find_element(By.TAG_NAME, ('body')).send_keys(Keys.PAGE_UP)
            texts2 = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
            dels2 = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw")
            for j in texts2:
                if j not in dict2:
                    dict2.add(j.text)
            for j in dels2:
                if j not in dels:
                    dels.append(j)
       
        users[user][1] = dict2
        users[user][3] = len(dels)

        #Compare to first scan
        if users[user][0] != users[user][1] and users[user][3] > users[user][2]: #If the before and after dictionaries aren't the same *and* the number of deleted messages in 2nd scan is more than 1st:
            for i in users[user][0]:
                if i not in users[user][1]:
                    print("A message has been deleted! By: " + user)
                    print("Deleted message is:")
                    print(i)
                    ctypes.windll.user32.MessageBoxW(0, "A message has been deleted! By: {}\n\nDeleted message is:\n{}".format(user, i), "Message deleted!", 1)
    
        users[user][0] = users[user][1].copy()  #Second scan is now the first one to repeat loop
        users[user][2] = users[user][3]


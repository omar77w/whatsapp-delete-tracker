import sys
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

driver = webdriver.Firefox(options=options)   #For Chrome, replace "Firefox" with "Chrome"

driver.get("https://web.whatsapp.com")

try:
    print("Please log into WhatsApp...\n")
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "side")))  #You have 120 seconds to login
except:
    print("You did not log in. Session timed out.")
    driver.quit()
    sys.exit(1)

print("Logged in! Loading messages...")

try:
    WebDriverWait(driver,7).until(EC.presence_of_element_located((By.CLASS_NAME, "_ak8l")))
except:
    print("Loading messages timed out.")
    driver.quit()
    sys.exit(1)

print("Please select a conversation to track")
time.sleep(5) #Wait ~5 seconds to load conversations

try:
    WebDriverWait(driver,40).until(EC.presence_of_element_located((By.CLASS_NAME, "_amm9")))
    print("Scanning...")
except:
    print("Session timed out. No conversation was selected.")
    driver.quit()
    sys.exit(1)

#First scan:
dict1 = {}
texts = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
dels = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw") #The number of messages that say "This message has been deleted"
for i in texts:
    dict1[i] = i.text
#Scroll up to load more messages
for i in range(3):
    driver.find_element(By.TAG_NAME, ('body')).send_keys(Keys.PAGE_UP)
    time.sleep(0.05)
    texts2 = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
    dels2 = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw")
    for j in texts2:
        if j not in dict1:
            dict1[j] = j.text
    for j in dels2:
        if j not in dels:
            dels.append(j)
num_dels1 = len(dels)


#Second scan:
while True:
    driver.find_element(By.TAG_NAME, ('body')).send_keys(Keys.END)
    time.sleep(5) #Wait for change in messages

    dict2 = {}
    texts = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
    dels = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw")
    for i in texts:
        dict2[i] = i.text
    #Scroll up to load more messages
    for i in range(4):
        driver.find_element(By.TAG_NAME, ('body')).send_keys(Keys.PAGE_UP)
        time.sleep(0.05)
        texts2 = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
        dels2 = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw")
        for j in texts2:
            if j not in dict1:
                dict2[j] = j.text
        for j in dels2:
            if j not in dels:
                dels.append(j)
    num_dels2 = len(dels)

    #Compare to first scan
    if dict1 != dict2 and num_dels2 > num_dels1:  #If the before and after dictionaries aren't the same *and8 the number of deleted messages in 2nd scan is more than 1st:
        for i in dict1:
            if i not in dict2:
                print("A message has been deleted!")
                print("Deleted message is:")
                print(dict1[i])

    dict1 = dict2  #Second scan is now the first one to repeat loop
    num_dels1 = num_dels2
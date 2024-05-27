import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.firefox.options import Options

import time


options = Options()
options.add_argument('-profile')
options.add_argument('C:\\Users\\Omar Arab\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\pfg80jo8.python profile')

driver = webdriver.Firefox(options=options)

driver.get("https://web.whatsapp.com")

try:
    print("Please log into WhatsApp...\n")
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "side"))) #You have 60 seconds to login
except:
    print("You did not log in. Session timed out.")
    driver.quit()
    sys.exit(1)

print("Logged in! Loading messages...")

try:
    WebDriverWait(driver,7).until(EC.presence_of_element_located((By.CLASS_NAME, "_ak8l")))
except:
    print("Loading messages timed out.")

time.sleep(10) #Wait ~20 seconds to load conversations
print("Please select a conversation to track")

try:
    WebDriverWait(driver,25).until(EC.presence_of_element_located((By.CLASS_NAME, "_amm9")))
except:
    print("Session timed out. No conversation was selected.")


dict1 = {}
texts = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
dels = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw")
for i in texts: #Add text in first view to the dictionary
    dict1[i] = i.text
#Scroll up
for i in range(3):
    driver.find_element(By.TAG_NAME, ('body')).send_keys(Keys.PAGE_UP) #Goes up to top of messages to expand dict2
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
    
print("Length of dict 1: ", len(dict1))
print("Num of dels = ", num_dels1)

while True:
    driver.find_element(By.TAG_NAME, ('body')).send_keys(Keys.END)
    time.sleep(5) #Wait for change in messages

    dict2 = {}
    texts = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
    dels = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw")
    for i in texts: #Add text in first view to the dictionary
        dict2[i] = i.text
    #Scroll up
    for i in range(4):
        driver.find_element(By.TAG_NAME, ('body')).send_keys(Keys.PAGE_UP) #Goes up to top of messages to expand dict2
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
    print("Length of dict 2: ", len(dict2))
    print("Num of dels = ", num_dels2)

    if dict1 != dict2 & num_dels2 > num_dels1:
        for i in dict1:
            if i not in dict2:
                print("A message has been deleted!")
                print("Deleted message is:")
                print(dict1[i])

    dict1 = dict2
    num_dels1 = num_dels2
    print("Length of dict 1: ", len(dict1))
    print("Num of dels = ", num_dels1)


#(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")


#Copy into a dict all akbu locations and their associated text
#every 2 seconds:
#scan through keys of dict. If one key no longer exists, say that it was deleted and print its message.
#rescan akbus and recreate dict

#for i in convos[2:]:
#    driver.execute_script("arguments[0].scrollIntoView();", i)
#    i.click()
#    time.sleep(1)



# Class for deleted message: _akbu _akbw
# for "_amk6 _amlo" >> "_akbu" >> "_ao3e selectable-text copyable-text"

#input_element = driver.find_element(By.ID, "APjFqb")
#input_element.send_keys("Full Clip" + Keys.ENTER)



#link = driver.find_element(By.CLASS_NAME, "cHaqb")
#link.click()

#time.sleep(10)

#driver.quit()
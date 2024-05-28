import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

import time


options = Options()
options.add_argument('-profile')
options.add_argument('C:\\Users\\Omar Arab\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\pfg80jo8.python profile')

driver = webdriver.Firefox(options=options)

driver.get("https://web.whatsapp.com")

try:
    print("Please log into WhatsApp...\n")
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, "side"))) #You have 60 seconds to login
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

time.sleep(20) #Wait ~20 seconds to load conversations
print("Scanning...")

convos = driver.find_elements(By.CLASS_NAME, "_ak8q") #List of conversations
users = {}

# Dict 1 loop:
for convo in convos[1:]:
    if convo not in users:
        users[convo.text] = [0,0,0,0] #initialize values of dict1 and dict2

    driver.execute_script("arguments[0].scrollIntoView();", convo)
    convo.click()

    dict1 = {}
    texts = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
    dels = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw")
    for i in texts: #Add text in first view to the dictionary
        dict1[i] = i.text
    #Scroll up
    for i in range(3):
        driver.find_element(By.TAG_NAME, ('body')).send_keys(Keys.PAGE_UP) #Goes up to top of messages to expand dict2
        texts2 = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
        dels2 = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw")
        for j in texts2:
            if j not in dict1:
                dict1[j] = j.text
        for j in dels2:
            if j not in dels:
                dels.append(j)

    users[convo.text][0] = dict1
    users[convo.text][2] = len(dels)

    if convos.index(convo) == 1:
        searchbar_item = convo.text


# Dict 2 loop and check differences
while True:
    #Go to top of chat list
    searchbar = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div[1]")
    for i in searchbar_item:
        searchbar.send_keys(i)
    for i in searchbar_item:
        searchbar.send_keys(Keys.BACKSPACE)

    for user in users:
        loc = driver.find_element(By.XPATH, "//*[contains(text(),'"+user+"')]")
        driver.execute_script("arguments[0].scrollIntoView();", loc)
        loc.click()

        dict2 = {}
        texts = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
        dels = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw")
        for i in texts: #Add text in first view to the dictionary
            dict2[i] = i.text
        #Scroll up
        for i in range(3):
            driver.find_element(By.TAG_NAME, ('body')).send_keys(Keys.PAGE_UP) #Goes up to top of messages to expand dict2
            texts2 = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjw")
            dels2 = driver.find_elements(By.CSS_SELECTOR, "div._akbu._akbw")
            for j in texts2:
                if j not in dict2:
                    dict2[j] = j.text
            for j in dels2:
                if j not in dels:
                    dels.append(j)
       
        users[user][1] = dict2
        users[user][3] = len(dels)

        #Compare to dict1
        if users[user][0] != users[user][1] and users[user][3] > users[user][2]: #If dict1 and dict2 aren't the same + the number of deleted messages in dict2 is more than dic1:
            for i in users[user][0]:
                if i not in users[user][1]:
                    print("A message has been deleted! By: " + user)
                    print("Deleted message is:")
                    print(users[user][0][i])
    
        users[user][0] = users[user][1]
        users[user][2] = users[user][3]

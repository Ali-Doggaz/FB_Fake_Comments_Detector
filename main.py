import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

def clickOnPosition(webElement):
    #Clicks on the position of an element
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element(webElement)
    action.click()
    action.perform()

def selenium_init():
    # Selenium's driver init
    options = Options()
    options.add_argument("user-data-dir=C:\\Users\\AliDo\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument('--profile-directory=Profile 6')
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.implicitly_wait(3)
    return driver


##Initializes the global variable containing the sellenium webdriver
driver = selenium_init()


def post_scraper(postUrl):
    """
    param : postUrl(String) : contains the Url of the post to scrap
    returns the ID of all the users who commented on a facebook post
    :return:
    Type: Set, Content: profiles' URLs of the users who commented on a particular post
    """
    usersProfileUrl = dict()

    driver.get(postUrl)

    '''Display all the comment'''

    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div/div/span').click()
    allCommentsButton = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/div/div[3]/div[1]')
    clickOnPosition(allCommentsButton)

    #continue clicking on "view more comments" until all of them are displayed
    while(True):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[4]/div/div/div[2]/div[4]/div[1]/div[2]").click()
            print('clicked')
            time.sleep(2) #TODO Replace this with explicit wait
        except NoSuchElementException:
            break

    #get the profile URL of all elements
    comments_ulTag = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[4]/div/div/div[2]/ul')
    all_li = comments_ulTag.find_elements_by_css_selector("li a")
    for li in all_li:
        try:
            raw_url = li.get_attribute('href')
            if not(raw_url.find('?')):
                continue
            url = raw_url[0:raw_url.find('?')]
            if not url.find('post') == -1 or not url.find('profile.php') == -1:
                continue
            if url not in usersProfileUrl:
                usersProfileUrl[url] = 1
            else:
                usersProfileUrl[url] += 1
        except NoSuchElementException:
            print("aie aie aie")
    #class name of "all comments" button: d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db gfeo3gy3 a3bd9o3v ekzkrbhg oo9gr5id hzawbc8m
    return usersProfileUrl


def Fake_Account_Detector(profileUrl):
    """
    params: profileUrl(String) : contains the url of the profile to test
    checks if a facebook account is fake or not.
    Test Criteria:
        *Number of posts
        *Profile picture (exists or not)
        *number of friends

    :return:
    Boolean res: 1 if the account is fake, 0 if the account is legit
    """


if __name__ == '__main__':
    fakeAccountsNumber = 0
    sample_URL = "https://www.facebook.com/RealMadrid/posts/10152418247294953" #TODO CHANGE THIS
    users = post_scraper(sample_URL)
    totalNumberOfAccounts = len(users)

    # Loops over all the accounts, and verifies if they're fake
    #for user in users:
        #isFakeBool = Fake_Account_Detector()
        #if isFakeBool:
            #fakeAccountsNumber += 1
            #print("Fake account detected: " + user)

import time
import random
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def youtube_login(email, password, incognito=False):
    # Browser
    driver_path = r"chromedriver.exe"
    brave_path = r"C:\Users\User\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"

    option = webdriver.ChromeOptions()
    option.binary_location = brave_path

    if incognito:
        option.add_argument("--incognito")

    # Create new Instance of Chrome
    driver = webdriver.Chrome(executable_path=driver_path, options=option)

    driver.get(
        "https://accounts.google.com/ServiceLogin?hl=en&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26feature%3Dsign_in_button%26app%3Ddesktop%26action_handle_signin%3Dtrue%26next%3D%252F&uilel=3&passive=true&service=youtube#identifier")

    # log in
    driver.find_element_by_id("identifierId").send_keys(email)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "identifierNext")))
    driver.find_element_by_id("identifierNext").click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "password")))
    driver.find_element_by_name("password").send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "passwordNext")))
    time.sleep(0.5)
    driver.find_element_by_id("passwordNext").click()

    return driver


def get_page(url):
    # Visit the page
    time.sleep(0.5)
    driver.get(url)
    driver.implicitly_wait(1)

    # Is video avaliable (deleted, private) ?
    if not check_exists_by_xpath(driver, '//*[@id="movie_player"]'):
        return comment_page(driver, url, random_comment())


def comment_page(driver, url, comment):
    # Comments are disabled?
    if check_exists_by_xpath(driver, '//*[@id="comments-disabled-message"]/div/span'):
        return comment_page(driver, url, random_comment())

    # wait for comment box to be clickable and click
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "simplebox-placeholder")))
    driver.find_element_by_id("simplebox-placeholder").click()

    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "submit-button")))
    # Send comment and post
    driver.find_element_by_id("contenteditable-root").send_keys(comment)
    driver.find_element_by_id("submit-button").click()

    # Lets wait a bit
    time.sleep(random.randrange(4, 7))


def get_length():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "player-container")))
    time.sleep(3)

    startTime = str(driver.find_element_by_id("player-container").text).replace(" ", "").split("/")[0]
    time.sleep(5)
    endTime = str(driver.find_element_by_id("player-container").text).replace(" ", "").split("/")[0]

    # if startTime == endTime:
        # start video
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "movie_player")))
        # driver.find_element_by_id("movie_player").click()

    # find length
    time.sleep(1)
    return str(driver.find_element_by_id("player-container").text).replace(" ", "").split("/")[1]


def watch(maxwatch, minwatch):
    length = get_length()

    if maxwatch is None:
        # convert length into seconds
        length = length.split(":")
        maxwatch = int((int(length[0]) * 60) + int(length[1]))

    if minwatch is None:
        minwatch = int(maxwatch / 2)

    # wait until it finished watching
    time.sleep(random.randrange(minwatch, maxwatch))


def random_comment():
    messages = [
        "msg1",
        "msg2"
    ]

    r = random.randrange(0, len(messages))

    return messages[r]


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False

    return True


def close_driver():
    # close the window
    try:
        driver.close()
    except selenium.common.exceptions.InvalidSessionIdException:
        print("Switching to next account")


if __name__ == "__main__":
    print("Please don't run this file directly!")


def start(comment=False, view=True, minwatch=None, maxwatch=None, accountspath=r"targets\accounts.txt", urlspath=r"targets\urls.txt"):
    global driver

    # Credentials
    emails = []
    passwords = []

    print("Loading accounts...")
    # format credentials to get passwords and emails from files
    with open(accountspath) as accounts:
        accounts = accounts.read().split("\n")
        for account in accounts:
            if ":" in account:
                account = account.replace(" ", "")
                account = account.split(":")
                emails.append(account[0])
                passwords.append(account[1])

    # List of Urls
    urlslist = []

    print("Loading urls...")
    # get urls from url file
    with open(urlspath) as urls:
        urls = urls.read().split("\n")
        print(urls)
        for url in urls:
            if "." in url:
                url = url.replace(" ", "")
                urlslist.append(url)

    # check if there's a password for every email
    assert len(emails) == len(passwords), "Amount of emails != amount passwords"

    # iterating trough all accounts
    for i in range(len(emails)):
        # Login youtube
        print("Login", emails[i])
        driver = youtube_login(emails[i], passwords[i])
        try:

            for url in urls:

                # open website and check if video is available
                get_page(url)

                if view:
                    print("Watching", url)
                    # watch the video
                    watch(minwatch, maxwatch)

                if comment:
                    rndcomment = random_comment()
                    print("Commenting", rndcomment)
                    # Random comment
                    comment_page(driver, url, rndcomment)

        except selenium.common.exceptions.TimeoutException:
            print("Timeout. Skipping account")
            close_driver()

        close_driver()

import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM

print('=====================================================================================================')
print('Heyy, you have to login manully on tiktok, so the bot will wait you 1 minute for loging in manually!')
print('=====================================================================================================')
time.sleep(8)
print('Running bot now, get ready and login manually...')
time.sleep(4)


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium_stealth import stealth
import random
import undetected_chromedriver as uc
import time

options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
bot = uc.Chrome(use_subprocess=True, headless=False)



timers = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
]
variables = [
    "https://www.tiktok.com/login/phone-or-email/email", "//input[@placeholder='Email or username']",
    "//input[@placeholder='Password']", """//*[@id="loginContainer"]/div[1]/form/button[@type='submit']"""
]

with open('user.txt') as f:
    line = f.readlines()
username = line[0][10:-1]
password = line[1][10:-1 ] + "!"

start_b = time.time()
stealth(bot,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

def sleeper():
        time.sleep(float("0." + random.choice(timers[0:3]) + random.choice(timers[0:4]) + random.choice(timers[0:9])))

def logging_in():
        bot.get(variables[0])

        try:
                WebDriverWait(bot, 10).until(EC.presence_of_element_located((By.XPATH, variables[1])))
                fieldForm = bot.find_element("xpath", variables[1])
        except:
                bot.quit()
        finally:
                for i in username:
                        fieldForm.send_keys(i)
                        sleeper()

        fieldForm = bot.find_element("xpath", variables[2])
        for i in password:
                fieldForm.send_keys(i)
                sleeper()

        try:
                WebDriverWait(bot, 3).until(EC.presence_of_element_located((By.XPATH, variables[3])))
        except:
                bot.quit()
        finally:
                button = bot.find_element("xpath", variables[3])
                button.click()

logging_in()
end = time.time()
print(f"You has been succesfully logged in to your tik tok account, script executed in {end-start_b}s")
time.sleep(10)
time.sleep(3)


def _set_video(driver, path: str = '', num_retries: int = 3) -> None:
    """
    Sets the video to upload
    Parameters
    ----------
    driver : selenium.webdriver
    path : str
        The path to the video to upload
    num_retries : number of retries (can occassionally fail)
    """
    # uploades the element
    for _ in range(num_retries):
        try:
            upload_box = driver.find_element(
                By.XPATH, "//input[@type='file']"
            )
            upload_box.send_keys(path)
            # waits for the upload progress bar to disappear
            upload_progress = EC.presence_of_element_located(
                (By.XPATH, "//*[.='Cancel']")
                )

            WebDriverWait(driver, 60).until(upload_progress)
            WebDriverWait(driver, 60).until_not(upload_progress)

            # waits for the video to upload
            upload_confirmation = EC.presence_of_element_located(
                (By.XPATH, "//video" )
                )

            # NOTE (IMPORTANT): implicit wait as video should already be uploaded if not failed
            # An exception throw here means the video failed to upload an a retry is needed
            WebDriverWait(driver, 3).until(upload_confirmation)

            # wait until a non-draggable image is found
            process_confirmation = EC.presence_of_element_located(
                (By.XPATH, "//img[@draggable='false']")
                )
            WebDriverWait(driver, 60).until(process_confirmation)
            return
        except Exception as exception:
            print('Upload exception:', exception)

    raise FailedToUpload()

class FailedToUpload(Exception):
    """
    A video failed to upload
    """

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element("xpath", xpath)
    except NoSuchElementException:
        return False

    return True


def upload(video_path):
    while True:
        bot.get("https://www.tiktok.com/upload?lang=en")
        try:
            WebDriverWait(bot, 5).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            bot.switch_to.frame(0)
            bot.implicitly_wait(1)

            root_selector = EC.presence_of_element_located((By.ID, 'root'))
            WebDriverWait(bot,60).until(root_selector)

            _set_video(bot, path=video_path)
        except:
            bot.quit()


        
        try:
            WebDriverWait(bot, 10).until(EC.presence_of_element_located((By.XPATH, variables[1])))
            caption = bot.find_element("xpath", '//*[@id="root"]/div/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div[1]/div/div/div/div/div/div/span')
        except:
                bot.quit()
        finally:
                bot.implicitly_wait(10)
                ActionChains(bot).move_to_element(caption).click( caption).perform()
                with open(r"caption.txt", "r") as f:
                    tags = [line.strip() for line in f]

                for tag in tags:
                    ActionChains(bot).send_keys(tag).perform()
                    time.sleep(2)
                    ActionChains(bot).send_keys(Keys.RETURN).perform()
                    time.sleep(1)
       
        time.sleep(5)
        bot.execute_script("window.scrollTo(150, 300);")
        time.sleep(5)

        post = WebDriverWait(bot, 100).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[2]/div[2]/div[7]/div[2]/button')))

        post.click()
        time.sleep(30)

        if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
            reupload = WebDriverWait(bot, 100).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))

            reupload.click()
        else:
            print('Unknown error cooldown')
            while True:
                time.sleep(600)
                post.click()
                time.sleep(15)
                if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
                    break

        if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
            reupload = WebDriverWait(bot, 100).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))
            reupload.click()

        time.sleep(1)


# ================================================================
# Here is the path of the video that you want to upload in tiktok.
# Plese edit the path because this is different to everyone.
upload(r"F:\Code\tiktokbot\tiktok-autouploader\ciaociao.mp4")
# ================================================================

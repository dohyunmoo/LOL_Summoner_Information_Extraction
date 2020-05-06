from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

PATH = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


def find_region(region):
    regions = {
        "North America": "na",
        "Korea": "www",
        "Japan": "jp",
        "EUW": "euw",
        "EUNE": "eune",
        "Oceania": "oce",
        "Brazil": "br",
        "LAS": "las",
        "LAN": "lan",
        "Russia": "ru",
        "Turkey": "tr"
    }
    return regions.get(region, "Invalid Region")


class Profile(object):
    def __init__(self, ID, region):
        self.ID = ID
        self.region = region

    def open(self):
        a = find_region(self.region)

        if a == "Invalid Region":
            print("Invalid Region, cannot find the corresponding server for " + self.region)
            driver.quit()

        driver.get(r"https://" + a + ".op.gg")  # changing URL based on the region of the player

        time.sleep(5)

        return self

    def search_player(self):
        search = driver.find_element_by_name("userName")
        search.send_keys(self.ID)
        search.send_keys(Keys.RETURN)

        time.sleep(5)

        try:
            driver.find_element(By.CLASS_NAME, "borderImage")  # checking if the profile exists
            return self
        except:
            driver.quit()
            print("The profile does not exist in the given region")

    def extract_info(self):
        update = driver.find_element_by_id("SummonerRefreshButton")  # refresh profile info
        update.click()

        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                           'Timed out waiting for PA creation ' +
                                           'confirmation popup to appear.')

            alert = driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            pass

        time.sleep(3)

        tier = driver.find_element_by_class_name("TierRank")
        tier_string = "Summoner " + self.ID + "'s tier is " + tier.text
        print(tier_string)

        i = 0
        while i < len(tier_string):
            print('_', end='', sep='')
            i += 1
        print("")

        most_played = driver.find_elements_by_class_name("ChampionName")

        print("The top 5 champions " + self.ID + " played this season:")
        j = 0
        while j < 5:
            print(str(j+1) + ". " + most_played[j].text)
            j += 1

        return self

    def close(self):
        print("Finished with " + self.ID + "'s information in " + self.region + " server.")
        print("")
        driver.quit()
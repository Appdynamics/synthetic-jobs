#### This is a sample script I put together in an effort to demo to Choice Hotels - view their website for references to ID's and Xpaths
#### I thought the use of the WebDriverWait library might come in handy to another SE looking to run a script against a React front end (or any componentized JS front end library)
####


from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

driver.get("https://www.choicehotels.com/")
wait = WebDriverWait(driver, 10)

# get a reference to the html tag element, but then wait for it to become stale (which happens when the page refreshes)
# reference:  https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
element = driver.find_element_by_tag_name('html')

try:
	wait.until(EC.staleness_of(element))
except TimeoutException as ex:
    # ignore the exception, we can continue
    pass

# now that the page has been reloaded, we can start executing our test

driver.find_element_by_id("placename").click()
driver.find_element_by_id("placename").clear()
driver.find_element_by_id("placename").send_keys("Detroit")
        
# placename = wait.until(EC.element_to_be_clickable((By.ID, 'placename')))
# placename.click()
# placename.clear()
# placename.send_keys("phoe")

driver.save_screenshot("entered-search-results.png")

searchresult = wait.until(EC.element_to_be_clickable((By.XPATH, "//form[@id='searchForm']/div/div/div/div/div/div/div/ul/li/div")))
searchresult.click()

driver.save_screenshot("selected-search-result.png")

findhotels = wait.until(EC.element_to_be_clickable((By.ID, "Find Hotels")))
driver.save_screenshot("about-to-click-find-hotels.png")
findhotels.click()

checkavailability = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='CheckAvailability_0']/span")))
driver.save_screenshot("about-to-click-check-availability.png")
checkavailability.click()

bookroom = wait.until(EC.element_to_be_clickable((By.ID, "BookRoom_Member_0")))
driver.save_screenshot("about-to-click-book-room.png")
bookroom.click()

firstName = wait.until(EC.element_to_be_clickable((By.ID, "firstName")))
firstName.click()
firstName.clear()
firstName.send_keys("John") 

driver.find_element_by_id("lastName").click()
driver.find_element_by_id("lastName").clear()
driver.find_element_by_id("lastName").send_keys("Smith")
driver.save_screenshot("populated-name-fields.png")

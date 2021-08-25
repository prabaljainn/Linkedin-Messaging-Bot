import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from scripts import constants
import csv

opening_csv= open("CSV File/donelist.csv",mode= 'a',newline='')
csv_append  = csv.writer(opening_csv)




def page_messeger(link,driver,page,keyword):
    list_of_applied_profiles=[]
    open_csv = open("CSV File/donelist.csv", mode='r', newline='')
    csv_open = csv.reader(open_csv)
    for elem in list(csv_open):
        list_of_applied_profiles.append(elem[3])
    print(list_of_applied_profiles)
    driver.get(link)
    list_of_cards = driver.find_elements_by_css_selector("li[class= 'reusable-search__result-container ']")
    print(f"a total of {len(list_of_cards)} Connections found on page {page} for {keyword} ")
    for i in range(1, len(list_of_cards)+1):
        try:
            name_container_with_link = driver.find_element_by_css_selector(
                f"li[class= 'reusable-search__result-container ']:nth-child({i}) span a span span")
            button_on_card2 = driver.find_element_by_css_selector(
                f"li[class= 'reusable-search__result-container ']:nth-child({i}) button span")
            if button_on_card2.text == "Message":
                name_container_with_link.click()
                time.sleep(1)
                name_grab = driver.find_element_by_tag_name("h1").text
                description1 = driver.find_element_by_css_selector(
                    "div[class= 'text-body-medium break-words']").text
                description2 = driver.find_element_by_css_selector(
                    "span[class = 'text-body-small inline t-black--light break-words']").text
                link_to_profile = str(driver.current_url)
                if link_to_profile in list_of_applied_profiles:
                    pass
                else:
                    list_of_applied_profiles.append(link_to_profile)
                    info_insert = [name_grab, description1, description2, link_to_profile]
                    csv_append.writerow(info_insert)
                    messege_button = driver.find_element_by_css_selector(
                        "a[class = 'message-anywhere-button pvs-profile-actions__action artdeco-button ']")
                    name_of_target = driver.find_element_by_css_selector(
                        "h1[class = 'text-heading-xlarge inline t-24 v-align-middle break-words']").text
                    first_name_of_target = name_of_target.split()[0]
                    if constants.with_name:
                        mess = "Hi " + first_name_of_target + ",\n" + constants.mess_to_send
                    else:
                        mess = constants.mess_to_send
                    messege_button.click()
                    driver.find_element_by_css_selector("div[aria-multiline='true']").send_keys(mess)
                    print(f"{mess} sent to {name_grab}")
                    # driver.find_element_by_css_selector(
                    #     "button[class='msg-form__send-button artdeco-button artdeco-button--1']").click()
                driver.get(link)
        except NoSuchElementException:
            pass
        except Exception as e:
            print(e)
            pass





def message_function():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options, executable_path="chromedriver/chromedriver.exe")
    driver.implicitly_wait(10)
    # opening website
    driver.get("https://www.linkedin.com/login")
    # filling username and pass with const and pressing login

    driver.find_element_by_css_selector("input[id= 'username']").send_keys(constants.username)
    driver.find_element_by_css_selector("input[id= 'password']").send_keys(constants.password)
    driver.find_element_by_css_selector("button[type= 'submit']").click()
    for keyword in constants.commaseparated.split(";"):
        link = "https://www.linkedin.com/search/results/people/?keywords=" + keyword + "&network=%5B%22F%22%5D"
        driver.get(link)
        pages= driver.find_elements_by_css_selector("li.artdeco-pagination__indicator")
        len_pages = len(pages)
        for page in range(0, len_pages + 1):
            link_to_page = "https://www.linkedin.com/search/results/people/?keywords=" + keyword + "&network=%5B%22F%22%5D&page=" + str(page)
            page_messeger(link_to_page, driver, page, keyword)

if __name__=="__main__":
    message_function()



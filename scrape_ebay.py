import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
import time


def ebay(product, driver):
    try:
        action = ActionChains(driver)

        def return_concatenate(lista):
            list_formated = []
            list_formated2 = []
            list_formated3 = []
            for i in range(len(lista)):
                if i % 2 == 0:
                    list_formated.append(lista[i])
                else:
                    list_formated2.append(lista[i])
            for i in range(int(len(lista) / 2)):
                list_formated3.append(list_formated[i] + ' ' + list_formated2[i])
            return list_formated3

        time.sleep(3)
        driver.get(product.url)
        product.sku = driver.find_element_by_css_selector("#descItemNumber").text
        product.name = driver.find_element_by_id("itemTitle").text
        product.main_image = driver.find_element_by_id("icImg").get_attribute("src").split('/s')[0] + "/s-l800.jpg"
        product.append_variant(True, "parent")

        description = driver.find_element_by_css_selector("#viTabs_0_is")
        source_code = description.get_attribute("outerHTML")
        product.description = source_code

        try:
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='gdpr-banner-accept']"))).click()
            except TimeoutException or ElementNotInteractableException:
                pass
        except ElementClickInterceptedException:
            driver.execute_script("window.scrollTo(0, 0)")

        def catch_content():
            bullet_points = description.find_elements_by_tag_name("td")
            try:
                images = driver.find_element_by_css_selector("#vi_main_img_fs").find_elements_by_tag_name("img")
                for img in images:
                    product.append_variant((img.get_attribute("src").split('/s')[0] + "/s-l800.jpg"), "other_main")
            except NoSuchElementException:
                for i in range(5):
                    product.append_variant("", "other_main")
            bp_list = []
            for bp in bullet_points:
                bp_list.append(bp.text)
            bp_list_formated = return_concatenate(bp_list)
            for i in range(len(bp_list_formated)):
                product.append_variant(f"{bp_list_formated[i]}", "bullet")  # bullet points
            try:
                names = driver.find_element_by_css_selector("#test12").find_elements_by_tag_name("option")
                for n in range(1, len(names)):
                    product.append_variant(names[n].text, "variant_names")
                for n in range(1, len(names)):
                    driver.find_element_by_css_selector("#test12").click()
                    names[n].click()
                    action.move_by_offset(250, 50).click()
                    product.append_variant(driver.find_element_by_xpath("//*[@id='icImg']").get_attribute("src").split('/s')[0] + "/s-l800.jpg", "variant_images")
                    price = driver.find_element_by_xpath("//span[@itemprop='price']").text
                    product.append_variant(re.search(r'[0-9]\w*\.[0-9][0-9]', price).group(0), "price")
                    shipping = driver.find_element_by_css_selector("#fshippingCost").text
                    product.append_variant(re.search(r'[0-9]\w*\.[0-9][0-9]', shipping).group(0), "shipping")
                    driver.get(product.url)
                    names = driver.find_element_by_css_selector("#test12").find_elements_by_tag_name("option")
            except NoSuchElementException:
                product.append_variant(" ", "variant_names")
                price = driver.find_element_by_xpath("//span[@itemprop='price']").text
                product.append_variant(re.search(r'[0-9]\w*(\.||,)[0-9][0-9]', price).group(0), "price")
                try:
                    shipping = driver.find_element_by_css_selector("#fshippingCost").text
                    product.append_variant(re.search(r'[0-9]\w*(\.||,)[0-9][0-9]', shipping).group(0), "shipping")
                except NoSuchElementException:
                    product.append_variant(0, "shipping")
                product.append_variant(" ", "variant_images")

            driver.execute_script("window.scrollTo(0, 1080)")

        try:
            catch_content()
        except ElementClickInterceptedException:
            driver.find_element_by_xpath("//*[@id='gdpr-banner-accept']").click()
            catch_content()

        return product
    except:
        raise Exception("Unexpected Error x03")

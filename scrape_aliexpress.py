from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
import time


def aliexpress(product, driver):
    try:
        def catch_contents():
            action = ActionChains(driver)
            driver.get(product.url)
            time.sleep(4)

            # close aliexpress coupon pop-up
            for i in range(3):
                try:
                    action.move_by_offset(100, 90).click().perform()
                except MoveTargetOutOfBoundsException:
                    pass

            try:
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@src, '__poplayer')]")))
                time.sleep(3)
                for i in driver.find_elements_by_xpath("//img[contains(@src, 'http')]"):
                    i.click()
                driver.switch_to.default_content()
            except TimeoutException:
                pass

            # change country to india and currençy to usd
            if product.alp != 0:
                try:
                    if product.url != driver.current_url:
                        driver.execute_script(f"window.history.back()")
                        time.sleep(5)
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'switcher-info')]/span[@class='ship-to']/i"))).click()
                    time.sleep(2)
                    driver.find_element_by_class_name("switcher-common").find_elements_by_tag_name("a")[0].click()
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, "//li[@class='address-select-item ']//span[@class='shipping-text' and text()='India']"))).click()
                    time.sleep(3)
                    try:
                        WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nav-global']/div[3]/div/div/div/div[3]/div/span"))).click()
                    except TimeoutException:
                        WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/div/div/div/div[3]/div/span"))).click()
                    driver.find_elements_by_xpath("//div[@class='search-container']//input[@class='search-currency']")[1].send_keys(
                        "usd")
                    driver.find_element_by_xpath("//a[@data-currency='USD']").click()
                    driver.find_element_by_class_name("switcher-common").find_elements_by_tag_name("button")[0].click()
                    product.alp = 0
                except ElementNotInteractableException:
                    pass
            else:
                pass

            try:
                product.main_image = driver.find_element_by_xpath("//img[@class='magnifier-image']").get_attribute("src").replace("_Q90.jpg_.webp", "")
            except NoSuchElementException:
                product.main_image = ""

            try:
                product.sku = driver.find_element_by_xpath("//meta[@itemprop='url']").get_attribute("content").split('/')[-1][::-1][5:][::-1]
            except NoSuchElementException:
                product.sku = ""

            try:
                product.name = driver.find_element_by_xpath("//h1[@class='product-title-text']").text
            except NoSuchElementException:
                product.name = ""

            # catch description and bullet points
            time.sleep(3)
            driver.execute_script(f"window.scrollTo(0, 1200)")
            time.sleep(1)
            driver.execute_script(f"window.scrollTo(0, 1400)")
            time.sleep(6)
            driver.execute_script(f"window.scrollTo(0, 1250)")
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//body/div[@id='root']/div[1]/div[3]/div[3]/div[2]/div[2]/div[1]/div[1]/ul[1]/li[3]/div[1]"))).click()
            except:
                try:
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/div[3]/div[2]/div/div[2]/div/ul/li[3]/div"))).click()
                except:
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                        (By.XPATH, "//*[@id='product-detail']/div[2]/div/div[1]/ul/li[3]/div"))).click()
            description = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='product-specs']")))
            product.description = description.get_attribute("outerHTML")
            time.sleep(2)

            bullet_points = description.find_elements_by_tag_name("li")
            bp_list = []
            for x in bullet_points:
                bp_list.append(x.text)
            time.sleep(1)
            for x in bp_list:
                product.append_variant(x, "bullet")
            time.sleep(1)

            driver.execute_script(f"window.scrollTo(0, 350)")
            variant_main_list = driver.find_element_by_xpath("//ul[@class='images-view-list']").find_elements_by_tag_name("img")
            for x in variant_main_list:
                product.append_variant((x.get_attribute("src").replace("_50x50.jpg_.webp", "")), "other_main")
            try:
                list_itens = driver.find_elements_by_xpath("//*[@id='root']/div/div[2]/div/div[2]/div[7]/div/div/ul/li")
                for x in range(len(list_itens)):
                    try:
                        list_itens[x].click()
                        name = driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div/div[2]/div[7]/div/div/div/span").text
                        product.append_variant(name, "variant_names")
                        element_url = driver.find_element_by_xpath("//img[@class='magnifier-image']").get_attribute("src")
                        try:
                            price = driver.find_element_by_xpath("//div[@class='product-price-current']").text
                            product.append_variant((price.split(' ')[1][1:]), "price")
                        except NoSuchElementException:
                            product.append_variant(0, "price")
                        try:
                            shipping = driver.find_element_by_css_selector("body.glo-detail-page:nth-child(2) div.glodetail-wrap div.product-main div.product-main-wrap div.product-info:nth-child(2) div.product-shipping:nth-child(13) > div.product-shipping-price:nth-child(1)").text
                            product.append_variant((shipping.split(' ')[2][1:]), "shipping")
                        except NoSuchElementException:
                            product.append_variant(0, "shipping")
                        product.append_variant((element_url.replace("_640x640.jpg", "").replace("_640x640.png", "")), "variant_images")
                        if x == 13:
                            driver.execute_script(f"window.scrollTo(0, 500)")
                        time.sleep(0.3)
                    except ElementClickInterceptedException or ElementNotInteractableException:
                        pass
            except NoSuchElementException:
                element_url = driver.find_element_by_xpath("//img[@class='magnifier-image']").get_attribute("src")
                try:
                    price = driver.find_element_by_xpath("//div[@class='product-price-current']").text
                    product.append_variant((price.split(' ')[1][1:]), "price")
                except NoSuchElementException:
                    pass
                try:
                    shipping = driver.find_element_by_css_selector(
                        "body.glo-detail-page:nth-child(2) div.glodetail-wrap div.product-main div.product-main-wrap div.product-info:nth-child(2) div.product-shipping:nth-child(13) > div.product-shipping-price:nth-child(1)").text
                    product.append_variant((shipping.split(' ')[2][1:]), "shipping")
                except NoSuchElementException:
                    product.append_variant(0, "shipping")
                product.append_variant((element_url.replace("_640x640.jpg", "").replace("_640x640.png", "")),
                                       "variant_images")
                time.sleep(0.3)

        try:
            catch_contents()
        except ElementClickInterceptedException or ElementNotInteractableException:
            driver.execute_script(f"window.scrollTo(0, 1080)")
            if product.url != driver.current_url:
                driver.execute_script(f"window.history.back()")
            catch_contents()

        return product
    except:
        raise Exception("Unexpected Error x03")

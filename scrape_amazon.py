from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
import re
import time


def amazon(product, driver):
    action = ActionChains(driver)
    driver.get(product.url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nav-global-location-slot']/span/a"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='GLUXCountryValue']"))).click()
    time.sleep(5)
    regions = driver.find_elements_by_xpath("//*[@id='a-popover-5']/div/div/ul/li")
    for i in regions:
        if "India" in i.text:
            i.click()
            break
        else:
            pass
    try:
        action.move_by_offset(250, 50).click().perform()
    except MoveTargetOutOfBoundsException:
        pass
    time.sleep(3)
    product.sku = re.search(r'/dp/([A-Z][0-9])\w+', product.url).group(0)[4:]
    try:
        product.name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[5]/div[5]/div[4]/div[1]/div"))).text
    except TimeoutException:
        product.name = "not found"
    time.sleep(1)
    try:
        product.main_image = driver.find_element_by_css_selector("#landingImage").get_attribute("src").split("_AC_")[0] + "_AC_SX650_.jpg"
    except NoSuchElementException:
        product.main_image = "not found"
    driver.execute_script("window.scrollTo(0, 1080)")
    time.sleep(1)
    try:
        description = driver.find_element_by_css_selector("#productDescription_feature_div")
    except NoSuchElementException:
        try:
            description = driver.find_element_by_xpath("//*[@id='aplus']/div")
        except NoSuchElementException:
            description = "not found"
    driver.execute_script("window.scrollTo(0, 0)")

    # catch a list of bullet points as selenium element
    try:
        bullet_points = driver.find_element_by_css_selector("#feature-bullets").find_elements_by_tag_name("li")
        if not bullet_points:
            for i in range(6):
                product.append_variant(" ", "bullet")
        else:
            for bp in bullet_points:
                product.append_variant(bp.text, "bullet")
    except:
        for i in range(6):
            product.append_variant("not found", "bullet")

    # catch the description in html
    try:
        source_code = description.get_attribute("outerHTML")
    except AttributeError:
        source_code = description
    product.description = source_code

    # base url to get variant itens
    products = driver.find_elements_by_class_name("swatchAvailable")
    base = product.url.split('/dp/')[0]
    url_variants = []
    product.append_variant(product.sku, "variant_asin")
    for p in products:
        url_variants.append(str(base) + p.get_attribute("data-dp-url"))
        product.append_variant(p.get_attribute("data-dp-url").split("/ref")[0].split("/dp/")[1], "variant_asin")

    try:
        price = driver.find_element_by_css_selector("#price").text
        product.append_variant(re.search(r"[0-9]\w*.[0-9]\w*", price).group(0).replace(',', '.'), "price")
    except:
        price = 0
        product.append_variant(price, "price")
    try:
        shipping = driver.find_element_by_css_selector("#exports_desktop_qualifiedBuybox_tlc_feature_div").text
        product.append_variant(re.search(r"[0-9]\w*.[0-9]\w*", shipping).group(0).replace(',', '.'), "shipping")
    except:
        shipping = 0
        product.append_variant(shipping, "shipping")
    try:
        product.append_variant(
            driver.find_element_by_xpath("//*[@id='variation_color_name']/div").text.replace("Color:", ""), "variant_names")
    except:
        pass
    try:
        product.append_variant(
            driver.find_element_by_xpath("//*[@id='variation_color_name']/ul").find_elements_by_tag_name("img")[
                0].get_attribute("src").split("_SS36_")[0] + "_AC_SX650_.jpg", "variant_images")
    except:
        pass
    for u in range(len(url_variants)):
        driver.get(url_variants[u])

        try:
            price = driver.find_element_by_css_selector("#price_inside_buybox").text
            product.append_variant(re.search(r"[0-9]\w*.[0-9]\w*", price).group(0).replace(',', '.'), "price")
        except NoSuchElementException:
            product.append_variant(0, "price")
        try:
            # search and format the shipping price
            shipping = driver.find_element_by_css_selector("#exports_desktop_qualifiedBuybox_tlc_feature_div").text
            product.append_variant(re.search(r"[0-9]\w*.[0-9]\w*", shipping).group(0).replace(',', '.'), "shipping")
        except NoSuchElementException:
            # if dont find shipping price (in case of free shipping or don't ship) shipping value will be 0
            product.append_variant(0, "shipping")
        time.sleep(5)

        driver.execute_script("window.scrollTo(0, 540)")
        time.sleep(3)
        images_preview = driver.find_elements_by_class_name("a-spacing-small item imageThumbnail a-declarative")
        product.append_variant(driver.find_element_by_xpath("//*[@id='variation_color_name']/div").text.replace("Color:", ""), "variant_names")
        for i in range(len(images_preview)):
            action.move_to_element(images_preview[i]).perform()
    try:
        images = driver.find_elements_by_xpath("/html/body/div[2]/div[2]/div[5]/div[5]/div[3]/div/div[1]/div/div/div[1]/ul/li")
    except NoSuchElementException:
        images = driver.find_elements_by_xpath("//*[@id='altImages']/ul/li")
    if not images:
        for i in range(5):
            product.append_variant(" ", "other_main")
    else:
        for i in range(len(images)):
            try:
                img = driver.find_element_by_xpath(f"/html/body/div[2]/div[2]/div[5]/div[5]/div[3]/div/div[1]/div/div/div[1]/ul/li[{i + 1}]/span/span/span/span/img").get_attribute("src")
                if img == "https://images-na.ssl-images-amazon.com/images/G/30/HomeCustomProduct/360_icon_73x73v2._CB485971309_SS40_FMpng_RI_.png":
                    pass
                else:
                    product.append_variant(img.split("_AC_")[0] + "_AC_SX650_.jpg", "other_main")
            except NoSuchElementException:
                pass

    if not products:
        for i in range(5):
            product.append_variant(" ", "variant_images")
    else:
        for i in range(len(products)):
            try:
                product.append_variant(driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[5]/div[5]/div[4]/div[27]/div[1]/div/form/div/ul").find_elements_by_tag_name("img")[i + 1].get_attribute("src").split("_SS36_")[0] + "_AC_SX650_.jpg", "variant_images")
            except NoSuchElementException:
                product.append_variant(driver.find_element_by_xpath("//*[@id='variation_color_name']/ul").find_elements_by_tag_name("img")[i + 1].get_attribute("src").split("_SS36_")[0] + "_AC_SX650_.jpg", "variant_images")
    product.amz = True
    return product

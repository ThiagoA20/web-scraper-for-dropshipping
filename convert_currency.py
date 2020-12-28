

def to_inr(product, driver):
    try:
        if product.store == 2:
            product.currency = "usd"
        driver.get(f"https://transferwise.com/gb/currency-converter/{product.currency}-to-inr-rate")
        shipping_converted = []
        price_converted = []
        standard_price = []
        for i in range(len(product.shipping)):
            driver.find_element_by_css_selector("#cc-amount-from").clear()
            driver.find_element_by_css_selector("#cc-amount-from").send_keys(str(product.shipping[i]).replace(",", "."))
            shipping_converted.append(driver.find_element_by_css_selector("#cc-amount-to").get_attribute('value'))
            driver.find_element_by_css_selector("#cc-amount-from").clear()
            driver.find_element_by_css_selector("#cc-amount-from").send_keys(str(product.price[i]).replace(",", "."))
            price_converted.append(driver.find_element_by_css_selector("#cc-amount-to").get_attribute('value'))
        for i in range(len(shipping_converted)):
            standard_price.append(round((float(price_converted[i]) + float(shipping_converted[i])) * 2, 0))
        return standard_price
    except:
        return "Unexpected Error x01"


def to_cad(product, driver):
    try:
        if product.store == 2:
            product.currency = "usd"
        driver.get(f"https://transferwise.com/gb/currency-converter/{product.currency}-to-cad-rate")
        shipping_converted = []
        price_converted = []
        standard_price = []
        for i in range(len(product.shipping)):
            driver.find_element_by_css_selector("#cc-amount-from").clear()
            driver.find_element_by_css_selector("#cc-amount-from").send_keys(str(product.shipping[i]).replace(",", "."))
            shipping_converted.append(driver.find_element_by_css_selector("#cc-amount-to").get_attribute('value'))
            driver.find_element_by_css_selector("#cc-amount-from").clear()
            driver.find_element_by_css_selector("#cc-amount-from").send_keys(str(product.price[i]).replace(",", "."))
            price_converted.append(driver.find_element_by_css_selector("#cc-amount-to").get_attribute('value'))
        for i in range(len(shipping_converted)):
            standard_price.append(round((float(price_converted[i]) + float(shipping_converted[i])) * 2, 2))
        return standard_price
    except:
        return "Unexpected Error x01"


def to_mxn(product, driver):
    try:
        if product.store == 2:
            product.currency = "usd"
        driver.get(f"https://transferwise.com/gb/currency-converter/{product.currency}-to-mxn-rate")
        shipping_converted = []
        price_converted = []
        standard_price = []
        for i in range(len(product.shipping)):
            driver.find_element_by_css_selector("#cc-amount-from").clear()
            driver.find_element_by_css_selector("#cc-amount-from").send_keys(str(product.shipping[i]).replace(",", "."))
            shipping_converted.append(driver.find_element_by_css_selector("#cc-amount-to").get_attribute('value'))
            driver.find_element_by_css_selector("#cc-amount-from").clear()
            driver.find_element_by_css_selector("#cc-amount-from").send_keys(str(product.price[i]).replace(",", "."))
            price_converted.append(driver.find_element_by_css_selector("#cc-amount-to").get_attribute('value'))
        for i in range(len(shipping_converted)):
            standard_price.append(round((float(price_converted[i]) + float(shipping_converted[i])) * 2, 2))
        return standard_price
    except:
        return "Unexpected Error x01"


def to_aed(product, driver):
    try:
        if product.store == 2:
            product.currency = "usd"
        driver.get(f"https://transferwise.com/gb/currency-converter/{product.currency}-to-aed-rate")
        shipping_converted = []
        price_converted = []
        standard_price = []
        for i in range(len(product.shipping)):
            driver.find_element_by_css_selector("#cc-amount-from").clear()
            driver.find_element_by_css_selector("#cc-amount-from").send_keys(str(product.shipping[i]).replace(",", "."))
            shipping_converted.append(driver.find_element_by_css_selector("#cc-amount-to").get_attribute('value'))
            driver.find_element_by_css_selector("#cc-amount-from").clear()
            driver.find_element_by_css_selector("#cc-amount-from").send_keys(str(product.price[i]).replace(",", "."))
            price_converted.append(driver.find_element_by_css_selector("#cc-amount-to").get_attribute('value'))
        for i in range(len(shipping_converted)):
            standard_price.append((float(price_converted[i]) + float(shipping_converted[i])) * 2)
        return standard_price
    except:
        return "Unexpected Error x01"

from proxies_randomizer import page_content
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar, OptionMenu, ttk, HORIZONTAL
from scrape_aliexpress import aliexpress
from scrape_amazon import amazon
from scrape_ebay import ebay
from write_spreadsheet import spreadsheet, close, append_spreadsheet
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from threading import Thread
from os import remove, getcwd
from sys import exit, exc_info
import time

window = Tk()
window.title("Products Dataframe")

driver = ""


class Product:

    def __init__(self):
        self.page_url = ""
        self.url = ""
        self.sku = ""
        self.brand = ""
        self.name = ""
        self.description = ""
        self.bullet_points = []
        self.main_image = ""
        self.other_main_images = []
        self.parent = []
        self.variant_images = []
        self.price = []
        self.shipping = []
        self.variant_names = []
        self.currency = "usd"
        self.asin = []
        self.store = 0
        self.alp = 1

    def append_variant(self, item, num):
        if num == "bullet":
            self.bullet_points.append(item)
        elif num == "other_main":
            self.other_main_images.append(item)
        elif num == "variant_images":
            self.variant_images.append(item)
        elif num == "price":
            self.price.append(item)
        elif num == "shipping":
            self.shipping.append(item)
        elif num == "variant_names":
            self.variant_names.append(item)
        elif num == "variant_asin":
            self.asin.append(item)
        else:
            pass


title = spreadsheet()
list_titles = [title]
extraction = 0
running = True


def extract():
    global running
    running = True
    global extraction
    global driver
    driver = page_content()
    global title
    list_titles.append(title)
    product = Product()
    product.currency = clicked.get().lower()
    page_max = clicked2.get()
    product.brand = input_brand.get()
    url = str(input_url.get())
    if not url.startswith("http"):
        errotxt['text'] = "Error, please enter a valid url (starting with http)"
        errotxt['bg'] = "red"
    elif clicked.get() == "":
        errotxt['text'] = "Select a currency to convert from"
        errotxt['bg'] = 'red'
    else:
        if "aliexpress." in url:
            Thread(target=update_gui).start()
            product.store = 1
            errotxt['text'] = ""
            errotxt['bg'] = "dark blue"

            def extract_aliexpress():
                global running
                if "/store/" in url:
                    process['text'] = "Extracting urls..."
                    process['bg'] = "dark gray"
                    product.page_url = url
                    pages_url = []
                    driver.get(product.page_url)
                    time.sleep(3)
                    if "/store/group/" in url:
                        if "login.aliexpress" in driver.current_url:
                            running = False
                            process['text'] = ""
                            process['bg'] = "dark blue"
                            errotxt['text'] = f"Aliexpress does not allow scrape this pages"
                            errotxt['bg'] = 'red'
                            driver.quit()
                            return
                        products = driver.find_element_by_css_selector("#node-gallery").find_elements_by_class_name(
                            "img")
                        for s in products:
                            pages_url.append(s.find_element_by_tag_name("a").get_attribute("href"))

                    else:
                        products = driver.find_elements_by_xpath(
                            "/html/body/div[4]/div/div/div[3]/div[13]/div/div/div[2]/div[2]/div")
                        for r in range(len(products)):
                            t = products[r].find_elements_by_tag_name("a")[0].get_attribute("data-href")
                            pages_url.append(f"https://{t[2:]}")

                    def page_aliexpress(lk):
                        product.url = lk
                        product_object1 = aliexpress(product, driver)
                        process['text'] = "Converting prices..."
                        append_spreadsheet(product_object1, driver, title)
                        product.url = ""
                        product.sku = ""
                        product.name = ""
                        product.description = ""
                        product.bullet_points = []
                        product.main_image = ""
                        product.other_main_images = []
                        product.parent = []
                        product.variant_images = []
                        product.price = []
                        product.shipping = []
                        product.variant_names = []

                    for i in range(len(pages_url)):
                        if page_max == "all":
                            process['text'] = f"Extracting data... {i + 1}/{len(pages_url)}"
                            process['bg'] = "dark gray"
                            product.alp = 0
                            try:
                                page_aliexpress(pages_url[i])
                            except:
                                running = False
                                process['text'] = ""
                                process['bg'] = "dark blue"
                                errotxt['text'] = f"error, try again or contact the support"
                                errotxt['bg'] = 'red'
                                driver.quit()
                                return
                        else:
                            process['text'] = f"Extracting data... {i + 1}/{int(page_max)}"
                            process['bg'] = "dark gray"
                            try:
                                page_aliexpress(pages_url[i])
                                product.alp = 0
                                if int(page_max) == i + 1:
                                    break
                            except:
                                running = False
                                process['text'] = ""
                                process['bg'] = "dark blue"
                                errotxt['text'] = f"error, try again or contact the support"
                                errotxt['bg'] = 'red'
                                driver.quit()
                                return

                else:
                    product.url = url
                    process['text'] = "Extracting data..."
                    process['bg'] = "dark gray"
                    try:
                        product_object = aliexpress(product, driver)
                        process['text'] = "Converting prices..."
                    except:
                        running = False
                        process['text'] = ""
                        process['bg'] = "dark blue"
                        errotxt['text'] = f"error, try again or contact the support"
                        errotxt['bg'] = 'red'
                        driver.quit()
                        return
                    try:
                        append_spreadsheet(product_object, driver, title)
                    except:
                        running = False
                        process['text'] = ""
                        process['bg'] = "dark blue"
                        errotxt['text'] = f"error, try again or contact the support"
                        errotxt['bg'] = 'red'
                        driver.quit()
                        return
                running = False
                process['text'] = ""
                process['bg'] = "dark blue"
                errotxt['text'] = "Data extracted successfully!"
                errotxt['bg'] = 'light green'
                driver.quit()

            try:
                Thread(target=extract_aliexpress).start()
            except:
                running = False
                process['text'] = ""
                process['bg'] = "dark blue"
                errotxt['text'] = f"error, try again or contact the support"
                errotxt['bg'] = 'red'
                driver.quit()
                return
        elif "ebay.c" in url:
            Thread(target=update_gui).start()
            product.store = 2
            errotxt['text'] = ""
            errotxt['bg'] = "dark blue"

            def extract_ebay():
                global running
                driver.get(url)
                if "/usr/" in url:
                    process['text'] = "Extracting urls..."
                    process['bg'] = "dark gray"
                    driver.find_element_by_xpath("/html/body/div[2]/div[6]/div[1]/div/a").click()
                    time.sleep(3)
                if "/sch/" in driver.current_url:
                    process['text'] = "Extracting urls..."
                    process['bg'] = "dark gray"
                    product.page_url = url
                    pages_url = []
                    urls = driver.find_elements_by_xpath(
                        "/html/body/div[5]/div[2]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[1]/div/w-root/div/div[2]/ul/li")
                    for i in range(len(urls)):
                        pages_url.append(driver.find_element_by_xpath(
                            f"/html/body/div[5]/div[2]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[1]/div/w-root/div/div[2]/ul/li[{i + 1}]/h3/a").get_attribute(
                            "href"))

                    def page_ebay(lk):
                        product.url = lk
                        product_object2 = ebay(product, driver)
                        process['text'] = "Converting prices..."
                        append_spreadsheet(product_object2, driver, title)
                        product.url = ""
                        product.sku = ""
                        product.name = ""
                        product.description = ""
                        product.bullet_points = []
                        product.main_image = ""
                        product.other_main_images = []
                        product.parent = []
                        product.variant_images = []
                        product.price = []
                        product.shipping = []
                        product.variant_names = []
                        product.currency = "usd"

                    for i in range(len(pages_url)):
                        if page_max == "all":
                            process['text'] = f"Extracting data... {i + 1}/{len(pages_url)}"
                            process['bg'] = "dark gray"
                            try:
                                page_ebay(pages_url[i])
                            except:
                                running = False
                                process['text'] = ""
                                process['bg'] = "dark blue"
                                errotxt['text'] = f"error, try again or contact the support"
                                errotxt['bg'] = 'red'
                                driver.quit()
                                return
                        else:
                            process['text'] = f"Extracting data... {i + 1}/{int(page_max)}"
                            process['bg'] = "dark gray"
                            try:
                                page_ebay(pages_url[i])
                                if int(page_max) == i + 1:
                                    break
                            except:
                                running = False
                                process['text'] = ""
                                process['bg'] = "dark blue"
                                errotxt['text'] = f"error, try again or contact the support"
                                errotxt['bg'] = 'red'
                                driver.quit()
                                return

                else:
                    product.url = url
                    process['text'] = "Extracting data..."
                    process['bg'] = "dark gray"
                    try:
                        product_object = ebay(product, driver)
                        process['text'] = "Converting prices..."
                    except:
                        running = False
                        process['text'] = ""
                        process['bg'] = "dark blue"
                        errotxt['text'] = f"error, try again or contact the support"
                        errotxt['bg'] = 'red'
                        driver.quit()
                        return
                    try:
                        append_spreadsheet(product_object, driver, title)
                    except:
                        running = False
                        process['text'] = ""
                        process['bg'] = "dark blue"
                        errotxt['text'] = f"error, try again or contact the support"
                        errotxt['bg'] = 'red'
                        driver.quit()
                        return
                running = False
                process['text'] = ""
                process['bg'] = "dark blue"
                errotxt['text'] = "Data extracted successfully!"
                errotxt['bg'] = 'light green'
                driver.quit()

            try:
                Thread(target=extract_ebay).start()
            except:
                running = False
                process['text'] = ""
                process['bg'] = "dark blue"
                errotxt['text'] = f"error, try again or contact the support"
                errotxt['bg'] = 'red'
                driver.quit()
                return
        elif "amazon" in url:
            Thread(target=update_gui).start()
            product.store = 3
            errotxt['text'] = ""
            errotxt['bg'] = "dark blue"

            def extract_amazon():
                global running
                if "/stores/" in url or "/s?k" in url:
                    process['text'] = "Extracting urls..."
                    process['bg'] = "dark gray"
                    product.page_url = url
                    pages_url = []
                    driver.get(product.page_url)
                    driver.execute_script("window.scrollTo(0, 1000)")
                    if "/stores/" in url:
                        urls = WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located(
                            (By.XPATH, "/html/body/div[1]/div[2]/div/div[5]/div/div/div/div/div/ul/li")))
                        for i in range(len(urls)):
                            pages_url.append(driver.find_element_by_xpath(
                                f'/html/body/div[1]/div[2]/div/div[5]/div/div/div/div/div/ul/li[{i + 1}]/div[1]/a').get_attribute(
                                'href'))
                    elif "/s?k" in url:
                        urls = WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located(
                            (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/span[3]/div[2]/div")))
                        for i in range(len(urls)):
                            try:
                                pages_url.append(driver.find_element_by_xpath(
                                    f'/html/body/div[1]/div[2]/div[1]/div[2]/div/span[3]/div[2]/div[{i + 1}]/div/span/div/div/div[2]/h2/a').get_attribute(
                                    'href'))
                            except:
                                pass

                    def page_amazon(lk):
                        product.url = lk
                        product_object3 = amazon(product, driver)
                        process['text'] = "Converting prices..."
                        append_spreadsheet(product_object3, driver, title)
                        product.url = ""
                        product.sku = ""
                        product.name = ""
                        product.description = ""
                        product.bullet_points = []
                        product.main_image = ""
                        product.other_main_images = []
                        product.parent = []
                        product.variant_images = []
                        product.price = []
                        product.shipping = []
                        product.variant_names = []
                        product.asin = []

                    for i in range(len(pages_url)):
                        if page_max == "all":
                            process['text'] = f"Extracting data... {i + 1}/{len(pages_url)}"
                            process['bg'] = "dark gray"
                            try:
                                page_amazon(pages_url[i])
                            except:
                                running = False
                                process['text'] = ""
                                process['bg'] = "dark blue"
                                errotxt['text'] = f"error, try again or contact the support"
                                errotxt['bg'] = 'red'
                                driver.quit()
                                return

                        else:
                            process['text'] = f"Extracting data... {i + 1}/{int(page_max)}"
                            process['bg'] = "dark gray"
                            try:
                                page_amazon(pages_url[i])
                                if int(page_max) == i + 1:
                                    break
                            except:
                                running = False
                                process['text'] = ""
                                process['bg'] = "dark blue"
                                errotxt['text'] = f"error, try again or contact the support"
                                errotxt['bg'] = 'red'
                                driver.quit()
                                return

                else:
                    product.url = url
                    process['text'] = "Extracting data..."
                    process['bg'] = "dark gray"
                    try:
                        product_object = amazon(product, driver)
                        process['text'] = "Converting prices..."
                    except:
                        running = False
                        process['text'] = ""
                        process['bg'] = "dark blue"
                        errotxt['text'] = f"error, try again or contact the support"
                        errotxt['bg'] = 'red'
                        driver.quit()
                        return
                    try:
                        append_spreadsheet(product_object, driver, title)
                    except:
                        running = False
                        process['text'] = ""
                        process['bg'] = "dark blue"
                        errotxt['text'] = f"error, try again or contact the support"
                        errotxt['bg'] = 'red'
                        driver.quit()
                        return
                running = False
                process['text'] = ""
                process['bg'] = "dark blue"
                errotxt['text'] = "Data extracted successfully!"
                errotxt['bg'] = 'light green'
                driver.quit()

            try:
                Thread(target=extract_amazon).start()
            except:
                running = False
                process['text'] = ""
                process['bg'] = "dark blue"
                errotxt['text'] = f"error, try again or contact the support"
                errotxt['bg'] = 'red'
                driver.quit()
                return
        else:
            errotxt['text'] = "insert url from aliexpress, ebay or amazon products only"
            errotxt['bg'] = "red"
    extraction += 1


def save_file():
    global title
    folder_selected = filedialog.askdirectory()
    close(folder_selected, title)
    title = spreadsheet()
    list_titles.append(title)
    errotxt['text'] = ""
    errotxt['bg'] = "dark blue"
    input_url.delete(0, "end")
    input_brand.delete(0, "end")


def on_closing():
    global list_titles
    for t in list_titles:
        try:
            remove(f"{getcwd()}\{t}")
        except FileNotFoundError:
            pass
    exit()


clicked = StringVar()
clicked.set("")
options = [
    "",
    "EUR",
    "USD",
    "GBP"
]

clicked2 = StringVar()
clicked2.set("2")
options2 = [
    "2",
    "4",
    "6",
    "8",
    "all"
]

drop = OptionMenu(window, clicked, *options)
drop.place(x=395, y=120, width=70, height=30)
lbtext = Label(window, text="Paste Url: ")
lbtext.place(x=50, y=90)
lbbrand = Label(window, text="Brand: ")
lbbrand.place(x=50, y=120)
errotxt = Label(window, text="", bg="dark blue")
errotxt.place(x=160, y=190)
input_url = Entry(window)
input_brand = Entry(window)
lbprice = Label(window, text="Page Currency:")
lbprice.place(x=280, y=120)
input_url.place(x=120, y=90, width=340)
input_brand.place(x=120, y=120, width=150)
lbmaxproducts = Label(window, text="Max store urls:")
lbmaxproducts.place(x=280, y=150)
drop_max_products = OptionMenu(window, clicked2, *options2)
drop_max_products.place(x=395, y=150, width=70, height=30)
btsavefile = Button(window, text="Extract", command=extract)
btsavefile.place(x=150, y=340, width=100)
btsavefile = Button(window, text="Save File", command=save_file)
btsavefile.place(x=270, y=340, width=100)
progress = ttk.Progressbar(window, orient=HORIZONTAL, length=315, mode='determinate')
progress.place(x=100, y=250)
window.protocol("WM_DELETE_WINDOW", on_closing)
process = Label(window, text="", bg="dark blue")
process.place(x=225, y=275)


def update_gui():
    global driver
    progress.start(10)
    while True:
        global running
        if running:
            window.update_idletasks()
            try:
                _ = driver.window_handles
            except WebDriverException:
                running = False
                process['text'] = ""
                process['bg'] = "dark blue"
                errotxt['text'] = f"error: the browser was closed, try again"
                errotxt['bg'] = 'red'
        else:
            progress.stop()
            break


window['bg'] = "dark blue"
window.geometry("500x400")
window.mainloop()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from kivy.uix.popup import Popup

class SearchUrl(BoxLayout):
    global filename, page_soup

    def search_url(self):

        # Taking the text input and saving in my_url
        my_url = self.search_input.text
        try:
            # Opening the URL and reading the html
            uClient = urlopen(my_url)
            page_html = uClient.read()
            uClient.close()
            # html Parsing
            self.page_soup = bs(page_html, "html.parser")
            # Getting the filename from text box
            self.filename = self.filename_input.text + ".csv"
        # Checking if the URL belongs to any of the supported websites
            if my_url.startswith("https://www.bestbuy") or my_url.startswith("http://www.bestbuy"):
                self.bestbuy_ws()
            elif my_url.startswith("https://www.flipkart.com") or my_url.startswith("http://www.flipkart.com"):
                self.flipkart_ws()
            elif my_url.startswith("https://www.ebay") or my_url.startswith("http://www.ebay"):
                self.ebay_ws()
            elif my_url.startswith("https://www.newegg") or my_url.startswith("http://www.newegg"):
                self.newegg_ws()
            # If not, using popup to display error message and clear textboxes
            else:
                self.show_sitepopup()
                self.text_clear()
        # If a valid URL is not entered, another popup message and clear textboxes
        except ValueError:
            self.show_urlpopup()
            self.text_clear()

    # WebScraping from Best Buy
    def bestbuy_ws(self):

        containers = self.page_soup.findAll("div", {"class": "item-inner clearfix"})
        f = open(self.filename, "w")
        headers = "Product Title, Selling Price, Savings \n"
        f.write(headers)

        for container in containers:
            product_name = container.find("h4", {"class": "prod-title"}).text
            product_price = container.find("span", {"class": "amount"}).text

            try:
                savings = container.find("div", {"class": "prod-saving"}).contents[3].text

            except:
                savings = '$0'

            f.write(product_name + "," + product_price + "," + savings + "\n")
        f.close()

    # From ebay
    def ebay_ws(self):

        containers = self.page_soup.findAll("div", {"class": "item-inner clearfix"})
        f = open(self.filename, "w")
        headers = "Item Title, Selling Price, Original Price, Shipping Details \n"
        f.write(headers)

        for container in containers:
            item_name = container.h3.text
            item_price = container.find('span', {"class": "s-item__price"}).text

            try:
                actual_price = container.find('span', {"class": "STRIKETHROUGH"}).text
                shipping_details = container.find('span', {"class": "s-item__shipping"}).text
            except:
                actual_price = 'N/A'
                shipping_details = 'N/A'

            f.write(item_name + "," + item_price + "," + actual_price + "," + shipping_details + "\n")
        f.close()

    # From newegg
    def newegg_ws(self):

        containers = self.page_soup.findAll("div", {"class": "item-inner clearfix"})
        f = open(self.filename, "w")
        headers = "Item Title, Selling Price, Original Price, Shipping Details \n"
        f.write(headers)

        for container in containers:

            item_name = container.a.img["title"]
            current = container.find("li", {"class": "price-current"}).contents
            item_price = current[2] + current[3].text + current[4].text

            try:
                actual_price = container.find("li", {"class": "price-was"}).contents[0].strip()
                shipping_details = container.find("li", {"class": "price-ship"}).text.strip()
            except:
                actual_price = 'N/A'
                shipping_details = 'N/A'

            f.write(item_name + "," + item_price + "," + actual_price + "," + shipping_details + "\n")

        f.close()

    # From Flipkart
    def flipkart_ws(self):

        containers = self.page_soup.findAll("div", {"class": "item-inner clearfix"})
        f = open(self.filename, "w")
        headers = "Item Title, Selling Price, Original Price, EMI \n"
        f.write(headers)

        for container in containers:
            item_name = container.find("div", {"class": "_3wU53n"}).text
            item_price = ("Rs." + container.find("div", {"class": "_1vC4OE _2rQ-NK"}).contents[4].replace(",", ""))

            try:
                actual_price = (
                "Rs." + container.find("div", {"class": "_3auQ3N _2GcJzG"}).contents[4].replace(",", ""))
                emi = container.find("div", {"class": "_3MCpsc"}).span.contents
                emi_pm = "Rs." + emi[4] + emi[7]
            except:

                actual_price = item_price
                emi_pm = 'N/A'

            f.write(item_name + "," + item_price + "," + actual_price + "," + emi_pm + "\n")

        f.close()
    #Popups one for Supported site error, other for URL Error
    def show_urlpopup(self):
        popup = UrlErrorPopup()
        popup.open()

    def show_sitepopup(self):
        popup = SiteErrorPopup()
        popup.open()

    # Clear function for the button
    def text_clear(self):
        self.search_input.text = ""
        self.filename_input.text = ""

class SiteErrorPopup(Popup):
    pass

class UrlErrorPopup(Popup):
    pass

class WebScrapingApp(App):
    pass

if __name__ == "__main__":
    WebScrapingApp().run()


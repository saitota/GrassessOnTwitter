
from base64 import b64decode
from PIL import Image
from io import BytesIO
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
import math
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

opts = Options()
#opts.binary_location = 'C:\headless\'
opts.add_argument('--headless')
opts.add_argument('--disable-gpu')
opts.add_argument('--no-sandbox')
# under auth proxy
# opts.add_argument('--proxy-server=http://PROXY:PORT')
# opts.add_argument('--proxy-auth=USER:PASSWORD')
browser = webdriver.Chrome(chrome_options=opts)

browser.get('https://github.com/a')
print(browser.title)

time.sleep(1) # wait rendering

# pharse html
#sources = browser.page_source
#bs = BeautifulSoup(sources, 'html.parser')
#graph_tag = bs.find('div', {'class': 'js-contribution-graph'})

# get contribtion graph element
graph_element = browser.find_element_by_class_name('js-contribution-graph')
# scroll
# browser.execute_script('arguments[0].scrollIntoView(true);', graph_element)
#browser.save_screenshot('screenshot_browser.png')

#def get_element_screenshot(element: WebElement) -> bytes:
driver = graph_element._parent
ActionChains(driver).move_to_element(graph_element).perform()  # focus
src_base64 = driver.get_screenshot_as_base64()
scr_png = b64decode(src_base64)

scr_img = Image.open(BytesIO(scr_png))
#scr_img.save('screenshot_movetoelement.png', 'PNG')

#scr_img = Image.open(blob=scr_png)

left = graph_element.location_once_scrolled_into_view['x']
top = graph_element.location_once_scrolled_into_view['y']
right = graph_element.location_once_scrolled_into_view['x'] + graph_element.size['width']
bottom = graph_element.location_once_scrolled_into_view['y'] + graph_element.size['height']


scr_img = scr_img.crop((left, top, right, bottom)) 

scr_img.save('screenshot_crop.png', 'PNG')

browser.quit()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import glob
import numpy as np
import cPickle

#### GLOBALS
dont_search_already_found_elem_ids = True
# choose: path or None.

use_random_proxy = False
use_random_user_agent = False
use_my_user_profile = True


url = 'https://www.google.com/'

key_words_list = [u'דוגמא']
####


# DO NOT CHANGE
visited_elem_ids = []
visited_missing_elem_ids = []
saved_elem_ids = []
visited_urls = []
visited_missing_urls = []
saved_urls = []
missing_urls = 0


def main():
    driver = get_driver()
    driver.get(url)
    print('breakpoint is supposed to be here')
    if dont_search_already_found_elem_ids:
        already_visited_elems_ids = []
        for x in sorted(glob.glob('data*')):
            data = cPickle.load(open(x, 'rb'))
            already_visited_elems_ids += data['visited_elem_ids']
        already_visited_elems_ids = list(set(already_visited_elems_ids))
        scrape_page(driver, already_visited_elems_ids)
    else:
        scrape_page(driver)


def scrape_page(driver, already_visited_elems_ids=None):
    global missing_urls
    print_status()
    save_data()
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    if is_page_contain_key_words(soup):
        save_url(driver)

    links = soup.find_all("div", {"class": "css-1ckt4aj eeehqy50 mapboxgl-marker"})
    randomized_indices = np.random.permutation(range(1, len(links)+1))
    for i in randomized_indices:
        elem = driver.find_element_by_xpath("//div[@class='css-1ckt4aj eeehqy50 mapboxgl-marker'][{}]".format(i))
        elem_id = elem.get_attribute('outerHTML').split('"')[1]
        if elem_id in (visited_elem_ids + visited_missing_elem_ids):
            continue
        if (already_visited_elems_ids is not None) and (elem_id in already_visited_elems_ids):
            continue
        click_on_elem(driver, elem)

        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-1drrg4o eraqb8o10']")))
            mark_url_as_visited(driver)
            mark_elem_id_as_visited(elem_id)
        except:
            mark_url_as_visited_missing(driver)
            mark_elem_id_as_visited_missing(elem_id)
            missing_urls+=1
            if missing_urls > 10:
                save_data()
                exit('too much missing urls')

        time.sleep(np.random.uniform(1,2))
        scrape_page(driver, already_visited_elems_ids)
    print('finished scraping :)')


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument('headless')

    if use_my_user_profile:
        userProfile = 'C:\\Users\\barh\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
        chrome_options.add_argument('--profile-directory={}'.format(userProfile))

    if use_random_user_agent:
        ua = UserAgent()
        rand_ua = ua.random
        print(rand_ua)
        chrome_options.add_argument('user-agent={}'.format(rand_ua))
    else:
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')

    if use_random_proxy:
        proxy = get_random_proxy()
        print(proxy)
        chrome_options.add_argument('--proxy-server={}'.format(proxy))

    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


def is_page_contain_key_words(soup):
    description = soup.find("div", {"class": "css-t34jn3 eraqb8o15"})
    description = unicode(description)
    for kw in key_words_list:
        if kw in description:
            return True
    return False


def click_on_elem(driver, elem):
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(elem, np.random.uniform(4.8,5.2), np.random.uniform(4.8,5.2))
    action.click()
    action.perform()


def print_status():
    print('visited urls = {}'.format(len(visited_urls)))
    print('visited missing urls = {}'.format(len(visited_missing_urls)))
    print('saved urls = {}\n'.format(len(saved_urls)))


def mark_url_as_visited(driver):
    visited_urls.append(driver.current_url)


def mark_url_as_visited_missing(driver):
    visited_missing_urls.append(driver.current_url)


def mark_elem_id_as_visited(elem_id):
    visited_elem_ids.append(elem_id)


def mark_elem_id_as_visited_missing(elem_id):
    visited_missing_elem_ids.append(elem_id)


def save_url(driver):
    saved_urls.append(driver.current_url)


def save_data():
    data = {
        'visited_urls': visited_urls,
        'visited_missing_urls': visited_missing_urls,
        'saved_urls': saved_urls,
        'visited_elem_ids': visited_elem_ids,
        'visited_missing_elem_ids': visited_missing_elem_ids,
        'saved_elem_ids': saved_elem_ids
    }
    if not dont_search_already_found_elem_ids:
        with open('data1.pkl', 'wb') as fp:
            cPickle.dump(data, fp)
    else:
        i = sorted(glob.glob('data*'))[-1][4]
        with open('data'+ str(i+1)+'.pkl', 'wb') as fp:
            cPickle.dump(data, fp)


def get_random_proxy():
    def random_proxy():
        import random
        return random.randint(0, len(proxies) - 1)

    from urllib2 import Request, urlopen
    ua = UserAgent()  # From here we generate a random user agent
    proxies = []
    # Retrieve latest proxies
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read()

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
          'ip':   row.find_all('td')[0].string,
          'port': row.find_all('td')[1].string
        })

    # Choose a random proxy
    proxy_index = random_proxy()
    proxy = proxies[proxy_index]
    proxy = proxy['ip'] + ':' + proxy['port']
    proxy = proxy.encode('utf8')
    return proxy


if __name__ == '__main__':
    main()
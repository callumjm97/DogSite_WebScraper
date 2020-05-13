#! /usr/bin/env/Python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

price = raw_input("How much are you willing to spend? : ")
distance = raw_input("How far are you willing to travel? : ")

print("STARTED SCRIPT")

title = []
description = []
location = []
price = []
def getResults():
    URL = 'https://www.pets4homes.co.uk/search/?type_id=3&breed_id=163&advert_type=1&location=gillingham_kent&distance='+ distance +'&results=10&sort=creatednew'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    job_elems = soup.find_all('div', class_='profilelisting')
    for job_elem in job_elems:
        # Each job_elem is a new BeautifulSoup object.
        # You can use the same methods on it as you did before.
        title_elem = job_elem.find('h2', class_='headline')
        location_elem = job_elem.find('div', class_='location')
        description_elem = job_elem.find('div', class_='description')
        price_elem = job_elem.find('div', class_='listingprice')
        if None in (title_elem, description_elem, location_elem):
            continue
        if "reserved" not in title_elem.text.lower().strip() and "sold" not in description_elem.text.lower().strip() and float(price_elem.text.strip().replace(',','').replace(u"\u00a3", "")) <= float(1200):
            title.append(title_elem.text.strip())
            description.append(description_elem.text.strip())
            location.append(location_elem.text.strip())
            price.append(price_elem.text.strip())
            print(title_elem.text.strip())
            print("")
            print(description_elem.text.strip())
            print("")
            print(location_elem.text.strip())
            print("")
            print (price_elem.text.strip())
            print("")
            print("-------------------------")
            print("")

      

def checkResults():
    pd.set_option('display.max_rows', 10)
    test_df = pd.DataFrame({
        "Title": title,
        "Description":description,
        "Location": location,
        "Price": price})
    i = 0
    while test_df.empty:
        getResults()
        i+=1
        if i == 4:
            break
        if not test_df.empty:
            break
        else:
            print("\n No results found\n")
            countdown(2)
    test_df.sort_values(['Price'], ascending=[True])
    print(test_df)
    print("FINISHED SCRIPT")  


def countdown(t):
    while t > 0:
        sys.stdout.write('\rSearching again in : {}s'.format(t))
        t -= 1
        sys.stdout.flush()
        time.sleep(1)

if __name__ == '__main__':
    checkResults()
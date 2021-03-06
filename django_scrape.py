'''
	The purpose of this scraper is to insert data into the orm
	it is a selenium scraper using chromedriver or phantomjs(as a headless browser)
	to accomplish this purpose.
	Sorry for not using PEP8 for line length
'''

import os
import sys
import django

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__),
											 'django_scraper/')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 
											 'django_scraper/django_scraper/')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from custom_scraper.models import ScrapeData

import re
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from pprint import pprint

import psycopg2
import time

def init_driver():
	driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
	#driver = webdriver.PhantomJS()
	driver.wait = WebDriverWait(driver, 30)
	return driver

def scrape(driver, search_term, beg_date, end_date):	
	driver.get('https://aca.slcgov.com/citizen/')
	time.sleep(5)
	driver.switch_to.default_content()
	driver.switch_to_frame("ACAFrame")
	driver.wait.until(EC.element_to_be_clickable((By.ID, "ctl00_PlaceHolderMain_TabDataList_TabsDataList_ctl00_LinksDataList_ctl00_LinkItemUrl"))).click()
	time.sleep(5)
	driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='ctl00$PlaceHolderMain$generalSearchForm$ddlGSPermitType']/option[text()='{}']".format(search_term)))).click()
	time.sleep(5)
	driver.wait.until(EC.element_to_be_clickable((By.NAME, "ctl00$PlaceHolderMain$generalSearchForm$txtGSStartDate"))).send_keys("{}".format(beg_date))
	time.sleep(2)
	driver.wait.until(EC.element_to_be_clickable((By.NAME, "ctl00$PlaceHolderMain$generalSearchForm$txtGSEndDate"))).send_keys("{}".format(end_date))
	time.sleep(2)
	driver.wait.until(EC.element_to_be_clickable((By.ID, "ctl00_PlaceHolderMain_btnNewSearch"))).click()
	time.sleep(5)

	while True:
		#extract links and scrape data
		soup = BeautifulSoup(driver.page_source, "html.parser")
		for a in soup.find_all('a', href=True):
			url = 'https://aca.slcgov.com' + a['href']
			if 'Cap' in url:
				print(url)
				response = requests.get(url)
				soup = BeautifulSoup(response.text)
				span = soup.find_all('span')
				#clean up span variable data with list comprehension
				span = [" ".join(s.get_text().split()).replace("'", " ").replace("\n", "") for s in span]
				try:
					permit_number = [span[i+2] for i, x in enumerate(span) if 'Record' in x][0]
					if not permit_number:
						permit_number = ""
					status = [span[i+1] for i, x in enumerate(span) if 'record status' in x.lower()][0]
					if not status:
						status = ""
					address = [span[i+4] for i, x in enumerate(span) if 'Work Location' in x][1]
					if not address:
						address = ""
					contractor = [span[i+1] for i, x in enumerate(span) if 'Applicant:' in x][0]
					if not contractor:
						contractor = ""
					description = [span[i+1] for i, x in enumerate(span) if 'Project Description:' in x][0]
					if not description:
						description = ""
					valuation = [i.replace("Additional Information Job Value($):", "") for i in span if 'Job Value' in i][0]
					if not valuation:
						valuation = ""
					licensed_professional = [span[i+1] for i, x in enumerate(span) if 'Licensed Professional:' in x][0]
					if not licensed_professional:
						licensed_professional = ""
					parcel_number = [i.replace("Parcel Information ", "") for i in span if 'Parcel Information Parcel Number:' in i][0][0:12]
					if not parcel_number:
						parcel_number = ""
				except:
					pass
				#insert values into ORM
				scrape_data = ScrapeData()
				scrape_data.permit_number = permit_number
				scrape_data.status = status
				scrape_data.address = address
				scrape_data.contractor = contractor
				scrape_data.description = description
				scrape_data.valuation = valuation
				scrape_data.parcel_number = parcel_number
				scrape_data.save()

				

		#iterate over all pages by clicking the next button
		try:
			next_page = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='{}']".format('Next >'))))
		except TimeoutException:
			print("there was a TimeoutException")
			driver.quit()
			print("Calling function with a new 2nd argument")
			break
		next_page.click()
				

scrape(init_driver(), 'Residential SolarPV', "01/01/1970", "12/10/2015")

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import datetime
import urllib
from BeautifulSoup import BeautifulSoup 

CURRENCY_URL = "http://finance.tut.by/?utm_source=main_page&utm_medium=main_resource_block&utm_campaign=tutby_links"

def get_money_block():
	page = urllib.urlopen(CURRENCY_URL).read()
	soup = BeautifulSoup(page)
	money_block = soup.find("div", {"id": "tab-kurs"})
	money_table = money_block.find("tbody")
	return money_table

def get_raw_currency_list(money_table): #returns a tuple of raw data
	currency_list = [tuple(row.findAll("td")) for row in money_table]
	return currency_list

def get_currency_list(currency_list):
	currency_list_ready = []
	for money_value in currency_list:
		currency_name = money_value[0].find("a").string
		currency_exchange_value = money_value[1].find("span").string
		currency_list_ready.append( (currency_name, currency_exchange_value) )
	return currency_list_ready

def is_current_date_already_written():
	f = open('currency_info.txt', 'r')
	string_list = f.readlines()
	current_date = str(datetime.date.today())+'\n'
	file_last_date = string_list[-11]
	if file_last_date == current_date:
		f.close()
		return True
	else:
		f.close()
		return False

def add_list_to_file(currency_list):
	f = open('currency_info.txt', 'a')
	f.write(str(datetime.date.today())+'\n')
	for money_value in currency_list:
		str_to_write = "%s %s\n" %(str(money_value[0]),str(money_value[1]))
		f.write(str_to_write)
	f.close()

def main():
	money_block = get_money_block()
	currency_list = get_raw_currency_list(money_block)
	clear_list = get_currency_list(currency_list)
	#add_list_to_file(clear_list)

	if not is_current_date_already_written():
		add_list_to_file(clear_list)

if __name__ == "__main__":
	main()
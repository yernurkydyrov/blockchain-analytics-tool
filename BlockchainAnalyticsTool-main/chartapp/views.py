from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
from . models import Address
import math

from audioop import add
from cgitb import reset
from curses.ascii import HT
from re import U
from attr import attr


def BalanceCalc(number, divisor):
    ans = "";
    idx = 0;
    temp = ord(number[idx]) - ord('0');
    while (temp < divisor):
        temp = (temp * 10 + ord(number[idx + 1]) -ord('0'));
        idx += 1;
    
    idx += 1;
    while ((len(number)) > idx): 
        ans += chr(math.floor(temp // divisor) + ord('0'));
        temp = ((temp % divisor) * 10 + ord(number[idx]) - ord('0'));
        idx += 1;

    ans += chr(math.floor(temp // divisor) + ord('0'));

    if (len(ans) == 0):
        return "0";
     
    return ans;

def index(request):
    Address.objects.all().delete()

    url = 'https://etherscan.io/accounts'

    driver = webdriver.Chrome(executable_path=r'C:\Users\леново\Desktop\Advanced Python 2\BlockchainAnalyticsTool\chromedriver.exe')


    driver.get(url)

    driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_ddlRecordsPerPage"]/option[4]').click();

    page = driver.page_source

    soup = BeautifulSoup(page, 'html.parser')

    attrs = soup.find_all('a')

    addresses = []

    for i in attrs:
        if "0x" in str(i) and "Donate" not in str(i):
            address = str(i)
            start = address.find("0x")
            x = slice(start, start + 42)
            addresses.append(address[x])

    api = 'https://api.etherscan.io/api?module=account&action=balancemulti&address='
    arr = []

    for i in range(101):
        if i == 20 or i == 40 or i == 60 or i == 80 or i == 100:
            api += '&tag=latest&apikey=XED6G9XDWAU6PJN16WXCTKWCW4JAFA41MR'
            arr.append(requests.get(api).json())
            api = 'https://api.etherscan.io/api?module=account&action=balancemulti&address='
        if i < 100:
            api += addresses[i] + ','

    for i in arr:
        for address in i['result']:
            ether = BalanceCalc(BalanceCalc(BalanceCalc(address['balance'], 1000000), 1000000), 1000000)
            a = Address(account=address['account'], balance=ether)
            a.save()

    addresses = Address.objects.all()

    responses = {
        'addresses': addresses
    }

    return render(request, 'index.html', responses)
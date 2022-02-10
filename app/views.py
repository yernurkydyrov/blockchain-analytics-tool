
from email import header
from django.shortcuts import render
import requests
import csv
import os
from bs4 import BeautifulSoup as BS


def getA(labels):
    api = 'VG28ZKAJRRE4AJCQDWADQN22QJJRNFJT85'
    balance = []
    inquiry = 0
    while inquiry != 100:
        tRes = ''
        for i in range(inquiry, inquiry + 20):
            tRes += labels[i] + ','

            lenghtRes = len(tRes)
            dest = tRes[:lenghtRes - 1]

            r = requests.get("https://api.etherscan.io/api" +
                             "?module=account" +
                             "&action=balancemulti" +
                             "&address=" + dest +
                             "&tag=latest" +
                             "&apikey=" + api)

            res = r.json()['result']
            for j in res:
                balanceRes = j['balance']
                balance.append(int(balanceRes))

            i = i + 20
    return balance


def bsparse():
    url = "https://etherscan.io/accounts/1?ps=100"
    servers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    ans = requests.get(url, headers=servers)
    wp = ans.content
    s = BS(wp, 'html.parser')
    ress = []
    for i in s.find_all('tr'):
        td = i.find_all('td')
        for j in td:
            if j.find('a'):
                ress.append(j.find('a').text)
    return ress


def convert(labels, data):
    with open('balances.csv', 'w+', newline='') as fileCSV:
        fileR = csv.writer(fileCSV)

        for i in range(0, 100):
            lines = [labels[i], data[i]]
            try:
                fileR.writerow(lines)
            except:
                pass


def index(request):
    if not os.path.exists('./balances.csv'):
        labels = bsparse()
        data = getA(labels)
        bsparse(labels=labels, data=data)
    labels = []
    data = []
    with open('balances.csv') as fileCSV:
        fileR = csv.reader(fileCSV)
        for i in fileR:
            labels.append(i[0])
            data.append(int(i[1]))

    return render(request, 'index.html', {'labels': labels, 'data': data})

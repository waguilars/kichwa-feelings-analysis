import pandas as pd
from bs4 import BeautifulSoup
import requests

keyworksKW = []
keyworksSP = []

for i in range(1, 122):
    req = requests.get(
        'https://www.kichwa.net/glossword/index.php/list/1/'+str(i)+'.xhtml')
    soup = BeautifulSoup(req.content, 'html.parser')

    for links in soup.find_all("dt"):
        keyworksKW.append(links.getText().lower())

    for links in soup.find_all("dd"):
        palabra = repr(links.getText().lower())
        palabraSin = palabra.strip("'( )'")
        keyworksSP.append(palabraSin)

dataset = pd.DataFrame(list(zip(keyworksKW, keyworksSP)),
                       columns=['Kichwa', 'Spanish'])

dataset.to_csv('dataset.csv',)

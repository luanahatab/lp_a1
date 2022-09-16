import requests
from bs4 import BeautifulSoup

albuns = ["https://www.letras.mus.br/mamonas-assassinas/discografia/mamonas-assassinas-1995/", "https://www.letras.mus.br/mamonas-assassinas/discografia/atencao-creuzebek-a-baixaria-continua-1998/"]
for url in albuns:
    req_al = requests.get(url)
    soup_al = BeautifulSoup(req_al.content, 'html.parser')

    for song in soup_al.find_all(class_="bt-play-song", href=True):
        song_url = "https://www.letras.mus.br" + song["href"]
        print(song_url)
#atribui a song_url o url de cada musica, a ser usado depois para obter os dados


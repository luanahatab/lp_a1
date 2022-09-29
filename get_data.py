import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

albuns_url = ["https://www.letras.mus.br/queen/discografia/queen-1974/",
"https://www.letras.mus.br/queen/discografia/sheer-heart-attack-1974/",
"https://www.letras.mus.br/queen/discografia/queen-ii-1975/",
"https://www.letras.mus.br/queen/discografia/a-night-at-the-opera-1975/",
"https://www.letras.mus.br/queen/discografia/a-day-at-the-races-1976/",
"https://www.letras.mus.br/queen/discografia/news-of-the-world-1976/",
"https://www.letras.mus.br/queen/discografia/jazz-1978/",
"https://www.letras.mus.br/queen/discografia/flash-gordon-1980/",
"https://www.letras.mus.br/queen/discografia/the-game-1980/",
"https://www.letras.mus.br/queen/discografia/hot-space-1982/",
"https://www.letras.mus.br/queen/discografia/the-works-1984/",
"https://www.letras.mus.br/queen/discografia/a-kind-of-magic-1986/",
"https://www.letras.mus.br/queen/discografia/the-miracle-1989/",
"https://www.letras.mus.br/queen/discografia/innuendo-1991/",
"https://www.letras.mus.br/queen/discografia/made-in-heaven-1995/",
"https://www.letras.mus.br/queen/discografia/the-cosmos-rocks-2008/"]

# cria csv que receberá dados do dataframe
df = open('dataframe.csv', 'w', encoding='utf-8-sig')
writer = csv.writer(df)
header = ['álbum', 'música', 'letra', 'duração', 'exibições']
writer.writerow(header)

for url in albuns_url:
    req_al = requests.get(url)
    soup_al = BeautifulSoup(req_al.content, 'html.parser')

    # cria variável que receberá nome dos álbuns
    album = soup_al.find(class_="header-name").text

    for song in soup_al.find_all(class_="bt-play-song", href=True):
        # atribui a song_url o url de cada música, para mais tarde acessar os dados de cada uma delas
        song_url = "https://www.letras.mus.br" + song["href"]
        req = requests.get(song_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        
        # cria variável que receberá nome da música
        song = soup.find(class_="cnt-head_title").find("h1").text

        # cria lista que receberá letras, cujos elementos são as estrofes
        lyrics=[]
        try:
            for estrofe in list(soup.find(class_="cnt-letra p402_premium").find("p"))[1:]:
            # separa os versos da primeira estrofe
                primeira_estrofe = [list(soup.find(class_="cnt-letra p402_premium").find("p"))[0]]
                for verso in list(estrofe):
                    if str(verso) != '<br/>':
                        primeira_estrofe.append(verso)
                lyrics.append(primeira_estrofe)

            for estrofe in soup.find(class_="cnt-letra p402_premium").find_all("p")[1:]:
            # adiciona as estrofes restantes
                versos = []
                for verso in estrofe:
                    if verso.text != "":
                        versos.append(verso.text)
                lyrics.append(versos)

        except AttributeError:
            lyrics.append("Letra Indisponível")

        # cria a variável duration referente à duração das músicas
        scripts = str(soup.find(id="js-scripts"))
        elemento = scripts.find("Duration")
        duration = scripts[elemento+13:elemento+18]

        if duration != "scrip":
        # converte para segundos
            try:
                duration = 60*int(duration[0]) + 10*int(duration[2]) + int(duration[3])
            except ValueError:
                try:
                    duration = 60*int(duration[0]) + int(duration[2])
                except ValueError:
                    duration = 10*int(duration[-2]) + int(duration[-1])


        # cria a variável exibicoes referente ao número de exibições da música
        try:
            exibicoes_str = soup.find(class_="cnt-info_exib").text
            exibicoes = ""
            for i in exibicoes_str:
                try:
                    int(i)
                except ValueError:
                    continue
                else:
                    exibicoes += i
            exibicoes = int(exibicoes)
        except AttributeError:
            exibicoes = 0

        # adiciona dados ao csv
        row = []
        row.append(album)
        row.append(song)
        row.append(lyrics)
        row.append(duration)
        row.append(exibicoes)
        writer.writerow(row)

df.close()

#Premiações
prem_al = requests.get('https://en.m.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Queen')
soup_prem = BeautifulSoup(prem_al.content, 'html.parser')
tabelas = soup_prem.find_all(class_="wikitable plainrowheaders")
awards_aux = []
awards_musicas = []
premio_lista = []
for tabela in tabelas:
    premios = tabela.find_all("tr")
    for premio in premios:
        info = [x.text.strip() for x in premio.find_all("td")]
        awards_aux.append(info)
for x in range(0,len(awards_aux)):
    if len(awards_aux[x])>3:
        if awards_aux[x][3] == 'Won':
            awards_musicas.append(awards_aux[x][1])
            premio_lista.append(awards_aux[x][2])

ser = pd.Series(data=awards_musicas, index=premio_lista)
#print(ser)
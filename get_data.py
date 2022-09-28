import requests
from bs4 import BeautifulSoup
import csv

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

# cria csv para receber índices
index = open('index.csv', 'w')
writer_index = csv.writer(index)
header_index = ['álbum', 'música']
writer_index.writerow(header_index)

# cria csv para receber dados
data = open('data.csv', 'w')
writer_data = csv.writer(data)
header_data = ['letra', 'duração', 'exibições']
writer_data.writerow(header_data)

for url in albuns_url:
    req_al = requests.get(url)
    soup_al = BeautifulSoup(req_al.content, 'html.parser')

    # cria as variáveis album e songs referentes ao nome do álbum e nome das músicas
    album = soup_al.find(class_="header-name").text
    songs = [x.text for x in soup_al.find_all(class_="song-name")[1:]]
    

    # adiciona índices ao csv index
    for song in songs:
        row_index = []
        row_index.append(album)
        row_index.append(song)
        writer_index.writerow(row_index)

    for song in soup_al.find_all(class_="bt-play-song", href=True):
        # atribui a song_url o url de cada música, para mais tarde acessar os dados de cada música
        song_url = "https://www.letras.mus.br" + song["href"]
        req = requests.get(song_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        
        # cria a lista das letras, cujos elementos são as estrofes
        letra=[]
        try:
            for estrofe in list(soup.find(class_="cnt-letra p402_premium").find("p"))[1:]:
            # separa os versos da primeira estrofe
                primeira_estrofe = [list(soup.find(class_="cnt-letra p402_premium").find("p"))[0]]
                for verso in list(estrofe):
                    if str(verso) != '<br/>':
                        primeira_estrofe.append(verso)
                letra.append(primeira_estrofe)

            for estrofe in soup.find(class_="cnt-letra p402_premium").find_all("p")[1:]:
            # adiciona as estrofes restantes
                versos = []
                for verso in estrofe:
                    if verso.text != "":
                        versos.append(verso.text)
                letra.append(versos)
        
        except AttributeError:
            letra.append("letra indisponível")
        
        # cria a variável duration referente a duração das músicas
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
            
        # adiciona dados ao csv data
        row_data = []
        row_data.append(letra)
        row_data.append(duration)
        row_data.append(exibicoes)
        writer_data.writerow(row_data)

index.close()
data.close()
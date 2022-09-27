import json
import requests
from bs4 import BeautifulSoup

albuns = ["https://www.letras.mus.br/charlie-brown-jr/discografia/transpiracao-continua-prolongada-1997/",
"https://www.letras.mus.br/charlie-brown-jr/discografia/preco-curto-prazo-longo-1999/",
"https://www.letras.mus.br/charlie-brown-jr/discografia/nadando-com-os-tubaroes-2000/",
"https://www.letras.mus.br/charlie-brown-jr/discografia/100-charlie-brown-jr-2001/",
"https://www.letras.mus.br/charlie-brown-jr/discografia/bocas-ordinarias-2002/",
"https://www.letras.mus.br/charlie-brown-jr/discografia/tamo-ai-na-atividade-2004/",
"https://www.letras.mus.br/charlie-brown-jr/discografia/imunidade-musical-2005/",
"https://www.letras.mus.br/charlie-brown-jr/discografia/ritmo-ritual-e-responsa-2007/",
"https://www.letras.mus.br/charlie-brown-jr/discografia/camisa-10-joga-bola-ate-na-chuva-2009/",
"https://www.letras.mus.br/charlie-brown-jr/discografia/la-familia-013-2013/"]

for url in albuns:
    req_al = requests.get(url)
    soup_al = BeautifulSoup(req_al.content, 'html.parser')

    #cria as variaveis do nome do album e das músicas (album e songs)
    album = soup_al.find(class_="header-name").text
    songs = []
    musicas = soup_al.find_all(class_="song-name")
    for musica in musicas[1:]:
        songs.append(musica.text)
    print(songs)

    for song in soup_al.find_all(class_="bt-play-song", href=True):
        #atribui a song_url o url de cada musica, a ser usado depois para obter os dados
        song_url = "https://www.letras.mus.br" + song["href"]
        req = requests.get(song_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        letra=[]

    #criar a lista das letras, cujos elementos são as estrofes
        try:
            for estrofe in list(soup.find(class_="cnt-letra p402_premium").find("p"))[1:]:
            #separar os versos da primeira estrofe
                primeira_estrofe = [list(soup.find(class_="cnt-letra p402_premium").find("p"))[0]]
                for verso in list(estrofe):
                    if str(verso) != '<br/>':
                        primeira_estrofe.append(verso)

                letra.append(primeira_estrofe)

            for estrofe in soup.find(class_="cnt-letra p402_premium").find_all("p")[1:]:
            #adicionar as estrofes restantes
                versos = []
                for verso in estrofe:
                    if verso.text != "":
                        versos.append(verso.text)
                letra.append(versos)
        except AttributeError:
            letra.append("letra indisponivel")
        
    #criar a variavel duration da duração das músicas
        scripts = str(soup.find(id="js-scripts"))
        elemento = scripts.find("Duration")
        duration = scripts[elemento+13:elemento+18]
        
        if duration != "scrip":
        #converter para segundos
            try:
                duration = 60*int(duration[0]) + 10*int(duration[2]) + int(duration[3])
            except ValueError:
                try: 
                    duration = 60*int(duration[0]) + int(duration[2])
                except ValueError:
                    duration = 10*int(duration[-2]) + int(duration[-1])
        

    #criar a variavel exibicoes referente ao numero de exibições da música
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

import json
import requests
from bs4 import BeautifulSoup

albuns = ["https://www.letras.mus.br/mamonas-assassinas/discografia/mamonas-assassinas-1995/", "https://www.letras.mus.br/mamonas-assassinas/discografia/atencao-creuzebek-a-baixaria-continua-1998/"]
for url in albuns:
    req_al = requests.get(url)
    soup_al = BeautifulSoup(req_al.content, 'html.parser')

    for song in soup_al.find_all(class_="bt-play-song", href=True):
        #atribui a song_url o url de cada musica, a ser usado depois para obter os dados
        song_url = "https://www.letras.mus.br" + song["href"]
        req = requests.get(song_url)
        soup = BeautifulSoup(req.content, 'html.parser')

    #criar a lista das letras, cujos elementos são as estrofes
        for estrofe in list(soup.find(class_="cnt-letra p402_premium").find("p"))[1:]:
        #separar os versos da primeira estrofe
            primeira_estrofe = [list(soup.find(class_="cnt-letra p402_premium").find("p"))[0]]
            for verso in list(estrofe):
                if str(verso) != '<br/>':
                    primeira_estrofe.append(verso)

            letra = [primeira_estrofe]

        for estrofe in soup.find(class_="cnt-letra p402_premium").find_all("p")[1:]:
        #adicionar as estrofes restantes
            versos = []
            for verso in estrofe:
                if verso.text != "":
                    versos.append(verso.text)
            letra.append(versos)

    #criar a variavel duration da duração das músicas
        scripts = list(soup.find(id="js-scripts"))[1].text
        elementos = 0
        for i in range(len(scripts)):
            if scripts[i] == ":":
                elementos +=1
            if elementos == 9:
                duration = scripts[i+17:i+22]
                break

        #converter para segundos
        try:
            duration = 60*int(duration[0]) + int(duration[2:3])
        except ValueError:
            duration = 60*int(duration[0]) + int(duration[2]) 
        print(duration)

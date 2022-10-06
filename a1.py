import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk import pos_tag, word_tokenize
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

df = pd.read_csv("dataframe.csv", index_col=[0,1])
albuns = df.index.unique(level="álbum")
musics = df.index.unique(level="música")


def naoseionomedafuncao(df, indice_idx, grupo_idx, coluna, path, opcao):
   """
   :df: dataframe com indices individuais e multi-index
   :indice_idx: nome do indice individual de cada elemento
   :grupo_idx: indice coletivo dos elementos
   :coluna: nome da coluna a ser analisada
   :path: caminho da pasta aonde a img deve ser salva
   :opcao: 0 para retornar os menores elementos e 1 para os maiores
   :return: retorna um df com os elementos de maiores e menores valores por grupo e salva suas visualizações no path
   """
   mais_idx = []
   menos_idx = []
   grupos = df.index.unique(level=grupo_idx)
   for grupo in grupos:
      mais = df[df[coluna]>0].loc[grupo].sort_values(by=coluna, ascending=False).head()
      menos = df[df[coluna]>0].loc[grupo].sort_values(by=coluna).head()
      mais_idx += mais[coluna].index.tolist()
      menos_idx += menos[coluna].index.tolist()
      mais_e_menos = pd.concat([mais, menos], keys=["mais", "menos"])

      grafico = sns.barplot(data=mais_e_menos.reset_index(), x="level_0", y=coluna, hue=indice_idx)
      grafico.figure.savefig(f"{path}/{grupo}.png")
      grafico.get_figure().clf()

   if opcao == 0:
      return df[df.index.isin(menos_idx, level=indice_idx)]
   else:
      return df[df.index.isin(mais_idx, level=indice_idx)]

print(naoseionomedafuncao(df, "música", "álbum", "exibições", "./img/Grupo1/Resposta_i", 0))
print(naoseionomedafuncao(df, "música", "álbum", "exibições", "./img/Grupo1/Resposta_i", 1))
print(naoseionomedafuncao(df, "música", "álbum", "duração", "./img/Grupo1/Resposta_ii", 0))
print(naoseionomedafuncao(df, "música", "álbum", "duração", "./img/Grupo1/Resposta_ii", 1))


mais_ouvidas = df[df["exibições"]!=0].sort_values(by="exibições", ascending=False)["exibições"].head()
menos_ouvidas = df[df["exibições"]!=0].sort_values(by="exibições")["exibições"].head()
grafico1 = sns.barplot(data=mais_ouvidas.reset_index(), x="exibições", y="música", hue="música")
grafico1.figure.savefig("./img/Grupo1/Resposta_iii/mais_ouvidas.png")
grafico1.get_figure().clf()
grafico2 = sns.barplot(data=menos_ouvidas.reset_index(), x="exibições", y="música", hue="música")
grafico2.figure.savefig("./img/Grupo1/Resposta_iii/menos_ouvidas.png")
grafico2.get_figure().clf()

mais_longas = df[df["duração"]!=0].sort_values(by="duração", ascending=False)["duração"].head()
mais_curtas = df[df["duração"]!=0].sort_values(by="duração")["duração"].head()
grafico1 = sns.barplot(data=mais_longas.reset_index(), x="duração", y="música", hue="música")
grafico1.figure.savefig("./img/Grupo1/Resposta_iv/mais_longas.png")
grafico1.get_figure().clf()
grafico2 = sns.barplot(data=mais_curtas.reset_index(), x="duração", y="música", hue="música")
grafico2.figure.savefig("./img/Grupo1/Resposta_iv/mais_curtas.png")
grafico2.get_figure().clf()

premiados = df.groupby("álbum").sum().sort_values(by=["prêmios", "indicações"], ascending=[False, False]).head()
grafico = premiados.reset_index().plot(x="álbum", y=["prêmios", "indicações"], kind="bar")
plt.xticks(rotation='horizontal')
plt.xticks(rotation=12)
grafico.figure.savefig("./img/Grupo1/Resposta_v/premiados.png")
grafico.get_figure().clf()

popularidade = sns.jointplot(data=df[df["duração"]>0], x="duração", y="exibições", kind="reg")
popularidade.figure.savefig("./img/Grupo1/Resposta_vi/popularidade.png")


def words(series):
   """
   :return: série com todas as palavras presentes na série passada como parâmetro
   """
   words_series = []
   for element in series:
      for word in str(element).split():
         words_series.append(word)
   return pd.Series(words_series)

def wordcloud(series, file):
   string = " ".join(word for word in words(series)) # une todas as palavras em uma única str
   wordcloud = WordCloud().generate(string)
   wordcloud.to_file(file)

# palavras mais comuns no título dos álbuns
#print("Palavras mais comuns - título álbuns:\n", words(albuns).value_counts().head(), sep="")
#wordcloud(albuns, "img/Grupo 3/wordcloud_albuns.png")

# palavras mais comuns no título das músicas
#print("Palavras mais comuns - título músicas:\n", words(musics).value_counts().head(), sep="")
#wordcloud(musics, "img/Grupo 3/wordcloud_musics.png")

# palavras mais comuns na letra das músicas por álbum
def words_freq(df, indice, coluna):
   """
   :df: dataframe
   :indice: nome do indice pelo qual as frequenciais devem ser agrupadas
   :coluna: nome da coluna que contem as strings com as palavras a serem analisadas
   :return: dataframe com as freq das palavras mais frequentes da coluna por indice
   """
   indices = df.index.unique(level=indice)
   words_df = []
   for album in indices:
      lyrics = df.loc[album][coluna].unique()

      words_lyrics = words(lyrics)
      words_freq = words_lyrics.value_counts().head().values
      words_idx = words_lyrics.value_counts().head().index.to_list()
      multi_idx = pd.MultiIndex.from_tuples([(album, x) for x in words_idx], names=[indice, "word"])
      words_df.append(pd.DataFrame(data=words_freq, index=multi_idx, columns=["freq"]))

   return pd.concat(words_df)

print(words_freq(df, "álbum", "letra"))

# palavras mais comuns na letra das músicas de toda a discografia
lyrics = df["letra"].unique()
print("Palavras mais comuns - letra músicas:\n", words(lyrics).value_counts().head(), sep="")
wordcloud(lyrics, "img/Grupo2/wordcloud_lyrics.png")

def nouns(series):
   nouns = []
   for element in series:
      words = pos_tag(word_tokenize(str(element)))
      for word,pos in words:
         if pos.startswith('NN'):
               nouns.append(word)
   return nouns

def theme(series1, series2):
   """
   checa se subst. da série 1 estão na série 2.
   :series1: thematic series
   :series2: 
   """
   theme = []
   for noum in nouns(series1):
      for word in words(series2):
         if noum == word:
            theme.append(noum)
   theme = pd.Series(theme)
   return theme

# título de álbum é tema recorrente nas letras
print("Tema álbuns:\n", theme(albuns, lyrics).value_counts().head(), sep="")

# título de música é tema recorrente nas letras
print("Tema músicas:\n", theme(musics, lyrics).value_counts().head(), sep="")

#Perguntas criadas:
# Qual é a quantidade média de palavras por música? 

def media_palavras_musicas(lyrics):
   """Calcula a média de palavras por música
   lyrics: lista com as letras das músicas
   """
   palavras_musica = []
   for i in range(0,len(lyrics)):
      qnt_palavras = len(str(lyrics[i]).split())
      if qnt_palavras >2:
         palavras_musica.append(qnt_palavras)
      else:
         palavras_musica.append(0)

   soma_palavras = sum(palavras_musica)
   if 0 in palavras_musica:
      media_palavras = soma_palavras/(len(musics)-1)
   elif 0 not in palavras_musica:
      media_palavras = soma_palavras/len(musics)
   
   return round(media_palavras,2)

def duracao_album(df):
   """Retorna uma série com o nome das músicas e suas durações em ordem decrescente
   df: dataframe que possui como um dos índices os nomes das músicas e uma de suas colunas é a duração da música
   """
   return (df[df["duração"]>0].groupby("álbum").mean().sort_values(by="duração")["duração"])

# Qual é a quantidade média de palavras por música? 
print(f'A média de palavras por música é: {media_palavras_musicas(lyrics)}')

#Quais são os álbuns com maior e menor média de duração das músicas?
print(type(duracao_album(df)))

#III)
# duracao_list=[]
# for album in albuns:
#    duracao = df.loc[album]['duração'].unique()
#    duracao_list.append(duracao)


#quando for comparar usar aql df do lyrics e head
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk import pos_tag, word_tokenize
nltk.download('averaged_perceptron_tagger')
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

df = pd.read_csv("dataframe.csv", index_col=[0,1])
albuns = df.index.unique(level="álbum")
musics = df.index.unique(level="música")

mais_ouvidas_idx = []
menos_ouvidas_idx = []
mais_longas_idx = []
menos_longas_idx = []
for album in albuns:
   mais_ouvidas_idx += df[df["exibições"]!=0].loc[album].sort_values(by="exibições", ascending=False)["exibições"].head().index.tolist()
   menos_ouvidas_idx += df[df["exibições"]!=0].loc[album].sort_values(by="exibições")["exibições"].head().index.tolist()
   mais_longas_idx += df[df["duração"]!=0].loc[album].sort_values(by="duração", ascending=False)["duração"].head().index.tolist()
   menos_longas_idx += df[df["duração"]!=0].loc[album].sort_values(by="duração").head().index.tolist()
   
   mais_ouvidas = df[df["exibições"]!=0].loc[album].sort_values(by="exibições", ascending=False).head()
   menos_ouvidas = df[df["exibições"]!=0].loc[album].sort_values(by="exibições").head()
   mais_e_menos_ouvidas = pd.concat([mais_ouvidas, menos_ouvidas], keys=["mais", "menos"])
   grafico1 = sns.barplot(data=mais_e_menos_ouvidas.reset_index(), x="level_0", y="exibições", hue="música")
   grafico1.figure.savefig(f"./img/Grupo1/Resposta_i/{album}.png")
   grafico1.get_figure().clf()

   mais_duracao = df[df["duração"]!=0].loc[album].sort_values(by="duração", ascending=False).head()
   menos_duracao = df[df["duração"]!=0].loc[album].sort_values(by="duração").head()
   mais_e_menos_duracao = pd.concat([mais_duracao, menos_duracao], keys=["mais", "menos"])
   grafico2 = sns.barplot(data=mais_e_menos_duracao.reset_index(), x="level_0", y="duração", hue="música")
   grafico2.figure.savefig(f"./img/Grupo1/Resposta_ii/{album}.png")
   grafico2.get_figure().clf()

print(df[df.index.isin(mais_ouvidas_idx, level="música")])
print(df[df.index.isin(menos_ouvidas_idx, level="música")])
print(df[df.index.isin(mais_longas_idx, level="música")])
print(df[df.index.isin(menos_longas_idx, level="música")])

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
print("Palavras mais comuns - título álbuns:\n", words(albuns).value_counts().head(), sep="")
wordcloud(albuns, "img/Grupo 3/wordcloud_albuns.png")

# palavras mais comuns no título das músicas
print("Palavras mais comuns - título músicas:\n", words(musics).value_counts().head(), sep="")
wordcloud(musics, "img/Grupo 3/wordcloud_musics.png")

# palavras mais comuns na letra das músicas por álbum
words_dfs = []
for album in albuns:
   lyrics = df.loc[album]["letra"].unique()

   words_lyrics = words(lyrics)
   words_freq = words_lyrics.value_counts().head().values
   words_idx = words_lyrics.value_counts().head().index.to_list()
   multi_idx = pd.MultiIndex.from_tuples([(album, x) for x in words_idx], names=["album", "word"])
   words_dfs.append(pd.DataFrame(data=words_freq, index=multi_idx, columns=["freq"]))

word_df = pd.concat(words_dfs)
print(word_df)

# palavras mais comuns na letra das músicas de toda a discografia
lyrics = df["letra"].unique()
print("Palavras mais comuns - letra músicas:\n", words(lyrics).value_counts().head(), sep="")
wordcloud(lyrics, "img/Grupo 3/wordcloud_lyrics.png")

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
# I) Qual é a quantidade média de palavras por música? 
palavras_musica = []
for i in range(0,len(lyrics)):
   try:
      qnt_palavras = len(lyrics[i].split())
      palavras_musica.append(qnt_palavras)
   except Exception:
      palavras_musica.append(0)

soma_palavras = sum(palavras_musica)
media_palavras = soma_palavras/len(musics)

print(f'A média de palavras por música é: {media_palavras:.2f}')

#II) Quais são os álbuns com maior e menor média de duração das músicas?

print(df[df["duração"]>0].groupby("álbum").mean().sort_values(by="duração")["duração"])

#III)
# duracao_list=[]
# for album in albuns:
#    duracao = df.loc[album]['duração'].unique()
#    duracao_list.append(duracao)


#quando for comparar usar aql df do lyrics e head
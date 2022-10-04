import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk import pos_tag, word_tokenize
nltk.download('averaged_perceptron_tagger')

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

   mais_exib = df[df["duração"]!=0].loc[album].sort_values(by="duração", ascending=False).head()
   menos_exib = df[df["duração"]!=0].loc[album].sort_values(by="duração").head()
   mais_e_menos_exib = pd.concat([mais_ouvidas, menos_ouvidas], keys=["mais", "menos"])
   grafico2 = sns.barplot(data=mais_e_menos_ouvidas.reset_index(), x="level_0", y="exibições", hue="música")
   grafico2.figure.savefig(f"./img/Grupo1/Resposta_ii/{album}.png")
   grafico2.get_figure().clf()

print(df[df.index.isin(mais_ouvidas_idx, level="música")])
print(df[df.index.isin(menos_ouvidas_idx, level="música")])
print(df[df.index.isin(mais_longas_idx, level="música")])
print(df[df.index.isin(menos_longas_idx, level="música")])

print(df[df["exibições"]!=0].sort_values(by="exibições", ascending=False)["exibições"].head())
print(df[df["exibições"]!=0].sort_values(by="exibições")["exibições"].head())
print(df[df["duração"]!=0].sort_values(by="duração", ascending=False)["duração"].head())
print(df[df["duração"]!=0].sort_values(by="duração")["duração"].head())

print(df.groupby("álbum").sum().sort_values(by=["prêmios", "indicações"], ascending=[False, False]).head())

popularidade = sns.jointplot(data=df[df["duração"]>0], x="duração", y="exibições", kind="reg")
popularidade.figure.savefig("./img/Grupo1/Resposta_vi/popularidade.png")

# palavras mais comuns no título dos álbuns
words_albuns = []
for album in albuns:
   for word in album.split():
      words_albuns.append(word)

words_albuns_pd = pd.Series(words_albuns)
print(words_albuns_pd.value_counts().head())


# palavras mais comuns no título das músicas
words_musics = []
for music in musics:
   for word in music.split():
      words_musics.append(word)

words_musics_pd = pd.Series(words_musics)
print(words_musics_pd.value_counts().head())

# palavras mais comuns na letra das músicas por álbum
words_dfs = []
for album in albuns:
   lyrics = df[(df["letra"]!="") & (df["letra"] != "Letra Indisponível")].drop_duplicates()["letra"]
   words_lyrics = []
   for lyric in lyrics:
      for word in str(lyric).split():
         words_lyrics.append(word)

   words_lyrics = pd.Series(words_lyrics)
   words_freq = words_lyrics.value_counts().head().values
   words_idx = words_lyrics.value_counts().head().index.to_list()
   multi_idx = pd.MultiIndex.from_tuples([(album, x) for x in words_idx], names=["album", "word"])
   words_dfs.append(pd.DataFrame(data=words_freq, index=multi_idx, columns=["freq"]))

word_df = pd.concat(words_dfs)
print(word_df)

# palavras mais comuns na letra das músicas de toda a discografia
lyrics = df["letra"].unique()
words_lyrics = []
for lyric in lyrics:
   for word in str(lyric).split():
      words_lyrics.append(word)

words_lyrics_pd = pd.Series(words_lyrics)
print(words_lyrics_pd.value_counts().head())

# título de álbum é tema recorrente nas letras
tema_albuns = []
nouns = []
for album in albuns:
    words = pos_tag(word_tokenize(str(album)))
    for word,pos in words:
        if pos.startswith('NN'):
             nouns.append(word)

for noum in nouns:
   for word_ly in words_lyrics:
      if noum == word_ly:
         tema_albuns.append(noum)

tema_albuns_pd = pd.Series(tema_albuns)
print("Tema álbuns:", tema_albuns_pd.value_counts().head(20))

# título de música é tema recorrente nas letras
# checa frequência, nas letras, das palavras presentes no título das músicas
tema_musics = []
nouns = []
for music in musics:
    words = pos_tag(word_tokenize(str(music)))
    for word,pos in words:
        if pos.startswith('NN'):
             nouns.append(word)

for noum in nouns:
   for word_ly in words_lyrics:
      if noum == word_ly:
         tema_albuns.append(noum)

tema_albuns_pd = pd.Series(tema_albuns)
print("Tema álbuns:", tema_albuns_pd.value_counts().head(20))

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
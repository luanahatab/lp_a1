import pandas as pd

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

print(df[df.index.isin(mais_ouvidas_idx, level="música")])
print(df[df.index.isin(menos_ouvidas_idx, level="música")])
print(df[df.index.isin(mais_longas_idx, level="música")])
print(df[df.index.isin(menos_longas_idx, level="música")])

print(df[df["exibições"]!=0].sort_values(by="exibições", ascending=False)["exibições"].head())
print(df[df["exibições"]!=0].sort_values(by="exibições")["exibições"].head())
print(df[df["duração"]!=0].sort_values(by="duração", ascending=False)["duração"].head())
print(df[df["duração"]!=0].sort_values(by="duração")["duração"].head())

# palavras mais comuns no título dos álbuns
words_albuns = []
for album in albuns:
   for word in album.split():
      words_albuns.append(word)

words_albuns = pd.Series(words_albuns)
print(words_albuns.value_counts().head())


# palavras mais comuns no título das músicas
words_musics = []
for music in musics:
   for word in music.split():
      words_musics.append(word)

words_musics = pd.Series(words_musics)
print(words_musics.value_counts().head())

# palavras mais comuns na letra das músicas por álbum
words_dfs = []
for album in albuns:
   lyrics = df.loc[album]["letra"].unique()
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

words_lyrics = pd.Series(words_lyrics)
print(words_lyrics.value_counts().head())
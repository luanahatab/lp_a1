import pandas as pd

#df = pd.read_csv("dataframe.csv", index_col=[0,1]
df = pd.read_csv("dataframe.csv")

# maior e menor número de exibições por álbum
#print(df.loc[df["exibições"] == df.groupby("álbum")["exibições"].max().to_string(index=False)])
print(df.groupby("álbum")["exibições"].max())
print(df.groupby("álbum")["exibições"].min())

# maior e menor duração das músicas por álbum
print(df.groupby("álbum")["duração"].max())
print(df.groupby("álbum")["duração"].min())

# maior e menor número de exibições da banda
print(df["exibições"].max())
print(df["exibições"].min())

# maior e menor duração das músicas por álbum
print(df["duração"].max())
print(df["duração"].min())

# palavras mais comuns no título dos álbuns
albuns = df["álbum"].unique()
words_albuns = []
for album in albuns:
   for word in album.split():
      words_albuns.append(word)

words_albuns = pd.Series(words_albuns)
print(words_albuns.value_counts().head())


# palavras mais comuns no título das músicas
musics = df["música"].unique()
words_musics = []
for music in musics:
   for word in music.split():
      words_musics.append(word)

words_musics = pd.Series(words_musics)
print(words_musics.value_counts().head())

# palavras mais comuns na letra das músicas por álbum

# palavras mais comuns na letra das músicas de toda a discografia
lyrics = df["letra"].unique()
words_lyrics = []
for lyric in lyrics:
   for word in str(lyric).split():
      words_lyrics.append(word)

words_lyrics = pd.Series(words_lyrics)
print(words_lyrics.value_counts().head())
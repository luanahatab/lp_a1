import pandas as pd
import nltk
from nltk import pos_tag, word_tokenize
nltk.download('averaged_perceptron_tagger')

df = pd.read_csv("dataframe.csv", index_col=[0,1])
albuns = df.index.unique(level="álbum")
musics = df.index.unique(level="música")

nouns = []
#print(nltk.pos_tag(nltk.word_tokenize("flower boy")))

for album in albuns:
    words = pos_tag(word_tokenize(str(album))) #tokenize sentences
    for word,pos in words:
        if pos.startswith('NN'):
             nouns.append(word)

print(nouns)
'''
for album in albuns:
   print(nltk.pos_tag(album))
   for word_ly in words_lyrics:
      if word_mu == word_ly:
         tema_musics.append(word_mu)

lista = []
#print(nltk.pos_tag(tema_musics)
for w in tema_musics:
   if nltk.pos_tag(text)[1].pos() == 'v':
      lista.append(w)
print("Lista:", lista)

tema_musics_pd = pd.Series(tema_musics)
print("Tema músicas:", tema_musics_pd.value_counts().head(20))
'''
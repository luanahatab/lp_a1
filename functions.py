import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk import pos_tag, word_tokenize
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
nltk.download("stopwords")
from nltk.corpus import stopwords

def maiores_menores_idx(df, indice_idx, grupo_idx, coluna, path, opcao):
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

def words(series):
   """Cria série pandas com todas as palavras de series.
   :series: série cujas palavras serão retornadas como elementos de uma nova série
   :return: série com todas as palavras presentes em "series" passado como parâmetro
   """
   words_series = []
   for element in series:
      for word in str(element).split():
         words_series.append(word)
   return pd.Series(words_series)
   
def words_n_stopwords(series):
   """Cria série pandas com as palavras de series que não são stopwords (i.e. pronomes e artigos).
   :series: série cujas palavras serão filtradas e retornadas como elementos de uma nova série
   :return: série com as palavras que não são stopwords
   """
   stop_words = set(stopwords.words("english"))
   n_stopwords = [word for word in words(series) if word.casefold() not in stop_words]
   return pd.Series(n_stopwords)

def wordcloud(series, file):
   """Cria wordcloud de série.

   :series: série pandas cujas palavras geraram o wordcloud
   :file: diretrizes para salvar o wordcloud
   """
   string = " ".join(word for word in words(series)) # une todas as palavras em uma única str
   wordcloud = WordCloud().generate(string)
   wordcloud.to_file(file)

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

def nouns(series):
   """Cria série com todos substantivos presentes nos elementos da série passada como parâmetro

   :series: série que terá seus elementos analizados
   :return: série apenas com os substantivos presentes na série passada como parâmetro
   """
   nouns = []
   for element in series:
      words = pos_tag(word_tokenize(str(element)))
      for word,pos in words:
         if pos.startswith('NN'):
               nouns.append(word)
   return nouns

def theme(series1, series2):
   """Checa se substantivos de series1 estão na series2.

   :series1: série pandas que origina os temas (substantivos)
   :series2: série pandas onde os temas(substantivos) serão procurados
   :return: série pandas com os temas (substantivos) da series1 presentes na series2, de acordo com a freq.
   """
   theme = []
   for noum in nouns(series1):
      for word in words(series2):
         if noum == word:
            theme.append(noum)
   theme = pd.Series(theme)
   return theme

#Perguntas criadas:
# Qual é a quantidade média de palavras por música?

def words_avg(series):
   """Calcula média de palavras entre os elementos de uma série
   :series: série com as letras das músicas
   """
   return round(words(series).count()/series.count(), 2)

def duracao_album(df):
   """Retorna uma série com o nome das músicas e suas durações em ordem decrescente
   df: dataframe que possui como um dos índices os nomes das músicas e uma de suas colunas é a duração da música
   """
   return (df[df["duração"]>0].groupby("álbum").mean().sort_values(by="duração")["duração"])

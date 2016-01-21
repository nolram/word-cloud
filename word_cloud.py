# -*- coding: utf-8 -*-
import re
import sys
import nltk
import string
import tweepy
import numpy as np

from os import path
from PIL import Image
from wordcloud import WordCloud


CONSUMER_KEY = "INSIRA A CONSUMER_KEY CRIADA NA ETAPA ANTERIOR"
CONSUMER_SECRET_KEY = "INSIRA A CONSUMER_SECRET_KEY CRIADA NA ETAPA ANTERIOR"
ACCESS_TOKEN = "INSIRA A ACCESS_TOKEN CRIADA NA ETAPA ANTERIOR"
ACCESS_TOKEN_SECRET = "INSIRA A ACCESS_TOKEN_SECRET CRIADA NA ETAPA ANTERIOR"

DIRECTORY = path.dirname(__file__)


def _load_stop_words():
    u"""
        return: retorna um set com todas as stop words do inglês e do português
    """
    stop_words_pt = nltk.corpus.stopwords.words('portuguese')
    stop_words_en = nltk.corpus.stopwords.words('english')
    d_stop_words = set(stop_words_pt+stop_words_en)
    return d_stop_words


class WordCloudTwitter:

    def __init__(self):
        u"""
            Inicializa a classe WordCloudTwitter
            Autentica no servidor do Twitter, carrega as stopwords e compila duas expressões regulares
            self.regex é resposável por remover todas as pontuações. Ex: [!.; e etc]
            self.re_url é responsável por remover todas url. Ex: http://www.google.com.br
        """
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)
        self.stop_words = _load_stop_words()
        self.regex = re.compile('[%s]' % re.escape(string.punctuation))
        self.re_url = re.compile(r'http\S+', re.DOTALL)
        
    def normalized_words(self, s):
        u"""
            Método responsável por 'limpar' o texto, aqui ele removerá as URL e as pontuações. 
        """
        words = []
        oneline = s.replace('\n', ' ')
        text = re.sub(self.re_url, '', oneline)
        toks1 = text.split()
        for t1 in toks1:
            translated = self.regex.sub('', t1)
            toks2 = translated.split()
            for t2 in toks2:
                t2s = t2.strip()
                if len(t2s) > 1:
                    words.append(t2s)
        return words
        
    def word_cloud_user_timeline(self, with_mask=False, filename="twitter_user_cloud.png", max_words=500):
        u"""
            param : with_mask -> boolean. Indica se o Word Cloud deverá ser gerado utilizando a máscara
            param : filename -> string. Indicar o nome da imagem, esse parâmetro só é utilizado se with_mask for True
            param : max_words -> integer. Indica a quantidade máxima de palavras na Word Cloud
        """
        words = []
        for tweet in tweepy.Cursor(self.api.user_timeline).items(200):
            #print(tweet.text)
            tmp_words = self.normalized_words(tweet.text)
            for i in tmp_words:
                if i not in self.stop_words:
                    words.append(i)

        if with_mask:
            twitter_bird_mask = np.array(Image.open(path.join(DIRECTORY, "twitter_bird.png")))
            wordcloud = WordCloud(background_color="white", max_words=max_words, mask=twitter_bird_mask).generate(u" ".join(words))
            wordcloud.to_file(path.join(DIRECTORY, filename))
        else:
            wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(u" ".join(words))
        image = wordcloud.to_image()
        image.show()

    def word_cloud_home_timeline(self, with_mask=False, filename="twitter_home_cloud.png", max_words=500): 
        words = []
        for tweet in tweepy.Cursor(self.api.home_timeline).items(200):
            #print(tweet.text)
            tmp_words = self.normalized_words(tweet.text)
            for i in tmp_words:
                if i not in self.stop_words:
                    words.append(i)

        if with_mask:
            twitter_bird_mask = np.array(Image.open(path.join(DIRECTORY, "twitter_bird.png")))
            wordcloud = WordCloud(background_color="white", max_words=max_words, mask=twitter_bird_mask).generate(u" ".join(words))
            wordcloud.to_file(path.join(DIRECTORY, filename))
        else:
            wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(u" ".join(words))
        image = wordcloud.to_image()
        image.show()

    def word_cloud_by_user(self, username, with_mask=False, filename="twitter_by_user.png", max_words=500): 
        words = []
        try:
            for tweet in tweepy.Cursor(self.api.user_timeline, id=username).items(200):
                #print(tweet.text)
                tmp_words = self.normalized_words(tweet.text)
                for i in tmp_words:
                    if i not in self.stop_words:
                        words.append(i)

            if with_mask:
                twitter_bird_mask = np.array(Image.open(path.join(DIRECTORY, "twitter_bird.png")))
                wordcloud = WordCloud(background_color="white", max_words=max_words, mask=twitter_bird_mask).generate(u" ".join(words))
                wordcloud.to_file(path.join(DIRECTORY, filename))
            else:
                wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(u" ".join(words))
            image = wordcloud.to_image()
            image.show()
        except ValueError:
            print(u"O username inserido não existe")

    def word_cloud_by_search(self, search, with_mask=False, filename="twitter_by_user.png", max_words=500): 
        words = []
        try:
            for tweet in tweepy.Cursor(self.api.search, q=search).items(200):
                #print(tweet.text)
                tmp_words = self.normalized_words(tweet.text)
                for i in tmp_words:
                    if i not in self.stop_words:
                        words.append(i)

            if with_mask:
                twitter_bird_mask = np.array(Image.open(path.join(DIRECTORY, "twitter_bird.png")))
                wordcloud = WordCloud(background_color="white", max_words=max_words, mask=twitter_bird_mask).generate(u" ".join(words))
                wordcloud.to_file(path.join(DIRECTORY, filename))
            else:
                wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(u" ".join(words))
            image = wordcloud.to_image()
            image.show()
        except ValueError:
            print(u"A pesquisa não encontrou resultados")
    

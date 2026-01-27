import nltk
import re
import pickle

import unicodedata
from lxml import etree
from nltk import word_tokenize
from HanTa import HanoverTagger as ht

# Dieses Script nimmt die Reden aus der XML Datei, Tokenised, Lemmatisiert, POS-Tagged und speichert sie dann als Pickledatei

# Genutzt wird der HanoverTagger Link: https://serwiss.bib.hs-hannover.de/frontdoor/index/index/docId/2457
tagger = ht.HanoverTagger('morphmodel_ger.pgz')

# Dieses Dict wird mit Dicts der einzelnen Perioden gefüllt, welche dann
# Dicts der einzelnen Parteien enthalten, in denen jeweils eine Liste an Sätzen/Listen mit den einzelen Tokens sind
sentences_per_periode = {}

# Diese Funktion Tokenized, tagged und lemmatized die einzelnen Elemente/Worte
def pre_processor(process_me):
    process_me = unicodedata.normalize("NFKD", process_me)  # Normalisierung um Sonderzeichen beizubehalten
    sentences = nltk.sent_tokenize(re.sub(r'([a-z])\.([A-Z])', r'\1. \2', re.sub(r'([a-z])!([A-Z])', r'\1! \2',
                                                                                 process_me)))  # wir holen uns die sätze und fügen ein leerzeichen an Punkte an, welche direkt von einem Großbuchstaben gefolgt werden
    print(sentences)
    return [tagger.tag_sent(word_tokenize(token)) for token in sentences]                           # wir tokenizen, taggen und lemmatizen die einzelnen Elemente/Worte und geben eine liste an Sätzen mit tokens zurück

# Funktion um den XML Tree in schöner Form zu printen
def prettyprint(element, **kwargs):
    xml = etree.tostring(element, encoding="UTF-8", pretty_print=True, **kwargs) #String erstellen
    print(xml.decode(), end='') # printing

def main():
    tree = etree.parse("xml_tests/bt_corpus.xml")   # Wir import XML Tree
    root = tree.getroot()                           # Wir sourcen die Root um davon aus zu iterieren

    for periode in root:                            # Iteration über alle Perioden
        sentences_per_periode.update({periode.tag : {}})    # Leere Dicts in die Perioden einfügen
        print(periode.tag)
        for partei in periode:                      # Iteration über alle Parteien in der Periode
            sentences_per_periode[periode.tag].update({partei.tag : []})    # Parteien Dictionaries anlegen
            print(partei.tag)
            for rede in partei:                     # Iteration über alle reden der Partei
                sentences_per_periode[periode.tag][partei.tag].extend(pre_processor(rede.text)) # Pre_processing aufrufen und Liste erweitern


main()

# Speichern als Pickle
with open('redendict.pickle', 'wb') as output:
    pickle.dump(sentences_per_periode, output, pickle.HIGHEST_PROTOCOL)



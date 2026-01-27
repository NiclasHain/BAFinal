from germansentiment import SentimentModel
import pickle

# dieses Skript führt die Sentiment Analyse durch und speichert die Ergebnisse als Pickle datei.

# Als Modell zu Sentiment Analyse wird das germansentiment Modell von Guhr et al. benutzt. https://huggingface.co/oliverguhr/german-sentiment-bert
# http://www.lrec-conf.org/proceedings/lrec2020/pdf/2020.lrec-1.202.pdf
model = SentimentModel()
dump_me = {}    # dies ist das Dictionary, in welchem die Ergebnisse geschrieben und in eine Pickle datei gespeichert werden

# führt die Sentiment analyse durch und gibt eine Liste an Ergebnissen Zurück
def analysis(sentences):
    return_me = [model.predict_sentiment([sent]) for sent in sentences] # Führt die Sentiment Analyse auf die einelnen Sätze durch und erstellt die Liste an ergebnissen

    return return_me

# importiert das Dataset mit den Sätzen aller parteien und startet pro Wahlperiode die Sentimentanalyse
def main():

    print("main started!")
    with open("sentences.pickle", "rb") as input:   # importiert alle sätze
        data = pickle.load(input)

    for periode in data.keys():                     # iteriert über alle Wahlperioden
        dump_me.update({periode: {}})               # erstellt für die Wahlperiode einen Key im Dict
        for partei in data[periode].keys():         # iteriert über alle Parteien
            print("senting!")
            dump_me[periode].update({partei: analysis(data[periode][partei])})  # führt sentiment Analyse auf den Sätzen der Partei durch
            print(dump_me[periode][partei])
            if len(dump_me[periode][partei]) == len(data[periode][partei]): # falls alle sätze analysiert wurden. (Dies war nur während der erstellung des skriptes wichtig)
                print("bingo!")


main()


with open("graphen/keyness/sent_sentences_newest.pickle", "wb") as output:  # speichert ergebnisse in Pickledatei
    data = pickle.dump(dump_me, output, pickle.HIGHEST_PROTOCOL)






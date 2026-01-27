import pickle
import pandas as pd
import dataframe_image as dfi
from collections import Counter

# Diese Funktion berechnet die Keyness mit der "add1" Glättungsmethode
def keyness_add1(freq1, freq2):

    return_me = {"difference" : {}}             #Dictionary zum returnen

    size1 = sum(freq1.values())                 #Größe der ersten Frequency Liste berechnen
    size2 = sum(freq2.values())                 #Größe der zweiten Frequency Liste berechnen

    def difference(freq1, freq2, size1, size2): # Funktion zur Berechnung des DIFF Wertes
        nf1 = freq1/size1 * 1000000             # Berechnung der normalisierten Frequenz
        nf2 = freq2/size2 * 1000000             # Berechnung der normalisierten Frequenz
        return (((nf1 - nf2)*100)/nf2)          # Berechnung und Rückgabe des DIFF Wertes

    for word in set(list(freq1.keys()) + list(freq2.keys())):   # Iteration über alle Items der Frequenz Listen

        if word not in freq1:                   # Check ob wort in nur einer Liste vorkommt
            if freq2[word] == 1:                # Falls ein Wort nur einmal in einer Liste vorkommt, verwerfen wir es
                continue
            freq1[word] = 0                     # Wort wird zur Liste hinzugefügt, in welche es noch nicht vorhanden ist
        if word not in freq2:                   # Check ob wort in nur einer Liste vorkommt
            if freq1[word] == 1:                # Falls ein Wort nur einmal in einer Liste vorkommt, verwerfen wir es
                continue
            freq2[word] = 0                     # Wort wird zur Liste hinzugefügt, in welche es noch nicht vorhanden ist
        elif freq1[word] == 1 and freq2[word] == 1: # Einzelerwähnungen werden herausgefiltert
            continue

        freq1[word] += 1                        # Add1 - Glättung
        freq2[word] += 1


        return_me["difference"][word] = difference(freq1[word], freq2[word], size1, size2) # Aufrufen der DIFF Funktion und einfügen in das return Dict

    return return_me

# Diese Funktion macht aus einer Liste von lemmatisierten Token Listen eine Frequenz Liste
def make_freq(sentlist):
    return_me = Counter()
    for sent in sentlist:               # iteriert über die Sätze, bzw. sub-Listen in der Liste
        for (word, lemma, pos) in sent: # iteriert über die einzelnen Tokens
            if "$" not in pos and "XY" not in pos:  # filtert Sonderzeichen und Nichtworte
                if lemma not in return_me:  # Falls noch nicht in return Liste, hinzufügen
                    return_me[lemma] = 1
                else: return_me[lemma] += 1 # hochzählen
            else: continue
    return return_me

# Main
def main():
    with open("redendict.pickle", "rb") as input:   # import von Dict mit Listen an Sätzen pro Periode und Partei
        data = pickle.load(input)

    for periode in data.keys():                 # Iterieren über Perioden
        print(periode)
        for partei in data[periode].keys():     # Iterieren über alle Parteien der Periode
            print(partei)
            compare_me = data[periode][partei]  # Corpus/Partei welche verglichen werden soll
            rest = []
            for par in [x for x in data[periode].keys() if x != partei]:
                rest.extend(data[periode][par]) # erstellen des Vergleichscorpus, aus den reden der anderen Parteien

            freq1 = make_freq(compare_me)       # Frequenzliste für Corpus1(Partei) erstellen
            freq2 = make_freq(rest)             # Frequenzliste für Corpus2(restliche Parteien) erstellen

            keyness_dict = keyness_add1(freq1, freq2)   # Keyness Berechnung aufrufen
            keyness_df = (pd.DataFrame.from_dict(keyness_dict).sort_values("difference", ascending=False)
                            .reset_index().rename(columns={"index": "Wort"}))  # Nach DIFF Value absteigend sortieren
            print(keyness_df)

            # Wir exportieren die oberen 200 Items als XML
            top = keyness_df.sort_values("difference", ascending=False).head(200).reset_index(drop=True)
            top.to_csv("graphen/keyness/pd_dataframes/" + periode + "/" + partei + "top200.csv", encoding="utf-8-sig")

            # Wir exportieren die unteren 200 Items als XML
            bottom = keyness_df.sort_values("difference", ascending=True).head(200).reset_index(drop=True)
            bottom.to_csv("graphen/keyness/pd_dataframes/" + periode + "/" +  partei + "bottom200.csv", encoding="utf-8-sig")

            # Wir exportieren die Items zwischen +10 Prozent und -10 Prozent als XML
            keyness_df_similarity = keyness_df.query('-10 <= difference <= 10') # zwischen -10 und +10 Prozent sortieren
            keyness_df_similarity.to_csv("graphen/keyness/pd_dataframes/" + periode + "/" + partei + "simmilarity.csv", encoding="utf-8-sig")


# main wird ausgeführt
main()
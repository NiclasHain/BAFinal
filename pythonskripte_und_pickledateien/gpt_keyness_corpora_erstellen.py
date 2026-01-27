from lxml import etree
import os

# Dieses Skript erstellt Ziel- und Vergleichskorpora für die Analyse mit ChatGPT und speichert sie als TXT Datei
def main():
    # importiert den Korpus mit den Reden
    tree = etree.parse('bt_corpus.xml')
    root = tree.getroot()

    # Hier periode und Partei eingeben, um für diese Korpora zu erstellen
    vergleichsperiode = "periode21"
    zielpartei = "afd"

    # leere Elemente, in denen die Korpora gespeichert werden
    zielcorpus = ""
    vergleichscorpus = ""

    # sucht die Perioden nach der gewählten periode ab
    for periode in root:
        print(periode.tag)

        if periode.tag == vergleichsperiode:
            for partei in periode:  # iteriert über Parteien
                print(partei.tag)

                if partei.tag == zielpartei:    # falls die Zielpartei, dann speichern der reden im zielkorpus
                    print("treffer")
                    for rede in partei:
                        zielcorpus += rede.text + "\n"
                else:                           # falls andere Partei, dann speichern im Vergleichskorpus
                    for rede in partei:
                        vergleichscorpus += rede.text + "\n"

    #Abspeichern der Korpora als TXT Dateien
    write_partei = open(("/gpt_input/keyness/" + vergleichsperiode + "/" + zielpartei + ".txt"), "w", encoding="utf-8")
    write_partei.write(zielcorpus)

    write_verleichscorpus = open(os.path.join("/gpt_input/keyness/", vergleichsperiode, zielpartei + "_vergleichscorpus.txt"), "w", encoding="utf-8")
    write_verleichscorpus.write(vergleichscorpus)

    write_partei.close()
    write_verleichscorpus.close()



    return


main()
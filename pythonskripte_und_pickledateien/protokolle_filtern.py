import os
import shutil

# Dieses Skript iteriert durch alle Protokolle durch und filtert die, welche Worte aus der Keywortliste Aufweisen.

# Eine liste an Keyworten, welche dazu dienen den Diskurs zu finden
keyworte = ["israel", "palästin", "gaza", "westjordanland", "hamas", "fatah", "hisbollah", "zion",
            "intifada", "bds", "nakba", "nahost", "nah-ost", "westbank", "west bank"]
# dieser Counter war zur gewinnung eines Überblicks da.
count = {"israel":0, "palästin":0, "gaza":0, "westjordanland":0,
         "hamas":0, "fatah":0, "hisbollah":0, "zion":0, "intifada":0, "bds":0, "nakba":0}


destination_path = "daten_gefiltert/"    # hier werden die Protokolle abgelegt, die ein Item der Liste enthalten
hit = 0 # state indicator, wird auf 1 gesetzt falls ein Wort im Protokoll gefunden wurde.

#prüft alle Protokolle auf hits in der Schlagwortliste
for (root,dirs,files) in os.walk('daten_roh/',topdown=True): # iteriert durch alle Protokolle aller Wahlperioden. die Wahlperioden sind einzelne Ordner, die die Protokolle beinhalten
  for file in files:
      fs = open(os.path.join(root, file), "r", encoding="utf-8")    # öffnet protokoll
      contents = fs.readlines()
      print(file)                                       #um bei möglichen errors zu sehen, bei welcher Datei das Problem aufgetaucht ist

      for line in contents:                             #iteriert über jede zeile des Protokolls
          for element in keyworte:                      #überprüft, ob worte aus Liste in Zeile vorhanden
              if element in line.lower():               #falls element in zeile
                  count[element] += 1                   #kleine abfrage der hits pro schlagwort
                  hit = 1
      if hit == 1:                                      #falls hit = 1, wird das Protokoll gespeichert.
          dest = os.path.join(destination_path, file)
          shutil.copy(os.path.join(root, file), dest)
      hit = 0   #state indicator wird zurückgesetzt
      fs.close()    #schließt protokoll



for key in count:   # gibt count von Worten aus
    print(key, count[key])




#sortiert die Protokolle in Ordner, nach Wahlperiode, weil ich es vorher vergessen hatte.

for file in os.scandir(destination_path):
    periode = file.name[0] + file.name[1]                           #Die ersten zwei Zahlen der Dateinamen sind die Periode in die das Protokoll gehört
    if not os.path.exists(os.path.join(destination_path, periode)): #falls ordner nicht existiert
        os.makedirs(os.path.join(destination_path, periode))        #Ordner erstellen
    print(periode)  #um zu sehen wo das programm ist
    shutil.move(destination_path + file.name, os.path.join(destination_path, periode))  #verschiebt protokoll
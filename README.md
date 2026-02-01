Dies ist das Repository der Bachelorarbeit von Niclas Hain.  
Ergebnisse der Keyness-Analyse mit ChatGPT befinden sich im Ordner "ergebnisse_keyness_chatgpt"    
Ergebnisse der Keyness-Analyse mit dem Python-Skript befinden sich im Ordner "ergebnisse_keyness_manuell"  
Der "gpt_input" Ordner beinhaltet die Input daten für die Sentiment-Analyse und die Keyness-Analyse mit ChatGPT.  
Bei der Keyness-Analyse mit ChatGPT wurde jeweils neben dem Promt die Datei mit dem Namen einer Partei und die Datei mit dem Namen   
der Partei und _vergleichskorpus.txt als Input eingegeben.  
Der Ordner "Korpus" beinhaltet den finalen Korpus im unterordner "final"  
Die Zwischenergebnisse des Korpus, vor seiner finalen Speicherung als XML datei sind im Unterordner "old"  
Der Unterordner "protokolle/gefiltert" beinhaltet die vorgefilterten Bundestagsprotokolle  

Der Ordner "pythonskripte_und_pickledateien" beinhaltet die für die Arbeit geschriebenen python Skripte und durch diese erstellen Pickledateien  
über die viele der Zwischenprodukte gespeichert wurden.  
zu den Pythonskripten:  
"convert_to_xml.py" konvertiert den Korpus aus seinem vorläufigen Format als TXT Dateien in eine XML Datei  
"get_sentences.py" nimmt die Reden aus dem Korpus und erzeugt ein Dict mit den Reden der Parteien, geteilt in einzelne Sätze, dies ist wichtig für die Sentiment-Analyse
"gpt_keyness_corpora_erstellen.py" erstellt die Input Dateien für die Keyness-Analyse mit ChatGPT  
"keynessanalyse.py" ist das Script mit dem die Keynessanalyse durchgeführt wird. Dieses Benötigt die Pickledatei "redendict.pickle" welches den vor-verarbeiteten Korpus   beinhaltet  
"Kommentarefiltern.py" wurde benutzt um die Kommentare aus der vorläufigen speicherung zu filtern  
"make_gpt_files.py" wurde benutzt um die Input Dateien für die Sentiment-Analyse mit ChatGPT zu erstellen  
"make_preprocessed_dict.py" Vor-verarbeitet den Korpus mit Tokenizing, Lemmatisierung und POS-Tagging. Speichert den vor-verarbeiteten Korpus in der Datei "redendict.pickle"  
"plot_sent.py" wurde benutzt um die Graphen für die Sentiment Analyse anzufertigen  
"protokolle_filtern.py" wurde benutzt um die Protkolle vor der Extraktion von Reden zu filtern.  
"reden_extrahieren_alte_protos.py" extrahiert die Reden aus den Bundestagsprotokollen vor der 19. Wahlperiode  
"reden_extrahieren_neue_protos.py" extrahiert die Reden aus den Bundestagsprotokollen ab der 19. Wahlperiode  
"sentiment_analyse.py" führt die Sentiment Analyse durch.  
"visualize_sentiment_gpt.py" skript mit dem die Ergebnisse der Sentiment Analyse mit ChatGPT visualisiert wurden  

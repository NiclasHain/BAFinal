from collections import Counter
import pickle
import pandas as pd
import plotly.express as px

# dieses Skript dient der Visualisierung der Ergebnisse der Sentiment Analyse, wird gegen Ende hin etwas unleserlich, weil er ursprünglich
# nur dafür gedacht gewesen ist nur eine sache auf einmal zu plotten

# da die Ergebnisse als Liste von Listen gespeichert werden, müssen diese in eine Liste umgewandelt werden
def zusammenlegen(listen):
    return_me = []
    for liste in listen:
        return_me.extend(liste) # vereint die Listen in einer Liste

    return return_me            # gibt die vereinte Liste zurück

# berechnet den Prozentsatz an negativen Sätzen in einer Liste(also einer Partei)
def negativitaet_berechnen(calc_me):
    calc_me = zusammenlegen(calc_me)    # vereint die Listen zu einer
    count = Counter(calc_me)            # Zählt die Vorkommnisse von "positive", "neutral" und "negative"
    g = sum(count.values())             # berechnet die gesamtzahl an Ergebnissen
    w = count["negative"]               # nimmt die zahl an negativen Ergebnissen
    return round(w/g, 4)                # Gibt den Prozentsatz an negativen Ergebnissen zurück, gerundet auf 2 Nachkommastellen

# berechnet den Prozentsatz an neutralen Sätzen in einer Liste(also einer Partei)
def neutralitaet_berechnen(calc_me):
    calc_me = zusammenlegen(calc_me)    # vereint die Listen zu einer
    count = Counter(calc_me)            # Zählt die Vorkommnisse von "positive", "neutral" und "negative"
    g = sum(count.values())             # berechnet die gesamtzahl an Ergebnissen
    w = count["neutral"]                # nimmt die Zahl an neutralen Ergebnissen
    return round(w / g, 4)              # Gibt den Prozentsatz an neutralen Ergebnissen zurück, gerundet auf 2 Nachkommastellen

# berechnet den Prozentsatz an positiven Sätzen in einer Liste(also einer Partei)
def positivitaet_berechnen(calc_me):
    calc_me = zusammenlegen(calc_me)    # vereint die Listen zu einer
    count = Counter(calc_me)            # Zählt die Vorkommnisse von "positive", "neutral" und "negative"
    g = sum(count.values())             # berechnet die gesamtzahl an Ergebnissen
    w = count["positive"]               # nimmt die Zahl an positiven Ergebnissen
    return round(w/g, 4)                # Gibt den Prozentsatz an positiven Ergebnissen zurück, gerundet auf 2 Nachkommastellen

# erstellt ein pandas Dataframe, um zu Plotten
def make_pandas(dataframe, partei):
    append_me = []
    i = 0

    # fügt so viele Einträge für die Partei ein, wie sie in den Perioden vorkommt
    while i < len(dataframe.keys()):
        i += 1
        append_me.append(partei)

    # Dict, dass in ein Pandaframe gewandelt und transponiert wird
    transform_me = {"periode" : dataframe.keys(),
                    "value" : dataframe.values(),
                    "partei": append_me}
    return_me = pd.DataFrame.from_dict(transform_me, orient='index').T  # umwandlung
    #print(return_me)

    return return_me

# lädt die Sentiment ergebnisse
with open("graphen/keyness/sentiment_ergebnisse.pickle", "rb") as input:
    data = pickle.load(input)

# macht das Dict für die negativen Ergebnisse
trans_me_negative = {}
iterator = ["01", "08", "17", "20", "21"]
for i in iterator:
    for partei in data["periode" + i]:
        if partei not in trans_me_negative.keys():
            trans_me_negative.update({partei: {}})
        trans_me_negative[partei].update({i: negativitaet_berechnen(data["periode"+i][partei])})

print(trans_me_negative)
#macht das dict für die neutralen Ergebnisse
trans_me_neutral = {}
iterator = ["01", "08", "17", "20", "21"]
for i in iterator:
    for partei in data["periode" + i]:
        if partei not in trans_me_neutral.keys():
            trans_me_neutral.update({partei: {}})
        trans_me_neutral[partei].update({i: neutralitaet_berechnen(data["periode"+i][partei])})

#macht das Dict für die positiven Ergebnisse
trans_me_positive = {}
iterator = ["01", "08", "17", "20", "21"]
for i in iterator:
    for partei in data["periode" + i]:
        if partei not in trans_me_positive.keys():
            trans_me_positive.update({partei: {}})
        trans_me_positive[partei].update({i: positivitaet_berechnen(data["periode"+i][partei])})




plot_me_negative    = pd.DataFrame(columns=["periode", "value", "partei"])     # erstellt zu plottendes Dataframe für die negativen Werte
plot_me_neutral     = pd.DataFrame(columns=["periode", "value", "partei"])     # für neutrale Werte
plot_me_positive    = pd.DataFrame(columns=["periode", "value", "partei"])     # für positive Werte

# iteriert durch das Dict mit den negativen Ergebnissen
for partei in trans_me_negative:
    if partei == "NA": continue
    plot_me_negative = pd.concat([plot_me_negative, make_pandas(trans_me_negative[partei], partei)])    # füllt das Pandas Dataframe mit Werten

# iteriert durch das Dict mit den neutralen Ergebnissen
for partei in trans_me_neutral:
    if partei == "NA": continue
    plot_me_neutral = pd.concat([plot_me_neutral, make_pandas(trans_me_neutral[partei], partei)])      # füllt das Pandas Dataframe mit Werten

# iteriert durch das Dict mit den positiven Ergebnissen
for partei in trans_me_positive:
    if partei == "NA": continue
    plot_me_positive = pd.concat([plot_me_positive, make_pandas(trans_me_positive[partei], partei)])    # füllt das Pandas Dataframe mit Werten


#plottet den positiven sentiment
fig = px.line(plot_me_positive, x = "periode", y = "value",
                color = "partei", symbol = "partei", title = "positive sentiment per party" ,
                markers = True, color_discrete_sequence=px.colors.qualitative.Dark24)

fig.update_layout(
    xaxis_title="Period", yaxis_title="Positivity"
)
fig.show()

#plottet den neutralen sentiment
fig = px.line(plot_me_neutral, x = "periode", y = "value",
                color = "partei", symbol = "partei", title = "neutral sentiment per party" ,
                markers = True, color_discrete_sequence=px.colors.qualitative.Dark24)

fig.update_layout(
    xaxis_title="Period", yaxis_title="Neutrality"
)
fig.show()

#plottet den negativen sentiment
fig = px.line(plot_me_negative, x = "periode", y = "value",
                color = "partei", symbol = "partei", title = "negative sentiment per party" ,
                markers = True, color_discrete_sequence=px.colors.qualitative.Dark24)

fig.update_layout(
    xaxis_title="Period", yaxis_title="Negativity"
)
fig.show()

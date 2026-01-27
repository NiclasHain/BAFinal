import pandas as pd
import plotly.express as px

# Dieses Skript ist lediglich dazu da, die Ergebnisse der Sentiment Analyse mit ChatGPT zu visualisieren. Die Graphen wurden
# nach Sichtung über die Browserfunktionalität von Plotly gespeichert, da diese die komplette Größe beibehält.

# Das ist das Dictionary mit den Prozentsätzen an positiven Sätzen
data_positiv = {
    'Periode'   : ['1','1','1','1','1','1','1','1',
                   '8','8','8','8',
                   '17','17','17','17','17',
                   '20','20','20','20','20','20','20','20',
                   '21','21','21','21','21'],

    'Partei'    : ["CDU/CSU", "FDP", "DP", "Fraktionslos", "FU", "KPD", "SPD", "Zentrum",
                   "CDU/CSU", "SPD", "FDP", "Fraktionslos",
                   "CDU/CSU", "SPD", "Bündnis90", "FDP", "DieLinke",
                   "CDU/CSU", "SPD", "Bündnis90", "FDP", "DieLinke", "BSW", "AfD", "Fraktionslos",
                   "CDU/CSU", "SPD", "Bündnis90", "DieLinke", "AfD"],

    'Prozent'   : [6.96, 12.68, 10.34, 7.69, 7.81, 2.41, 10.28, 40.91,
                   9.3, 11.9, 17.2, 4.2,
                   5.26, 3.95, 3.25, 4.71, 1.20,
                   6.79, 5.54, 5.03, 5.43, 2.68, 2.43, 2.12, 3.10,
                   6.59, 5.05, 4.29, 2.30, 2.14]

}

# Das ist das Dictionary mit den Prozentsätzen an neutralen Sätzen
data_neutral = {
    'Periode'   : ['1','1','1','1','1','1','1','1',
                   '8','8','8','8',
                   '17','17','17','17','17',
                   '20','20','20','20','20','20','20','20',
                   '21','21','21','21','21'],
    'Partei'    : ["CDU/CSU", "FDP", "DP", "Fraktionslos", "FU", "KPD", "SPD", "Zentrum",
                   "CDU/CSU", "SPD", "FDP", "Fraktionslos",
                   "CDU/CSU", "SPD", "Bündnis90", "FDP", "DieLinke",
                   "CDU/CSU", "SPD", "Bündnis90", "FDP", "DieLinke", "BSW", "AfD", "Fraktionslos",
                   "CDU/CSU", "SPD", "Bündnis90", "DieLinke", "AfD"],

    'Prozent'   : [82.44, 60.56, 65.52, 61.54, 60.94, 34.94, 57.94, 50.00,
                   67.9, 56.7, 58.6, 72.7,
                   85.71, 82.01, 79.19, 83.17, 87.27,
                   80.79, 77.92, 75.17, 80.05, 69.17, 63.63, 41.49, 65.69,
                   81.55, 76.71, 71.90, 67.01, 40.67]


}

# Das ist das Dictionary mit den Prozentsätzen an negativen Sätzen
data_negativ = {
    'Periode'   : ['1','1','1','1','1','1','1','1',
                   '8','8','8','8',
                   '17','17','17','17','17',
                   '20','20','20','20','20','20','20','20',
                   '21','21','21','21','21'],
    'Partei'    : ["CDU/CSU", "FDP", "DP", "Fraktionslos", "FU", "KPD", "SPD", "Zentrum",
                   "CDU/CSU", "SPD", "FDP", "Fraktionslos",
                   "CDU/CSU", "SPD", "Bündnis90", "FDP", "DieLinke",
                   "CDU/CSU", "SPD", "Bündnis90", "FDP", "DieLinke", "BSW", "AfD", "Fraktionslos",
                   "CDU/CSU", "SPD", "Bündnis90", "DieLinke", "AfD"],

    'Prozent'   : [10.60, 26.76, 24.14, 30.77, 31.25, 62.65, 31.78, 9.09,
                   22.8, 31.4, 24.2, 23.1,
                   9.00, 14.04, 17.56, 12.12, 11.53,
                   12.42, 16.54, 19.80, 14.52, 28.15, 33.94, 56.39, 31.21,
                   11.88, 18.25, 23.81, 30.69, 57.19]

}

# Umwandlung der positiven Ergebnisse in ein Dataframe
plot_me = pd.DataFrame.from_dict(data_positiv)
# im folgenden wird das gerade deklarierte Dataframe geplottet.
fig = px.line(plot_me, x = "Periode", y = "Prozent",
                color = "Partei", symbol = "Partei", title = "positive sentiment per party" ,
                markers = True, color_discrete_sequence=px.colors.qualitative.Dark24)
fig.update_layout(
    xaxis_title="Wahlperiode", yaxis_title="Prozentsatz an positiven Sätzen"
)

fig.show() # Graph wird angezeigt.

# Umwandlung der neutralen Ergebnisse in ein Dataframe
plot_me = pd.DataFrame.from_dict(data_neutral)
# im folgenden wird das gerade deklarierte Dataframe geplottet.
fig = px.line(plot_me, x = "Periode", y = "Prozent",
                color = "Partei", symbol = "Partei", title = "neutral sentiment per party" ,
                markers = True, color_discrete_sequence=px.colors.qualitative.Dark24)
fig.update_layout(
    xaxis_title="Wahlperiode", yaxis_title="Prozentsatz an neutralen Sätzen"
)


fig.show()  # Graph wird angezeigt.
# Umwandlung der negativen Ergebnisse in ein Dataframe
plot_me = pd.DataFrame.from_dict(data_negativ)
# im folgenden wird das gerade deklarierte Dataframe geplottet.
fig = px.line(plot_me, x = "Periode", y = "Prozent",
                color = "Partei", symbol = "Partei", title = "negative sentiment per party" ,
                markers = True, color_discrete_sequence=px.colors.qualitative.Dark24)
fig.update_layout(
    xaxis_title="Wahlperiode", yaxis_title="Prozentsatz an negativen Sätzen"
)

fig.show() # Graph wird angezeigt.
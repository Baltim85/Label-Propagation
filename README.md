## README

# Inhaltsverzeichnis
1. [Beschreibung](#Beschreibung)
2. [Anforderungen](#Anforderungen)
3. [Abhängigkeiten](#Abhängigkeiten)
4. [Entwicklungsrechner](#Entwicklungsrechner)
5. [Ausführung des Frameworks](#Ausführung-des-Frameworks)
6. [Ausführen des Konsolenprogramms](#Ausführen-des-Konsolenprogramms)

# Beschreibung
Mit dem Programm erfolgt eine visuelle Darstellung der Arbeitsweise des Label Propagation Algorithmus.
Dazu bietet das Programm ein Framework an, indem eine .graphml Datei eingelesen werden kann, und durch unterschiedliche Einstellungen erfolgt die Community Ermittlung mittels des Algorithmus.
Neben der Visualisierung des Graphen erfolgt eine Darstellung der Modularität in einem Plot sowie die Darstellung der Werte in einer Tabelle.

Sowohl der Graph nach Anwendung des Algorithmus wie auch die Tabelle mit den Werten können für spätere Zwecke gespeichert werden.

**ACHTUNG:** Das Framework sollte ausschließlich für kleinere Graphen verwendet werden. Zu große Graphen beeinträchtigen die Performance sowie die deutliche Darstellung des Netzwerkes.

Sollen größere Netzwerke untersucht werden, so bietet das Programm die Möglichkeit, die Visualisierung zu unterbinden, sodass ausschließlich der Graph mit den Einstellungen getestet wird.
Zusätzlich bietet das Framework die Möglichkeit alle Varianten an einem Graphen zu testen.

**Anmerkung:** Je nach Größe des Graphen und Anzahl der Testläufe, die zu absolvieren sind, kann solch ein Test mehrere Stunden bis Tage in Anspruch nehmen.

Neben dem Framework ist es zusätzlich möglich, das Programm in der Konsole ausführen zu lassen. Eine Visualisierung des Graphen entfällt hier vollständig und dient eher dem Testen unterschiedlicher Varianten an einem oder mehreren Netzwerken.
Gespeichert werden die Werte in einer.csv Datei.

# Anforderungen
Das Programm wurde mit Python 3.

# Abhängigkeiten
Folgende zusätzliche Packete wurden neben den Standard Packeten von Python genutzt. Es ist wichtig das diese Versionen verwendet werden. 
* [PyQT5 5.15.4](https://pypi.org/project/PyQt5/)
* [click 7.1.2](https://pypi.org/project/click/)
* [networkx 2.5](https://pypi.org/project/networkx/2.5/)
* [numpy 1.19.3](https://pypi.org/project/numpy/1.19.3/)
* [progress 1.6](https://pypi.org/project/progress/)
* [matplotlib 3.3.3](https://pypi.org/project/matplotlib/3.3.3/)
* [tqdm 4.59.0](https://pypi.org/project/tqdm/)
* [sklearn 0.0](https://pypi.org/project/sklearn/)
* [pandas 1.2.3](https://pypi.org/project/pandas/1.2.3/)

# Entwicklungsrechner
Das Programm wurde auf einem 64 Bit Windows 10 System entwickelt, mit einem AMD Ryzen 7 2700x und 16GB DDR4 Arbeitsspeicher.

# Ausführung des Frameworks
Die Datei zum Starten des Programmes befindet sich im Ordner
LabelPropagation/src/View/TestModul.py
Zum Starten über die Konsole den Befehl python TestModul.py eingeben und das Framework öffnet sich.
Über den Punkt "Open File" kann die .graphml Datei ausgewählt werden. Je nach Größe des Graphen nimmt das Laden der Datei etwas Zeit in Anspruch.

Nachdem die Datei eingelesen und der Graph dargestellt wurde, können über den Punkt Setup Einstellungen an dem Algorithmus durchgeführt werden.
Default entspricht dem klassischen Label Propagation Algorithmus.

# Ausführen des Konsolenprogramms
Die Datei zum Starten des Programmes befindet sich im Ordner
LabelPropagation/src/ConsoleApp/Start.py
Zum Starten über die Konsole den Befehl python Start.py eingeben und das Programm öffnet sich.
Das Programm verlangt eine oder mehrere .graphml Dateien, die durch ein Leerzeichen getrennt werden.
Sollte sich die Datei nicht in dem Ordner befinden, so muss der komplette Pfad, zu der Datei angegeben werden.
Das Programm erzeugt von sich aus eine Ausgangsdatei, sodass diese nicht explizit verlangt wird. Nach Eingabe der verlangten Parameter wird der Algorithmus angestoßen.

Das Programm erzeugt nach Ausführung des Algorithmus zwei Dateien. Die erste Datei enthält die Werte zu jedem Testlauf, sofern mehrere durchgeführt wurden. Die zweite Datei enthält den Eintrag des Testlaufes, der die beste Modularität erreichte, nachdem der Algorithmus terminiert.

# Angaben in der Tabelle
Die Tabelle ist so aufgebaut, dass zunächst der Name des Graphen erscheint, sowie die Einstellungen des Algorithmus, die gewählt wurden.
**Modularity:** Beschreibt die Modularität, die am Ende des Algorithmus gemessen wurde
**Best Modularity:** Beschreibt die beste Modularität, die wären des gesamten Testlaufes verzeichnet wurde.
**Terminate:** Gibt an, ob Konvergenz vorliegt
**Iterations:** Beschreibt wie viele Iterationen der Testlauf bis zum Terminieren benötigt.
**Compare:** Bezeichnet den zweiten Algorithmus der zum Vergleich genutzt wurde
**Compare Modularity:** Enthält den Eintrag des zweiten Algorithmus und die erreichte Modularität mit diesem.
**Test Run:** Gibt an, welcher Testlauf diese Werte erreicht hat
**Fehlercode:** Das Programm beschreibt vier Codes:
**0:** bedeutet der Algorithmus hat Konvergenz erreicht
**-1:** Es kam zu einer Oszillation und der Algorithmus wurde abgebrochen
**-2:** Es kam zu einer Schleifenbildung, der Algorithmus wurde abgebrochen
**-3:** Die maximale Anzahl Iterationen wurde erreicht, der Algorithmus wurde abgebrochen
**Avg. Mod*:** Beschreibt die durchschnittliche Modularität, die erreicht wurde
**Avg. Conv*.:** Beschreibt die durchschnittliche Konvergenz des Algorithmus
**Avg Iter*.:** Beschreibt wie viele Iterationen im Durchschnitt benötigt wurden
*Mod < 0, Mod = 0, Mod > 0** : Beschreibt den Wert der Modularität, ob dieser kleiner, gleich oder größer Null ist.
*Oszillation, Indirekte Osz. Abbruch:** Gibt an, wenn der Algorithmus nicht terminierte aus welchem Grund

Die mit * markierten Einträge werden für die spätere Auswertung verwendet und laufen in die jeweils zweite Datei ein, die das Programm nach Ausführung der Testläufe erstellt.
Dadurch lässt sich ermitteln, wie oft lag Konvergenz vor, wie oft wurde eine Modularität größer, kleiner oder gleich null erreicht und wie oft wurde der Algorithmus aus welchem Grund abgebrochen.

# -*- coding: utf-8 -*-

#===============================================================================
# Dieses Programm Startet die Konsolen Anwendung des LPA, um schnell
# Grpahen einzulesen und diese mit der jeweiligen Variante ohne eine Visulaisierung
# Testen zu lassen. 
#
# Das Programm erzeugt selbsständig zwei neue Dateien, nachdem der Testlauf beendet wurde. 
# Eine Datei enthält sämtliche Ergebnisse, die zweite Datei enthält aus der Liste
# aller Ergebnisse nur das Beste (mehrere, wenn es keine Eindeutige entscheidung gibt)
# Beurteilt wird nach der Modularität die am Ende des Algorithmus erreicht wurde.
#===============================================================================


import click
import networkx as nx
import sys, csv, os


sys.path.append('../')
from ConsoleApp.LPConsole import LP
from Helper.LPAConstants import Constant as LPAM
import pandas as pd



sys.tracebacklimit = 0

#===============================================================================
# Eingabe der Parameter um den LPA auszuführen 
#===============================================================================

print("Hinweis")
print("Eingangsdatei: Verlangt eine GraphML Datei. \nBei Verwendung mehrere Dateien werden diese durch ein Leerzeichen getrennt.")
print("Eine Explizite Dateiendung wird von dem Programm übernommen")
print("\nEs muss der vollständige Pfad angegeben werden, wenn die Daten sich nicht im Ordner des Programms befinden.")
print("\nAusgangsdate: Das Programm erzeugt pro Graphen zwei Dateien. \nEine Datei enthält die Ergebnisse aller Testläufe.")
print("\nDie zweite Datei enthält den Eintrag mit den Besten Werten aus der Datei")

@click.command()
@click.option("--inp", "-i",  prompt="Eingangsdatei", help="Dateipfad zur Eingabe im graphml-Format")

#@click.option("--out", prompt="Ausgangsdatei", help="Dateipfad zur Eingabe im graphml-Format")

@click.option("--mode", prompt="Mode: Synchron (s) oder Asynchron (a)", help="Use a synchronous or asynchronous update")
@click.option("--labels", prompt="Initialisierung der Knoten: Unique (u) oder Zufaellig (r)", help="Initialisiert die Knoten mit einem Label")
@click.option("--k", prompt="Setzen des k: k = 1 oder 2, wenn Unique k = 0", help="Set the random Value")
@click.option("--order", prompt="Reihenfolge festlegen: Fixiert (fo) or Zufällig (ro)", help="Use a fixed order for every Iteration or use after each iteration a new order")
@click.option("--nbr", prompt="Hop-Distanz: 0, 1, 2 oder 3", help="Attribut der durch Algorithmus ermittelten Communities")
@click.option("--lb", prompt="Labelwahl: Zufällig (r), Label behalten (s), Erste (f), letzte (l) oder Mittlere (m)", help="Attribut der durch Algorithmus ermittelten Communities")
@click.option("--conv", prompt="Konvergenz: Algorithmus stoppt selber (c) oder Iteration (i)", help="Attribut der durch Algorithmus ermittelten Communities")
@click.option("--iter", prompt="Anzahl Iteration: ", help="Attribut der durch Algorithmus ermittelten Communities")
@click.option("--test", prompt="Anzahl Testlaeufe: ", help="Attribut der durch Algorithmus ermittelten Communities")
#@click.option("--sa", prompt="Synchron/Asynchron: sa ", help="Attribut der durch Algorithmus ermittelten Communities")

#def module(inp, out,  mode, labels, k, order, nbr, lb, conv, iter, test):

def module(inp,  mode, labels, k, order, nbr, lb, conv, iter, test):
    trigger = True
    gFiles = []
    oFiles = []
    bFiles = []
    str_AS =""
    str_c =""
    str_l =""
    str_h = ""
    str_or= ""
    str_k = ""
    while trigger:
        if(mode == "s"):
            mode = LPAM._SYNC.value
            str_AS = "Sync"
        elif(mode == "a"):
            mode = LPAM._ASYNC.value
            str_AS = "Async"
        else:
            print(f'Kein gültiger Mode')
            
        if(labels == "u"):
            labels = LPAM._UNIQUE.value
        elif(labels == "r"):
            labels = LPAM._RANDOM.value
        else:
            print(f'Keine gültige Initialisierung')
        if(k == "1"):
            k = 1
            str_k ="1"
        elif(k == "2"):
            k = 2
            str_k ="2"
        elif(k == "0"):
            k = 3
            str_k ="0"
        else:
            print(f'Keine gültiger Wert')
            return
        
        if(order == "fo"):
            order = True
            str_or= "FO"
        elif(order == "ro"):
            order = False
            str_or= "RO"
        else:
            print(f'Keine gültige Reihenfolge')
            return
        
        if(nbr == "0"):
            nbr = 0
            str_h = "0"
        elif(nbr == "1"):
            nbr = 1
            str_h = "1"
        elif(nbr == "2"):
            nbr = 2
            str_h = "2"
        elif(nbr == "3"):
            nbr = 3
            str_h = "3"
        else:
            print(f'Kein gültiger Wert nbr')
            return
        
        if(lb == "r"):
            lb = LPAM._RANDOM.value
            str_l ="Random"
        elif(lb == "s"):
            lb = LPAM._SELF.value
            str_l ="self"
        elif(lb == "f"):
            lb = LPAM._FIRST.value
            str_l ="First"
        elif(lb == "l"):
            lb = LPAM._LAST.value
            str_l ="Last"
        elif(lb == "m"):
            lb = LPAM._MEDIAN.value
            str_l ="Median"
        else:
            print(f'Kein gültiger Wert, lb')
            return
        
        if(conv == "c"):
            conv =  True
            str_c ="Conv."
        elif(conv == "i"):
            conv = False
            str_c="MaxIter"
        else:
            print(f'Keine gültiger Wert')
            return
        #wFile = out +"BestValues.csv"
        #out = out +".csv"
        
        
        #if(sa == "sa"):
        #    sa = True
        #else:
        #    sa =False
    
        #try:
        #    outFile = open(out, 'w', encoding='UTF8', newline='')
        #except FileNotFoundError:
        #    print("File Not Found: " + out)
        #    return
        header = ["Graph", "Mode", "Initialize", "K", "Update Order", "Neighbor", "Label Sel.", "Convergence", "Modularity", "Best Modularity", "Terminate", "Iterations", "NMI", "Compare", "Compare Modularity", "Test Run"]
        #writer = csv.writer(outFile)
        #writer.writerow(header)
        #wfile = out
        #print(wfile)
        lp = LP()
    
        files = inp.split(" ")
        #=======================================================================
        # In diesem Teil des Programmes wird der LPA mit den Einstellungen ausgeführt
        # Nach Beendung des Aktuellen laufes werden die beiden Dateien erzeugt. 
        # Mittels Pandas wird die erste Liste bearbeitet und der 
        # jeweils beste Eintrag aus der Datei in eine zweite Datei geschrieben.
        #=======================================================================
        for f in files:
            gFiles.append(f+".graphml")
            oFiles.append(f+"Mode_"+str_AS+"Kon_"+str_c+"Label_"+str_l+"Hop_"+str_h+"order_"+str_or+"k_"+str_k+".csv")
            bFiles.append(f+"Mode_"+str_AS+"Kon_"+str_c+"Label_"+str_l+"Hop_"+str_h+"order_"+str_or+"k_"+str_k+"BestValues.csv")
        
        for i in range(len(gFiles)):
            try:
                outFile = open(oFiles[i], 'w', encoding='UTF8', newline='')
            except FileNotFoundError:
                print("File Not Found: " + oFiles[i])
                return
            header = ["Graph", "Mode", "Initialize", "K", "Update Order", "Neighbor", "Label Sel.", "Convergence", "Modularity", "Best Modularity", "Terminate", "Iterations", "NMI", "Compare", "Compare Modularity", "Test Run", "Fehlercode"]
            writer = csv.writer(outFile)
            writer.writerow(header)
            #wfile = out
            try:
                graph=nx.read_graphml(gFiles[i])
                graph=graph.to_undirected()
            except Exception as e:
                raise Exception("Input file %s is not a graph! Parsing error: %s" % (gFiles[i], e))
                return
            graphName = os.path.basename(gFiles[i])
            
            writer = lp.LPA(graph, k, iter, mode, labels, lb, nbr, conv, order, test, graphName, writer)
            outFile.flush()
            #time.sleep(0.5)  # emulating long-playing job
            #bar.finish()
            #return
            #df = pd.read_csv(out)
            
            df = pd.read_csv(oFiles[i])
            
            #df = df["Modularity"].mean()
            df1 = df[df['Modularity']==df['Modularity'].max()].copy(deep=True)
            #df2 = df.drop(df[df["Modularity"] == 0].index)
            #print(df2)
            df1["Avg. Mod"] = df["Modularity"].mean()
            vale = ((df['Terminate'] == "Convergence").sum()*100)/int(test)
            iter = df['Iterations'].sum()/int(test)
            df1["Avg. Conv. %"] = vale
            df1["Avg. Iter. "] = iter
            details = df.apply(lambda x : True
                if x['Modularity'] < 0 else False, axis = 1)
            df1["Mod < 0"] = len(details[details == True].index)
            details = df.apply(lambda x : True
                if x['Modularity'] == 0 else False, axis = 1)
            df1["Mod = 0"] = len(details[details == True].index)
            details = df.apply(lambda x : True
                if x['Modularity'] > 0 else False, axis = 1)
            df1["Mod > 0"] = len(details[details == True].index)
            
            details = df.apply(lambda x : True
                if x['Fehlercode'] == -1 else False, axis = 1)
            df1["Ozsilation"] = len(details[details == True].index)
            details = df.apply(lambda x : True
                if x['Fehlercode'] == -2 else False, axis = 1)
            df1["Indirekte Osz."] = len(details[details == True].index)
            details = df.apply(lambda x : True
                if x['Fehlercode'] == -3 else False, axis = 1)
            df1["Abbruch"] = len(details[details == True].index)
            
            
            #vale = df1.iat[0,1]       
            
            #df = df.append(df1, ignore_index=True)
            #df_out = df[df['Modularity']==df['Modularity'].max()]
            #df1["Avg Modularity"] = df["Modularity"].mean() 
            df1.to_csv(bFiles[i])
            #df_workingFile = df_workingFile["Modularity"].max()
            #print(df)
            outFile.close()
        
        if click.confirm('Do you want to continue?', default=trigger):
            #print('Do something')
            module()
        else:
            trigger = False
           

if __name__=='__main__':
    #if click.confirm('Do you want to continue?', default=True):
    #   print('Do something')
    module()


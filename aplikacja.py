import pandas as pd
import math
import tkinter as tk
import os

latCentrum = 56.9475804          
lonCentrum = 24.1093500


#uzyteczne funkcje
def obliczOdleglosc(lat1,lon1,lat2,lon2):
    return math.sqrt((lat1-lat2)**2+(lon1-lon2)**2)*111

#funkcje użyte póxniej w celu standaryzacji
def LiczStyl(x,tab):
    if tab.max()==tab.min():
        return 100
    return (x-tab.min())/(tab.max()-tab.min())*100

def LiczDes(x,tab):
    if tab.max()==tab.min():
        return 100
    return (tab.max()-x)/(tab.max()-tab.min())*100

def LiczLog(x,tab):
   
    return math.log10((x-tab.min()+1)/(tab.max()-tab.min()+1)*100)*50
    
def LiczLogDes(x,tab):
    
    return math.log10(((tab.max()-x+1)/(tab.max()-tab.min()+1))*100)*50



data = pd.read_excel("C:/Users/gorec/Documents/seminarium/Riga/Ryga.xlsx")

#dodanie cena za metr
data["price for m2"]=data["price"]/data["area"]

#dodanie zmiennej standard data
Standard_data=0

#przesortowanie kolumny z pokojami
def filtrInt(x):
    try:        
        int(x)
        return True
    except ValueError:
        return False
def Int(x):
    return int(x)   

data=data[data["rooms"].apply(filtrInt)]  
data["rooms"]=data["rooms"].apply(Int)

def Type(x):
    if x=="For sale" or x=="For rent":
        return True
    else:
        return False
data=data[data["op_type"].apply(Type)]    

def inicjalizacjaOkienka():
    root = tk.Tk()
    root.geometry("900x700")
    root.title("Aplikacja")
    
    return root


class Tabela:
    def __init__(self,rzad,kolumna):       
        Tab=tk.Label(root,text="")
        Tab.grid(row=rzad,column=kolumna,pady=1, padx=0)
        self.Tab = Tab
        self.rzad=rzad
        self.kolumna=kolumna
    def setTabela(self,text):
        self.Tab.destroy()
        self.Tab=tk.Label(root,text=str(text))
        self.Tab.grid(row=self.rzad, column=self.kolumna, pady=1, padx=0)
    def Clear(self):
        self.Tab.destroy()


class KrytMinMax:
    def __init__(self,nazwa,rzad,kryt,Des):
        self.nazwa=nazwa
        self.rzad=rzad
        self.kryt=kryt
        self.Des=Des
        self.log=False
        self.waga_normal=0
        
        
        #Labelnazwa
        label_nazwa=tk.Label(root,text=self.nazwa)
        self.label_nazwa=label_nazwa
        
        #min
        label_min=tk.Label(root, text="Min:")
        self.label_min=label_min        
        MinPole = tk.Entry(root, width=10)
        self.MinPole=MinPole
        
        #max
        label_max=tk.Label(root, text="Max:",width=10)
        self.label_max=label_max
        MaxPole= tk.Entry(root,width=10)
        self.MaxPole=MaxPole
        
        #error
        Pusty=tk.Label(root,text="")
        Pusty.grid(row=rzad+1,column=2,pady=1,padx=0)
        self.Pusty=Pusty
        
        #Współrzedne
        LabelLat=tk.Label(root, text="Szerokosc geograficzna:")
        LatEntry=tk.Entry(root)
        LabelLon=tk.Label(root, text="Dlugosc geograficzna:")
        LonEntry=tk.Entry(root)
        self.LabelLat=LabelLat
        self.LatEntry=LatEntry
        self.LabelLon=LabelLon
        self.LonEntry=LonEntry
        
        #waga
        WagaLabel=tk.Label(root, text="Waga:",width=10)
        self.WagaLabel=WagaLabel
        Waga=tk.Entry(root, width=8)
        self.Waga=Waga
        
        #nominanty
        clicked = tk.StringVar()
        tabNom=["Stymulanta","Destymulanta"]
        self.tabNom=tabNom
        self.clicked=clicked
        self.clicked.set(tabNom[self.Des])       
        Nom=tk.OptionMenu(root, clicked, *tabNom)
        Nom.config(width=15)
        self.Nom=Nom       
        
        if kryt=="Odleglosc":            
            data["Odleglosc"]=(((data['lat']-latCentrum)**2+(data['lon']-lonCentrum)**2)**(1/2))*111           
    
    #standaryzacja
    def standard(self,dane,tab):
        
        if self.log:
            if self.clicked.get()=="Stymulanta":
                         
                return dane[self.kryt].apply(LiczLog, args=[tab])
            else:
                               
                return dane[self.kryt].apply(LiczLogDes, args=[tab])
        if self.clicked.get()=="Stymulanta":
            return dane[self.kryt].apply(LiczStyl, args=[tab])
        else:
            return dane[self.kryt].apply(LiczDes, args=[tab])       
   
    def getWaga(self):
        if len(self.Waga.get())>0:
            try:
                return int(self.Waga.get())
            except ValueError:
                self.error()                    
        else:
            return 0        
            
    def show(self):
        self.label_nazwa.grid(row=self.rzad,column=0,pady=1, padx=0)
        self.label_min.grid(row=self.rzad,column=1,pady=1, padx=0)
        self.MinPole.grid(row=self.rzad,column=2,pady=1, padx=0)
        self.label_max.grid(row=self.rzad,column=3,pady=1, padx=0)
        self.MaxPole.grid(row=self.rzad,column=4,pady=1, padx=0)
        self.Pusty.grid(row=self.rzad+1,column=2,pady=1,padx=0)
        self.WagaLabel.grid(row=self.rzad,column=5,pady=1,padx=0)
        self.Waga.grid(row=self.rzad,column=6,pady=1,padx=0)
        self.Nom.grid(row=self.rzad,column=7,pady=1,padx=0)   
        
    def error(self):
        self.Pusty.destroy()
        Pusty=tk.Label(root,text="Wprowadzone dane muszą być liczbą")
        if self.kryt=="Odleglosc":
            Pusty.grid(row=self.rzad+2,column=2,pady=1,padx=0)
        else:
            Pusty.grid(row=self.rzad+1,column=2,pady=1,padx=0)   
        self.Pusty=Pusty
    

    def getMin(self): 
            if len(self.MinPole.get())>0:
                try:
                    return int(self.MinPole.get())
                except ValueError:
                    self.error()                    
            else:
                return data[self.kryt].min()
                
        
        
    
    def getMax(self):        
            if len(self.MaxPole.get())>0:
                try:
                    return int(self.MaxPole.get())
                except ValueError:
                    self.error()                    
            else:
                return data[self.kryt].max()
            
    def filtruj(self,dane):
        if len(self.LatEntry.get())>0 and len(self.LonEntry.get())>0:
            try:
                dane["Odleglosc"]=(((dane['lat']-float(self.LatEntry.get()))**2+(dane['lon']-float(self.LonEntry.get()))**2)**(1/2))*111
               
            except ValueError:
                self.error()            
        return dane[((dane[self.kryt])>=self.getMin()) & ((dane[self.kryt])<=self.getMax())]
    
    def clear(self):
        self.MinPole.delete(0,(len(self.MinPole.get())))
        self.MaxPole.delete(0,(len(self.MaxPole.get())))
        self.Waga.delete(0,(len(self.Waga.get())))
        self.Pusty.destroy()
        self.Pusty=tk.Label(root,text="")
        self.Pusty.grid(row=self.rzad+1,column=2,pady=1,padx=0)       
        self.LatEntry.delete(0,(len(self.LatEntry.get())))
        self.LonEntry.delete(0,(len(self.LonEntry.get())))
        
    def inicjalizajcaInneWspol(self):
        #Szerokosc
        self.LabelLat.grid(row=self.rzad+1,column=1,pady=1, padx=0)
        self.LatEntry.grid(row=self.rzad+1,column=2,pady=1, padx=0)
        
        #Dłougosc
        self.LabelLon.grid(row=self.rzad+1,column=3,pady=1, padx=0)
        self.LonEntry.grid(row=self.rzad+1,column=4,pady=1, padx=0)        
        
        #Przycisk innego punktu
    def InnyPuntkt(self):
        Inne_button=tk.Button(root, text="Odleglosc od wybranego punktu", command=self.inicjalizajcaInneWspol)
        Inne_button.grid(row=self.rzad+1,column=0,pady=1, padx=0)
    
         
class KrytWybor:
    def __init__(self,nazwa,rzad,kryt):
        self.nazwa=nazwa
        self.rzad=rzad
        self.kryt=kryt
        tab=[]
        self.tab=tab
           
        dataSorted=data.sort_values([kryt])
        datafiltred=dataSorted[kryt][dataSorted[kryt].notnull()].unique()
                   
        label_nazwa=tk.Label(root,text=self.nazwa)
        self.label_nazwa=label_nazwa
        WybOp=tk.Label(root,text="Wybrane opcje:")
        self.WybOp=WybOp
        
        clicked = tk.StringVar()
        self.clicked=clicked
        self.clicked.set("Wszystkie")                
        Menu=tk.OptionMenu(root, clicked, *datafiltred)
        self.Menu=Menu 
        
        Opcje=tk.Label(root,text="")
        self.Opcje=Opcje        
        
    def show(self):
        self.label_nazwa.grid(row=self.rzad,column=0,pady=1, padx=0)
        self.Menu.grid(row=self.rzad+1,column=0, pady=1, padx=0)
        self.Opcje.grid(row=self.rzad+1,column=1,pady=1, padx=0,)
        
    def setOpcje(self):
        self.Opcje.destroy()
        self.Opcje=tk.Label(root,text=str(self.tab)[1:-1])
        self.Opcje.grid(row=self.rzad+1,column=1,pady=1, padx=0)        
        
    def dodaj(self):
        if self.clicked.get() not in self.tab:
            self.tab.append(self.clicked.get())
            self.setOpcje()
            
        
    def usun(self):
        if(len(self.tab)>0):
            self.tab.pop(-1)
            self.setOpcje()
            
    
    def filtrujTab(self,obiekt,tab):
        if obiekt in tab:
            return True
        return False       
    
    def filtruj(self,data): 
        if len(self.tab)==0:
            self.clicked.set("Wszystkie")
            return data        
        return data[data[self.kryt].apply(self.filtrujTab, args=[self.tab])]
    
    def clear(self):
        self.clicked.set("Wszystkie")
        self.tab=[]
        self.setOpcje()
                   
    def inicjalizacjaButtons(self):
        self.WybOp.grid(row=self.rzad,column=1,pady=1, padx=0)
        Dodaj=tk.Button(root, text="Dodaj",command=self.dodaj)
        Dodaj.grid(row=self.rzad+2,column=0, pady=1, padx=0)
        Usun=tk.Button(root, text="Usun",command=self.usun)
        Usun.grid(row=self.rzad+2,column=1, pady=1, padx=0)

def inicjalizacjaKryteriow(root): 
    
    def inicjalizacjaKryteriow2():
        
        #Cena za m2
        CenaZam2.show()
        
        #lpokoi
        LPokoi.show()        
        
        #pietro
        Pietro.show()        
        
        #rodzaj zabudowy
        Zabudowa.show()
        Zabudowa.inicjalizacjaButtons()
        
        #Ilosc pieter
        Pietra.show()
        
        #Odległosc od centrum
        Odleglosc.show()
        Odleglosc.InnyPuntkt()
        
    # Tabela informacyjna
    Wyniki=Tabela(1, 1)
    #Nick uzytwkonika
    label_nick=tk.Label(root, text="Nick Użytkwonika:")
  
    label_nick.grid(row=0,column=2,pady=1, padx=0)
    entry_nick=tk.Entry(root, width=10)
    entry_nick.grid(row=0,column=3,pady=1, padx=0)
    
    #Scenariusz
    ScenClicked = tk.StringVar()
    ScenClicked.set("Scenariusz")  
    Scenariusze=("Scenariusz 1","Scenariusz 2","Scenariusz 3","Scenariusz 4" )        
    Scen=tk.OptionMenu(root, ScenClicked, *Scenariusze)
    Scen.grid(row=0,column=4,pady=1, padx=0)   
    
    # Typ
    Typ=KrytWybor("Typ ogłoszenia",0,"op_type")
    Typ.show()
    Typ.clicked.set("For sale")
    
    
    # Dzielnica 
    Dzielnice=KrytWybor("Dzielnica", 3, "district") 
    Dzielnice.show()
    Dzielnice.inicjalizacjaButtons()
    
    #Cena    
    Cena=KrytMinMax("Cena",6,"price",1)
    Cena.show()
    
    #Powierzchnia    
    Powierzchnia=KrytMinMax("Powierzchnia",8,"area",0)
    Powierzchnia.show()
    
    #Cena za m2
    CenaZam2=KrytMinMax("Cena za m2", 12, "price for m2",1)
    
    #lpokoi
    LPokoi=KrytMinMax("Liczba pokoi", 14, "rooms",0)
    
    #pietro
    Pietro=KrytMinMax("Piętro", 16, "floor",1)
    
    #Ilosc pieter
    Pietra=KrytMinMax("Ilość kodygnacji w budynku",18, "total_floors",1)
    
    #Rodzaj zabudowy
    Zabudowa = KrytWybor("Rodzaj zabudowy", 20, "house_type")
    
    #Odleglosc
    Odleglosc=KrytMinMax("Odleglosc od Centrum",23, "Odleglosc",1)
    
    #funkcja normalizująca wagi
    def normalizuj_wagi():
        Wagi_Suma=Cena.getWaga()+Powierzchnia.getWaga()+CenaZam2.getWaga()+LPokoi.getWaga()+Pietro.getWaga()+Pietra.getWaga()+Odleglosc.getWaga()
        
        def normalizuj_wage(KrytMinMax):
            if Wagi_Suma>0:
                KrytMinMax.waga_normal=KrytMinMax.getWaga()*100/Wagi_Suma
            else:
                #gdy wagi = 0
                KrytMinMax.waga_normal=1
                
            
        normalizuj_wage(Cena)    
        normalizuj_wage(Powierzchnia)
        normalizuj_wage(CenaZam2)   
        normalizuj_wage(LPokoi)   
        normalizuj_wage(Pietro)
        normalizuj_wage(Pietra)
        normalizuj_wage(Odleglosc)        
       
    # funkcja szukająca oferty
    def szukaj():
        #stworzenie zmiennej na podstawie używanego zestawu danych
        filtred_data=data
        
        #Typ
        filtred_data=filtred_data[filtred_data["op_type"]==Typ.clicked.get()]
        # Dzielnica
        filtred_data=Dzielnice.filtruj(filtred_data)
        
        #Cena
        filtred_data= Cena.filtruj(filtred_data)
        #Powierzchnia
        filtred_data= Powierzchnia.filtruj(filtred_data)
        #WIęcej Krytriów
        #Cena za m2
        filtred_data=CenaZam2.filtruj(filtred_data)
        #lpokoi
        filtred_data=LPokoi.filtruj(filtred_data)        
        
        #pietro
        filtred_data=Pietro.filtruj(filtred_data)
        
        #Ilosc pieter
        filtred_data=Pietra.filtruj(filtred_data)
        
        #zabudowa
        filtred_data=Zabudowa.filtruj(filtred_data)
        
        #Odleglosc
        filtred_data=Odleglosc.filtruj(filtred_data)    
        
        Wyniki.setTabela("Znaleziono {0} wyników".format(len(filtred_data)))
        
        #usuwanie zbędnych kolumn w filtred data
        filtred_data.drop("Unnamed: 0", axis=1, inplace=True)
        filtred_data.drop('ID', axis=1, inplace=True)
        filtred_data.drop('lat', axis=1, inplace=True)
        filtred_data.drop('lon', axis=1, inplace=True)
        
        if len(filtred_data)>0:
            #Standaryzacja         
            Standard_data=filtred_data.copy()
            
            #Cena
            Standard_data["price"]=Cena.standard(filtred_data,filtred_data["price"])
            
            #Powierzchnia
            Standard_data["area"]=Powierzchnia.standard(filtred_data,filtred_data["area"])
            
            # Cena za m2
            Standard_data["price for m2"]=CenaZam2.standard(filtred_data,filtred_data["price for m2"])
            
            #lpokoi
            LPokoi.log=True
            Standard_data["rooms"]=LPokoi.standard(filtred_data,filtred_data["rooms"])
            Standard_data["rooms"]=Standard_data["rooms"].apply(LiczStyl, args=[Standard_data["rooms"]])
            
            #pietro
            Pietro.log=True
            Standard_data["floor"]=Pietro.standard(filtred_data,filtred_data["floor"])
            Standard_data["floor"]=Standard_data["floor"].apply(LiczStyl, args=[Standard_data["floor"]])
            
            #Ilosc pieter
            Pietra.log=True
            Standard_data["total_floors"]=Pietra.standard(filtred_data,filtred_data["total_floors"])
            Standard_data["total_floors"]=Standard_data["total_floors"].apply(LiczStyl, args=[Standard_data["total_floors"]])            
           
            Standard_data["Odleglosc"]=Odleglosc.standard(filtred_data,filtred_data["Odleglosc"])           
            
            normalizuj_wagi()
            
            CenWag=Standard_data["price"]*Cena.waga_normal
            PowWag=Standard_data["area"]*Powierzchnia.waga_normal
            CenaZam2Wag=Standard_data["price for m2"]*CenaZam2.waga_normal
            PokWag=Standard_data["rooms"]*LPokoi.waga_normal
            PietWag=Standard_data["floor"]*Pietro.waga_normal
            IlPietWag=Standard_data["total_floors"]*Pietra.waga_normal
            OdlWag=Standard_data["Odleglosc"]*Odleglosc.waga_normal
            
            
            Max_wynik=CenWag.max()+PowWag.max()+CenaZam2Wag.max()+PokWag.max()+PietWag.max()+IlPietWag.max()+OdlWag.max()
            
            Standard_data["Wartoć x waga"]=CenWag+PowWag+CenaZam2Wag+PokWag+PietWag+IlPietWag+OdlWag
            Standard_data["Wynik %"]=Standard_data["Wartoć x waga"]*100/Max_wynik
            Standard_data=Standard_data.sort_values("Wynik %", ascending=False)         
            
            #usuwanie zbędnych kolumn w standard data
            
            Standard_data.drop("district", axis=1, inplace=True)
            Standard_data.drop("street", axis=1, inplace=True)
            Standard_data.drop("house_type", axis=1, inplace=True)
       
        def zapisz(nick,scenariusz):
           
            def save():
                Standard_data.to_excel("C:/Users/gorec/Documents/seminarium/wyniki_badania"+"/"+nick+"/"+scenariusz+"/Dane sdandaryzowane.xlsx")
                            
            if  os.path.exists("C:/Users/gorec/Documents/seminarium/wyniki_badania"+"/"+nick):
                if os.path.exists("C:/Users/gorec/Documents/seminarium/wyniki_badania"+"/"+nick+"/"+scenariusz):
                    save()
                else:
                    os.mkdir("/Users/gorec/Documents/seminarium/wyniki_badania"+"/"+nick+"/"+scenariusz)
                    save()
                
            else:
                os.mkdir("C:/Users/gorec/Documents/seminarium/wyniki_badania"+"/"+nick)
                zapisz(nick, scenariusz)
                
            
        #guzik zapisz do excel tylko bez wiecej kryteriow
        ZapiszButton=tk.Button(root, text="Zapisz",command=zapisz(entry_nick.get(), ScenClicked.get()))
        ZapiszButton.grid(row=0,column=7,pady=1, padx=0)
        
        
        
    def czysc():
        
        #typ
        Typ.clicked.set("For sale")
        
        #pole nazwy użytkownika
        entry_nick.delete(0,(len(entry_nick.get())))
        
        ScenClicked.set("Scenariusz")
        
        #Wyniki
        Wyniki.Clear()
        
        #Dzielnica
        Dzielnice.clear()
        
        #Cena
        Cena.clear()
        Cena.clicked.set(Cena.tabNom[Cena.Des])
        
        #Powierzchnia
        Powierzchnia.clear()
        Powierzchnia.clicked.set(Powierzchnia.tabNom[Powierzchnia.Des])
        
        #WIęcej Krytriów
        #Cena za m2
        CenaZam2.clear()
        CenaZam2.clicked.set(CenaZam2.tabNom[CenaZam2.Des])
        
        #lpokoi
        LPokoi.clear()
        LPokoi.clicked.set(LPokoi.tabNom[LPokoi.Des])
        
        #pietro
        Pietro.clear()
        Pietro.clicked.set(Pietro.tabNom[Pietro.Des])
        
        #iloć kondygnacji
        Pietra.clear()
        Pietra.clicked.set(Pietra.tabNom[Pietra.Des])
        
        #ordzaj zabudowy
        Zabudowa.clear()
        
        #Odleglosc
        Odleglosc.clear()
        Odleglosc.clicked.set(Odleglosc.tabNom[Odleglosc.Des])
         
        

    

        
    #Guzik Szukaj  
    SzukajButton=tk.Button(root, text="Szukaj",command=szukaj)
    SzukajButton.grid(row=0,column=5,pady=1, padx=0)
    
    # Guzik Czysc
    CzyscButton=tk.Button(root, text="Wyczyść",command=czysc)
    CzyscButton.grid(row=0,column=6,pady=1, padx=0)
    CzyscButton.config(pady=1, padx=0, width=8)
    #Więcej Kryteriów
    Wiecej=tk.Button(root, text="Więcej kryteriów:",command=inicjalizacjaKryteriow2)
    Wiecej.grid(row=10,column=0,pady=1, padx=0)
    

root = inicjalizacjaOkienka()
label = inicjalizacjaKryteriow(root)    
root.mainloop() 
"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from os import replace
from DISClib.DataStructures.arraylist import addLast, getElement, size
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import quicksort as qs
from DISClib.Algorithms.Sorting import shellsort as ss
import datetime as dt
import time as chronos
import math
assert cf


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def NewCatalog():
    catalogo = {"Artista":None,
                "Obra": None}
    catalogo["Artista"] = lt.newList()
    catalogo["Obra"] = lt.newList()
    return catalogo
# Funciones para agregar informacion al catalogo
def addArtist(catalogo,Artist):
    lt.addLast(catalogo["Artista"],Artist)
def addArtwork(catalogo,Artwork):
    lt.addLast(catalogo["Obra"],Artwork)
# Funciones para creacion de datos
def ArtworkvArtist(nombre_artista,catalogo):
    obras_artista = {}
    total_obras = 0
    total_medios = 0
    posicion = 0
    while posicion < lt.size(catalogo["Artista"]) and nombre_artista != lt.getElement(catalogo["Artista"],posicion)["DisplayName"]:
        posicion += 1
    constituenID_artista = lt.getElement(catalogo["Artista"],posicion)["ConstituentID"]
    print(constituenID_artista)
    constituenID_artista = "[" + constituenID_artista + "]"
    print(constituenID_artista)
    posicion = 0
    while posicion < lt.size(catalogo["Obra"]):
        obra = lt.getElement(catalogo["Obra"],posicion)
        print(posicion)
        if obra["ConstituentID"] == constituenID_artista:
            if obra["Medium"] in obras_artista:
                lt.addLast(obras_artista[obra["Medium"]],obra)
            else:
                obras_artista[obra["Medium"]] = lt.newList()
                lt.addLast(obras_artista[obra["Medium"]],obra["Medium"])
                total_medios += 1
            total_obras += 1
        posicion += 1
    print(obras_artista)
    medio_n = 0
    nombre = ""
    for llave in obras_artista:
        if lt.size(obras_artista[llave]) > medio_n:
            medio_n = lt.size(obras_artista[llave])
            nombre = llave
    return (total_obras,total_medios,nombre,obras_artista[nombre])
    


def ArtworkvNacionality(catalogo):
    
    cat_obras = catalogo["Obra"]
    cat_artistas = catalogo["Artista"]
    size = lt.size(cat_obras)
    obras_nacionalidad = {}
    pos = 1

    
    while pos<=size:
        obra = lt.getElement(cat_obras,pos)
        ids=obra['ConstituentID']
        ids=ids.replace(']','').replace('[','').split(',')
        for id in ids:
            nacionalidad = nationality_artist(cat_artistas,id)
            if nacionalidad not in obras_nacionalidad:
                obras_nacionalidad[nacionalidad] = lt.newList()
            lt.addLast(obras_nacionalidad[nacionalidad],obra)
        pos+=1

    
    
    orden=lt.newList("ARRAY_LIST")
    repe=lt.newList("ARRAY_LIST")
    dic_top={}
    mayor=1000000
    n=1
    llave=""
    
    while n<=10:
        anterior = mayor
        aux=0
        pais = ""
        for i in obras_nacionalidad:
            valor =lt.size(obras_nacionalidad[i])
            if aux <= valor and (i not in repe['elements']):
                mayor = valor
                aux = valor
                llave = "top " + str(n)
                lt.addLast(orden,valor)
                pais = i
                dic_top[llave]=pais + " : " + str(valor)
        if n == 1:
            top_1 = pais
        lt.addLast(repe,pais)
        n+=1

    n=5
    while n>=1:
        top = dic_top["top " + str(n)]
        lt.addLast(orden,top)
        n-=1

    centinela = True
    while centinela:
        for i in obras_nacionalidad:
            if i == top_1:
                obras_top = obras_nacionalidad[i]
                centinela = False
    


    
    return orden, obras_top


# Funciones de consulta
def dateartist(año_inicio,año_final,catalogo):
    aux = catalogo["Artista"]
    artistas_rango = lt.newList()
    size = lt.size(aux)
    cantidad = 0
    n = 0

    while n < size:
        artista = lt.getElement(aux,n)
        nacimiento = int(artista["BeginDate"])
        if año_inicio<=nacimiento<=año_final:
            lt.addLast(artistas_rango,artista)
            cantidad+=1
        n+=1
    
    artistas_sorted = merge_sort(artistas_rango,cantidad,compareBeginDate)
    artistas_sorted = artistas_sorted[1]
    primeros_3 = lt.newList()
    lt.addLast(primeros_3,lt.getElement(artistas_sorted,lt.size(artistas_sorted)))
    lt.addLast(primeros_3,lt.getElement(artistas_sorted,lt.size(artistas_sorted)-1))
    lt.addLast(primeros_3,lt.getElement(artistas_sorted,lt.size(artistas_sorted)-2))
    ultimos_3 = lt.newList()
    lt.addLast(ultimos_3,lt.getElement(artistas_sorted,2))
    lt.addLast(ultimos_3,lt.getElement(artistas_sorted,1))
    lt.addLast(ultimos_3,lt.getElement(artistas_sorted,0))
    return(cantidad,primeros_3,ultimos_3)



def dateArtwork(fecha_inicio,fecha_fin,catalogo):
    obras_rango = lt.newList()
    obras_purchase = 0
    posicion = 0
    while posicion < lt.size(catalogo["Obra"]):
        obra = lt.getElement(catalogo["Obra"],posicion)
        fecha = obra["Date"]
        if fecha == "":
            fecha = -1
        if int(fecha) > fecha_inicio and int(fecha) < fecha_fin:
            lt.addLast(obras_rango,obra)
            if obra["CreditLine"] == "Purchase":
                obras_purchase += 1
        posicion += 1
    tamaño = lt.size(obras_rango)
    print("entrando en la parte dura: ")
    obras_sorted = merge_sort(obras_rango,tamaño,compareData)
    obras_sorted = obras_sorted[1]
    primeras_3 = lt.newList()
    lt.addLast(primeras_3,lt.getElement(obras_sorted,lt.size(obras_sorted)))
    lt.addLast(primeras_3,lt.getElement(obras_sorted,lt.size(obras_sorted)-1))
    lt.addLast(primeras_3,lt.getElement(obras_sorted,lt.size(obras_sorted)-2))
    ultimos_3 = lt.newList()
    lt.addLast(primeras_3,lt.getElement(obras_sorted,2))
    lt.addLast(primeras_3,lt.getElement(obras_sorted,1))
    lt.addLast(primeras_3,lt.getElement(obras_sorted,0))
    return(tamaño, obras_purchase,primeras_3,ultimos_3)


def nationality_artist(catalogo,id):
    nacionalidad = ""
    aux = ""
    n=0
    while (lt.size(catalogo)>n) and (aux!=id):
        artista = lt.getElement(catalogo,n)
        aux = artista["ConstituentID"]
        if aux == id:
            nacionalidad = artista["Nationality"]
        n+=1

    return nacionalidad


def departmentArtworks(catalogo,departamento):
    aux = catalogo["Obra"]
    obras_depart = lt.newList()
    size = lt.size(aux)
    cantidad = 0
    n = 0

    while n <= size:
        obra = lt.getElement(aux,n)
        cmp_depart = obra["Department"]
        if departamento==cmp_depart:
            lt.addLast(obras_depart,obra)
            cantidad+=1
        n+=1
    
    print("se han terminado de contabilizar las obras pertenecientes al departamento: "+departamento)
    print("se comenzará a calcular costos y pesos, por favor espere")

    n = 0
    peso_total = 0
    costo_total = 0
    size = lt.size(obras_depart)
    while  n <= size:
        obra = lt.getElement(obras_depart,n)
        dimensiones = lt.newList()
        costo_medida = 1
        costo_peso = 0
        costo_obra = 0
        medidas = 1
        if obra["Weight (kg)"] != "":
            peso_obra = float(obra["Weight  (kg)"])
            costo_peso = peso_obra*72
            peso_total += peso_obra

        if obra["Height (cm)"] != "":
            medida = float(obra["Height (cm)"])/100
            lt.addLast(dimensiones,medida)
        if obra["Length (cm)"] != "":
            medida = float(obra["Length (cm)"])/100
            lt.addLast(dimensiones,medida)
        if obra["Width (cm)"] != "":
            medida = float(obra["Width (cm)"])/100
            lt.addLast(dimensiones,medida)
        lt.addLast(dimensiones,1)

        if lt.size(dimensiones) != 1:
            for i in range(lt.size(dimensiones)):
                medidas*= lt.getElement(dimensiones,i)
                costo_medida = medidas*72

        costos=lt.newList()
        lt.addLast(costos,costo_peso)
        lt.addLast(costos,costo_medida)
        if (lt.size(dimensiones)==1) and (costo_peso == 0):
            lt.addLast(costos,48)

        if (lt.size(dimensiones)==1) and (obra["Diameter (cm)"]!=""):
            area_volumen =3.14*((float(obra["Diameter (cm)"])/200)^2)
            if obra["Height (cm)"]!="":
                area_volumen = area_volumen*(float(obra["Height (cm)"])/100)
            costo_circular = area_volumen*72
        lt.addLast(costos,costo_circular)
                
        

        for i in range(lt.size(costos)+1):
            if lt.getElement(costos,i) > costo_obra:
                costo_obra=lt.getElement(costos,i)
        costo_total+=costo_obra
        if costo_obra==0:
            costo_obra=48
        obra["costo"]=costo_obra

        
        n+=1
    for i in range(lt.size(obras_depart)+1):
        obra=lt.getElement(obras_depart,i)
        print(obra["costo"])

    obras_sorted = merge_sort(obras_depart,cantidad,compareData)
    obras_sorted = obras_sorted[1]
    antiguas_5 = lt.newList()
    lt.addLast(antiguas_5,lt.getElement(obras_sorted,lt.size(obras_sorted)))
    lt.addLast(antiguas_5,lt.getElement(obras_sorted,lt.size(obras_sorted)-1))
    lt.addLast(antiguas_5,lt.getElement(obras_sorted,lt.size(obras_sorted)-2))
    lt.addLast(antiguas_5,lt.getElement(obras_sorted,lt.size(obras_sorted)-3))
    lt.addLast(antiguas_5,lt.getElement(obras_sorted,lt.size(obras_sorted)-4))
    
    obras_sorted = merge_sort(obras_depart,cantidad,comparePrice)
    obras_sorted = obras_sorted[1]
    costosas_5 = lt.newList()
    lt.addLast(costosas_5,lt.getElement(obras_sorted,4))
    lt.addLast(costosas_5,lt.getElement(obras_sorted,3))
    lt.addLast(costosas_5,lt.getElement(obras_sorted,2))
    lt.addLast(costosas_5,lt.getElement(obras_sorted,1))
    lt.addLast(costosas_5,lt.getElement(obras_sorted,0))
    
    

    return cantidad,costo_total,peso_total,antiguas_5,costosas_5

def nueva_expo(catalogo,año_inicio,año_fin,area):
    obras_expo = lt.newList()
    area_restante = area
    posicion = 0
    while posicion <= lt.size(catalogo["Obra"]) and area_restante > 0:
        obra = lt.getElement(catalogo["Obra"],posicion)
        if obra["Date"] != "" and int(obra["Date"]) > año_inicio and int(obra["Date"]) < año_fin:
            diametro = obra["Diameter (cm)"]
            largo = obra["Height (cm)"]
            ancho = obra["Width (cm)"]
            area_obra = -1
            if diametro != "":
                area_obra = math.pi * (float(diametro)/2)**2
            elif largo != "" and ancho != "":
                area_obra = float(largo) * float(ancho)
            if area_obra != -1 and area_restante - area_obra >= 0:
                lt.addLast(obras_expo,obra)
                area_restante -= area_obra
        posicion += 1
    total_obras = lt.size(obras_expo)
    obras_expo_sorted = merge_sort(obras_expo,total_obras,compareData)[1]
    area_utilizada = (area - area_restante) * (1/10000)
    primeras_5 = lt.newList()
    lt.addLast(primeras_5,lt.getElement(obras_expo_sorted,lt.size(obras_expo_sorted)))
    lt.addLast(primeras_5,lt.getElement(obras_expo_sorted,lt.size(obras_expo_sorted)-1))
    lt.addLast(primeras_5,lt.getElement(obras_expo_sorted,lt.size(obras_expo_sorted)-2))
    lt.addLast(primeras_5,lt.getElement(obras_expo_sorted,lt.size(obras_expo_sorted)-3))
    lt.addLast(primeras_5,lt.getElement(obras_expo_sorted,lt.size(obras_expo_sorted)-4))
    ultimas_5 = lt.newList()
    lt.addLast(ultimas_5,lt.getElement(obras_expo_sorted,1))
    lt.addLast(ultimas_5,lt.getElement(obras_expo_sorted,2))
    lt.addLast(ultimas_5,lt.getElement(obras_expo_sorted,3))
    lt.addLast(ultimas_5,lt.getElement(obras_expo_sorted,4))
    lt.addLast(ultimas_5,lt.getElement(obras_expo_sorted,5))
    return(total_obras,area_utilizada,primeras_5,ultimas_5)
def encontrar_artista(catalogo,constituent_ID):
    posicion = 0
    while posicion < lt.size(catalogo["Artista"]) and constituent_ID != lt.getElement(catalogo["Artista"],posicion)["ConstituentID"]:
        posicion += 1
    artista = lt.getElement(catalogo["Artista"],posicion)["DisplayName"]
    return artista

            

# Funciones utilizadas para comparar elementos dentro de una lista
def compareBeginDate(obra1,obra2):
    orden = None
    if (obra1["BeginDate"]!="") and (obra2["BeginDate"]!=""):
        orden = (int(obra1["BeginDate"]) > int(obra2["BeginDate"]))
    return orden

def comparePrice(obra1,obra2):
    orden = (int(obra1["costo"]) > int(obra2["costo"]))
    return orden

def compareDateAcquired(obra1,obra2):
    orden = None
    if (obra1["DateAcquired"]!="") and (obra2["DateAcquired"]!=""):
        orden = (dt.datetime.strptime(obra1["DateAcquired"],"%Y-%m-%d") > dt.datetime.strptime(obra2["DateAcquired"],"%Y-%m-%d"))
    return orden

def compareData(obra1,obra2):
    orden = None
    if (obra1["Date"]!="") and (obra2["Date"]!=""):
        orden = (int(obra1["Date"]) > int(obra2["Date"]))
    return orden
# Funciones de ordenamiento
def insertion_sort(catalogo,size,cmpfuncion):
    sub_list = lt.subList(catalogo, 1, size)
    start_time = chronos.process_time()
    sorted_list = ins.sort(sub_list,cmpfuncion)
    stop_time = chronos.process_time()
    time = (stop_time - start_time)*1000
    return (time,sorted_list)

def merge_sort(catalogo,size,cmpfuncion):
    sub_list = lt.subList(catalogo, 1, size)
    start_time = chronos.process_time()
    sorted_list = ms.sort(sub_list,cmpfuncion)
    stop_time = chronos.process_time()
    time = (stop_time - start_time)*1000
    return (time,sorted_list)

def quick_sort(catalogo,size,cmpfuncion):
    sub_list = lt.subList(catalogo, 1, size)
    start_time = chronos.process_time()
    sorted_list = qs.sort(sub_list,cmpfuncion)
    stop_time = chronos.process_time()
    time = (stop_time - start_time)*1000
    return (time,sorted_list)

def shell_sort(catalogo,size,cmpfuncion):
    sub_list = lt.subList(catalogo, 1, size)
    start_time = chronos.process_time()
    sorted_list = ss.sort(sub_list,cmpfuncion)
    stop_time = chronos.process_time()
    time = (stop_time - start_time)*1000
    return (time,sorted_list)

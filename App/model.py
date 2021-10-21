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
from DISClib.ADT.stack import top
from DISClib.DataStructures.arraylist import addLast, getElement, size
from DISClib.DataStructures.chaininghashtable import get
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import quicksort as qs
from DISClib.Algorithms.Sorting import shellsort as ss
from DISClib.DataStructures import mapentry as ma
from DISClib.DataStructures import orderedmapstructure as om
from datetime import timedelta as td
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
                "Obra": None,
                "medio": mp.newMap(maptype='CHAINING',loadfactor=8.00),
                "Nacionalidad" : mp.newMap(maptype='CHAINING',loadfactor=8.00),
                "Nacimiento" : mp.newMap(maptype='CHAINING',loadfactor=8.00),
                "Adquisicion" : mp.newMap(maptype='CHAINING',loadfactor=8.00),
                "Obras Artista" : mp.newMap(maptype='CHAINING',loadfactor=8.00) }
    catalogo["Artista"] = mp.newMap()  
    catalogo["Obra"] = mp.newMap()
    catalogo["Departamento"] = mp.newMap()
    return catalogo
# Funciones para agregar informacion al catalogo
def addArtist(catalogo,Artist):
    mp.put(catalogo["Artista"],Artist["ConstituentID"].replace(']','').replace(' ','').replace('[',''),Artist)
def addArtwork(catalogo,Artwork):
    artistas = Artwork["ConstituentID"]
    artistas = artistas.replace(']','').replace(' ','').replace('[','').split(',')
    for id in artistas:
        if mp.contains(catalogo["Obra"],id)==False:
            lista = lt.newList(datastructure="ARRAY_LIST")
        else:
            tupla = mp.get(catalogo["Obra"],id)
            lista = ma.getValue(tupla)
        lt.addLast(lista,Artwork)
        mp.put(catalogo["Obra"],id,lista)

def addNacionality(catalogo,Artwork):
    """
    Creación mapa de obras por su nacionalidad
    """
    artistas = Artwork["ConstituentID"]
    artistas = artistas.replace(']','').replace(' ','').replace('[','').split(',')
    for id in artistas:
        artista = mp.get(catalogo["Artista"],id)
        nacionalidad = ma.getValue(artista)["Nationality"]

        if mp.contains(catalogo["Nacionalidad"],nacionalidad)==False:
            obras = lt.newList()
            lt.addLast(obras,Artwork)
            mp.put(catalogo["Nacionalidad"],nacionalidad,obras)
    
        else:
            tupla = mp.get(catalogo["Nacionalidad"],nacionalidad)
            lista = tupla["value"]
            lt.addLast(lista,Artwork)
            mp.put(catalogo["Nacionalidad"],nacionalidad,lista)


def addMedio(catalogo,Artwork):
    """
    Creación mapa de obras por su medio
    """
    if mp.contains(catalogo["medio"],Artwork["Medium"])==False:
        obras = lt.newList()
        lt.addLast(obras,Artwork)
        mp.put(catalogo["medio"],Artwork["Medium"],obras)
    
    else:
        tupla = mp.get(catalogo["medio"],Artwork["Medium"])
        lista = tupla["value"]
        lt.addLast(lista,Artwork)
        mp.put(catalogo["medio"],Artwork["Medium"],lista)

def addNacimiento(catalogo,Artist):
    """
    Creación mapa de artistas por su fecha de nacimiento
    """
    nacimiento = Artist["BeginDate"]
    if mp.contains(catalogo["Nacimiento"],nacimiento)==False:
        artistas = lt.newList()
        lt.addLast(artistas,Artist)
        mp.put(catalogo["Nacimiento"],nacimiento,artistas)
    else:
        tupla = mp.get(catalogo["Nacimiento"],nacimiento)
        artistas = ma.getValue(tupla)
        lt.addLast(artistas,Artist)
        mp.put(catalogo["Nacimiento"],nacimiento,artistas)
    
def addDataAcquired(catalogo,Artwork):
    """
    Creación mapa de obras por su fecha de adquisicion
    """
    if Artwork["DateAcquired"] != "":
        fecha = dt.datetime.strptime(Artwork["DateAcquired"],"%Y-%m-%d")
    else:
        fecha = dt.datetime.strptime("9999-12-31","%Y-%m-%d")
    if mp.contains(catalogo["Adquisicion"],fecha)==False:
        obras = lt.newList()
        lt.addLast(obras,Artwork)
    else:
        tupla = mp.get(catalogo["medio"],Artwork["Medium"])
        obras = ma.getValue(tupla)
        lt.addLast(obras,Artwork)
    mp.put(catalogo["Adquisicion"],fecha,obras)

def addArtworkxArtist(catalogo,Artwork):
    artistas = Artwork["ConstituentID"]
    artistas = artistas.replace(']','').replace(' ','').replace('[','').split(',')
    for id in artistas:
        artista = ma.getValue(mp.get(catalogo["Artista"],id))
        nombre = artista["DisplayName"]

        if mp.contains(catalogo["Obras Artista"],nombre)==False:
            obras = lt.newList()
            lt.addLast(obras,Artwork)
        else:
            tupla = mp.get(catalogo["Obras Artista"],nombre)
            obras = ma.getValue(tupla)
            lt.addLast(obras,Artwork)
        mp.put(catalogo["Obras Artista"],nombre,obras)

def addDepartamento(catalogo,Artwork):
    """
    Creación mapa de obras por su departamento
    """
    if mp.contains(catalogo["Departamento"],Artwork["Department"])==False:
        obras = lt.newList()
        lt.addLast(obras,Artwork)
        mp.put(catalogo["Departamento"],Artwork["Department"],obras)

    else:
        tupla = mp.get(catalogo["Departamento"],Artwork["Department"])
        lista = tupla["value"]
        lt.addLast(lista,Artwork)
        mp.put(catalogo["Departamento"],Artwork["Department"],lista)

# Funciones para creacion de datos
def ArtworkvArtist(nombre_artista,catalogo):
    start_time = chronos.process_time()
    medios = mp.newMap()
    if mp.contains(catalogo["Obras Artista"],nombre_artista)==True:
        obras = ma.getValue(mp.get(catalogo["Obras Artista"],nombre_artista))
        obras_totales = lt.size(obras)
        for obra in lt.iterator(obras):
            if obra["Medium"] != "":
                if mp.contains(medios,obra["Medium"])==False:
                    obras_medio = lt.newList(datastructure="ARRAY_LIST")
                else:
                    obras_medio = ma.getValue(mp.get(medios,obra["Medium"]))
                lt.addLast(obras_medio,obra)
                mp.put(medios,obra["Medium"],obras_medio)
        total_medios = mp.size(medios)
        llaves = mp.keySet(medios)
        mayor = ""
        n_mayor = 0
        for medio in lt.iterator(llaves):
            if lt.size(ma.getValue(mp.get(medios,medio))) > n_mayor:
                mayor = medio
                n_mayor = lt.size(ma.getValue(mp.get(medios,medio)))
        if n_mayor > 4:
            primeras_3 = lt.newList(datastructure="ARRAY_LIST")
            for posicion in range(1,4):
                lt.addLast(primeras_3,lt.getElement(ma.getValue(mp.get(medios,mayor)),posicion))
            ultimas_3 = lt.newList(datastructure="ARRAY_LIST")
            for posicion in range(lt.size(ma.getValue(mp.get(medios,mayor)))-2,lt.size(ma.getValue(mp.get(medios,mayor)))+1):
                lt.addLast(ultimas_3,lt.getElement(ma.getValue(mp.get(medios,mayor)),posicion))
        else:
            primeras_3 = ma.getValue(mp.get(medios,mayor))
            ultimas_3 = ma.getValue(mp.get(medios,mayor))
    stop_time = chronos.process_time()
    time = (stop_time - start_time)*1000
    print("se demoro: ", time)
    return (obras_totales,total_medios,mayor,primeras_3,ultimas_3)

def artista_prolifico(num_artista,año_inicial,año_fina,catalogo):
    start_time = chronos.process_time()
    fecha = año_inicial
    artistas = lt.newList(datastructure="ARRAY_LIST")
    nartistas = 0
    while fecha <= año_fina and nartistas < num_artista:
        adquisiciones = mp.get(catalogo["Nacimiento"],str(fecha))
        if adquisiciones != None:
            adquisiciones = ma.getValue(adquisiciones)
            for artista in lt.iterator(adquisiciones):
                lt.addLast(artistas,artista["ConstituentID"])
                nartistas += 1
        fecha += 1
    
    mayor = 0
    nombre = ""
    fecha_nacimiento = 0
    genero = ""
    id = ""
    for artista in lt.iterator(artistas):
        if mp.get(catalogo["Obra"],artista) != None:
            obras = ma.getValue(mp.get(catalogo["Obra"],artista))
            if  lt.size(obras) > mayor:
                id = artista
                mayor = lt.size(obras)
                nombre = ma.getValue(mp.get(catalogo["Artista"],artista))["DisplayName"]
                fecha_nacimiento = ma.getValue(mp.get(catalogo["Artista"],artista))["BeginDate"]
                genero = ma.getValue(mp.get(catalogo["Artista"],artista))["Gender"]
    medios = mp.newMap()
    for obra in lt.iterator(ma.getValue(mp.get(catalogo["Obra"],id))):
        if mp.contains(medios,obra["Medium"])==False:
            obras_medio = lt.newList(datastructure="ARRAY_LIST")
        else:
            tupla = mp.get(medios,obra["Medium"])
            obras_medio = ma.getValue(tupla)
        lt.addLast(obras_medio,obra)
        mp.put(medios,obra["Medium"],obras_medio)
    mayor_medio = 0
    nombre_medio = ""
    for medio in lt.iterator(mp.keySet(medios)):
        if mp.get(medios,medio) != None:
            obras = ma.getValue(mp.get(medios,medio))
            if  lt.size(obras) > mayor_medio:
                mayor_medio = lt.size(obras)
                nombre_medio = medio
    tamaño = mp.size(medios)
    stop_time = chronos.process_time()
    time = (stop_time - start_time)*1000
    print("se demoro: ", time)
    return (nombre,fecha_nacimiento,genero,mayor,tamaño,nombre_medio,ma.getValue((mp.get(medios,nombre_medio))))

def ArtworkvNacionality(catalogo):
    start_time = chronos.process_time()
    nacionalidades = catalogo["Nacionalidad"]
    llaves = mp.keySet(nacionalidades)
    top_10 = lt.newList()


    n=0
    while n<10:
        mayor = 0
        obras_mayor = None
        nacio_mayor = ""
        n2 = 0
        tamaño = lt.size(llaves)
        while n2<=tamaño:
            nacio = lt.getElement(llaves,n2)
            if nacio !="" and nacio!="Nationality unknown":
                aux = mp.get(nacionalidades,nacio)
                if aux != None:
                    obras = aux["value"]
                    size = lt.size(obras)
                    if size > mayor:
                        mayor = size
                        obras_mayor = obras
                        nacio_mayor = nacio
            n2+=1
        if n == 0:
            obras_top = obras_mayor
        lt.addLast(top_10,nacio_mayor)
        lt.removeFirst(llaves)
        mp.remove(nacionalidades,nacio_mayor)
        n+=1


    primeras_3 = lt.newList(datastructure="ARRAY_LIST")
    for posicion in range(4):
        lt.addLast(primeras_3,lt.getElement(obras_top,posicion))
    ultimas_3 = lt.newList(datastructure="ARRAY_LIST")
    for posicion in range(lt.size(obras_top)-3,lt.size(obras_top)):
        lt.addLast(ultimas_3,lt.getElement(obras_top,posicion))

    stop_time = chronos.process_time()
    time = (stop_time - start_time)*1000
    print("se demoro: ", time)
    return top_10, primeras_3, ultimas_3


def tops(cantidad,mapa):
    start_time = chronos.process_time()
    top_10 = lt.newList()
    obras_top = None
    
    n=0
    while n<10:
        llave = lt.getElement(cantidad,n)
        aux = mp.get(mapa,llave)
        obras = aux["value"]
        nacio = lt.getElement(obras,lt.size(obras))
        if n == 0:
            obras_top = obras
        lt.addLast(top_10,nacio)
        n+=1

    stop_time = chronos.process_time()
    time = (stop_time - start_time)*1000
    print("se demoro: ", time)
    return top_10, obras_top


# Funciones de consulta
def dateartist(año_inicio,año_final,catalogo):  
    start_time = chronos.process_time()
    artistas = lt.newList(datastructure="ARRAY_LIST")
    año = año_inicio
    num_artistas = 0
    while año <= año_final:
        nacimientos = mp.get(catalogo["Nacimiento"],str(año))
        if nacimientos != None:
            nacimientos = ma.getValue(nacimientos)
            for artista in lt.iterator(nacimientos):
                lt.addLast(artistas,artista)
            num_artistas += lt.size(nacimientos)
        año += 1
    
    primeras_3 = lt.newList(datastructure="ARRAY_LIST")
    for posicion in range(4):
        lt.addLast(primeras_3,lt.getElement(artistas,posicion))
    ultimas_3 = lt.newList(datastructure="ARRAY_LIST")
    for posicion in range(lt.size(artistas)-3,lt.size(artistas)):
        lt.addLast(ultimas_3,lt.getElement(artistas,posicion))
    stop_time = chronos.process_time()
    time = (stop_time - start_time)*1000
    print("se demoro: ", time)
    return (num_artistas,primeras_3,ultimas_3)



def dateArtwork(fecha_inicio,fecha_fin,catalogo):
    start_time = chronos.process_time()
    fecha = fecha_inicio
    obras = lt.newList(datastructure="ARRAY_LIST")
    purchase = 0
    num_obras = 0
    while fecha <= fecha_fin:
        adquisiciones = mp.get(catalogo["Adquisicion"],fecha)
        if adquisiciones != None:
            adquisiciones = ma.getValue(adquisiciones)
            for obra in lt.iterator(adquisiciones):
                lt.addLast(obras,obra)
                if obra["CreditLine"] == "Purchase":
                    purchase += 1
            num_obras += lt.size(adquisiciones)
        fecha += dt.timedelta(1,0,0)
    
    primeras_3 = lt.newList(datastructure="ARRAY_LIST")
    for posicion in range(1,4):
        lt.addLast(primeras_3,lt.getElement(obras,posicion))
    ultimas_3 = lt.newList(datastructure="ARRAY_LIST")
    for posicion in range(lt.size(obras)-3,lt.size(obras)):
        lt.addLast(ultimas_3,lt.getElement(obras,posicion))
    stop_time = chronos.process_time()
    time = (stop_time - start_time)*1000
    print("se demoro: ", time)
    return (num_obras, purchase, primeras_3,ultimas_3)


def departmentArtworks(catalogo,departamento):
    start_time = chronos.process_time()
    tupla = mp.get(catalogo["Departamento"],departamento)
    obras = tupla["value"]
    size = lt.size(obras)


    print("se han terminado de contabilizar las obras pertenecientes al departamento: "+departamento)
    print("se comenzará a calcular costos y pesos, por favor espere")

    n = 0
    peso_total = 0
    costo_total = 0
    while  n <= size:
        obra = lt.getElement(obras,n)
        dimensiones = lt.newList(datastructure="ARRAY_LIST")
        costo_medida = 1
        costo_peso = 0
        costo_obra = 0
        medidas = 1
        if obra["Weight (kg)"] != "":
            peso_obra = float(obra["Weight (kg)"])
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
                medidas= lt.getElement(dimensiones,i)
                costo_medida = medidas

        costos=lt.newList()
        lt.addLast(costos,costo_peso)
        lt.addLast(costos,costo_medida)
        if (lt.size(dimensiones)==1) and (costo_peso == 0):
            lt.addLast(costos,48)

        if (lt.size(dimensiones)==1) and (obra["Diameter (cm)"]!=""):
            diametro = float(obra["Diameter (cm)"])
            area_volumen =3.14*((diametro/200)**2)
            if obra["Height (cm)"]!="":
                area_volumen = area_volumen(float(obra["Height (cm)"])/100)
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
    for i in range(lt.size(obras)+1):
        obra=lt.getElement(obras,i)
        obras_sorted = merge_sort(obras,size,compareData)
    obras_sorted = obras_sorted[1]
    antiguas_5 = lt.newList()
    lt.addLast(antiguas_5,lt.getElement(obras_sorted,lt.size(obras_sorted)))
    lt.addLast(antiguas_5,lt.getElement(obras_sorted,lt.size(obras_sorted)-1))
    lt.addLast(antiguas_5,lt.getElement(obras_sorted,lt.size(obras_sorted)-2))
    lt.addLast(antiguas_5,lt.getElement(obras_sorted,lt.size(obras_sorted)-3))
    lt.addLast(antiguas_5,lt.getElement(obras_sorted,lt.size(obras_sorted)-4))

    obras_sorted = merge_sort(obras,size,compareData)
    obras_sorted = obras_sorted[1]
    costosas_5 = lt.newList()
    lt.addLast(costosas_5,lt.getElement(obras_sorted,4))
    lt.addLast(costosas_5,lt.getElement(obras_sorted,3))
    lt.addLast(costosas_5,lt.getElement(obras_sorted,2))
    lt.addLast(costosas_5,lt.getElement(obras_sorted,1))
    lt.addLast(costosas_5,lt.getElement(obras_sorted,0))

 


    stop_time = chronos.process_time()
    time = (stop_time - start_time)*1000
    print("se demoro: ", time)
    return size,costo_total,peso_total,antiguas_5,costosas_5

def encontrar_artista(catalogo,constituent_ID):
    start_time = chronos.process_time()
    posicion = 0
    while posicion < lt.size(catalogo["Artista"]) and constituent_ID != lt.getElement(catalogo["Artista"],posicion)["ConstituentID"]:
        posicion += 1
    artista = lt.getElement(catalogo["Artista"],posicion)["DisplayName"]
    stop_time = chronos.process_time()
    time = (stop_time - start_time)*1000
    print("se demoro: ", time)
    return artista


def antiguedad_tecntica(catalogo,tecnica,top):
    start_time = chronos.process_time()
    obras = mp.get(catalogo["medio"],tecnica)
    obras = obras["value"]
    
    obras_sorted = merge_sort(obras,lt.size(obras),compareData)
    obras_sorted = obras_sorted[1]

    n=1
    aux = lt.newList()
    while n<top:
        lt.addLast(aux,lt.getElement(obras_sorted,n))
        n+=1

    stop_time = chronos.process_time()
    time = (stop_time - start_time)*1000
    print("se demoro: ", time)
    return obras
            

# Funciones utilizadas para comparar elementos dentro de una lista
def compareKey(key1,key2):
    orden = (int(key1) > int(key2))
    return orden

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

"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listado cronologico de artistas")
    print("3- Listado cronologico de adquisiciones")
    print("4- Clasificar las obras de un artista por tecnica")
    print("5- Clasificar obras por nacionalidad de sus creadores")
    print("6- Mover Obra de un departamento")
    print("7- Proponer una nueva exposición")
    print("8- Organizar una muestra de obras por fecha")
    print("0- Salir")


"""
Ejecución de funciones
"""

def ejecutar_dateartist(catalogo):
    año_inicio = int(input("Ingrese el año en el que desea iniciar: "))
    año_final = int(input("Ingrese el año en el que desea terminar: "))
    cantidad,primeros_3,ultimos_3 = controller.initdateartist(año_inicio,año_final,catalogo)
    print("En ese rango de años nacieron un total de: ",cantidad," artistas.")
    print("Los primeros 3 en nacer fueron:")
    n = 1
    while n <= lt.size(primeros_3):
        artista = lt.getElement(primeros_3,n)
        print("*"*50)
        print("Nombre : ", artista["DisplayName"])
        print("Fecha de Nacimiento : ", artista["BeginDate"])
        death = artista["EndDate"]
        if artista["EndDate"]== "0":
            death = "Desconocida"
        print("Fecha de Fallecimiento : ",death)
        print("Nacionalidad : ", artista["Nationality"])
        print("Género : ", artista["Gender"])
        n += 1
    n = 1
    print("Los últimos 3 en nacer fueron:")
    while n <= lt.size(ultimos_3):
        artista = lt.getElement(ultimos_3,n)
        print("*"*50)
        print("Nombre : ", artista["DisplayName"])
        print("Fecha de nacimiento : ", artista["BeginDate"])
        death = "Fecha de Fallecimiento : ", artista["EndDate"]
        if artista["EndDate"]== "0":
            death = "Fecha de Fallecimiento : Desconocida"
        print(death)
        print("Nacionalidad : ", artista["Nationality"])
        print("Género : ", artista["Gender"])
        n += 1


def ejecutar_nacionalidad(catalogo):
    orden,obras_top = controller.initArtwokvNationality(catalogo)
    print("El top 10 de las nacionalidad con más obras de arte, son:")
    print(lt.getElement(orden,lt.size(orden)))
    print(lt.getElement(orden,lt.size(orden)-1))
    print(lt.getElement(orden,lt.size(orden)-2))
    print(lt.getElement(orden,lt.size(orden)-3))
    print(lt.getElement(orden,lt.size(orden)-4))
    print(lt.getElement(orden,lt.size(orden)-5))
    print(lt.getElement(orden,lt.size(orden)-6))
    print(lt.getElement(orden,lt.size(orden)-7))
    print(lt.getElement(orden,lt.size(orden)-8))
    print(lt.getElement(orden,lt.size(orden)-9))
    print("*"*50)

    n = 1
    print("Las obras pertenecientes al top 1 son: ")
    while n <= lt.size(obras_top):
        obra = lt.getElement(obras_top,n)
        print("*"*50)
        print("Titulo : ", obra["Title"])

        ids=obra["ConstituentID"]
        ids=ids.replace(']','').replace('[','').split(',')
        for id in ids:
            aux = ""
            n2=0
            while (lt.size(catalogo["Artista"])>n2) and (aux!=id):
                artista = lt.getElement(catalogo,n2)
                aux = artista["ConstituentID"]
                if aux == id:
                    print("Artista : ", artista["DisplayName"])
                n2+=1

        print("Fecha de la obra : ", obra["Date"])
        print("Medio : ", obra["Medium"])
        print("Dimensiones : ", obra["Dimensions"])
        n += 1


def ejecutar_departmentartworks(catalogo):
    departamento = input("Ingrese el departamento a transportar: ")
    cantidad,costo_total,peso_total,antiguas_5,costosas_5 = controller.initdepartmentArtworks(catalogo,departamento)
    print("la cantidad de obras del departamento "+departamento+"que se han de transportar son "+cantidad)
    print("Valor promedio (USD): "+costo_total)
    print("Las 5 obras más antiguas son: ")
    n=1
    while n <= lt.size(antiguas_5):
        obra = lt.getElement(antiguas_5,n)
        print("*"*50)
        print("Titulo : ", obra["Title"])
        ids=obra["ConstituentID"]
        ids=ids.replace(']','').replace('[','').split(',')
        for id in ids:
            aux = ""
            n2=0
            while (lt.size(catalogo["Artista"])>n2) and (aux!=id):
                artista = lt.getElement(catalogo,n2)
                aux = artista["ConstituentID"]
                if aux == id:
                    print("Artista : ", artista["DisplayName"])
                n2+=1
        print("Fecha de la obra : ", obra["Date"])
        print("Medio : ", obra["Medium"])
        print("Dimensiones : ", obra["Dimensions"])
        print("Costo : ", obra["costo"])
        n += 1
    print("Las 5 obras más costosas son: ")
    n=1
    while n <= lt.size(antiguas_5):
        obra = lt.getElement(antiguas_5,n)
        print("*"*50)
        print("Titulo : ", obra["Title"])
        ids=obra["ConstituentID"]
        ids=ids.replace(']','').replace('[','').split(',')
        for id in ids:
            aux = ""
            n2=0
            while (lt.size(catalogo["Artista"])>n2) and (aux!=id):
                artista = lt.getElement(catalogo,n2)
                aux = artista["ConstituentID"]
                if aux == id:
                    print("Artista : ", artista["DisplayName"])
                n2+=1
        print("Fecha de la obra : ", obra["Date"])
        print("Medio : ", obra["Medium"])
        print("Dimensiones : ", obra["Dimensions"])
        print("Costo : ", obra["costo"])
        n += 1
        


catalogo = None
def viewdateartwork():
            año_inicio = int(input("Ingrese el año en el que desea iniciar: "))
            año_final = int(input("Ingrese el año en el que desea terminar: "))
            total_obras, purchase, primeras_3,ultimas_3 = controller.initdateartwork(año_inicio,año_final,catalogo)
            print("En esas fechas ubo: ",total_obras," obras")
            print("De esas obras ",purchase," fueron compradas")
            print("¡¡PRIMEROS 3!!")
            posicion = 1
            while posicion <= lt.size(primeras_3):
                obra = lt.getElement(primeras_3,posicion)
                print("*"*50)
                print("Titulo : ", obra["Title"])
                print("Fecha : ", obra["Date"])
                print("Medio : ", obra["Medium"])
                print("Dimensiones : ",obra["Dimensions"])
                posicion += 1
            posicion = 1
            print("¡¡ULTIMAS 3!!")
            while posicion <= lt.size(ultimas_3):
                obra = lt.getElement(ultimas_3,posicion)
                print("*"*50)
                print("Titulo : ",obra["Title"])
                print("Fecha : ",obra["Date"])
                print("Medio : ",obra["Medium"])
                print("Dimensiones : ",obra["Dimensions"])
                posicion += 1

def viewartworkvartist():
            nombre_artista = input("Ingrese el nombre del artista: ")
            total_obras,total_tecnicas,tecnica_usada,obras_tecnica = controller.initArtworkvArtist(nombre_artista,catalogo)
            print(nombre_artista," hizo ",total_obras," obras")
            print(nombre_artista," uso ", total_tecnicas," tecnicas")
            print(nombre_artista," usaba mayormente ",tecnica_usada," como tecnica")
            posicion = 0
            while posicion < lt.size(obras_tecnica):
                obra = lt.getElement(obras_tecnica,posicion)
                print("*"*25)
                print("Titulo : ",obra["Title"])
                print("Fecha : ",obra["Date"])
                print("Medio : ",obra["Medium"])
                print("Dimensiones : ",obra["Dimensions"])
                posicion += 1

def viewnuevaexpo():
    año_inicio = int(input("En que año desea iniciar: "))
    año_fin = int(input("En que año desea terminar: "))
    area = float(input("Con cuanta area cuenta: "))
    total_obras,area_usada,primeras_5,ultimas_5 = controller.initnuevaexpo(catalogo,año_inicio,año_fin,area)
    print("La exposicion tendria ",total_obras," en total")
    print("La exposicion usarias ", area_usada, "m**2")
    print("¡¡¡PRIMERAS 5!!!")
    posicion = 1
    while posicion <= lt.size(primeras_5):
        obra = lt.getElement(primeras_5,posicion)
        print("*"*50)
        print("Titulo : ", obra["Title"])
        print("Artista: ", controller.encontrar_artista(catalogo,obra["ConstituentID"]))
        print("Fecha : ", obra["Date"])
        print("Clasificacion: ", obra["Classification"])
        print("Medio : ", obra["Medium"])
        print("Dimensiones : ",obra["Dimensions"])
        posicion += 1
    posicion = 1
    print("¡¡ULTIMAS 5!!")
    while posicion <= lt.size(ultimas_5):
        obra = lt.getElement(ultimas_5,posicion)
        print("*"*50)
        print("Titulo : ", obra["Title"])
        print("Artista: ", controller.encontrar_artista(catalogo,obra["ConstituentID"]))
        print("Fecha : ", obra["Date"])
        print("Clasificacion: ", obra["Classification"])
        print("Medio : ", obra["Medium"])
        print("Dimensiones : ",obra["Dimensions"])
        posicion += 1

def viewsort():
    print("¿Que Algoritmo desea utilizar?")
    print("1- Insertion Sort")
    print("2- Merge Sort")
    print("3- Quick Sort")
    print("4- Shell Sort")
    ordenamiento = int(input("Ingrese el algoritmo que le interesa: "))
    size = int(input("Cuantos datos le interesa tomar: "))
    time, sorted_list = controller.initordenamientodataAdquire(catalogo,ordenamiento,size)
    print("El resultado fue:\n",sorted_list)
    print("El proceso tardo: ", time, "ms")
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs) == 1:
        print("Cargando información de los archivos ....")
        catalogo = controller.InitCatalog()
        controller.loadArtist(catalogo)
        controller.loadArtwork(catalogo)
        print(lt.getElement(catalogo["Artista"],lt.size(catalogo["Artista"])))
        print(lt.getElement(catalogo["Artista"],lt.size(catalogo["Artista"])-1))
        print(lt.getElement(catalogo["Artista"],lt.size(catalogo["Artista"])-2))
        print(lt.getElement(catalogo["Obra"],lt.size(catalogo["Artista"])))
        print(lt.getElement(catalogo["Obra"],lt.size(catalogo["Artista"])-1))
        print(lt.getElement(catalogo["Obra"],lt.size(catalogo["Artista"])-2))
        print("Se cargaron " + str(lt.size(catalogo["Artista"]))+" artistas")
        print("Se cargaron " + str(lt.size(catalogo["Obra"]))+" obras")
    
    elif int(inputs) == 2:
        print(ejecutar_dateartist(catalogo))
    
    elif int(inputs) == 3:
        viewdateartwork()
    elif int(inputs) == 4:
        viewartworkvartist()
    elif int(inputs) == 5:
        ejecutar_nacionalidad(catalogo)
    elif  int(inputs) == 6:
        ejecutar_departmentartworks(catalogo)
    elif int(inputs) == 7:
        viewnuevaexpo()
    elif int(inputs) == 8:
        viewsort()
    else:
        sys.exit(0)
sys.exit(0)
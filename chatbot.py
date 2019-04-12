import random as rd
import pyttsx3 as ptx
#Agregar palabras a una lista

def pasarListaArchivos(archivo,separador):
    f=open(archivo, "r",encoding="utf-8")
    lista=f.readlines()
    f.close()
    tmp=lista[0]
    return tmp.split(separador)
def pasarListaArchivosCompleja(archivo):
    #f=io.open(archivo,mode="r",encoding="utf-8")
    f=open(archivo, "r", encoding="utf-8")
    lista=f.readlines()
    f.close()
    return lista

def eliminarResuduos(listaCompleta,residuos):
    listaCompleta[0][len(listaCompleta[0]) - 1]
    for i in range(len(listaCompleta)):
        listaCompleta[i][len(listaCompleta[i])-1]=listaCompleta[i][len(listaCompleta[i])-1].replace(residuos,"")
    return listaCompleta

def separarLista(lista,separador):
    for i in range(len(lista)):
        lista[i]=lista[i].lower().split(separador)
    return lista

def hablar(texto):
    engine= ptx.init() #motor de voz
    """engine.setProperty("rate",engine.getProperty("rate")-40)
    engine.say(texto)
    engine.runAndWait()"""
    voices = engine.getProperty('voices')
    voices = engine.setProperty('voice', voices[0].id)
    engine.setProperty("rate",engine.getProperty('rate')-60)
    engine.say(texto)
    engine.runAndWait()


def saludoAndDespedida(saludo, disponibles):
    return saludo in disponibles #retorna true or false si encuentra la palabra

def comparaPalabrasPregunta(wordWrite, wordSave):
    auxWrite=wordWrite
    auxSave=wordSave
    auxWrite=auxWrite.replace('á', 'a')
    auxWrite=auxWrite.replace('é', 'e')
    auxWrite=auxWrite.replace('í', 'i')
    auxWrite=auxWrite.replace('ó', 'o')
    auxWrite=auxWrite.replace('ú', 'u')
    for i in range(len(auxSave)):
        auxSave[i]=auxSave[i].replace('á', 'a')
        auxSave[i]=auxSave[i].replace('é', 'e')
        auxSave[i]=auxSave[i].replace('í', 'i')
        auxSave[i]=auxSave[i].replace('ó', 'o')
        auxSave[i]=auxSave[i].replace('ú', 'u')
    return auxWrite in auxSave

#Verificar que la frase esté dentro de la lista que envia
def verificarFrase(frase, lista,signo,signo2):
    #for dato in lista:
    for li in lista:
        contador = 0
        datoListaSeparado = li.split(" ")
        auxFrase = frase.split(" ")
        for j in range(len(auxFrase)):
            auxFrase[j]=auxFrase[j].replace(signo,"") #reemplazar si es una pregunta -> ? por ""
            auxFrase[j] = auxFrase[j].replace(signo2, "")  # reemplazar si es una pregunta -> ¿ por ""
        for dat in datoListaSeparado:
            ##if dat in auxFrase:
            if comparaPalabrasPregunta(dat, auxFrase ):
                contador+=1
        if contador == len(datoListaSeparado):
            return True
    return False

def posicionFrasePregunta( frase, listaCompleta , signo,signo2):
    posicion=0
    for lista in listaCompleta:
        if verificarFrase(frase,lista, signo, signo2):
            return posicion
        posicion+=1
    return -1

def varificarFraseDicha(frase  ,  lista  , signo   , tipo  , listaFrasesHechas, signo2, signal):
    if signal ==3:#no ha saludado
        if len(listaFrasesHechas[tipo])==0:
            randomFrase=["Por lo menos saludame antes de preguntarme" ,"Ok, pero primero dime hola","Qué mal educado, preguntar sin saludar"]
            return [0,randomFrase[  rd.randint(0,len(randomFrase)-1)]]
    if len(listaFrasesHechas[tipo])==0:
        return [0,""]
    retornarFrase=""
    pos=-1
    if tipo == 0:
        pos = 0
    else:
        pos = posicionFrasePregunta(frase , lista , signo,signo2)
    totalDichas=listaFrasesHechas[tipo].count(pos)
    #print(listaFrasesHechas[tipo], tipo,"  ", pos,"  ", totalDichas)
    if signal == 0:
        if totalDichas == 1:
            retornarFrase= "ya me habias saludado antes"
        if totalDichas == 2:
            retornarFrase= "Porque me has saludado dos veces"
        if totalDichas >= 3:
            retornarFrase= "Sigamos con la conversa, deja de saludar en la misma conversacion"
    if signal == 2:
        if totalDichas == 1:
            retornarFrase= "mmm, ya ha habias preguntado aquello"
        if totalDichas == 2:
            retornarFrase= "¿Porque me prguntas lo mismo otra vez?"
        if totalDichas == 3:
            retornarFrase= "Mejor pregunte otra cosa, no me gusta que preguntn lo mismo varias veces"
        elif totalDichas > 3:
            retornarFrase = "No me estes preguntando lo mismo, ya te dije."

    return [totalDichas  ,  retornarFrase]


"""Datos disponibles para la comunicacion"""
saludosDisponibles=pasarListaArchivos("saludos.txt",";")
despedidasDisponibles= pasarListaArchivos("despedidas.txt",";")
#preguntas  = eliminarResuduos(pasarListaArchivos("preguntas.txt",";"),"\n")
#respuestas = eliminarResuduos(pasarListaArchivos("respuestas.txt",";"), '\n')
preguntas  = eliminarResuduos(separarLista(pasarListaArchivosCompleja("preguntas.txt"),';'),'\n')
respuestas = eliminarResuduos(separarLista(pasarListaArchivosCompleja("respuestas.txt"),';'),'\n')

auxPregRP=eliminarResuduos(separarLista(pasarListaArchivosCompleja("preguntas_personajes.txt"),';'),'\n')
preguntas.extend(auxPregRP)
auxPregRP = eliminarResuduos(separarLista(pasarListaArchivosCompleja("respuestas_personajes.txt"),';'),'\n')
respuestas.extend(auxPregRP)
auxPregRP=eliminarResuduos(separarLista(pasarListaArchivosCompleja("preguntasEpisodios.txt"),';'),'\n')
preguntas.extend(auxPregRP)
auxPregRP = eliminarResuduos(separarLista(pasarListaArchivosCompleja("respuestasEpisodios.txt"),';'),'\n')
respuestas.extend(auxPregRP)

pregutnasHechas=[]
"""for preg in preguntas:
    for p in preg:
        print(p)
        """
# [   [ 'code' , 'code-Frase'   ] ,  ['code-2' , 'cod-pregunta'] ]
#  codigos: 0-saludo, 1-despedida, 2-pregunta, 3-exclaacion, 4-conversa
frasesDichas=[[],[],[],[],[]]
"""               ----------              """

despedida=False
#hablar("Hola, bienvenido")

while despedida == False:
    codeSpeakPerson=-1
    var =input(": ").lower()

    print(var)
    codigoFrase = -1
    #Saludar si saluda
    if saludoAndDespedida(var,saludosDisponibles):
        verificacion = varificarFraseDicha(var, saludosDisponibles, '', 0,frasesDichas,'',0)

        hablar(verificacion[1])
        codeSpeakPerson = 0
        if verificacion[0] < 2: #si ya se ha repetido no entrar
            nr=rd.randint(0, len(saludosDisponibles)-1)
            hablar(saludosDisponibles[nr]+" espero estes muy bien")
            print(saludosDisponibles[nr])
        codigoFrase = 0
    #pregunta
    elif var.find("?") >-1:
        antesSaludar=varificarFraseDicha(var, saludosDisponibles,'',0,frasesDichas,'',3)
        print( antesSaludar[1])
        hablar(antesSaludar[1])

        posicion = posicionFrasePregunta(var, preguntas,  "?","¿")
        verificacion=varificarFraseDicha(var, preguntas, '?', 2 ,frasesDichas,"¿",2)
        print(verificacion[1])
        hablar(verificacion[1])
        codeSpeakPerson = posicion
        if posicion>-1:
            codigoFrase = 2
        if verificacion[0] < 3:#pasar

            if posicion >-1:
                respuesta = respuestas[posicion]
                responder=rd.randint(0,len(respuesta)-1)
                hablar(respuesta[responder])
                print(respuesta[responder])
            else:
                desconocidoAsk=["No te entiendo","No se que es eso compa","No se","Npi no poseo es informacion","no se que estas tratando de preguntarme","Ni idea de lo que me estas preguntando"]
                hablar(desconocidoAsk[rd.randint(0,len(desconocidoAsk)-1)])
                print(desconocidoAsk[rd.randint(0,len(desconocidoAsk)-1)])
    elif var.find("!"):
        print()
    elif saludoAndDespedida(var,despedidasDisponibles):
        nr = rd.randint(0, len(despedidasDisponibles) - 1)
        hablar(despedidasDisponibles[nr])
        print(despedidasDisponibles[nr])
        despedida=True;
        codigoFrase = 2
    else:
        print()
    if codigoFrase != -1:
        frasesDichas[codigoFrase].append(codeSpeakPerson)

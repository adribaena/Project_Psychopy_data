from __future__ import division
import random , csv, funcionesExtras, itertools
from psychopy import gui,core, data, visual, event, logging, prefs
from psychopy.hardware import joystick
from scipy.spatial import distance
from labjack import u3






# el tiempo en segundos durante el que se escribe un valor en DAC1_REGISTER durante el cue 
tiempoEsperaU3Cue = 0.2


# la celula solar se muestra solo 0.30 segundos
timeInSecondsOfCueShown = 0.3


# la aceleración que se usa más abajo para mover el Joystick

acel = 0.8


# otros valores de otros screens
cuetime = 1.5
imperativeTarget1 = 0.5
interstimulusInterval = 4.0






miu3 = u3.U3()
miu3.getCalibrationData

DAC1_REGISTER = 5002
miu3.writeRegister(DAC1_REGISTER,0)


#Allows to display messsages in the output when a file is saved
logging.console.setLevel(logging.DEBUG)

#Headers and trial are imported from the file conditions
headers=list(csv.reader(open('conditions.csv',"rU")))[0]
trials=list(csv.reader(open('conditions.csv',"rU")))[1:]


#First GUI is ready to get subject's data and desired number of trials
info = {'Session': 1, 'Subject':'', 'gender':['male','female'], 'numberTrials' : 12 }
dialog = gui.DlgFromDict(dictionary= info, title='Posner with Joystick')


if dialog.OK:
    infoUser = dialog.data
    #Subject's data is saved in infoUser and are ready to print them on each file
else:
    print('user cancelled')
    core.quit()
    

#Date is saved on each trial

info['dateStr'] = data.getDateStr()



#We create a screen on which our program will run
#We also set up the internal clock meanwhile the remaining functions are ready to use

mywin = visual.Window([1366,768], fullscr = False, monitor='testMonitor', color='black',units='deg', allowGUI = False)
respClock = core.Clock()


joystick.backend='pyglet'
nJoysticks=joystick.getNumJoysticks()

if nJoysticks>0:
    joy = joystick.Joystick(0)
else:
    print("You don't have a joystick connected!?")
    mywin.close()
    core.quit()





# We declare the 2 types of stimuli to be detected with the solar panels declaramos las 2 formas para las celulas solares, de mas claro a mas oscuro

solar_cellcue = visual.Circle(mywin, radius=0.5, edges=30, lineColor = 'white',fillColor = 'white', opacity = 1, pos=[-14,7.5], interpolate= True)
solar_celltarget = visual.Circle(mywin, radius=0.5, edges=30, lineColor = 'white',fillColor = 'white', opacity = 1, pos=[-14,7.5], interpolate= True)
solar_cell100 = visual.Circle(mywin, radius=0.5, edges=30, fillColor = 'white', opacity = 1, pos=[-14,7.5], interpolate= True)
solar_cell75 = visual.Circle(mywin, radius=0.5, edges=30, fillColor = 'white', opacity = 1, pos=[-14,7.5], interpolate= True)
solar_cell50 = visual.Circle(mywin, radius=0.5, edges=30, fillColor = 'white', opacity = 1, pos=[-14,7.5], interpolate= True)

#preparamos la celula del punto de fijacion, de color blanco, y la cruz del punto de fijacion
solar_cellFixation = visual.Circle(mywin, radius= 0.5, edges=30, lineColor = 'white',fillColor = 'white', pos=[-14,7.5], interpolate= True) 
black_solarCell = visual.Circle(mywin, radius= 0.6, edges=30, lineColor = 'black',fillColor = 'black', pos=[-14,7.5], interpolate= True) 


fixationCross = visual.ImageStim(mywin, size = 0.9, image = None, mask = 'cross',color = 'white')


#preparamos las formas de la flecha , siendo un cuadrado seguido de un triangulo
square1=[ [-0.2,0.05], [-0.2,-0.05], [0.0,-0.05],[0.0,0.05]]
triangle1 = [[0.0,-0.1], [0.2,0], [0.0,0.1]]


#preparamos la flecha para el 100 por 100 de aciertos, de color verde
square100 = visual.ShapeStim(mywin, lineWidth=2.0,vertices=square1, fillColor=[-0.5,0.5,-0.5], size=6, lineColor=[-0.5,0.5,-0.5])
triangle100 = visual.ShapeStim(mywin, lineWidth=2.0,vertices=triangle1, fillColor=[-0.5,0.5,-0.5], size=6, lineColor=[-0.5,0.5,-0.5])

#preparamos la flecha para el 75 por 100 de aciertos, de color rojo
square75 = visual.ShapeStim(mywin, lineWidth=2.0,vertices=square1, fillColor='red', size=6, lineColor='red')
triangle75 = visual.ShapeStim(mywin, lineWidth=2.0,vertices=triangle1, fillColor='red', size=6, lineColor='red')

#preparamos la flecha para el 50 por 100 de aciertos, de color azul
square50 = visual.ShapeStim(mywin, lineWidth=2.0,vertices=square1, fillColor='blue', size=6, lineColor='blue')
triangle50 = visual.ShapeStim(mywin, lineWidth=2.0,vertices=triangle1, fillColor='blue', size=6, lineColor='blue')


#declaramos el resto de items, los circulos superiores de espera, y el rojo inferior
leftWhiteCircle = visual.Circle(mywin, radius=1.0, edges=30, lineColor = 'white',fillColor = 'white', pos=(-6, 3), interpolate=True)
rightWhiteCircle = visual.Circle(mywin, radius=1.0, edges=30,fillColor = 'white', pos=(6, 3), interpolate=True)
downOrangeButton = visual.Circle(mywin, radius=0.7, edges=30, lineColor = 'orange', fillColor = 'orange', pos=(0, -5), interpolate=True)

# no le ponemos direccion, antes de pintarlo se la pondremos, pero eso es mas adelante
targetGreyCircle = visual.Circle(mywin, radius=1.0, edges=30,lineColor = 'grey', fillColor = 'grey', interpolate=True)


#declaramos una sublista para pseudorandomizar los siguientes trials, y la iniciamos con 3 elementos aleatorios
sublista = [random.choice(trials),random.choice(trials),random.choice(trials)]


#declaramos el nombre del fichero, siendo primero el sexo del sujeto, luego el id del mismo, y luego el numero de sesion
filename = 'data/'+str(info['gender'])+'_'+str(info['Subject'])+'_'+str(info['Session'])

# iniciamos nuestro experimento con un nombre, y las condiciones iniciales que hemos definido antes
exp = data.ExperimentHandler(name='PosnerSubject',
                version='0.1',
                extraInfo=info,
                runtimeInfo=None,
                originPath=None,
                savePickle=True,
                saveWideText=True,
                dataFileName=filename)


#tomamos de la primera GUI el numero de trials, y lo usamos para nuestro manejador de los trials, que va a ser nuestro numero de repeticiones del bucle
numeroReps = int(float(info['numberTrials']))
training = data.TrialHandler(trialList=[], nReps=numeroReps, name='train', method='sequential')

#unimos con nuestro experimento los trials, de manera secuencial (definido arriba en el method), en forma de bucle
exp.addLoop(training)


#para cada vez que hemos escrito en nuestro numero de trials
for trial in training:
    
    #obtenemos la lista presudoaleatoria sin repetir 3 veces seguidas el mismo trigger
    sublista = funcionesExtras.siguienteValor(trials,sublista)
    
    #de la lista anterior, nuestro elemento es el tercero de la lista.
    elem = sublista[2]
    
    
    # colocamos el trial en nuestro csv, para que podamos ver que se cumple la pseudorandomizacion
    training.addData('elemento', elem)
    
    
    
    #declaramos el SOA, un intervalo de tiempo entre 1 y 2 segundos que usaremos para la pantalla de fixation
    timeFixation = random.uniform(1,2)
    
    # redondeamos el SOA a un solo decimal, y colocamos el valor en el fichero de salida
    soa=round(timeFixation,1)
    training.addData('soa',soa)
    
    
    respClock = core.Clock()
    

    
    # soa esta entre 1 y 2
    
    while respClock.getTime() < soa:
        
        fixationCross.draw()
        solar_cellFixation.draw()
        fixationCross.draw()
        #timeInSecondsOfCueShown es el tiempo de espera hasta ocultar el solarCell
        if respClock.getTime() > timeInSecondsOfCueShown:     
            black_solarCell.draw()
        mywin.flip()
    
    
    
    
    
    #preguntamos por si queremos una celula de 100 por 100 de acierto, que se encuentra en nuestra variable elem, en el primer parametro 
    if (elem[0] == '100') :
        #dibujamos la celula de 100 por 100 
        itemSolar = solar_cell100
        #ademas, si el segundo elemento de elem (posicion 1 de elem, ya que la 0 representaba el procentaje de acierto) es 180
        if (elem[1] == '180'):
            # si lo es, giramos la flecha (cuadrado y triangulo del elemento del color que nos interesa) un total de 180 grados para darle la vuelta
            square100.ori = int(float('180'))
            triangle100.ori = int(float('180'))
        # hay que fijarse en los saltos de linea de arriba, es decir, giremos o no la figura, vamos a pintarla igualmente en nuestra ventana
        squareItem = square100
        triangleItem = triangle100
    #hacemos lo mismo para 75 y 50 por ciento
    elif (elem[0] == '75') :
        itemSolar = solar_cell75
        if (elem[1] == '180'):
            square75.ori = int(float('180'))
            triangle75.ori = int(float('180'))
        squareItem = square75
        triangleItem = triangle75
    elif (elem[0] == '50'):
        itemSolar = solar_cell50
        if (elem[1] == '180'):
            square50.ori = int(float('180'))
            triangle50.ori = int(float('180'))
        squareItem = square50
        triangleItem = triangle50
    
    
    
    ttlText = elem[2]
    
    ttlNumber = float(ttlText.strip('"'))
    
    respClock = core.Clock()
    
    while respClock.getTime() < cuetime:
        itemSolar.draw()
        squareItem.draw()
        triangleItem.draw()
        #timeInSecondsOfCueShown es el tiempo de espera hasta ocultar el solarCell
        if respClock.getTime() > timeInSecondsOfCueShown:     
            black_solarCell.draw()
        if respClock.getTime() < tiempoEsperaU3Cue :
            miu3.writeRegister(DAC1_REGISTER, ttlNumber)
        else :
            miu3.writeRegister(DAC1_REGISTER, 0)
        mywin.flip()
    
    
    
    
    
    training.addData('cueTime',cuetime)
    
    # una vez que ha pasado el tiempo de cue, reseteamos la posicion de las cue, y lo hacemos poniendo la inclinacion de todas a 0 grados
    # asi nos aseguramos que para el siguiente trial, todas las flechas estan orientadas como inicio a la derecha
    square50.ori = 0
    square75.ori = 0
    square100.ori = 0
    triangle100.ori = 0
    triangle50.ori = 0
    triangle75.ori = 0
    
    
    # ahora dibujamos el imperative target 1, es decir, el circulo rojo inferior, y los dos blancos superiores, al igual que una celula f de un solo tipo
    # vamos a reutilizar la de la celula solar del punto de fijacion
    #solar_cellFixation.draw()



    respClock = core.Clock()
    
    # soa esta entre 1 y 2
    
    while respClock.getTime() < imperativeTarget1:
        
        leftWhiteCircle.draw()
        rightWhiteCircle.draw()
        downOrangeButton.draw()
        solar_cellFixation.draw()
        #timeInSecondsOfCueShown es el tiempo de espera hasta ocultar el solarCell
        if respClock.getTime() > timeInSecondsOfCueShown:
            black_solarCell.draw()
        mywin.flip()

    # como nuestro target dura un total de medio segundo, declaramos la variable, y la usamos como espera, para luego guardar ese valor en nuestro fichero de salida
    
    training.addData('imperativeTarget1', imperativeTarget1)
    
    # vamos a obtener el porcentaje de acierto del cue, que es el primer elemento de elem
    valor = elem[0]
    
    # usaremos ese elemento para obtener un 1 o un 0 dependiendo de la tasa de acierto de nuestro elemento.
    # para ello usaremos la funcion extra que se encuentra en el fichero funcionesExtras
    acierto = funcionesExtras.elementoPorPorcentaje(valor)
    
    # guardamos un 0 o un 180, que indica los grados de giro del cueTime
    direccion = elem[1]
    
    # vamos a ir actualizando el reloj interno cada vez que hagamos un flip (cargar la pantalla) de nuestra ventana. Vamos a resetear el reloj interno cada vez.
    #mywin.callOnFlip(respClock.reset)
    
    # si la flecha ha acertado, y marcaba la direccion de la derecha con 0 grados
    # o si la flecha a mentido, y marcaba la direccion de la izquierda con 180 grados
    if (acierto and elem[1] == '0') or (acierto == 0 and elem[1] == '180'):
        
        #dibujamos el circulo objetivo a la derecha, en la posicion que nos interese
        targetGreyCircle.pos = ( 6,3)
        
        #aprovechamos y dejamos dibujado el circulo blanco a la izquierda
        #leftWhiteCircle.draw()
        
        # declaramos un valor corrAns, que indica que el circulo target es a la derecha, con un 2
        corrAns = 2
    else :
        targetGreyCircle.pos = (-6,3)
        
        #dejamos dibujado el ciruclo a la derecha
        #rightWhiteCircle.draw()
        
        # en caso contrario, se pinta a la izquierda y corrAns vale 1
        corrAns = 1
    
    # dibujamos nuestro circulo objetivo, y el resto de elementos que nos interesan para nuestro imperative target 2
    
    
    # vamos a colocar las variables que hemos declarado anteriormente en nuestro fichero
    training.addData('direccion', direccion) # guardamos el valor 0 o 180 dependiendo de nuestro elem
    training.addData('acierto', acierto) # guardamos un 0 o un 1, dependiendo si se ha predecido con acierto o no el cue
    training.addData('corrAns', corrAns) # guardamos un 1 si el circulo target esta a la izquierda, y un 2 si el green target esta a la derecha
    
    
    
    # borramos los eventos de teclado, que para futuros bucles nos interesa borrar las teclas pulsadas anteriormente
    
    
    #reseteamos la variable del reloj interno para poder guardar lo que se tarde en pulsar la tecla target
    respClock = core.Clock()
    
    
    # AQUI TENDRIA QUE IR EL CODIGO PARA EL JOYSTICK
    
    
    
    lim = 0
    finbucle = 0

    # declaramos los limites de pantalla
    
    limHoriz = 13
    limVert = 8
    
    # fin declarar limites
    
    solar_celltarget.draw()
    leftWhiteCircle.draw()
    rightWhiteCircle.draw()
    targetGreyCircle.draw()
    
    respClock = core.Clock()
    
    while finbucle == 0:
        xx = joy.getX()
        yy = joy.getY()
        [left,right] = downOrangeButton.pos
        
        nuevoX = left + acel* xx  # si avanzamos a la derecha, se incrementa el vector direccion X
        nuevoY = right - acel* yy # el eje Y esta invertido en los joystick, si vamos hacia arriba, se decrementa el vector direccion Y
        
        
        
        ## comprobamos los limites de pantalla
        
        nuevoX =  limHoriz  if (nuevoX > limHoriz ) else nuevoX
        nuevoX =  -limHoriz  if (nuevoX < -limHoriz ) else nuevoX
        nuevoY =  limVert  if (nuevoY > limVert ) else nuevoY
        nuevoY =  -limVert  if (nuevoY < -limVert ) else nuevoY
        
        
        ## fin comprobar limites 


        downOrangeButton.setPos((nuevoX, nuevoY))

        
        distancia = distance.euclidean(downOrangeButton.pos,targetGreyCircle.pos)
        
        
        if distancia < 0.3 :   # mientras estamos teniendo contacto con los dos circulos
            
            lim = lim+1
        if distancia > 0.3 : #si dejan de estar en contacto los circulos, reseteamos el limite
            lim = 0
            
        if lim > 50:   # criterio de parada temporal (50 es un ejemplo, serian 50 veces el bucle seguidas) 
            finbucle = 1  # salimos del while
            
        if 'q' in event.getKeys():   # abortar operacion si pulsamos q
            core.quit()
            
        solar_celltarget.draw()
        leftWhiteCircle.draw()
        rightWhiteCircle.draw()
        targetGreyCircle.draw()
        downOrangeButton.draw()
        
        if respClock.getTime() > timeInSecondsOfCueShown:
            black_solarCell.draw()
        mywin.flip()
        
        
    downOrangeButton.setPos((0, -5))
    # guardamos el tiempo en pulsar esa tecla, que como hemos reseteado anteriormente el reloj, es el tiempo de respuesta del sujeto, en segundos
    imperativeTarget2 = respClock.getTime()
    
    # guardamos los resultados en el fichero
    training.addData('imperativeTarget2',imperativeTarget2) # el tiempo que hemos tardado en pulsar la tecla del teclado
    training.addData('imperativeTarget2MS',imperativeTarget2*1000) # el tiempo de arriba, pero en milisegundos    
    
    # hacemos un flip despues de otro flip sin dibujar nada, por lo que se muestra una pantalla en negro
    mywin.flip()
    
    # declaramos el tiempo de interstimulo antes de pasar al siguiente trial
    training.addData('interstimulusInterval',interstimulusInterval)
    
    # esperamos ese tiempo interstimulus y pasamos al siguiente trial
    core.wait(interstimulusInterval)
    exp.nextEntry()

# una vez terminado, imprimimos por la pantalla del psychopy nuestras variables de salida
for e in exp.entries:
    print(e)
    
# por ultimo, mostramos un mensaje de que todo ha ido bien
print("Done. We will save data to a csv file")

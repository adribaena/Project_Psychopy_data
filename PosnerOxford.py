import random , csv, funcionesExtras, itertools
from psychopy import gui,core, data, visual, event, logging, prefs
from psychopy.hardware import joystick
from scipy.spatial import distance


#permitimos que se puedan cargar mensajes en el output cada vez que se guarde en un fichero
logging.console.setLevel(logging.DEBUG)

#importamos cabeceras y trials del fichero raiz condiciones
headers=list(csv.reader(open('conditions.csv',"rU")))[0]
trials=list(csv.reader(open('conditions.csv',"rU")))[1:]


#preparamos el primer gui para introducir datos del sujeto, y el numero de trials 
info = {'Session': 1, 'Subject':'', 'gender':['male','female'], 'numberTrials' : 12 }
dialog = gui.DlgFromDict(dictionary= info, title='JFMR and ARB task')


if dialog.OK:
    infoUser = dialog.data
    #Guardamos los datos en infoUser, y tenemos los datos preparados para imprimirlos en cada file
else:
    print('user cancelled')
    core.quit()
    

#guardamos la fecha de hoy en el cada trial

info['dateStr'] = data.getDateStr()



#creamos la pantalla sobre la que vamos a usar nuestro programa
#tambien preparamos el reloj interno para ir funcionando mientras se van 
#cargando el resto de componentes

mywin = visual.Window([1366,768], fullscr = True, monitor='testMonitor', color='black',units='deg', allowGUI = False)
respClock = core.Clock()


nJoysticks=joystick.getNumJoysticks()

if nJoysticks>0:
    joy = joystick.Joystick(0)
else:
    print("You don't have a joystick connected!?")
    mywin.close()
    core.quit()





# declaramos las tres formas para las celulas solares, de mas claro a mas oscuro

solar_cell100 = visual.Circle(mywin, radius=0.5, edges=30, lineColor = 'white',fillColor = 'white', pos=[-14,7.5], interpolate= True)
solar_cell75 = visual.Circle(mywin, radius=0.5, edges=30, lineColor = 'white',fillColor = 'white', pos=[-14,7.5], interpolate= True)
solar_cell50 = visual.Circle(mywin, radius=0.5, edges=30, lineColor = 'white',fillColor = 'white', pos=[-14,7.5], interpolate= True)


#preparamos la celula del punto de fijacion, de color blanco, y la cruz del punto de fijacion
solar_cellFixation = visual.Circle(mywin, radius= 0.5, edges=30, lineColor = 'white',fillColor = 'white', pos=[-14,7.5], interpolate= True) 
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
leftWhiteCircle = visual.Circle(mywin, radius=1.0, edges=30, lineColor = 'white',fillColor = 'white', pos=(-9, 6), interpolate=True)
rightWhiteCircle = visual.Circle(mywin, radius=1.0, edges=30,fillColor = 'white', pos=(9, 6), interpolate=True)
downRedButton = visual.Circle(mywin, radius=1.0, edges=30, lineColor = 'orange', fillColor = 'orange', pos=(0, -5), interpolate=True)

# no le ponemos direccion, antes de pintarlo se la pondremos, pero eso es mas adelante
targetGreenCircle = visual.Circle(mywin, radius=1.0, edges=30,lineColor = 'orange', fillColor = 'orange', interpolate=True)


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
    
    #dibujamos la cruz de fijacion, y la celula solar de fijacion
    fixationCross.draw()
    solar_cellFixation.draw()
    fixationCross.draw()
    #hacemos que se recargue la pantalla mywin, con los elementos dibujados antes (se refresca la pantalla con esos elementos)
    mywin.flip()
    
    #esperamos para cerrar esa ventan un tiempo igual al SOA ( 1- 2 segs)
    core.wait(soa)
    
    #preguntamos por si queremos una celula de 100 por 100 de acierto, que se encuentra en nuestra variable elem, en el primer parametro 
    if (elem[0] == '100') :
        #dibujamos la celula de 100 por 100 
        solar_cell100.draw()
        #ademas, si el segundo elemento de elem (posicion 1 de elem, ya que la 0 representaba el procentaje de acierto) es 180
        if (elem[1] == '180'):
            # si lo es, giramos la flecha (cuadrado y triangulo del elemento del color que nos interesa) un total de 180 grados para darle la vuelta
            square100.ori = int(float('180'))
            triangle100.ori = int(float('180'))
        # hay que fijarse en los saltos de linea de arriba, es decir, giremos o no la figura, vamos a pintarla igualmente en nuestra ventana
        square100.draw()
        triangle100.draw()
    #hacemos lo mismo para 75 y 50 por ciento
    elif (elem[0] == '75') :
        solar_cell75.draw()
        if (elem[1] == '180'):
            square75.ori = int(float('180'))
            triangle75.ori = int(float('180'))
        square75.draw()
        triangle75.draw()
    elif (elem[0] == '50'):
        solar_cell50.draw()
        if (elem[1] == '180'):
            square50.ori = int(float('180'))
            triangle50.ori = int(float('180'))
        square50.draw()
        triangle50.draw()
    
    #una vez dibujados los elementos, actualizamos la pantalla
    mywin.flip()
    
    #declaramos y usamos una variable igual al tiempo de espera de esta ventana de CUE, en nuestro caso 1 segundo y medio
    cueTime = 1.5
    #cueTime = 2
    
    core.wait(cueTime)
    training.addData('cueTime',cueTime)
    
    # una vez que ha pasado el tiempo de cue, reseteamos la posicion de las cue, y lo hacemos poniendo la inclinacion de todas a 0 grados
    # asi nos aseguramos que para el siguiente trial, todas las flechas estan orientadas como inicio a la derecha
    square50.ori = 0
    square75.ori = 0
    square100.ori = 0
    triangle100.ori = 0
    triangle50.ori = 0
    triangle75.ori = 0
    
    
    # ahora dibujamos el imperative target 1, es decir, el circulo rojo inferior, y los dos blancos superiores, al igual que una celula solar de un solo tipo
    # vamos a reutilizar la de la celula solar del punto de fijacion
    solar_cellFixation.draw()
    leftWhiteCircle.draw()
    rightWhiteCircle.draw()
    downRedButton.draw()
    mywin.flip()
    
    # como nuestro target dura un total de medio segundo, declaramos la variable, y la usamos como espera, para luego guardar ese valor en nuestro fichero de salida
    imperativeTarget1 = 0.5
    core.wait(imperativeTarget1)
    training.addData('imperativeTarget1', imperativeTarget1)
    
    # vamos a obtener el porcentaje de acierto del cue, que es el primer elemento de elem
    valor = elem[0]
    
    # usaremos ese elemento para obtener un 1 o un 0 dependiendo de la tasa de acierto de nuestro elemento.
    # para ello usaremos la funcion extra que se encuentra en el fichero funcionesExtras
    acierto = funcionesExtras.elementoPorPorcentaje(valor)
    
    # guardamos un 0 o un 180, que indica los grados de giro del cueTime
    direccion = elem[1]
    
    # vamos a ir actualizando el reloj interno cada vez que hagamos un flip (cargar la pantalla) de nuestra ventana. Vamos a resetear el reloj interno cada vez.
    mywin.callOnFlip(respClock.reset)
    
    # si la flecha ha acertado, y marcaba la direccion de la derecha con 0 grados
    # o si la flecha a mentido, y marcaba la direccion de la izquierda con 180 grados
    if (acierto and elem[1] == '0') or (acierto == 0 and elem[1] == '180'):
        
        #dibujamos el circulo objetivo a la derecha, en la posicion que nos interese
        targetGreenCircle.pos = ( 9,6)
        
        #aprovechamos y dejamos dibujado el circulo blanco a la izquierda
        leftWhiteCircle.draw()
        
        # declaramos un valor corrAns, que indica que el circulo target es a la derecha, con un 2
        corrAns = 2
    else :
        targetGreenCircle.pos = (-9,6)
        
        #dejamos dibujado el ciruclo a la derecha
        rightWhiteCircle.draw()
        
        # en caso contrario, se pinta a la izquierda y corrAns vale 1
        corrAns = 1
    
    # dibujamos nuestro circulo objetivo, y el resto de elementos que nos interesan para nuestro imperative target 2
    
    
    # vamos a colocar las variables que hemos declarado anteriormente en nuestro fichero
    training.addData('direccion', direccion) # guardamos el valor 0 o 180 dependiendo de nuestro elem
    training.addData('acierto', acierto) # guardamos un 0 o un 1, dependiendo si se ha predecido con acierto o no el cue
    training.addData('corrAns', corrAns) # guardamos un 1 si el circulo target esta a la izquierda, y un 2 si el green target esta a la derecha
    
    
    
    # borramos los eventos de teclado, que para futuros bucles nos interesa borrar las teclas pulsadas anteriormente
    
    
    #reseteamos la variable del reloj interno para poder guardar lo que se tarde en pulsar la tecla target
    respClock.reset
    
    
    # AQUI TENDRIA QUE IR EL CODIGO PARA EL JOYSTICK
    
    
    lim = 0
    finbucle = 0

    # declaramos los limites de pantalla
    
    limHoriz = 13
    limVert = 8
    
    # fin declarar limites




    while finbucle == 0:
        xx = joy.getX()
        yy = joy.getY()
        [left,right] = downRedButton.pos
        
        acel = 0.4  #aceleracion que se aplica a cada recogida de datos
        nuevoX = left + acel* xx  # si avanzamos a la derecha, se incrementa el vector direccion X
        nuevoY = right - acel* yy # el eje Y esta invertido en los joystick, si vamos hacia arriba, se decrementa el vector direccion Y
        
        
        
        ## comprobamos los limites de pantalla
        
        nuevoX =  limHoriz  if (nuevoX > limHoriz ) else nuevoX
        nuevoX =  -limHoriz  if (nuevoX < -limHoriz ) else nuevoX
        nuevoY =  limVert  if (nuevoY > limVert ) else nuevoY
        nuevoY =  -limVert  if (nuevoY < -limVert ) else nuevoY
        
        
        ## fin comprobar limites 


        downRedButton.setPos((nuevoX, nuevoY))

        
        distancia = distance.euclidean(downRedButton.pos,targetGreenCircle.pos)
        
        
        if distancia < 2 :   # mientras estamos teniendo contacto con los dos circulos
            
            lim = lim+1
        if distancia > 2 : #si dejan de estar en contacto los circulos, reseteamos el limite
            lim = 0
            
        if lim > 50:   # criterio de parada temporal (50 es un ejemplo, serian 50 veces el bucle seguidas) 
            finbucle = 1  # salimos del while
            
        if 'q' in event.getKeys():   # abortar operacion si pulsamos el dulce q
            core.quit()
        
        # si no pasa nada de eso
        
        leftWhiteCircle.draw()
        rightWhiteCircle.draw()
        targetGreenCircle.draw() #aqui el orden importa y primero imprimimos los dos circulos blancos, y luego el objetivo
        downRedButton.draw()
        solar_cellFixation.draw()
        event.clearEvents()
        mywin.flip()
        
        
    downRedButton.setPos((0, -5))
    # guardamos el tiempo en pulsar esa tecla, que como hemos reseteado anteriormente el reloj, es el tiempo de respuesta del sujeto, en segundos
    imperativeTarget2 = respClock.getTime()
    
    # guardamos los resultados en el fichero
    training.addData('imperativeTarget2',imperativeTarget2) # el tiempo que hemos tardado en pulsar la tecla del teclado
    training.addData('imperativeTarget2MS',imperativeTarget2*1000) # el tiempo de arriba, pero en milisegundos    
    
    # hacemos un flip despues de otro flip sin dibujar nada, por lo que se muestra una pantalla en negro
    mywin.flip()
    
    # declaramos el tiempo de interstimulo antes de pasar al siguiente trial
    interstimulusInterval = 4.0
    training.addData('interstimulusInterval',interstimulusInterval)
    
    # esperamos ese tiempo interstimulus y pasamos al siguiente trial
    core.wait(interstimulusInterval)
    exp.nextEntry()

# una vez terminado, imprimimos por la pantalla del psychopy nuestras variables de salida
for e in exp.entries:
    print(e)
    
# por ultimo, mostramos un mensaje de que todo ha ido bien
print("Done. We will save data to a csv file")

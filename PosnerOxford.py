import random , csv, funcionesExtras, itertools
from psychopy import gui,core, data, visual, event, logging
logging.console.setLevel(logging.DEBUG)

headers=list(csv.reader(open('conditions.csv',"rU")))[0]
trials=list(csv.reader(open('conditions.csv',"rU")))[1:]

print headers
print trials, 'sdasdsa'

numConditions =  range(len(trials))


conditions = data.importConditions('conditions.csv')
print conditions    


info = {'Session': 1, 'Subject':'', 'gender':['male','female'], 'numberTrials' : 12 }
dialog = gui.DlgFromDict(dictionary= info, title='JFMR and ARB task')


if dialog.OK:
    infoUser = dialog.data #this will be a list of data returned from each field added in order
    print(infoUser)
else:
    print('user cancelled')
    core.quit()
    

#Guardamos los datos en infoUser, y tenemos 

#print info['numberTrials']

info['dateStr'] = data.getDateStr()

print 'la info es : ' , info

#create a window
mywin = visual.Window([1366,768], fullscr = True, monitor='testMonitor', color=(0, 0, 0),units='deg')
respClock = core.Clock()




solar_cell100 = visual.GratingStim(mywin,tex='sin', mask='raisedCos',color='white', opacity=0.2 , size= 2, colorSpace='hsv', pos=[-18,9],sf=0)
solar_cell75 = visual.GratingStim(mywin,tex='sin', mask='raisedCos',color=(0,200,0), opacity= 0.6, size= 2 , colorSpace='hsv', pos=[-18,9],sf=0)
solar_cell50 = visual.GratingStim(mywin,tex='sin', mask='raisedCos',color=(0,230,0), opacity= 0.8, size= 2 ,colorSpace='hsv', pos=[-18,9],sf=0)


solar_cellFixation = visual.Circle(mywin, radius=1, edges=30, lineColor = 'white',fillColor = 'white', pos=[-18,9], interpolate= True) 
fixationCross = visual.ImageStim(mywin, size = 0.9, image = None, mask = 'cross',color = 'white')



square1=[ [-0.2,0.05], [-0.2,-0.05], [0.0,-0.05],[0.0,0.05]]
triangle1 = [[0.0,-0.1], [0.2,0], [0.0,0.1]]


square100 = visual.ShapeStim(mywin, lineWidth=2.0,vertices=square1, fillColor=[-0.5,0.5,-0.5], size=10, lineColor=[-0.5,0.5,-0.5])
triangle100 = visual.ShapeStim(mywin, lineWidth=2.0,vertices=triangle1, fillColor=[-0.5,0.5,-0.5], size=10, lineColor=[-0.5,0.5,-0.5])

square75 = visual.ShapeStim(mywin, lineWidth=2.0,vertices=square1, fillColor='red', size=10, lineColor='red')
triangle75 = visual.ShapeStim(mywin, lineWidth=2.0,vertices=triangle1, fillColor='red', size=10, lineColor='red')

square50 = visual.ShapeStim(mywin, lineWidth=2.0,vertices=square1, fillColor='blue', size=10, lineColor='blue')
triangle50 = visual.ShapeStim(mywin, lineWidth=2.0,vertices=triangle1, fillColor='blue', size=10, lineColor='blue')



leftWhiteCircle = visual.Circle(mywin, radius=1.5, edges=30, lineColor = 'white',fillColor = 'white', pos=(-12, 7.5), interpolate=True)
rightWhiteCircle = visual.Circle(mywin, radius=1.5, edges=30,fillColor = 'white', pos=(12, 7.5), interpolate=True)
downRedButton = visual.Circle(mywin, radius=1.5, edges=30, lineColor = 'red', fillColor = 'red', pos=(0, -6), interpolate=True)
targetGreenCircle = visual.Circle(mywin, radius=1.5, edges=30,lineColor = 'green', fillColor = 'green', interpolate=True)





sublista = [random.choice(trials),random.choice(trials),random.choice(trials)]


#info = {'Session': 1, 'Subject':'', 'gender':['male','female'], 'numberTrials' : 12 }




clockTimer = core.Clock()

gender = info['gender']
sessionNum = info['Session']
subjectName = info['Subject']

print gender , ',,,' , sessionNum , ',,,,' , subjectName


filename = 'data/'+str(gender)+'_'+str(sessionNum)+'_'+str(subjectName)

exp = data.ExperimentHandler(name='PosnerSubject',
                version='0.1',
                extraInfo=info,
                runtimeInfo=None,
                originPath=None,
                savePickle=True,
                saveWideText=True,
                dataFileName=filename)



numeroReps = int(float(info['numberTrials']))

training = data.TrialHandler(trialList=[], nReps=numeroReps, name='train', method='sequential')
exp.addLoop(training)



for trial in training:
    sublista = funcionesExtras.siguienteValor(trials,sublista)
    
    elem = sublista[2]
    print elem
    
    rt = None
    
    
    training.addData('elemento', elem)
    
    timeFixation = random.uniform(1,2)
    c=round(timeFixation,1)
    print 'soa' , c
    
    training.addData('soa',c)
    
    fixationCross.draw()
    solar_cellFixation.draw()
    mywin.flip()
    core.wait(c)
    
    mywin.color=(0, 0, 0)
    
    if (elem[0] == '100') :
        solar_cell100.draw()
        if (elem[1] == '180'):
            square100.ori = int(float('180'))
            triangle100.ori = int(float('180'))
        square100.draw()
        triangle100.draw()
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
        
    mywin.flip()
    
    cueTime = 1.5
    core.wait(cueTime)
    
    training.addData('cueTime',cueTime)
    
    square50.ori = 0
    square75.ori = 0
    square100.ori = 0
    triangle100.ori = 0
    triangle50.ori = 0
    triangle75.ori = 0
    
    
    solar_cellFixation.draw()
    leftWhiteCircle.draw()
    rightWhiteCircle.draw()
    downRedButton.draw()
    mywin.flip()
    
    imperativeTarget1 = 0.5
    
    core.wait(imperativeTarget1)
    
    training.addData('imperativeTarget1', imperativeTarget1)
    
    valor = elem[0]
    acierto = funcionesExtras.elementoPorPorcentaje(valor)
    
    direccion = elem[1]
    
    mywin.callOnFlip(respClock.reset)
    
    if (acierto and elem[1] == '0') or (acierto == 0 and elem[1] == '180') :
        targetGreenCircle.pos = ( 12, 7.5)
        leftWhiteCircle.draw()
        corrAns = 2
    else :
        targetGreenCircle.pos = (-12, 7.5)
        rightWhiteCircle.draw()
        corrAns = 1
        
    targetGreenCircle.draw()
    downRedButton.draw()
    solar_cellFixation.draw()
    mywin.flip()
    
    
    training.addData('direccion', direccion)
    training.addData('acierto', acierto)
    training.addData('corrAns', corrAns)
    
    
    print ' , direccion : ' , direccion , ' ,  acierto : ' , acierto , 'correct_answer: ' , corrAns 
    
    
    event.clearEvents()
    

    respClock.reset
    
    keys = event.waitKeys(keyList = ['left','right','escape'])
    resp = keys[0] 
    imperativeTarget2 = respClock.getTime()

    if corrAns == 1  and resp=='left':
        corr = 1
    elif corrAns == 2  and resp=='right':
        corr = 1
    elif resp=='escape':
        corr = None
        core.quit()
    else:
        corr = 0    
    
    training.addData('imperativeTarget2',imperativeTarget2)
    training.addData('imperativeTarget2MS',imperativeTarget2*1000)
    training.addData('respuesta', corr)
    
    mywin.flip()
    
    interstimulusInterval = 4.0
    training.addData('interstimulusInterval',interstimulusInterval)
    
    core.wait(interstimulusInterval)
    exp.nextEntry()
    
    
for e in exp.entries:
    print(e)
print("Done. We will save data to a csv file")



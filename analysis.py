import csv
import numpy as np
from collections import Counter
import datetime
#import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt

file  = open('data/allDefunciones.csv', "r")
#fileDataName  = open('data/allNacimientos.csv', "rb")
reader = csv.reader(file)

rownum = 0
allData = []
ALLDATA = []

for iRow, row in enumerate(reader):

    # Header row.
    if iRow == 0:
        header = row

    else:
        allData.append( row )
        ALLDATA.append( [x.upper() for x in row] )

file.close()

# put all data in  numpy
npData = np.array(allData)
NPDATA = np.array(ALLDATA)


print ( "\nNumber of Entries: %4d" % npData.shape[0] )
print ( "Number of Columns: %4d\n" % npData.shape[1] )


# Check number of entries per column and the most common value
print ( "                      # - Unique - Most common" )

for idx in range(len(header)):
    vec  = NPDATA[:,idx]
    vec2 = vec [ NPDATA[:,idx] != '' ]

    if len(vec2) > 0:
        count = Counter(vec2)
        print ( "[%2s] %-15s: %4d - %6d - ( %4d | %s )" % (idx, header[idx], vec2.size, len(count), count.most_common(1)[0][1], count.most_common(1)[0][0]) )
    else:
        print ( " [%2s] %-15s: %4d" % (idx, header[idx], vec2.size) )


# print more common jobs
if False:

    vec  = NPDATA[:,18]
    vec2 = vec [ NPDATA[:,18] != '' ]
    count = Counter(vec2)

    print ("\nOficios mas comunes")
    for idx in range(len(count)):
        print ( "%4d : %s" % (count.most_common()[idx][1], count.most_common()[idx][0]) )

# print diff between death and burial
if False:
    diffBurial = []
    # we compare the death date DEFUNCION2 (8) with burial date ENTERRAMIENTO2 (11)
    for ii, defuncion in enumerate(NPDATA[:,8]):
        if (defuncion != '') and (NPDATA[ii,11] != ''):
            try:
                deathDate  = datetime.datetime.strptime(defuncion,     '%d/%m/%Y').date()
                burialDate = datetime.datetime.strptime(NPDATA[ii,11], '%d/%m/%Y').date()
                diffBurial.append( (burialDate - deathDate).days )

    
            except: 
                pass

    delay = Counter(diffBurial)
    print ( "\nTiempo de la muerte al entierro" )
    for idx in range(len(delay)):
        print ( "%4d : %d dias" % (delay.most_common()[idx][1], delay.most_common()[idx][0]) )


# Print all observations
if False:
    for obs in npData[:,17]:
        if obs != '':
            print ("%s\n" % obs)

# Distribution of deaths by month (text version)
if True:
    distributionDay = []
    distributionMonth = []

    for d in npData[:,8]:
        try:
            deathDate = datetime.datetime.strptime(d, '%d/%m/%Y').date()
            distributionDay.append( deathDate.strftime("%A") )
            distributionMonth.append( deathDate.strftime("%B") )
        except: 
            pass

    dayCounter = Counter(distributionDay)
    print ( "\nDefuncion segun dia de la semana" )
    for idx in range(len(dayCounter)):
        print ( "%4d : %s" % (dayCounter.most_common()[idx][1], dayCounter.most_common()[idx][0]) )

    monthCounter = Counter(distributionMonth)
    print ( "\nDefuncion segun mes" )
    for idx in range(len(monthCounter)):
        print ( "%4d : %s" % (monthCounter.most_common()[idx][1], monthCounter.most_common()[idx][0]) )


# Distribution of deaths by month or date (plot version)
if True:
    distributionDay = [0] * 7
    distributionMonth = [0] * 12

    for d in npData[:,8]:
        try:
            deathDate = datetime.datetime.strptime(d, '%d/%m/%Y').date()

            distributionDay[deathDate.weekday()] += 1
            distributionMonth[deathDate.month-1] += 1
        except: 
            pass

    y_pos = np.arange(len(distributionMonth))

    str_months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Junio',
                'Julio', 'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre']

    plt.bar(y_pos, distributionMonth, align='center', alpha=0.5)
    plt.xticks(y_pos, str_months, rotation='vertical')
    plt.ylabel('# Defunciones')
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.05, 0)
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,y1,y2 + 20))    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.2)
    plt.show()

    y_pos = np.arange(len(distributionDay))

    str_day = ['Lunes', 'martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    
    plt.bar(y_pos, distributionDay, align='center', alpha=0.5)
    plt.xticks(y_pos, str_day, rotation='vertical')
    plt.ylabel('# Defunciones')
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.05, 0)
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,y1,y2 + 20))    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.2)
    plt.show()

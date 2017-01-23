import csv
import numpy as np
import datetime
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter

print ( " ---- BIRTHS ---------------------------------------------" )

#file  = open('data/allDefunciones.csv', "r")
file  = open('data/allNacimientos.csv', "r")
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
npBirthData = np.array(allData)
NPBIRTHDATA = np.array(ALLDATA)

print ( "\nNumber of Entries: %4d" % npBirthData.shape[0] )
print ( "Number of Columns: %4d\n" % npBirthData.shape[1] )

# Check number of entries per column and the most common value
print ( "                      # - Unique - Most common" )

for idx in range(len(header)):
    vec  = NPBIRTHDATA[:,idx]
    vec2 = vec [ NPBIRTHDATA[:,idx] != '' ]

    if len(vec2) > 0:
        count = Counter(vec2)
        print ( "[%2s] %-15s: %4d - %6d - ( %4d | %s )" % (idx, header[idx], vec2.size, len(count), count.most_common(1)[0][1], count.most_common(1)[0][0]) )
    else:
        print ( " [%2s] %-15s: %4d" % (idx, header[idx], vec2.size) )

# Births by months
if True:
    distributionDay = [0] * 7
    distributionMonth = [0] * 12

    for d in npBirthData[:,4]:
        try:
            deathDate = datetime.datetime.strptime(d, '%d/%m/%Y').date()

            distributionDay[deathDate.weekday()] += 1
            distributionMonth[deathDate.month-1] += 1
        except: 
            pass

    y_pos = np.arange(len(distributionMonth))
    str_months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre']

    f1 = plt.figure()
    plt.bar(y_pos, distributionMonth, align='center', alpha=0.5)
    plt.xticks(y_pos, str_months, rotation='vertical')
    plt.ylabel('# Nacimientos')
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.05, 0)
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,y1,y2 + 20))    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.2)
    f1.show()


    f2 = plt.figure()
    y_pos = np.arange(len(distributionDay))
    str_day = ['Lunes', 'martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    
    plt.bar(y_pos, distributionDay, align='center', alpha=0.5)
    plt.xticks(y_pos, str_day, rotation='vertical')
    plt.ylabel('# Nacimientos')
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.05, 0)
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,y1,y2 + 20))    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.2)
    f2.show()

print ( "\n\n ---- DEATHS ---------------------------------------------" )

file  = open('data/allDefunciones.csv', "r")
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
npDefData = np.array(allData)
NPDEFDATA = np.array(ALLDATA)

print ( "\nNumber of Entries: %4d" % npDefData.shape[0] )
print ( "Number of Columns: %4d\n" % npDefData.shape[1] )

# Check number of entries per column and the most common value
print ( "                      # - Unique - Most common" )

for idx in range(len(header)):
    vec  = NPDEFDATA[:,idx]
    vec2 = vec [ NPDEFDATA[:,idx] != '' ]

    if len(vec2) > 0:
        count = Counter(vec2)
        print ( "[%2s] %-15s: %4d - %6d - ( %4d | %s )" % (idx, header[idx], vec2.size, len(count), count.most_common(1)[0][1], count.most_common(1)[0][0]) )
    else:
        print ( " [%2s] %-15s: %4d" % (idx, header[idx], vec2.size) )

# print more common jobs
if False:

    vec  = NPDEFDATA[:,18]
    vec2 = vec [ NPDEFDATA[:,18] != '' ]
    count = Counter(vec2)

    print ("\nOficios mas comunes")
    for idx in range(len(count)):
        print ( "%4d : %s" % (count.most_common()[idx][1], count.most_common()[idx][0]) )

# print diff between death and burial
if False:
    diffBurial = []
    # we compare the death date DEFUNCION2 (8) with burial date ENTERRAMIENTO2 (11)
    for ii, defuncion in enumerate(NPDEFDATA[:,8]):
        if (defuncion != '') and (NPDEFDATA[ii,11] != ''):
            try:
                deathDate  = datetime.datetime.strptime(defuncion,     '%d/%m/%Y').date()
                burialDate = datetime.datetime.strptime(NPDEFDATA[ii,11], '%d/%m/%Y').date()
                diffBurial.append( (burialDate - deathDate).days )

    
            except: 
                pass

    delay = Counter(diffBurial)
    print ( "\nTiempo de la muerte al entierro" )
    for idx in range(len(delay)):
        print ( "%4d : %d dias" % (delay.most_common()[idx][1], delay.most_common()[idx][0]) )


# Print all observations
if False:
    for obs in npDefData[:,17]:
        if obs != '':
            print ("%s\n" % obs)

# Distribution of deaths by month (text version)
if True:
    distributionDay = []
    distributionMonth = []

    for d in npDefData[:,8]:
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

    for d in npDefData[:,8]:
        try:
            deathDate = datetime.datetime.strptime(d, '%d/%m/%Y').date()

            distributionDay[deathDate.weekday()] += 1
            distributionMonth[deathDate.month-1] += 1
        except: 
            pass

    y_pos = np.arange(len(distributionMonth))
    str_months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre']

    f3 = plt.figure()
    plt.bar(y_pos, distributionMonth, align='center', alpha=0.5)
    plt.xticks(y_pos, str_months, rotation='vertical')
    plt.ylabel('# Defunciones')
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.05, 0)
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,y1,y2 + 20))    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.2)
    f3.show()

    y_pos = np.arange(len(distributionDay))
    str_day = ['Lunes', 'martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    
    f4 = plt.figure()
    plt.bar(y_pos, distributionDay, align='center', alpha=0.5)
    plt.xticks(y_pos, str_day, rotation='vertical')
    plt.ylabel('# Defunciones')
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.05, 0)
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,y1,y2 + 20))    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.2)
    f4.show()

    # add z-test for statistical significance of deaths by month
    print( "Z-Tests for deaths each month" )
    print( stats.zscore(distributionMonth) )


input() # keep alive the figures
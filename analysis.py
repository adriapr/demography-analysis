import csv
import numpy as np
import datetime
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter

def main():
    print ( " ---- BIRTHS ---------------------------------------------" )

    [headerBirth, npBirthData, NPBIRTHDATA] = readDB ('data/allNacimientos.csv')

    # Distribution of births by month and weekday (text version)
    if True:
        #printDateDistribution( npBirthData[:,4] )
        [f1, f2, deathByDay, deathByMonth] = plotDateDistribution ( npBirthData[:,4], '#Nacimientos' )

    print ( "\n\n ---- DEATHS ---------------------------------------------" )

    [headerDeath, npDeathData, NPDEATHDATA] = readDB ('data/allDefunciones.csv')

    # print more common jobs
    if True:
        printMostCommon( NPDEATHDATA[:,18], 15 )

    # print diff between death and burial
    if False:
        diffBurial = []
        # we compare the death date DEFUNCION2 (8) with burial date ENTERRAMIENTO2 (11)
        for ii, defuncion in enumerate(NPDEATHDATA[:,8]):
            if (defuncion != '') and (NPDEATHDATA[ii,11] != ''):
                try:
                    deathDate  = datetime.datetime.strptime(defuncion,     '%d/%m/%Y').date()
                    burialDate = datetime.datetime.strptime(NPDEATHDATA[ii,11], '%d/%m/%Y').date()
                    diffBurial.append( (burialDate - deathDate).days )
                except: 
                    pass

        delay = Counter(diffBurial)
        print ( "\nTiempo de la muerte al entierro" )
        for idx in range(len(delay)):
            print ( "%4d : %d dias" % (delay.most_common()[idx][1], delay.most_common()[idx][0]) )


    # Print all observations
    if False:
        for obs in npDeathData[:,17]:
            if obs != '':
                print ("%s\n" % obs)

    # Death distributions
    if True:
        #printDateDistribution( npDeathData[:,8] )
        [f1, f2, deathByDay, deathByMonth] = plotDateDistribution ( npDeathData[:,8], '#Nacimientos' )

    print( "\n\n - PRESS ANY KEY TO FINISH THE SCRIPT (will close all figures) -")
    input() # keep alive the figures



# ----------------------- Functions --------------------------------------------------------

def readDB( str_file ):

    file  = open(str_file, "r")
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

    return [header, npData, NPDATA]

def printMostCommon( vec, n=float("inf") ):

    vec2 = vec [ vec != '' ]
    count = Counter(vec2)

    print ("\nOficios mas comunes")
    for idx in range(len(count)):
        if idx  > n-1:
            break
        print ( "%4d : %s" % (count.most_common()[idx][1], count.most_common()[idx][0]) )

def plotDateDistribution ( vec, str_ylabel ):

        str_day = ['Lunes', 'martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']

        str_months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                    'Julio', 'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre']

        distributionDay = [0] * 7
        distributionMonth = [0] * 12

        for d in vec:
            try:
                deathDate = datetime.datetime.strptime(d, '%d/%m/%Y').date()

                distributionDay[deathDate.weekday()] += 1
                distributionMonth[deathDate.month-1] += 1
            except: 
                pass

        # compute z-scores to detect outliers
        zScoreDay   = stats.zscore(distributionDay)
        zScoreMonth = stats.zscore(distributionMonth)

        print( "\nPor dia de la semana: ")
        for i, v in enumerate(distributionDay):
            print ( "%12s : %4d ( %+.2f )" % (str_day[i], v, zScoreDay[i]) )

        print( "\nPor mes del año: ")
        for i, v in enumerate(distributionMonth):
            print ( "%12s : %4d ( %+.2f )" % (str_months[i], v, zScoreMonth[i]) )

        y_pos = np.arange(len(distributionMonth))

        f1 = plt.figure()
        plt.bar(y_pos, distributionMonth, align='center', alpha=0.5)
        plt.xticks(y_pos, str_months, rotation='vertical')
        plt.ylabel( str_ylabel )
        # Pad margins so that markers don't get clipped by the axes
        plt.margins(0.05, 0)
        x1,x2,y1,y2 = plt.axis()
        plt.axis((x1,x2,y1,y2 + 20))    # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.2)
        f1.show()


        f2 = plt.figure()
        y_pos = np.arange(len(distributionDay))
        
        plt.bar(y_pos, distributionDay, align='center', alpha=0.5)
        plt.xticks(y_pos, str_day, rotation='vertical')
        plt.ylabel( str_ylabel )
        # Pad margins so that markers don't get clipped by the axes
        plt.margins(0.05, 0)
        x1,x2,y1,y2 = plt.axis()
        plt.axis((x1,x2,y1,y2 + 20))    # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.2)
        f2.show()

        return [f1, f2, distributionDay, distributionMonth]


if __name__ == "__main__":
    main()
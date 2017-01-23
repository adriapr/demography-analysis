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
        [figBirth, birthByDay, birthByMonth, birthByYear] = \
            plotDateDistribution ( npBirthData[:,4], '#Nacimientos', True )

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

    # Death distributions
    if True:
        [figDeath, deathByDay, deathByMonth, deathByYear] = \
            plotDateDistribution ( npDeathData[:,8], '#Defunciones', True )

    # Print all observations
    if False:
        for obs in npDeathData[:,17]:
            if obs != '':
                print ("%s\n" % obs)

    # Print observations of year 1803 (max number od deaths)
    # Print observations of year 1781 (max number od deaths in summer)
    if False:
        for i, val in enumerate(npDeathData[:,8]):
            try:
                dYear = datetime.datetime.strptime(val, '%d/%m/%Y').date().year
                if dYear == 1781 and npDeathData[i,17] != '':
                    print ("%s\n" % npDeathData[i,17])
            except:
                pass

    # check distribution by month of 1803, was it concentrated or just a bad year?
    if True:
        deaths1802 = []
        deaths1803 = []
        for d in npDeathData[:,8]:
            try:
                deathDate = datetime.datetime.strptime(d, '%d/%m/%Y').date()

                if deathDate.year == 1802:
                    deaths1802.append(d)
                if deathDate.year == 1803:
                    deaths1803.append(d)
            except: 
                pass

        [figDeath, deathByDay, deathByMonth, deathByYear] = \
            plotDateDistribution ( deaths1802, '#Defunciones 1802', True )
        [figDeath, deathByDay, deathByMonth, deathByYear] = \
            plotDateDistribution ( deaths1803, '#Defunciones 1803', True )

    # Check if there are years when people died a lot in summer
    if True:
        distributionDeathsInSummer   = [0] * 2000
        distributionDeathsNotSummer  = [0] * 2000

        for i, val in enumerate(npDeathData[:,8]):
            try:
                dYear  = datetime.datetime.strptime(val, '%d/%m/%Y').date().year
                dMonth = datetime.datetime.strptime(val, '%d/%m/%Y').date().month-1

                if dMonth == 6 or dMonth == 7 or dMonth == 8:
                    distributionDeathsInSummer[dYear] += 1
                else:
                    distributionDeathsNotSummer[dYear] += 1
            except:
                pass

        # find first and last year with data 
        min_year = next(i for i, v in enumerate(distributionDeathsInSummer) if v > 0)
        max_year_tmp = next(i for i, v in enumerate(reversed(distributionDeathsInSummer)) if v > 0)
        max_year = len(distributionDeathsInSummer) - 1 - max_year_tmp
        yearRange = np.arange(min_year, max_year+1)

        fig = plt.figure()
        values = distributionDeathsInSummer[min_year:max_year+1]
        ax1 = plt.subplot(2,1,1)
        ax1.bar( yearRange, values, align='center', alpha=0.3)
        ax1.set_xticks( [v for v in yearRange if v % 10 == 0] )
        plt.ylabel( '#defunciones Julio, Agosto y Setiembre' )
        # Pad margins so that markers don't get clipped by the axes
        plt.margins(0.05, 0)
        x1,x2,y1,y2 = ax1.axis()
        ax1.axis((x1,x2,y1,y2 + 20))    # Tweak spacing to prevent clipping of tick-labels

        values = distributionDeathsNotSummer[min_year:max_year+1]
        ax2 = plt.subplot(2,1,2)
        ax2.bar( yearRange, values, align='center', alpha=0.3)
        ax2.set_xticks( [v for v in yearRange if v % 10 == 0] )
        plt.ylabel( '#defunciones resto año' )
        # Pad margins so that markers don't get clipped by the axes
        plt.margins(0.05, 0)
        x1,x2,y1,y2 = ax2.axis()
        ax2.axis((x1,x2,y1,y2 + 20))    # Tweak spacing to prevent clipping of tick-labels


        fig.subplots_adjust(left=0.06, right=0.99, top= 0.99, bottom=0.05)
        fig.show()        

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
    print ( "                         # - Unique - Most common" )

    for idx in range(len(header)):
        vec  = NPDATA[:,idx]
        vec2 = vec [ NPDATA[:,idx] != '' ]

        if len(vec2) > 0:
            count = Counter(vec2)
            print ( "[%2s] %-15s: %4d - %6d - ( %4d | %s )" % (idx, header[idx], vec2.size, len(count), count.most_common(1)[0][1], count.most_common(1)[0][0]) )
        else:
            print ( "[%2s] %-15s: %4d" % (idx, header[idx], vec2.size) )

    return [header, npData, NPDATA]

def printMostCommon( vec, n=float("inf") ):

    vec2 = vec [ vec != '' ]
    count = Counter(vec2)

    print ("\nOficios mas comunes")
    for idx in range(len(count)):
        if idx  > n-1:
            break
        print ( "%4d : %s" % (count.most_common()[idx][1], count.most_common()[idx][0]) )

def plotDateDistribution ( vec, str_ylabel, showPlot=True ):

        str_day = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado']

        str_months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                    'Julio', 'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre']

        str_monthsShort = [v[0] for v in str_months]

        distributionDay   = [0] * 7
        distributionMonth = [0] * 12
        distributionYear  = [0] * 2000

        for d in vec:
            try:
                deathDate = datetime.datetime.strptime(d, '%d/%m/%Y').date()

                distributionDay[deathDate.weekday()] += 1
                distributionMonth[deathDate.month-1] += 1
                distributionYear[deathDate.year]     += 1
            except: 
                pass

        # compute z-scores to detect outliers
        # zScoreDay   = stats.zscore(distributionDay)
        # zScoreMonth = stats.zscore(distributionMonth)
        # zScoreYear  = stats.zscore(distributionYear)

        zScoreDay   = MADscore(distributionDay)
        zScoreMonth = MADscore(distributionMonth)
        zScoreYear  = MADscore(distributionYear)

        # find first and last year with data 
        min_year = next(i for i, v in enumerate(distributionYear) if v > 0)
        max_year_tmp = next(i for i, v in enumerate(reversed(distributionYear)) if v > 0)
        max_year = len(distributionYear) - 1 - max_year_tmp
        yearRange = np.arange(min_year, max_year+1)
        # print( " %d - %d" % (min_year, max_year) )

        print( "\nPor dia de la semana: ")
        for i, v in enumerate(distributionDay):
            print ( "%12s : %4d ( %+.2f )" % (str_day[i], v, zScoreDay[i]) )

        print( "\nPor mes del año: ")
        for i, v in enumerate(distributionMonth):
            print ( "%12s : %4d ( %+.2f )" % (str_months[i], v, zScoreMonth[i]) )

        # print( "\nPor año: ")
        # for i, v in enumerate(distributionYear):
        #     if v > 0:
        #         print ( "%12s : %4d ( %+.2f )" % (i, v, zScoreYear[i]) )

        if showPlot:


            fig = plt.figure()

            ax1 = plt.subplot(2,2,1)
            ax1.bar(range(12), distributionMonth, align='center', alpha=0.5)
            ax1.set_xticks( range(12) )
            ax1.set_xticklabels( [v[0] for v in str_months] )
            ax1.set_ylabel( str_ylabel )
            # Pad margins so that markers don't get clipped by the axes
            ax1.margins(0.05, 0)
            x1,x2,y1,y2 = ax1.axis()
            ax1.axis((x1,x2,y1,y2 + 20))


            ax2 = plt.subplot(2,2,2)
            ax2.bar(range(7), distributionDay, align='center', alpha=0.5)
            ax2.set_xticks( range(7) )
            ax2.set_xticklabels( [v[0] for v in str_day] )
            plt.ylabel( str_ylabel )
            # Pad margins so that markers don't get clipped by the axes
            plt.margins(0.05, 0)
            x1,x2,y1,y2 = ax2.axis()
            ax2.axis((x1,x2,y1,y2 + 20))    # Tweak spacing to prevent clipping of tick-labels

            values = distributionYear[min_year:max_year+1]

            ax3 = plt.subplot(2,2,(3,4))
            ax3.bar( yearRange, values, align='center', alpha=0.3)
            ax3.set_xticks( [v for v in yearRange if v % 10 == 0] )
            plt.ylabel( str_ylabel )
            # Pad margins so that markers don't get clipped by the axes
            plt.margins(0.05, 0)
            x1,x2,y1,y2 = ax3.axis()
            ax3.axis((x1,x2,y1,y2 + 20))    # Tweak spacing to prevent clipping of tick-labels


            fig.subplots_adjust(left=0.06, right=0.99, top= 0.99, bottom=0.05)
            fig.show()
        else:
            fig = None

        return [fig, distributionDay, distributionMonth, distributionYear]

def MADscore(vec):

    median = np.median(vec)
    median_absolute_deviation = np.median([np.abs(v - median) for v in vec])
    modified_z_scores = [0.6745 * (v - median) / median_absolute_deviation for v in vec]
    return modified_z_scores


if __name__ == "__main__":
    main()
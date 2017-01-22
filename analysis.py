import csv
import numpy as np
from collections import Counter
import datetime

file  = open('data/allDefunciones.csv', "rb")
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


print '\nNumber of Entries: %4d' % npData.shape[0]
print 'Number of Columns: %4d\n' % npData.shape[1]


# Check number of entries per column and the most common value
print '                      # - Unique - Most common'

for idx in range(len(header)):
    vec  = NPDATA[:,idx]
    vec2 = vec [ NPDATA[:,idx] != '' ]

    if len(vec2) > 0:
        count = Counter(vec2)
        print '  %-15s: %4d - %6d - ( %4d | %s )' % (header[idx], vec2.size, len(count), count.most_common(1)[0][1], count.most_common(1)[0][0])
    else:
        print '  %-15s: %4d' % (header[idx], vec2.size)


# for defunciones
if True:

    vec  = NPDATA[:,18]
    vec2 = vec [ NPDATA[:,18] != '' ]
    count = Counter(vec2)

    print '\nOficios mas comunes'
    for idx in range(len(count)):
        print '%4d : %s' % (count.most_common()[idx][1], count.most_common()[idx][0])


if True:
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
    print '\nTiempo de la muerte al entierro'
    for idx in range(len(delay)):
        print '%4d : %d dias' % (delay.most_common()[idx][1], delay.most_common()[idx][0])

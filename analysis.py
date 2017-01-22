import csv # The digger
import numpy as np # The magic
from collections import Counter

fileDataName  = open('data/allNacimientos.csv', "rb")
reader = csv.reader(fileDataName)

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

fileDataName.close()

# put all data in  numpy
npData = np.array(allData)
NPDATA = np.array(ALLDATA)


print '\nNumber of Entries: %4d' % npData.shape[0]
print 'Number of Columns: %4d\n' % npData.shape[1]

# Check number of entries per column and the most common value
for idx in range(len(header)):
    vec  = NPDATA[:,idx]
    vec2 = vec [ NPDATA[:,idx] != '' ]

    if len(vec2) > 0:
        count = Counter(vec2)
        print '  %-15s: %4d - (%5d | %s)' % (header[idx], vec2.size, count.most_common(1)[0][1], count.most_common(1)[0][0])
    else:
        print '  %-15s: %4d' % (header[idx], vec2.size)

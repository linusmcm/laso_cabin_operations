import csv
import datetime
import time
from datetime import datetime

alltrans = []
fraud_cards = []
threshold = float(40)
p = '%Y-%m-%dT%H:%M:%S'
epoch = datetime(1970, 1, 1)

# opening, reading the CSV file, populating list
with open('trans1.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
            alltrans.append(lines)

#read the transactions one by one. remove the transaction from the array if it has been processed
for trans in alltrans[:]:

    #get the details of the current transaction
    current_card = str(trans[0])
    current_time = (datetime.strptime(trans[1], p) - epoch).total_seconds()
    current_max_time = current_time + 86400
    current_total = float(trans[2])
    alltrans.pop(0)

    # only check cards that are not yet marked fraudulent
    # break from loop when the next trans is more than 24h from current trans. data is chronological
    if((len(alltrans) != 0) and (fraud_cards.count(str(current_card))==0)):
        for nexttrans in alltrans:
            nexttrans_card = str(nexttrans[0]);
            nexttrans_time = (datetime.strptime(nexttrans[1], p) - epoch).total_seconds()
            nexttrans_amount = float(nexttrans[2])

            if((nexttrans_time < current_max_time) and (current_card == nexttrans_card)):
                current_total = current_total + nexttrans_amount
            if(nexttrans_time > current_max_time):
                 break

    # dont add card already in the fraudulent card list
    if((current_total > threshold) and (fraud_cards.count(str(current_card))==0)):
        fraud_cards.append(current_card)
    current_total = 0

print (fraud_cards)

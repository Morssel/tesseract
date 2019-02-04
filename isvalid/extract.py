import os
import csv

import sys
from decimal import Decimal
from re import sub


from util import ValidateVIN



# python ml.py training/AI_VehicleInfo_Joined_Lexus.txt
# python ml.py training/lexus/vin_dataset_lexus.txt

# Remove invalid characters from vin I,O,Q
blacklist = [["I", "1"], ["O", "0"], ["Q", "0"]]

# Per ISO 3779 valid prefixs for World Manufacturer Identifier
# and Vehicle Descriptor Section
# basis: looking for ocr errors that misrepresent portions of the VIN
# This is done by creating a dictionary of common mistakes and resolution
# example: record.replace(mfg["kia"]["WMIVDS"][0...n][0], mfg["kia"]["WMIVDS"][0...n][1])
mfg_kia = {"WMIVDS": [["SX", "5X"], ["3KP", "5X"]]}
# valid kia: 5X:3KP:KN

mfg_rules = {
    "mfg": {"kia": mfg_kia}
}

def export_vin(filePath):

    value = 0.0
    current_principal = 0.0
    current_principal_total = 0
    data = csv.reader(open(filePath), delimiter=' ',)
    


    print mfg_kia["WMIVDS"][1]

    # validFile = open("validVins.txt", "w")
    # encodedFile = open("encodedvins.txt", "w")
    # invalidFile = open("invalidVins.txt", "w")

    # should be lookup table for manufcaturer type
    mfg_header = "5X"


    for row in data:

        if len(row) > 1:

            if len(row[0]) == 11  and len(row[1]) == 6:
                
                record = "{0}{1}".format(row[0], row[1])
                # TODO: Waiting on spliced file
                #current_principal = row[6]

                # TODO: Waiting on spliced file
                #value = Decimal(sub(r'[^\d.]', '', current_principal))

                # Remove invalid characters from VIN
                for key in blacklist:
                    record = record.replace(key[0], key[1])

                # TODO: Waiting on spliced file
                #current_principal_total += value
                result = ValidateVIN(record.upper())
                
                if result[0]:
                    # we have good data
                    print record
                    # TODO: Waiting on spliced file
                    #print record, current_principal, current_principal_total
                    # validFile.write(recordData + "\n")
                    # encodedFile.write(encodedData + "\n")
                else:

                    for key in mfg_kia["WMIVDS"]:
                        record = record.replace(key[0], key[1])

                    #if record.startswith("SX"):
                        # limit replacement of header to 1 occurence in the
                        # event the vin has the header as a legitimate part of
                        # its structure downstream
                        #record = record.replace("SX", "5X", 1)

                    result = ValidateVIN(record.upper())

                    if result[0]:
                        # TODO: Waiting on spliced file
                        #print record, current_principal, current_principal_total
                        print record
                    else: 
                        # TODO: Waiting on spliced file
                        #print record, " invalid", current_principal
                        print record
                    #invalidFile.write(recordData + "\t" + vinResult[2] + "\n")

    # TODO: Waiting on spliced file
    #print "Total: ", current_principal_total

        
        #print(row)
        
        # try:
        #     recordData = "{0}\t{1}".format(row[0], row[4])
        #     encodedData = "{0}\t{1}\t{2}\t{3}".format(row[0], row[4], sum(row[0][:8].encode('utf-8')), 1)

        #     vinResult = ValidateVIN(row[0].upper())
            
        #     if vinResult[0]:
        #         validFile.write(recordData + "\n")
        #         encodedFile.write(encodedData + "\n")
        #     else:
        #         invalidFile.write(recordData + "\t" + vinResult[2] + "\n")
        # except csv.Error as e:
        #     print(e)
        #     pass



    # validFile.flush()
    # validFile.close()
    # encodedFile.flush()
    # encodedFile.close()
    # invalidFile.flush()
    # invalidFile.close()


# cat vinValidation.txt | grep False > invalidVins.txt
# cat vinValidation.txt | grep True > validVins.txt
# python ml.py > vinValidation.txt


if __name__ == "__main__": 
    print "Running extractor..."

    export_vin(sys.argv[1])    
 

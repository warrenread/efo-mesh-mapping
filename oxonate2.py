#!/usr/bin/env python3

import logging                              # Enable logging in an external file
from configparser import SafeConfigParser   # For parsing the config file
import requests                             # For doing API callas
import sys                                  # For the imput parameters
import time                                 # Just to use the sleep methode
import json
import csv
import grab_gwas

""" Method to execute API call; do this in a function to catch potential errors """
def apiCall(url, data):
    try:
        r = requests.post(url, data)        # Execute POST with url and data
    except:                                 # Executed if there is an error
        time.sleep(10)                      # Sleep 10 seconds
        logging.info("API exception, try again after 10 second delay")
        try:
            r = requests.post(url, data)    # Try again to call the API
            logging.info("Success after 10 seconds")
        except:
            logging.info("API call failed!")
            raise                           # Did not work, so we quit
    return r

""" Method to load new entry into dictionary (mapperDict) of EFO->MeSH mappings """
def loadMapping(mapperDict, efoId, efoLabel, meshId, meshLabel, steps, confidence):
    meshHit = { "efoLabel": efoLabel, "meshId": meshId, "meshLabel": meshLabel, "distance": steps, "confidence": confidence }
    """ Has this EFO id already been added? - in which case, add MeSH id to array associated with EFO id dictionary key"""
    if efoId in mapperDict.keys():
        meshIdMappings = []
        """ Build array of existing MeSH hits for this EFO id """
        for meshMapping in mapperDict[efoId]:
            meshIdMappings.append(meshMapping["meshId"])
        """ Check whether this MeSH id was already found for this EFO id; if not, append it """
        if not ( meshId in meshIdMappings ):
            mapperDict[efoId].append(meshHit)
    else:
        """ If EFO id is not in dictionary, create new dictionary entry """
        mapperDict[efoId] = [ meshHit ]


#
# Start with: ./oxonate2.py oxoconfig.ini
#

# Check that we have 2 input parameters
if (len(sys.argv)!=2):
    msg = "Incorrect number of parameters: config file required as input parameter"
    print(msg)
else:

    """ Main program code """
    path=sys.argv[1]                        # Read in input parameter
    config = SafeConfigParser()             # "Start" the config
    config.read(path)                       # Read in config from path
    path_to_validate_log=config.get('Params', 'pathToLogFile')  # Set log file to path from config
    logging.basicConfig(filename=path_to_validate_log, level=logging.INFO, format='%(asctime)s - %(message)s')
    url = config.get('Params', 'oxoUrl')    # Get url from config
    stepConf = config.get('Params', 'stepConfidence')  # Get confidence per step from config
    print("Getting traits ...")
    traits = grab_gwas.get_efo_traits()
    print("Count of unique EFO traits is %d" % (len(traits)))
    print("No of keys is %d" % (len(traits.keys())))
    print()
    print("Here are the EFO->MeSH X-references from Oxo ...")
    print()
    data = {"ids":list(traits.keys()),"mappingTarget":["MeSH"]}

    jsonStrings = []
    for dis in range(1, 4):                   # From 1 to 3
        disString = "%d" % dis 
        data["distance"] = disString
        reply = apiCall(url, data)            # Execute API call with url and data
        jsonContent = reply.content
        jsonString = json.loads(jsonContent)
        jsonStrings.append(jsonString)
        # print(json.dumps(jsonString))

    print("No of successful calls to URI (max=3): %d" % (len(jsonStrings)))
    print()
    meshDict = {}
    cnt = 1
    allResCnt = 0
    for eachString in jsonStrings:  # I.e. each distance: 1 to 3
        subJson = eachString["_embedded"]["searchResults"]
        for res in subJson:
            # print("ok")
            for mappingFound in res["mappingResponseList"]:
                # print("EFO ID: %s; distance: %d; MeSH ID: %s" % (res["queryId"], cnt, mappingFound["curie"]))
                # print("ok")
                loadMapping(
                        meshDict,
                        res["queryId"],
                        traits[res["queryId"]],
                        mappingFound["curie"],
                        mappingFound["label"],
                        ("%d" % cnt),
                        ("%f" % (float(stepConf) ** cnt)))
                # print("EFO id: %s; MeSH id: %s" % (res["queryId"], mappingFound["curie"]))
                allResCnt += 1
        cnt += 1
    print("Total MeSH terms at distances 1-3: %d" % (allResCnt))
    print()

    # print()
    # print(json.dumps(meshDict))
    # print()
    for efoSource in meshDict.keys():
        for meshTarget in meshDict[efoSource]:
            outFields = []
            outFields.append(efoSource)
            # outFields.append(efoLabel)
            outFields.append(meshTarget["efoLabel"])
            outFields.append(meshTarget["meshId"])
            outFields.append(meshTarget["confidence"])
            outFields.append(meshTarget["meshLabel"])
            print("\t".join(outFields))
        # print("Query term: %s" % efoSource)
    print()
    # print("Ok, we're done.")

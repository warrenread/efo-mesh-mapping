#!/usr/bin/env python3

import requests
import csv

def get_efo_traits():

    """ Uncomment the bit below to re-download GWAS spreadsheet """
    """
    gwasUrl = "https://www.ebi.ac.uk/gwas/api/search/downloads/alternative"
    r = requests.get(gwasUrl, allow_redirects=True)
    gwasFile = open("gwas.tsv", "wb")
    gwasFile.write(r.content)
    gwasFile.close()
    """

    with open("gwas.tsv", "r", newline='') as gwasFile:
        # efoTraits = []
        recordCount = 0
        nonUniqueTraitCount = 0
        efoTraitsDict = {}
        gwasReader = csv.DictReader(gwasFile, delimiter='\t')
        for gwasRecord in gwasReader:
            gMappedTraits = gwasRecord["MAPPED_TRAIT"]
            traitList = gMappedTraits.split(", ")
            gMappedTraitUris = gwasRecord["MAPPED_TRAIT_URI"]
            traitUriList = gMappedTraitUris.split(", ")
            traitCnt = 0  # Unnecessary
            for traitUri in traitUriList:
                uriFragments = traitUri.split("/")
                # print(traitUri)
                if len(uriFragments) > 3 and uriFragments[3] == "efo":
                    efoId = ""
                    efoTrait = ""
                    try:
                        efoId = uriFragments[4].replace("_", ":", 1)
                    except:
                        print("URI is unnaturally truncated!")
                    try:
                        efoTrait = traitList[traitCnt]
                    except:
                        print("Trait and URI list lengths do not match!")
                    efoTraitsDict.update({efoId:efoTrait})
                nonUniqueTraitCount += 1
            recordCount += 1
        # print(len(efoTraits))
        print("Record count: %d" % (recordCount))
        print("Non-unique EFO trait count: %d" % (nonUniqueTraitCount))
        return efoTraitsDict

# traits = get_efo_traits()
# print(traits)
# print(len(traits))

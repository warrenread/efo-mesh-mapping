#!/usr/bin/env python3

import requests
import csv
import spotilities as spot

def get_efo_traits():

    """
    Uncomment the bit below to re-download GWAS spreadsheet
    """
    # gwasUrl = "https://www.ebi.ac.uk/gwas/api/search/downloads/alternative"
    # r = requests.get(gwasUrl, allow_redirects=True)
    # gwasFile = open("gwas.tsv", "wb")
    # gwasFile.write(r.content)
    # gwasFile.close()
    
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
            """
            We have an issue with traits that include a comma! Because lists of
            traits are also comma-separated, we may need to rejoin strings that
            have been split in error: this we do with an algorithmic best guess.
            """
            while len(traitList) > len(traitUriList):
                shortest_string = min(traitList[1:], key=len)
                shortest_index = traitList.index(shortest_string)
                traitList[shortest_index - 1] = ", ".join(
                        traitList[(shortest_index - 1):(shortest_index + 1)])
                del(traitList[shortest_index])
                """
                Just for checking
                """
                # for trait in traitList:
                #     spot.newsflash(trait)
                
            traitCnt = 0  # Very necessary, for matching EFO URI to correct EFO trait
            for traitUri in traitUriList:
                uriFragments = traitUri.split("/")
                # spot.newsflash(traitUri)
                if len(uriFragments) > 3 and uriFragments[3] == "efo":
                    efoId = ""
                    efoTrait = ""
                    try:
                        efoId = uriFragments[4].replace("_", ":", 1)
                    except:
                        spot.newsflash("URI is unnaturally truncated!")
                    try:
                        efoTrait = traitList[traitCnt]
                    except:
                        spot.newsflash("Trait and URI list lengths do not match!")
                    efoTraitsDict.update({efoId:efoTrait})
                traitCnt += 1
                nonUniqueTraitCount += 1
            recordCount += 1
        # spot.newsflash(len(efoTraits))
        spot.newsflash("Record count: %d" % (recordCount))
        spot.newsflash("Non-unique EFO trait count: %d" % (nonUniqueTraitCount))
        return efoTraitsDict

# traits = get_efo_traits()
# print(traits)
# spot.newsflash(len(traits))

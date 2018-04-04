#!/usr/bin/env python3

import requests
import json
import urllib
import grab_gwas

# olsUrl = "http://www.ebi.ac.uk/ols/api/ontologies"
# olsUrl = "http://www.ebi.ac.uk/ols/api/ontologies/efo"
""" olsUrl = "http://www.ebi.ac.uk/ols/api/search" """
encodedEfoStem = urllib.parse.quote(urllib.parse.quote("http://www.ebi.ac.uk/efo/", "safe"))
efoTermStem = "http://www.ebi.ac.uk/ols/api/ontologies/efo/terms/%s" % (encodedEfoStem)
olsSearchUrl = "http://snarf.ebi.ac.uk:8980/ols-beta/api/search"
# olsData = {"page":"1","size":"1"}
# olsData = {"q":"rheumatoid","queryFields":"{label,synonym}"}
# olsData = {"q":"rheumatoid","queryFields":"{label}","ontology":"{mesh}"}
# olsData = {"q":"rheumatoid","queryFields":"synonym","ontology":"efo"}
# olsData = {"q":"rheumatoid,cardiac","queryFields":"label,synonym","ontology":"mesh"}

def olsCall(url, data):
    """ Put in error-catching stuff here """
    r = requests.get(url, data)
    return r

traits = grab_gwas.get_efo_traits()
for efoId in traits:
    efoTermUrl = "%s%s" % (efoTermStem, efoId.replace(":", "_", 1))
    # print(efoTermUrl)
    efoReply = olsCall(efoTermUrl, {})
    efoContent = efoReply.content
    efoObject = json.loads(efoContent)
    efoLabel = efoObject["label"]
    """ Seed search terms array with EFO label """
    encodedEfoSearchTerms = [urllib.parse.quote(efoLabel)]
    efoSynonyms = efoObject["synonyms"]

    """ Add EFO synonyms to search terms array """
    """
    if not efoSynonyms is None:
        for efoSynonym in efoSynonyms:
            # print("Synonym is %s" % (urllib.parse.quote(efoSynonym)))
            encodedEfoSearchTerms.append(urllib.parse.quote(efoSynonym))
    """

    efoQueryString = ",".join(encodedEfoSearchTerms)
    # print("EFO ID: %s\tLabel: %s\tSynonym: %s" % (efoId, efoLabel, efoSynonyms))
    # print(json.dumps(json.loads(efoContent)["label"]))
    olsData = {"q":efoQueryString,"queryFields":"label,synonym","ontology":"mesh","fieldList":"id,iri,label,score,synonym"}
    olsResponse = olsCall(olsSearchUrl, olsData)
    print(json.dumps(olsResponse.json()))
    # print()

# olsResponse = olsCall(olsSearchUrl, olsData)
# print(json.dumps(olsResponse.json()))

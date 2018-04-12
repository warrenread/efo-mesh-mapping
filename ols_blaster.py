#!/usr/bin/env python3
"""
This script generates tsv (simple spreadsheet) output providing all
lexcially-mapped MeSH terms based on labels of unique EFO ids from the GWAS
catalogue, with scores on each match. It can optionally be extended to perform a
lexical search on all EFO term synonyms as well (by uncommenting the indicated
lines of code) but this is not done by default.
"""
import requests
import json
import urllib
import grab_gwas as gwas
import spotilities as spot

efo_stem = "http://www.ebi.ac.uk/efo/"
encodedEfoStem = urllib.parse.quote(urllib.parse.quote(efo_stem, "safe"))
efoTermStem = "http://www.ebi.ac.uk/ols/api/ontologies/efo/terms/%s" % (encodedEfoStem)
olsSearchUrl = "http://snarf.ebi.ac.uk:8980/ols-beta/api/search"

# olsData = {"page":"1","size":"1"}
# olsData = {"q":"rheumatoid","queryFields":"{label,synonym}"}
# olsData = {"q":"rheumatoid","queryFields":"{label}","ontology":"{mesh}"}
# olsData = {"q":"rheumatoid","queryFields":"synonym","ontology":"efo"}
# olsData = {"q":"rheumatoid,cardiac","queryFields":"label,synonym","ontology":"mesh"}

def olsCall(url, data):
    """ Put in error-catching stuff here. """
    r = requests.get(url, data)
    return r

traits = gwas.get_efo_traits()
print("\t".join(("efo_id", "efo_label", "efo_trait", "mesh_id", "mesh_iri", "mesh_label", "mesh_synonym", "score")))
for efoId in traits:
    efoTermUrl = "%s%s" % (efoTermStem, efoId.replace(":", "_", 1))
    # spot.newsflash(efoTermUrl)
    efoReply = olsCall(efoTermUrl, {})
    efoContent = efoReply.content
    efoObject = json.loads(efoContent)
    """ Grab EFO label and synonyms. """
    efoLabel = efoObject["label"]
    efoSynonyms = efoObject["synonyms"]
    """ Seed search terms array with EFO label. Do not pre-encode! """
    # encodedEfoSearchTerms = [urllib.parse.quote(efoLabel)]
    encodedEfoSearchTerms = [efoLabel]
    
    """ Extend search terms to encompass all synonyms. """
    # if not efoSynonyms is None:
    #     for efoSynonym in efoSynonyms:
    #         # spot.newsflash("Synonym is %s" % (urllib.parse.quote(efoSynonym)))
    #         # encodedEfoSearchTerms.append(urllib.parse.quote(efoSynonym))
    #         encodedEfoSearchTerms.append(efoSynonym)

    efoQueryString = ",".join(encodedEfoSearchTerms)
    # print("EFO query string is %s" % (efoQueryString))
    # spot.newsflash("EFO ID: %s\tLabel: %s\tSynonym: %s" % (efoId, efoLabel, efoSynonyms))
    # print(json.dumps(json.loads(efoContent)["label"]))
    olsData = {"q":efoQueryString,"queryFields":"label,synonym","ontology":"mesh","fieldList":"id,iri,label,score,synonym"}
    olsResponse = olsCall(olsSearchUrl, olsData)
    olsJsonObject = olsResponse.json()  # Is this actually necessary?
    # print(json.dumps(olsResponse.json()))
    for hit in olsJsonObject["response"]["docs"]:
        # synonym_count = 0
        if "synonym" in hit:
            for each_synonym in hit["synonym"]:
                print("\t".join((efoId, efoLabel, traits[efoId], hit["id"], hit["iri"], hit["label"], each_synonym, "%f" % (hit["score"]))))
                # synonym_count += 1
        else:
            print("\t".join((efoId, efoLabel, traits[efoId], hit["id"], hit["iri"], hit["label"], "", "%f" % (hit["score"]))))
        # print()
    # spot.newsflash(efoLabel)
    # input("\nPress any key to continue ...\n")

# olsResponse = olsCall(olsSearchUrl, olsData)
# print(json.dumps(olsResponse.json()))

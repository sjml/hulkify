#!/usr/bin/env python
# -*- coding: utf-8 -*-

# system imports
import sys
import pkg_resources
import re
import random
import json

# library imports
import pattern.en

try:
    data = pkg_resources.resource_string(__name__, "./grammar.json")
    GRAMMAR = json.loads(data)
except:
    raise RuntimeError("Couldn't load hulkify grammar file.")


# preprocess to account for unicode
def fixList(myList):
    replacement = []
    for entry in myList:
        replacement.append(entry)
        if u"'" in entry:
            replacement.append(entry.replace(u"'", u"’"))
    return replacement

def fixDict(myDict):
    replacement = {}
    for key, value in myDict.iteritems():
        replacement[key] = value
        if u"'" in key:
            replacement[key.replace(u"'", u"’")] = value
    return replacement

GRAMMAR["PERSONAL_PRONOUNS"] = fixList(GRAMMAR["PERSONAL_PRONOUNS"])
GRAMMAR["PERSONAL_POSSESSIVE_PRONOUNS"] = fixList(GRAMMAR["PERSONAL_POSSESSIVE_PRONOUNS"])
GRAMMAR["CONTRACTION_MAPPING"] = fixDict(GRAMMAR["CONTRACTION_MAPPING"])
GRAMMAR["LINKING_VERBS"] = fixList(GRAMMAR["LINKING_VERBS"])
GRAMMAR["ARTICLES"] = fixList(GRAMMAR["ARTICLES"])
GRAMMAR["DIMINUTIVE_ADJECTIVES"] = fixList(GRAMMAR["DIMINUTIVE_ADJECTIVES"])


def hulkify(bannerText, maxLength=None, encoding="utf-8"):
    if type(bannerText) != unicode:
        hulkText = unicode(bannerText, encoding)
    else:
        hulkText = bannerText

    def removeWordFromMatch(matchObject):
        before = len(matchObject.group(1)) > 0
        after  = len(matchObject.group(3)) > 0

        if not before and not after:
            return matchObject.expand(ur"\2")
        if before and after:
            return matchObject.expand(ur"\1")
        if before:
            return matchObject.expand(ur"\3")
        if after:
            return matchObject.expand(ur"\1")

    def changeTextUnlessOverrun(oldText, newText, maximum):
        if maximum == None:
            return newText
        if len(newText) > maximum:
            return oldText
        return newText

    # Change contractions to their main word. ("can't" -> "not")
    for con, main in GRAMMAR["CONTRACTION_MAPPING"].iteritems():
        hulkText = re.sub(ur"(\s?|^)(\b%s\b)(\s?|$)" % (con), ur"\1%s\3" % main, hulkText, flags=re.IGNORECASE | re.UNICODE)

    # Drop all linking verbs ("am" or "to be")
    for lv in GRAMMAR["LINKING_VERBS"]:
        hulkText = re.sub(ur"(\s?|^)(\b%s\b)(\s?|$)" % (lv), removeWordFromMatch, hulkText, flags=re.IGNORECASE | re.UNICODE)

    # Remove articles.
    for a in GRAMMAR["ARTICLES"]:
        hulkText = re.sub(ur"(\s?|^)(\b%s\b)(\s?|$)" % (a), removeWordFromMatch, hulkText, flags=re.IGNORECASE | re.UNICODE)


    ### everything above here only removes content; after this we have to consider length

    # Replace all personal pronouns (I/me/I've/I'm/etc) with "Hulk"
    for pp in GRAMMAR["PERSONAL_PRONOUNS"]:
        hulkText = changeTextUnlessOverrun(
            hulkText,
            re.sub(ur"(\s?|^)(\b%s\b)(\s?|$)" % (pp), ur"\1Hulk\3", hulkText, flags=re.IGNORECASE | re.UNICODE),
            maxLength
        )
    for ppp in GRAMMAR["PERSONAL_POSSESSIVE_PRONOUNS"]:
        if u"’" in bannerText:
            hulkText = changeTextUnlessOverrun(
                hulkText,
                re.sub(ur"(\s?|^)(\b%s\b)(\s?|$)" % (ppp), ur"\1Hulk’s\3", hulkText, flags=re.IGNORECASE | re.UNICODE),
                maxLength
            )
        else:
            hulkText = changeTextUnlessOverrun(
                hulkText,
                re.sub(ur"(\s?|^)(\b%s\b)(\s?|$)" % (ppp), ur"\1Hulk's\3", hulkText, flags=re.IGNORECASE | re.UNICODE),
                maxLength
            )

    parsed = pattern.en.tag(hulkText, tokenize=False)

    # Change verbs to present tense.
    for wordData in parsed:
        if wordData[1][0] == u"V":
            hulkText = changeTextUnlessOverrun(
                hulkText,
                re.sub(ur"\b%s\b" % wordData[0], pattern.en.lemma(wordData[0]), hulkText, flags=re.IGNORECASE | re.UNICODE),
                maxLength
            )

    # Replace any diminuitive adjective with "puny."
    for wordData in parsed:
        if wordData[1][:2] == u"JJ":
            if wordData[0] in GRAMMAR["DIMINUTIVE_ADJECTIVES"]:
                hulkText = changeTextUnlessOverrun(
                    hulkText,
                    re.sub(ur"\b%s\b" % wordData[0], u"puny", hulkText, flags=re.IGNORECASE | re.UNICODE),
                    maxLength
                )

    # Exclamation points.
    def exclaim(matchObject):
        punct = matchObject.group(0)
        if u"." in punct and punct.count(u"!") == 0:
            # change out periods most of the time
            if (random.random() < 0.7):
                punct = u"!"

        # if we're already at the max, don't intensify
        if (maxLength != None) and (len(hulkText) >= maxLength):
            return punct

        # 30% chance of intensifying
        if (u"." not in punct) and (random.random() < 0.3):
            punct += u"!"
            # slight chance of double intensifying
            if (random.random() < 0.45):
                punct += u"!"
                if u"?" in punct:
                    punct += u"?!"

        return punct

    hulkText = re.sub(ur"([.?!]+)", exclaim, hulkText)

    # Easter egg at mention of "strong"
    strongest = u" Hulk is the strongest there is!"
    if re.search(ur"\bstrong\b", hulkText, re.IGNORECASE | re.UNICODE) != None:
        if (maxLength == None) or (len(hulkText) + len(strongest) <= maxLength):
            hulkText += strongest

    # Convert the whole thing to uppercase. 
    hulkText = hulkText.upper()
    
    return hulkText


if __name__ == '__main__':
    try:
        with open("../test_corpus.txt", "r") as corpusFile:
            corpus = corpusFile.read().split("\n")
    except:
        corpus = []

    for text in corpus:
        print hulkify(unicode(text, "utf-8"), maxLength=140).encode("utf-8")


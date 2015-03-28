#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import random

import pattern.en


PERSONAL_PRONOUNS = [
    u"me",
    u"myself",
    u"I've",
    u"I'm",
    u"I'd",
    u"I'll",
    u"I",
]

PERSONAL_POSSESSIVE_PRONOUNS = [
    u"my",
    u"mine",
]

CONTRACTION_MAPPING = {
    u"ain't" : u"not",
    u"aren't" : u"not",
    u"can't" : u"not",
    u"could've" : u"could",
    u"couldn't" : u"not",
    u"didn't" : u"not",
    u"doesn't" : u"not",
    u"don't" : u"no",
    u"hadn't" : u"not",
    u"hasn't" : u"not",
    u"haven't" : u"not",
    u"he'd" : u"he",
    u"he'll" : u"he",
    u"he's" : u"he",
    u"how'd" : u"how",
    u"how'll" : u"how",
    u"how's" : u"how",
    u"isn't" : u"not",
    u"it'd" : u"it",
    u"it'll" : u"it",
    u"it's" : u"it",
    u"let's" : u"let",
    u"might've" : u"might",
    u"mightn't" : u"not",
    u"must've" : u"must",
    u"mustn't" : u"not",
    u"needn't" : u"not",
    u"not've" : u"not",
    u"oughtn't" : u"not",
    u"shan't" : u"not",
    u"she'd" : u"she",
    u"she'll" : u"she",
    u"she's" : u"she",
    u"should've" : u"should",
    u"shouldn't" : u"not",
    u"that'll" : u"that",
    u"that's" : u"that",
    u"there'd" : u"there",
    u"there're" : u"there",
    u"there's" : u"there",
    u"they'd" : u"they",
    u"they'll" : u"they",
    u"they're" : u"they",
    u"they've" : u"they",
    u"wasn't" : u"not",
    u"we'd" : u"we",
    u"we'll" : u"we",
    u"we're" : u"we",
    u"we've" : u"we",
    u"weren't" : u"not",
    u"what'll" : u"what",
    u"what're" : u"what",
    u"what's" : u"what",
    u"what've" : u"what",
    u"when's" : u"when",
    u"where'd" : u"where",
    u"where's" : u"where",
    u"where've" : u"where",
    u"who'd" : u"who",
    u"who'll" : u"who",
    u"who're" : u"who",
    u"who's" : u"who",
    u"who've" : u"who",
    u"why'll" : u"why",
    u"why're" : u"why",
    u"why's" : u"why",
    u"won't" : u"not",
    u"would've" : u"would",
    u"wouldn't" : u"not",
    u"y'all" : u"you",
    u"you'd" : u"you",
    u"you'll" : u"you",
    u"you're" : u"you",
    u"you've" : u"you",
}

ARTICLES = [
    u"a",
    u"an",
    u"the",
]

LINKING_VERBS = [
    u"be",
    u"is",
    u"was",
    u"shall be",
    u"will be",
    u"has been",
    u"had been",
    u"may be",
    u"should be",
    u"am",
    u"are",
    u"were",
    u"shall have been",
    u"will have been",
    u"have been",
]

DIMINUTIVE_ADJECTIVES = [
    u"small",
    u"meager",
    u"cramped",
    u"limited",
    u"meager",
    u"microscopic",
    u"miniature",
    u"minuscule",
    u"modest",
    u"narrow",
    u"paltry",
    u"short",
    u"slight",
    u"small-scale",
    u"young",
    u"baby",
    u"little",
    u"mini",
    u"petite",
    u"trifling",
    u"wee",
    u"bitty",
    u"immature",
    u"inadequate",
    u"inconsequential",
    u"inconsiderable",
    u"insufficient",
    u"piddling",
    u"pint-sized",
    u"pitiful",
    u"pocket-sized",
    u"stunted",
    u"teensy",
    u"teeny",
    u"trivial",
    u"undersized",
]

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

PERSONAL_PRONOUNS = fixList(PERSONAL_PRONOUNS)
PERSONAL_POSSESSIVE_PRONOUNS = fixList(PERSONAL_POSSESSIVE_PRONOUNS)
CONTRACTION_MAPPING = fixDict(CONTRACTION_MAPPING)
LINKING_VERBS = fixList(LINKING_VERBS)


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
    for con, main in CONTRACTION_MAPPING.iteritems():
        hulkText = re.sub(ur"(\s?|^)(\b%s\b)(\s?|$)" % (con), ur"\1%s\3" % main, hulkText, flags=re.IGNORECASE | re.UNICODE)

    # Drop all linking verbs ("am" or "to be")
    for lv in LINKING_VERBS:
        hulkText = re.sub(ur"(\s?|^)(\b%s\b)(\s?|$)" % (lv), removeWordFromMatch, hulkText, flags=re.IGNORECASE | re.UNICODE)

    # Remove articles.
    for a in ARTICLES:
        hulkText = re.sub(ur"(\s?|^)(\b%s\b)(\s?|$)" % (a), removeWordFromMatch, hulkText, flags=re.IGNORECASE | re.UNICODE)


    ### everything above here only removes content; after this we have to consider length

    # Replace all personal pronouns (I/me/I've/I'm/etc) with "Hulk"
    for pp in PERSONAL_PRONOUNS:
        hulkText = changeTextUnlessOverrun(
            hulkText,
            re.sub(ur"(\s?|^)(\b%s\b)(\s?|$)" % (pp), ur"\1Hulk\3", hulkText, flags=re.IGNORECASE | re.UNICODE),
            maxLength
        )
    for ppp in PERSONAL_POSSESSIVE_PRONOUNS:
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
            if wordData[0] in DIMINUTIVE_ADJECTIVES:
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
    if (u" strong " in hulkText):
        if (maxLength == None) or (len(hulkText) + len(strongest) <= maxLength):
            hulkText += strongest

    # Convert the whole thing to uppercase. 
    hulkText = hulkText.upper()
    
    return hulkText


if __name__ == '__main__':
    try:
        with open("./test_corpus.txt", "r") as corpusFile:
            corpus = corpusFile.read().split("\n")
    except:
        corpus = []

    for text in corpus:
        print hulkify(unicode(text, "utf-8"), maxLength=140).encode("utf-8")


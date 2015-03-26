#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import random

import pattern.en


PERSONAL_PRONOUNS = [
    "me",
    "myself",
    "I've",
    "I'm",
    "I'd",
    "I'll",
    "I",
]

PERSONAL_POSSESSIVE_PRONOUNS = [
    "my",
    "mine",
]

CONTRACTION_MAPPING = {
    "ain't" : "not",
    "aren't" : "not",
    "can't" : "not",
    "could've" : "could",
    "couldn't" : "not",
    "didn't" : "not",
    "doesn't" : "not",
    "don't" : "no",
    "hadn't" : "not",
    "hasn't" : "not",
    "haven't" : "not",
    "he'd" : "he",
    "he'll" : "he",
    "he's" : "he",
    "how'd" : "how",
    "how'll" : "how",
    "how's" : "how",
    "isn't" : "not",
    "it'd" : "it",
    "it'll" : "it",
    "it's" : "it",
    "let's" : "let",
    "might've" : "might",
    "mightn't" : "not",
    "must've" : "must",
    "mustn't" : "not",
    "needn't" : "not",
    "not've" : "not",
    "oughtn't" : "not",
    "shan't" : "not",
    "she'd" : "she",
    "she'll" : "she",
    "she's" : "she",
    "should've" : "should",
    "shouldn't" : "not",
    "that'll" : "that",
    "that's" : "that",
    "there'd" : "there",
    "there're" : "there",
    "there's" : "there",
    "they'd" : "they",
    "they'll" : "they",
    "they're" : "they",
    "they've" : "they",
    "wasn't" : "not",
    "we'd" : "we",
    "we'll" : "we",
    "we're" : "we",
    "we've" : "we",
    "weren't" : "not",
    "what'll" : "what",
    "what're" : "what",
    "what's" : "what",
    "what've" : "what",
    "when's" : "when",
    "where'd" : "where",
    "where's" : "where",
    "where've" : "where",
    "who'd" : "who",
    "who'll" : "who",
    "who're" : "who",
    "who's" : "who",
    "who've" : "who",
    "why'll" : "why",
    "why're" : "why",
    "why's" : "why",
    "won't" : "not",
    "would've" : "would",
    "wouldn't" : "not",
    "y'all" : "you",
    "you'd" : "you",
    "you'll" : "you",
    "you're" : "you",
    "you've" : "you",
}

ARTICLES = [
    "a",
    "an",
    "the",
]

LINKING_VERBS = [
    "be",
    "is",
    "was",
    "shall be",
    "will be",
    "has been",
    "had been",
    "may be",
    "should be",
    "am",
    "are",
    "were",
    "shall have been",
    "will have been",
    "have been",
]

DIMINUTIVE_ADJECTIVES = [
    "small",
    "meager",
    "cramped",
    "limited",
    "meager",
    "microscopic",
    "miniature",
    "minuscule",
    "modest",
    "narrow",
    "paltry",
    "short",
    "slight",
    "small-scale",
    "young",
    "baby",
    "little",
    "mini",
    "petite",
    "trifling",
    "wee",
    "bitty",
    "immature",
    "inadequate",
    "inconsequential",
    "inconsiderable",
    "insufficient",
    "piddling",
    "pint-sized",
    "pitiful",
    "pocket-sized",
    "stunted",
    "teensy",
    "teeny",
    "trivial",
    "undersized",
]

# preprocess to account for unicode
def fixList(myList):
    replacement = []
    for entry in myList:
        replacement.append(entry)
        if "'" in entry:
            replacement.append(entry.replace("'", "’"))
    return replacement

def fixDict(myDict):
    replacement = {}
    for key, value in myDict.iteritems():
        replacement[key] = value
        if "'" in key:
            replacement[key.replace("'", "’")] = value
    return replacement

PERSONAL_PRONOUNS = fixList(PERSONAL_PRONOUNS)
PERSONAL_POSSESSIVE_PRONOUNS = fixList(PERSONAL_POSSESSIVE_PRONOUNS)
CONTRACTION_MAPPING = fixDict(CONTRACTION_MAPPING)
LINKING_VERBS = fixList(LINKING_VERBS)


def hulkify(bannerText):
    hulkText = bannerText

    def removeWordFromMatch(matchObject):
        before = len(matchObject.group(1)) > 0
        after  = len(matchObject.group(3)) > 0

        if before and after:
            return matchObject.expand(r"\1")
        if before:
            return matchObject.expand(r"\3")
        if after:
            return matchObject.expand(r"\1")

    # Replace all personal pronouns (I/me/I've/I'm/etc) with "Hulk"
    for pp in PERSONAL_PRONOUNS:
        hulkText = re.sub(r"(\s?)(\b%s\b)(\s?)" % (pp), r"\1Hulk\3", hulkText, flags=re.IGNORECASE)
    for ppp in PERSONAL_POSSESSIVE_PRONOUNS:
        if "’" in bannerText:
            hulkText = re.sub(r"(\s?)(\b%s\b)(\s?)" % (ppp), r"\1Hulk’s\3", hulkText, flags=re.IGNORECASE)
        else:
            hulkText = re.sub(r"(\s?)(\b%s\b)(\s?)" % (ppp), r"\1Hulk's\3", hulkText, flags=re.IGNORECASE)

    # Change contractions to their main word. ("can't" -> "not")
    for con, main in CONTRACTION_MAPPING.iteritems():
        hulkText = re.sub(r"(\s?)(\b%s\b)(\s?)" % (con), r"\1%s\3" % main, hulkText, flags=re.IGNORECASE)

    # Drop all linking verbs ("am" or "to be")
    for lv in LINKING_VERBS:
        hulkText = re.sub(r"(\s?)(\b%s\b)(\s?)" % (lv), removeWordFromMatch, hulkText, flags=re.IGNORECASE)

    # Remove articles.
    for a in ARTICLES:
        hulkText = re.sub(r"(\s?)(\b%s\b)(\s?)" % (a), removeWordFromMatch, hulkText, flags=re.IGNORECASE)

    parsed = pattern.en.tag(hulkText)

    # Change verbs to present tense.
    for wordData in parsed:
        if wordData[1][0] == 'V':
            hulkText = re.sub(r"\b%s\b" % wordData[0], pattern.en.lemma(wordData[0]), hulkText, flags=re.IGNORECASE)

    # Randomly replace the occasional verb with "smash."

    # Replace any diminuitive adjective with "puny."
    for wordData in parsed:
        if wordData[1][:2] == 'JJ':
            if wordData[0] in DIMINUTIVE_ADJECTIVES:
                hulkText = re.sub(r"\b%s\b" % wordData[0], "puny", hulkText, flags=re.IGNORECASE)

    # Exclamation points.
    def exclaim(matchObject):
        punct = matchObject.group(0)
        startingMarks = punct.count("!")
        if "." in punct and startingMarks == 0:
            # change out periods most of the time
            if (random.random() < 0.7):
                punct = "!"

        # 30% chance of intensifying
        if ("." not in punct) and (random.random() < 0.3):
            punct += "!"
            # slight chance of double intensifying
            if (random.random() < 0.45):
                punct += "!"

        return punct

    hulkText = re.sub(r"([.?!]+)", exclaim, hulkText)

    # Easter egg at mention of "strong"
    strongest = " Hulk is the strongest there is!"
    if (" strong " in hulkText) and (len(hulkText) + len(strongest) <= 140):
        hulkText += strongest

    # Convert the whole thing to uppercase. 
    hulkText = hulkText.upper()
    
    return hulkText


if __name__ == '__main__':
    corpus = [
    ]
    for text in corpus:
        print hulkify(text.strip())
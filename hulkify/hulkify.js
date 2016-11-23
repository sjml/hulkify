
var fs  = require('fs');
var pos = require('pos');
var nlp = require('nlp_compromise');
var ent = require('html-entities').AllHtmlEntities;

var GRAMMAR = require('./grammar.json');

module.exports = hulkify;

function fixList(list) {
  var replacement = Array();
  for (var i = 0; i < list.length; i++) {
    replacement.push(list[i]);
    if (list[i].indexOf("'") >= 0) {
      replacement.push(list[i].replace("'", "’"));
    }
  }
  return replacement;
}
function fixDict(dict) {
  var replacement = {};
  for (var key in dict) {
    replacement[key] = dict[key];
    if (key.indexOf("'") >= 0) {
      replacement[key.replace("'", "’")] = dict[key];
    }
  }
  return replacement;
}

GRAMMAR.PERSONAL_PRONOUNS = fixList(GRAMMAR.PERSONAL_PRONOUNS);
GRAMMAR.PERSONAL_POSSESSIVE_PRONOUNS = fixList(GRAMMAR.PERSONAL_POSSESSIVE_PRONOUNS);
GRAMMAR.CONTRACTION_MAPPING = fixDict(GRAMMAR.CONTRACTION_MAPPING);
GRAMMAR.LINKING_VERBS = fixList(GRAMMAR.LINKING_VERBS);
GRAMMAR.ARTICLES = fixList(GRAMMAR.ARTICLES);
GRAMMAR.DIMINUTIVE_ADJECTIVES = fixList(GRAMMAR.DIMINUTIVE_ADJECTIVES);

function hulkify(bannerText, maxLength) {
  var entProc = new ent();
  bannerText = entProc.decode(bannerText);
  
  var hulkText = bannerText;

  function removeWordFromMatch(match, g1, g2, g3) {
    var before = g1.length > 0;
    var after  = g3.length > 0;

    if (!before && !after) {
      return g2;
    }
    if (before && after) {
      return g1;
    }
    if (before) {
      return g3;
    }
    if (after) {
      return g1;
    }
  }

  function changeTextUnlessOverrun(oldText, newText, maximum) {
    if (maximum === undefined) {
      return newText;
    }
    if (newText.length > maximum) {
      return oldText;
    }
    return newText;
  }

  // Change contractions to their main word. ("can't" -> "not")
  for (var con in GRAMMAR.CONTRACTION_MAPPING) {
    var main = GRAMMAR.CONTRACTION_MAPPING[con];
    var re = new RegExp("(\\s?|^)(\\b" + con + "\\b)(\\s?|$)", "gi");
    hulkText = hulkText.replace(re, "$1" + main + "$3");
  }

  // Drop all linking verbs ("am" or "to be")
  for (var i=0; i < GRAMMAR.LINKING_VERBS.length; i++) {
    var lv = GRAMMAR.LINKING_VERBS[i];
    var re = new RegExp("(\\s?|^)(\\b" + lv + "\\b)(\\s?|$)", "gi");
    hulkText = hulkText.replace(re, removeWordFromMatch);
  }

  // Remove articles.
  for (var i=0; i < GRAMMAR.ARTICLES.length; i++) {
    var a = GRAMMAR.ARTICLES[i];
    var re = new RegExp("(\\s?|^)(\\b" + a + "\\b)(\\s?|$)", "gi");
    hulkText = hulkText.replace(re, removeWordFromMatch);
  }

  // // everything above here only removes content; after this we have to consider length

  // Replace all personal pronouns (I/me/I've/I'm/etc) with "Hulk"
  for (var i = 0; i < GRAMMAR.PERSONAL_PRONOUNS.length; i++) {
    var pp = GRAMMAR.PERSONAL_PRONOUNS[i];
    var re = new RegExp("(\\s?|^)(\\b" + pp + "\\b)(\\s?|$)", "gi");
    hulkText = changeTextUnlessOverrun(
        hulkText,
        hulkText.replace(re, "$1Hulk$3"), 
        maxLength
      );
  }
  for (var i = 0; i < GRAMMAR.PERSONAL_POSSESSIVE_PRONOUNS.length; i++) {
    var ppp = GRAMMAR.PERSONAL_POSSESSIVE_PRONOUNS[i];
    var re = new RegExp("(\\s?|^)(\\b" + ppp + "\\b)(\\s?|$)", "gi");
    if (ppp.indexOf("’") >= 0) {
      hulkText = changeTextUnlessOverrun(
          hulkText,
          hulkText.replace(re, "$1Hulk’s$3"), 
          maxLength
        );
    }
    else {
      hulkText = changeTextUnlessOverrun(
          hulkText,
          hulkText.replace(re, "$1Hulk's$3"), 
          maxLength
        );
    }
  }

  var words = new pos.Lexer().lex(hulkText);
  var parsed = new pos.Tagger().tag(words);

  for (var i = 0; i < parsed.length; i++) {
    var wordData = parsed[i];
    if (wordData[1][0] == 'V' && wordData[1] != 'VBG') {
      var re = new RegExp("\\b" + wordData[0] + "\\b", "gi");
      hulkText = changeTextUnlessOverrun(
        hulkText,
        hulkText.replace(re, nlp.verb(wordData[0]).conjugate().infinitive),
        maxLength
      );
    }
  }

  // Replace any diminutive adjective with "puny."
  for (var i = 0; i < parsed.length; i++) {
    var wordData = parsed[i];
    if (wordData[1].substring(0,2) == 'JJ') {
      if (GRAMMAR.DIMINUTIVE_ADJECTIVES.indexOf(wordData[0]) >= 0) {
        var re = new RegExp("\\b" + wordData[0] + "\\b", "gi");
        hulkText = changeTextUnlessOverrun(
          hulkText,
          hulkText.replace(re, "puny"),
          maxLength
        );
      }
    }
  }

  // Exclamation points
  function exclaim (match, g0, g1) {
    var punct = g0;
    if ( (punct.indexOf('.') >= 0) && ((punct.match(/!/g) || []).length == 0) ) {
      // change out periods most of the time
      if (Math.random() < 0.7) {
        punct = '!';
      }
    }

    // if we're already at the max, don't intensify
    if ( (maxLength !== undefined) && (hulkText.length >= maxLength) ) {
      return punct;
    }

    // 30% chance of intensifying
    if ( (punct.indexOf('.') < 0) && (Math.random() < 0.3) ) {
      punct += '!';
      // slight chance of double intensifying
      if (Math.random() < 0.45) {
        punct += '!';
        if (punct.indexOf('?') >= 0) {
          punct += '?!';
        }
      }
    }

    return punct + g1;
  }

  hulkText = hulkText.replace(/([.?!]+)(\s|$)/gi, exclaim);

  // Easter egg at mention of "strong"
  var strongest = ' Hulk is the strongest there is!';
  var strongRe = new RegExp('\\bstrong\\b', 'gi');
  if (strongRe.test(hulkText)) {
    if ( (maxLength === undefined) || (hulkText.length + strongest.length <= maxLength) ) {
      hulkText += strongest;
    }
  }

  // Convert the whole thing to uppercase.
  hulkText = hulkText.toUpperCase();

  return hulkText;
}


var main = function(){
  var corpusString = fs.readFileSync('./test_corpus.txt').toString();
  corpusString = corpusString.replace(/\r/g, '');
  var corpus = corpusString.split("\n");
  for (var i=0; i < corpus.length; i++) {
    if (corpus[i].length === 0) {
      continue;
    }
    var val = hulkify(corpus[i], 140);
    console.log(val);
  }
}

if (require.main === module) {
  main();
}

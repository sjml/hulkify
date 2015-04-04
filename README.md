# HULKIFY

Turns normal English into HULK-SPEAK! 

This is a combined Python/JavaScript package -- it should be easily usable by either language, with the other language's files just appearing as cruft. At the moment, all the logic is duplicated. Could this be unified through some kind of clever cross-language regex engine? PERHAPS! But I am not really interested in making such a thing. (I already have the aphoristic ["two problems,"](http://regex.info/blog/2006-09-15/247) and I have a feeling trying to generalize regex logic would lead to many more than two.)

BUT YOU ARE NOT HERE TO HEAR ABOUT PROGRAMMING CONUNDRA! You are here to turn plain English into something that might be said by the Hulk. 

Both implementations follow the same basic algorithm:

1. Change contractions to a designated main word. ("can't" -> "not")
2. Drop all linking verbs. ("am," "to be," etc.)
3. Remove articles. ("a," "an," and "the")
4. Replace all personal pronouns ("I"/"me"/"I've"/"I'm"/etc.) with "Hulk."
5. Change verbs to present tense. 
6. Replace any diminutive adjective with "puny."
7. Exclamation points. 
8. If the word "strong" is present, add, "Hulk is the strongest there is!"
9. Convert the whole thing to uppercase. 

(Note: I would also like to make it change the occasional verb to "smash," but it's not clear how to select those verbs properly. Needs to only be particularly active or violent verbs, but I haven't found any linguistic databases with attributes like that.)

You can also specify a maximum character length for the returned Hulk string (for example, 140), and it will be smart about what it appends. 

There is some randomness involved in the exclamation marks, so the output is not always the same. 

**Important note:** Presently, the Python version tends to produce better results than the JavaScript one. So far as I can tell, the grammatical library I'm using with Python ([pattern.en](http://www.clips.ua.ac.be/pages/pattern-en)) is better at figuring out correct semantics and conjugations than the two JavaScript libraries I'm using ([pos](https://www.npmjs.com/package/pos) and [nlp_compromise](https://www.npmjs.com/package/nlp_compromise)). I'd love to get them into parity, but JavaScript isn't my usual rowboat, so I don't know how best to explore. If you have thoughts, please open a pull request! :D

Also note that it's been developed and tested with only bite-sized text; my eyes were towards a particularly popular microblogging service and producing text for it. It might work with larger texts? Might not? If it seems to break, try doing smaller chunks at a time. Or not. Just consider this an admonition. 

## Installation

### Python
Hulkify is [available in PyPI](https://pypi.python.org/pypi/hulkify/). 

```$ pip install hulkify```

### Node.js
Hulkify is [available in npm](https://www.npmjs.com/package/hulkify).

```$ npm install hulkify```

## Example Code

### Python
```python
from hulkify import hulkify

bannerText = "Hello, I'm very happy to be seeing you all. It's a small wonder that I survived."

print hulkify(bannerText)

```
**output:** HELLO, HULK VERY HAPPY TO SEE YOU ALL! IT PUNY WONDER THAT HULK SURVIVED!!!

### Node.js
```javascript
// (for Node.js; presently Hulkify won't work in the browser)
var hulkify = require('hulkify');

var bannerText = 'You are very kind to try and educate me as to the perils of smoking, but I\'m content to risk it. "Health" is a relative matter.';

console.log(hulkify(bannerText));

```
**output:** YOU VERY KIND TO TRY AND EDUCATE HULK AS TO PERILS OF SMOKING, BUT HULK CONTENT TO RISK IT!! "HEALTH" RELATIVE MATTER!
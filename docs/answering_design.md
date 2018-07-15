Design for Commenting Duties
---------------------

To keep the coding to a minimal, all the design has been kept generic, and NLP APIs/NLTK is kept at least.

###### Firstly, to reduce server pressure, the listeners will be set only on channels - #intro, #newcomers and #questions only

**1. How to figure out if a sentence is a question or not?**
  
```
START_WORDS = [who, what, when, where, why, how, is, can, does, do]

def isQuestion(sentence): 
    if sentence ends with '?' OR 
        sentence starts with one of START_WORDS

```


However, firstly, we will sent_tokenize a paragraphic reply. Then we will perform the above check. If the check passes we will extract the keywords from the sentence as explained later.

**2. List of questions that bot aims to answer:**  

a. About Systers community and AnitaB: keywords to look for - Systers, Systers Community, AnitaB, Anita Borg, AnitaBorg Institution  
b. About Programs- Outreachy, GSoC, RGSoC, GCI  
c. Getting started questions: getting started, start contributing, how to contribute, would love to contribute to Systers  
d. Project suggestions based on the skills mentioned in the intro message.  
e. Open source workflow: new to opensource, link to the workflow  
f. If someone mentions channel names, we can tag the teams for that channel to the message.  
g. Answer questions about gender restrictions of contributors

**3. Answering questions**

For answering questions based on keyword, we would use lemmatization to introduce variety. 
Also, I have tried out a keyword summarizer which uses a bigram tagger to find out key phrases in a sentence.


#### Trial

Following photo shows a sample trial. I have tried it on some intro messages, works well for Named entities. Can be used to detect -> GSoC, GCI, Google programs, Systers, channel names. 

![sample_summarizer](https://user-images.githubusercontent.com/24635701/42744616-85d8ef12-88eb-11e8-8e42-f7dfa77050c3.png)

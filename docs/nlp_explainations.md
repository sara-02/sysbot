Intents and Entities
----

The key for a bot to understand the humans is its ability 
to understand the intentions of humans and extraction of relevant information from that intention and of course relevant action against that information.

#### Intents

This is an important part of the bots answering facilities.
Simply put, intents are the intentions of the end-user. It helps the bot
understand what specific class of activity the user wants it to do.
Fr eg:- Let's say a user comments the following:  

```
I would like to know who the mentor of this project is?
```
This basically shows that the user intends to know more about mentors
of the project. So, based on some comment made by the user to the bot, 
we need to map that to a specific and discrete use case using intents.

Intents are mainly of 2 categories

1. Casual Intents
2. Business Intents

- Casual Intents — These intents are the opener or closer of a conversation. 
The Greetings like “hi”, “hello”, “bye” are the opening or closing statements 
in a conversation. These intents should direct your bot to respond with a small 
talk reply like “Hello what can I do for you today” or “Bye thanks for talking to me”.

- Business Intents — These are the intents that directly map to business of the bot. 
For eg — for Sysbot an utterance from the user like “Tell me about Systers?” is a business intent
 that intends to find out more about Systers and we should label it accordingly 
 with an understandable name like “CommunityInformation”.


#### Entities

An entity represents a term or object in the user's input that provides 
clarification or specific context for a particular intent. If intents 
represent verbs (something a user wants to do), entities represent nouns 
(such as the object of, or the context for, an action). Entities make it 
possible for a single intent to represent multiple specific actions. 
An entity defines a class of objects, with specific values representing 
possible objects in that class.

Essentially, if you want to capture a request, or perform an action, 
use an intent. If you want to capture information that may affect how you 
respond to a request or action, use an entity.

##### NER(Named Entity Recognition)

Named Entity Recognition is a process where an algorithm takes a string
 of text (sentence or paragraph) as input and identifies relevant nouns 
 (people, places, and organizations) that are mentioned in that string.

Some popular NLP as a service platforms are
1. LUIS.ai — By Microsoft
2. Wit.ai — By Facebook
3. Api.ai — By Google
4. Watson — By IBM

I have tried Wit.ai, Api.ai and LUIS.ai. Based on performance and
the ease of integration and also the amount of free usage allowed,
 I have decided to use LUIS.ai for the project.
 
Currently we mainly use Intents but we can also use NER to 
improve the bots answering features for community and programs based
questions.

We have trained 3 Business Intents on LUIS and a fallback (None).
The three intents are as follows:

1. Maintainers
2. getting-started
3. participation-gender

[Here](https://docs.google.com/document/d/1mgTq9etOVN95Dic6AUl-XrQZkoG0tKXQbt7tfIgDwAA/edit?usp=sharing) are the 
collected sentences. An issue has been opened up for the same purpose
in Sysbot repo: [Issue #111](https://github.com/systers/sysbot/issues/111)

The collection method I used was:

I used Slack API to read messages from a channel as mentioned
 [here](https://api.slack.com/methods/channels.history). 
Then I used pasted the data into a Python file as a dictionary,
 and used a Python script to read only the main thread messages.
 From these messages I used the script to print messages or sentences 
 which had certain keyword pertaining to each Intent(words like getting started, contributing, 
 maintainers, gender, male, female etc), and did this for 3-4 channels. 
 I used that data for training.
 
 You can use the same data to train your LUIS agent, for local development.
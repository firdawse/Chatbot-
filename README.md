# Building  a WhatsApp Chatbot With Python

### A [chatbot](https://en.wikipedia.org/wiki/Chatbot) is a software application that is able to conduct a conversation with a human user through written or spoken language. The level of “intelligence” among chatbots varies greatly. While some chatbots have a fairly basic understanding of language, others employ sophisticated artificial intelligence (AI) and machine learning (ML) algorithms to achieve an almost human conversational level.

### Table of content

1.  Requirement
2.  Set up of the WhatsApp chatbot
    -   Create a Flask chatbot service
    -    Testing the WhatsApp chatbot
4.  Chatbot logic
    -   NLP Concept
    -    Text detection from images
         - Install core dependencies
         - Importing Libraries
         - Reading images
         - Extracting text from the image
     - Sending mails

###  Requirements :
> - Python 3.6 or newer. 
> -  [Flask](https://www.palletsprojects.com/p/flask/). We will create a web application that responds to incoming WhatsApp messages with it.
>  -   A smartphone with an active phone number and WhatsApp installed.
>  -   A Twilio account. You can [create a free account](http://www.twilio.com/referral/7fB3Je)  . You can review the  [features and limitations of a free Twilio account](https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account).
>  - [ngrok](https://ngrok.com/). We will use this handy utility to connect the Flask application running on your system to a public URL that Twilio can connect to. This is necessary for the development version of the chatbot because your computer is likely behind a router or firewall, so it isn’t directly reachable on the Internet. If you don’t have ngrok it installed, you can  [download a copy for Windows, MacOS or Linux](https://ngrok.com/download)

 
 
- The following sections will give you all the necessary details to configure and create a WhatsApp chatbot using Python and the Flask framework **LET'S GO!**
- ### Creating a WhatsApp chatbot

   > The following sections will give you all the necessary details to configure and create a WhatsApp chatbot using Python and the Flask framework.
   
   Twilio provides a  [WhatsApp sandbox](https://www.twilio.com/console/sms/whatsapp/learn)  where you can easily develop and test your application. Once your application is complete you can request  [production access for your Twilio phone number](https://www.twilio.com/whatsapp/request-access), which requires approval by WhatsApp.

  Let’s connect your smartphone to the sandbox. From your  [Twilio Console](https://www.twilio.com/console), select  [Programmable Messaging](https://www.twilio.com/console/sms/dashboard), then click on "Try it Out" and finally click on  [Try WhatsApp](https://www.twilio.com/console/sms/whatsapp/learn). The WhatsApp sandbox page will show you the sandbox number assigned to your account, and a join code.
  
  ![](https://twilio-cms-prod.s3.amazonaws.com/images/qMtxTvSPXKjaw8L7GOF69_dfR8Kve8YI-Pvj2at1ShJEMg.width-800.png)

  To enable the WhatsApp sandbox for your smartphone send a WhatsApp message with the given code to the number assigned to your account. The code is going to begin with the word  **join**, followed by a randomly generated two-word phrase. Shortly after you send the message you should receive a reply from Twilio indicating that your mobile number is connected to the sandbox and can start sending and receiving messages.

***Note that this step needs to be repeated for any additional phones you’d like to have connected to your sandbox.***

  Install the three packages that we are going to use in this project  ***pip install twilio flask requests*** , which are:

>-   The  [Flask](https://www.palletsprojects.com/p/flask/)  framework, to create the web application
>-   The  [Twilio Python Helper library](https://www.twilio.com/docs/libraries/python), to work with the Twilio APIs
>-   The  [Requests](https://requests.kennethreitz.org/en/master/)  package, to access third party APIs

### Create a Flask chatbot service

#### - Webhook : 
The [Twilio API for WhatsApp](https://www.twilio.com/whatsapp) uses a [webhook](https://sendgrid.com/blog/whats-webhook/) to notify an application when there is an incoming message. Our chatbot application needs to define an endpoint that is going to be configured as this webhook so that Twilio can communicate with it.

```python
from flask import Flask

app = Flask(__name__)


@app.route('/bot’, methods=['POST'])
def bot():
    # add webhook logic here and return a response


if __name__ == '__main__':
    app.run(port=4000)
```
The important thing to keep in mind about the code above is that the application defines a `/bot` endpoint that listens to `POST` requests. Each time an incoming message from a user is received by Twilio, they will in turn invoke this endpoint. The body of the function `bot()` is going to analyze the message sent by the user and provide the appropriate response.

#### Messages and responses

The first thing we need to do in our chatbot is obtain the message entered by the user. This message comes in the payload of the  `POST`  request with a key of  `’Body’`. We can access it through Flask’s  `request`  object:

```python
from flask import request
incoming_msg = request.values.get('Body', '').lower()
```
## Testing the WhatsApp chatbot

Are you ready to test the chatbot? Start the chatbot by running  `python bot.py`. The output should be something like this:

```bash
(whatsapp-bot-venv) $ python bot.py
 * Serving Flask app "bot" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

The service is now running as a private service on port 5000 inside your computer and will sit there waiting for incoming connections. To make this service reachable from the Internet we need to use ngrok.

Open a second terminal window and run  `ngrok http 5000`  to allocate a temporary public domain that redirects HTTP requests to our local port 4000. On a Unix or Mac OS computer you may need to use  `./ngrok http 5000`  if you have the ngrok executable in your current directory. The output of ngrok should be something like this:

![Running ngrok to connect port 4000](https://twilio-cms-prod.s3.amazonaws.com/images/ng4000.width-500.png)

Note the lines beginning with “Forwarding”. These show the public URL that ngrok uses to redirect requests into our service. What we need to do now is tell Twilio to use this URL to send incoming message notifications.

Go back to the  [Twilio Console](https://www.twilio.com/console), click on  [Programmable Messaging](https://www.twilio.com/console/sms/dashboard), then on  [Settings](https://www.twilio.com/console/sms/settings), and finally on  [WhatsApp Sandbox Settings](https://www.twilio.com/console/sms/whatsapp/sandbox). Copy the https:// URL from the ngrok output and then paste it on the “When a message comes in” field. Since our chatbot is exposed under the  `/bot`  URL, append that at the end of the root ngrok URL. Make sure the request method is set to  `HTTP Post`. Don’t forget to click the red Save button at the bottom of the page to record these changes.

![Twilio Sandbox for WhatsApp configuration screenshot](https://twilio-cms-prod.s3.amazonaws.com/images/e2z9Pv472N9CRz9516JFpnnS7GgQm0HjHPtAmJQkBh6kwg.width-500.png)

Now you can start sending messages to the chatbot from the smartphone that you connected to the sandbox. 
Keep in mind that You will need to update the URL in the Twilio Console every time you restart ngrok.

# Chatbot logic
Now we are on to the fun part. Let’s build a conversation with our chatbot!

But first let's discorver the types of chatbots that already exist:

- RULE-BASED CHAT -BOT :
where the chatbot's responses are fully predefined and returned to the user according to a series of rules. This includes decision trees that have a clear set of possible outputs defined for each step in the dialog box.

- RETRIEVAL BASED CHAT-BOT :
where the chatbot's responses are extracted from an existing dialog corpus.
Machine learning models, such as statistical models of NLP and sometimes supervised neural networks, are used to interpret user input and determine the most appropriate response to retrieve. Like rule-based models, retrieval-based models rely on predefined responses, but they have the added ability to self-learn and improve their response selection over time.

- GENERATIVE CHAT-BOT:
generative chatbots are able to formulate their own original responses based on user input, rather than relying on existing text.
This involves using deep learning, such as LSTM-based seq2seq models, to train chatbots to be able to make decisions about the appropriate response to return.

For our case we choosed to work on a rule based chtabot but using some NLP tools  to make it a little smarter.
## NLP Concept

NLP methods are at the heart of how today's Chatbots work. Although these systems are not totally perfect, they can now easily handle standard tasks such as informing customers about products or services, answering their questions, etc. They are used by several channels, including the Internet, applications and messaging platforms. The opening of the Facebook Messenger platform to chatbots in 2016 contributed to their development.

 ### What are the main methods used in NLP? 
Overall, we can distinguish two essential aspects to any NLP problem: 
- The “linguistic” part, which consists of preprocessing and transforming the input information into a usable dataset. 
- The “automatic learning” or “Data Science” part, which concerns the application of Machine Learning or Deep Learning models to this dataset.

#### The pre-processing phase: from text to data
Suppose you want to be able to determine whether an email is spam or not, just from its content. To this end, it is essential to transform the raw data (the text of the email) into usable data.

Among the main steps are:

- **Cleaning**: Variable depending on the data source, this phase consists of performing tasks such as deleting urls, emoji, etc.
Data normalization:
- **Tokenization**, or splitting text into multiple pieces called tokens.
Example: “You will find the document in question attached”; "You", "find", "as an attachment", "the document", "in question".
- **Stemming** the same word can be found in different forms depending on gender (masculine feminine), number (singular, plural), person (me, you, them…) etc. Stemming generally refers to the crude heuristic process of cutting out the end of words in order to keep only the root of the word.
Example: “find” -> “find”
- **Lemmatization**: this consists of carrying out the same task but using a vocabulary and a detailed analysis of the construction of words. Lemmatization therefore makes it possible to remove only the inflexible endings and thus to isolate the canonical form of the word, known as the lemma. Example: “find” -> find
- **Other operations**: deletion of numbers, punctuation, symbols and stopwords, conversion to lowercase.
In order to be able to apply Machine Learning methods to problems relating to natural language, it is essential to transform textual data into numerical data.
There are several approaches, the main ones being:

>- **Term-Frequency (TF)**: this method consists of counting the number of occurrences of tokens present in the corpus for each text. Each text is then represented by a vector of occurrences. We generally speak of Bag-Of-Word.
  ![NLP](https://datascientest.com/wp-content/uploads/2020/07/Capture-d%E2%80%99e%CC%81cran-2020-07-19-a%CC%80-11.17.46.png)
Representation of vectors from the Term-Frequency (TF) method.

However, this approach has a major drawback: some words are by nature more used than others, which can lead the model to erroneous results.

>- **Term Frequency-Inverse Document Frequency (TF-IDF)**: this method consists of counting the number of occurrences of the tokens present in the corpus for each text, which is then divided by the total number of occurrences of these same tokens in the whole body.
For the term x present in the document y, we can define its weight by the following relation:
![NLP formule](https://datascientest.com/wp-content/uploads/2020/07/Capture-d%E2%80%99e%CC%81cran-2020-07-19-a%CC%80-10.53.53.png)

Where :
- tƒx,y is the frequency of the term x in y;
- dƒx is the number of documents containing x;
- N is the total of documents.
This approach therefore makes it possible to obtain for each text a vectorial representation which comprises weight vectors and no longer occurrences.

The effectiveness of these methods differs depending on the application case. However, they have two main limitations:

The richer the vocabulary of the corpus, the larger the size of the vectors, which can represent a problem for the learning models used in the next step.
Counting the occurrence of words does not make it possible to account for their arrangement and therefore the meaning of sentences.
There is another approach that can remedy these problems: Word Embedding. It consists in constructing vectors of fixed size which take into account the context in which the words are found.

Thus, two words present in similar contexts will have closer vectors (in terms of vector distance). This then makes it possible to capture both semantic, syntactic or thematic similarities of the words , for this many methods exists such as :
- _**Cosine similarity** which is a metric used to measure how similar the documents are irrespective of their size. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space._
 The cosine similarity is advantageous because even if the two similar documents are far apart by the Euclidean distance (due to the size of the document), chances are they may still be oriented closer together. The smaller the angle, higher the cosine similarity.
 

![](https://storage.googleapis.com/lds-media/images/cosine-similarity-vectors.original.jpg)

Now let's see how we implement this staff 
When our chatbot recieve a message from a user the whole NLP process assigned above happens to associete it  to the most compatible answer   
from a long list of suggestions based principally on cosine similarity 
``` python
def response(user_response):
robo_response=''
sent_tokens.append(user_response)
final_stopwords_list = stopwords.words('english') + stopwords.words('french')
TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=final_stopwords_list
tfidf =TfidfVec.fit_transform(sent_tokens)
vals = cosine_similarity(tfidf[-1], tfidf)
idx=vals.argsort()[0][-2]
flat = vals.flatten()
flat.sort()
req_tfidf = flat[-2]
sent_tokens.remove(user_response)
if(req_tfidf==0):
robo_response=robo_response+"I am sorry! I don't understand you , can you specify"
return robo_response
else:
robo_response = robo_response+sent_tokens[idx]
return robo_response
```
## Text detection from images using EasyOCR:
### What is OCR?

OCR is formerly known as  **Optical Character Recognition**  which is revolutionary for the digital world nowadays. OCR is actually a complete process under which the **images/documents**  which are present in a digital world are processed and from the text are being processed out as normal  **editable text**.

### Purpose of OCR

OCR is a technology that enables you to convert different types of documents, such as  **scanned paper documents, PDF files, or images**  captured by a digital camera into  **editable and searchable data.**

### What is EasyOCR?

EasyOCR is actually a python package that holds  **PyTorch as a backend handler**. EasyOCR like any other OCR(tesseract of Google or any other) detects the text from images but in my reference, while using it I found that it is the most  **straightforward**  way to detect text from images also when high end deep learning library(PyTorch) is supporting it in the backend which makes it accuracy more credible.  
## 1. Install core dependencies

-   ### Pytorch
    

Installing PyTorch as a complete package can be a little tricky so I would recommend traversing through the official site of  **PyTorch**. When you will open its official site then that’s what you will see in its interface as in the image below.

![Install core dependencies easyocr](https://editor.analyticsvidhya.com/uploads/929991.png)

Image Source:  [**PyTorch**](https://pytorch.org/)

Now, if you will look closely at the above image one can find out that there are numerous options available for us to choose from and get the command most compatible according to our choices.

> **Let me show you a representation of what I’m trying to mention!**.

![Install core dependencies pytorch](https://editor.analyticsvidhya.com/uploads/270192.2.2.png)

Image Source:  [**PyTorch**](https://pytorch.org/)

In the above representation, one can notice that I have chosen the  **Package: pip**  and  **Compute platform: CPU**  and based on my choices I got the command as –  **pip install torch torchvision torchaudio**. After getting this command it would be like walking on a cake, simply just run this command on your command prompt and your PyTorch library will be installed successfully.

-   ### EasyOCR
    

After installing the PyTorch library successfully it’s quite easy to install  **the EasyOCR**  library, one just has to run the following command:

pip3 install easyocr

> Then your command prompt interface will be like:

![command prompt easyocr](https://editor.analyticsvidhya.com/uploads/631123.png)

## 2. Importing Libraries

import os
import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np

### 3. Reading images

-   **Taking an online image:**  Here we will take an image from  **a URL**  (online)

IMAGE_PATH = 'https://blog.aspose.com/wp-content/uploads/sites/2/2020/05/Perform-OCR-using-C.jpg'

In the above code snippet, one can notice that the  **IMAGE_PATH**  holds the  **URL**  of the image.

-   **Taking image as input locally**: Here we will take an image from the local system.

>IMAGE_PATH = 'Perform-OCR.jpg'

In the above code snippet, one can notice that I have taken the  **image locally**  i.e. from the local system.

## 4. Extracting text from the image

-   **English text detection**

>reader = easyocr.Reader(['en'])
result = reader.readtext(IMAGE_PATH,paragraph="False")
result

**Output:**

>[[[[95, 71], [153, 71], [153, 107], [95, 107]], **'OCR'**]]  

Adding an image for your preference.

![Extracting text from the image EasyOCR](https://editor.analyticsvidhya.com/uploads/92382Perform-OCR.jpg)

Image Source:  [LaptrinhX](https://laptrinhx.com/perform-ocr-on-images-using-c-ocr-library-3100762731/)

Now finally, we have extracted the text from the given image 
Now Let's see a concretisation of those functionalities in our chatbot !
- FIRST whe should detect that a picture has been sent from the user and then get the link from it 
   ``` python
  media_msg = request.form.get('NumMedia')
  if(media_msg == '1'):
      path = request.form.get('MediaUrl0')
  ```
  - Now that the link is ours we can process the image and then extract some useful information ,for our case we had to extract the id of employee
   ``` python
    def recognize_text(img_path):
  '''loads an image and recognizes text.'''
  req = Request(img_path, headers={'User-Agent': 'Mozilla/5.0'})
  webpage = urlopen(req).read()
  reader = easyocr.Reader(['en'])
  return reader.readtext(webpage)
   ```
and yes it works all we need to do now is detecting the location of the targeted information  .

## Sending mails 
Our chatbot gives the user the possibility to make an administrative request which should be sent to the responsible service via ana email to do that we use the (SMTP) protocol, which handles sending e-mail and routing e-mail between mail servers.
Python provides **smtplib** module, which defines an SMTP client session object that can be used to send mail to any Internet machine with an SMTP or ESMTP listener daemon.

Here is a simple way to send one e-mail using Python script.
``` python 
import smtplib

def sendmailWork ( first_name, last_name, type):
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('Your Mail','PASSWORD')
subject = 'Administrative request'
body = first_name + ' '+last_name + ' is asking for '+type
msg = f'Subject: {subject}\n\n{body}'
server.sendmail('Receiver Mail','Sender Mail ,msg )
print("login success")
```


# Building  a WhatsApp Chatbot With Python

### A [chatbot](https://en.wikipedia.org/wiki/Chatbot) is a software application that is able to conduct a conversation with a human user through written or spoken language. The level of “intelligence” among chatbots varies greatly. While some chatbots have a fairly basic understanding of language, others employ sophisticated artificial intelligence (AI) and machine learning (ML) algorithms to achieve an almost human conversational level.


###  Requirements :



>
> - Python 3.6 or newer. If your operating system does not provide a Python interpreter, you can go to  [python.org](https://python.org/)  to download an installer.
> - Profits were higher than ever.
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

Are you ready to test the chatbot? After you copy the above code into the  _bot.py_  file, start the chatbot by running  `python bot.py`, making sure you do this while the Python virtual environment is activated. The output should be something like this:

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



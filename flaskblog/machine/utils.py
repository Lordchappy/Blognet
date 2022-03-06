'''
This file defines functions for Sentiment Analysis on a given text
     
                        and 
              
Text Summarizer function for extracting useful informmations in a text 



'''


def sentiment_analysis(text):  
    #Importing all neccessary libraries 
    from keras.models import load_model
    from keras.preprocessing.sequence import pad_sequences
    import pickle
    
    #Loading the saved model
    model = load_model('flaskblog/machine/Model.h5')
    with open('flaskblog/machine/tokenize.pickle', 'rb') as (handle):
        tokenizer = pickle.load(handle)
        
    
    text_token = tokenizer.texts_to_sequences([text])
    text_pad = pad_sequences(text_token, maxlen=241, padding='pre')
    pred = model.predict(text_pad)
    if pred[0][0] > 0.5:
        result = 'Positive Review!'
        per = str(round(pred[0][0] * 100, 2)) + '%'
    else:
        result = 'Negative Review! '
        per = str(100 - round(pred[0][0] * 100, 2)) + '%'
    return (result, per)


def summmarize(text, num):
    import heapq
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    max_sentence = int(num)
    text = text.lower()
    Stopwords = set(stopwords.words('english'))
    word_freq = {}
    for word in word_tokenize(text):
        if word not in Stopwords:
            if word not in word_freq.keys():
                word_freq[word] = 1
            else:
                word_freq[word] += 1

    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] = word_freq[word] / max_freq

    sent_list = sent_tokenize(text)
    sent_scores = {}
    for sent in sent_list:
        for word in word_tokenize(sent.lower()):
            if word in word_freq.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = word_freq[word]
                    else:
                        sent_scores[sent] += word_freq[word]

    summary_sentences = heapq.nlargest(max_sentence, sent_scores, key=(sent_scores.get))
    print(summary_sentences)
    summary = ' '.join(summary_sentences)
    return summary
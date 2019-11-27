import os
import re
import sys
import nltk
import warnings
import numpy as np
from tensorflow import keras
from nltk.corpus import stopwords
from gensim.models import KeyedVectors
nltk.download('stopwords')
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def tokenizeEssay(essay):
    """
        This funciton tokenizes the text provided as input in the from of essay 
        
        We remove ``stopwords`` from the essay  

            >>> This is america
            >>> america

        :param essay: Input in the form of text
        :rtype: Tokenized words

    """
    essay = re.sub("[^a-zA-Z]", " ", essay)
    words = essay.lower().split()
    stops = set(stopwords.words("english"))
    words = [w for w in words if not w in stops]
    return (words)

def makeFeatureVec(words, model, num_features):
    """
        This function generates feature vectors for each dimension ie. plane

        :param words: We pass the words that we needed
        :param model: Model to decide on what basis police have been arrested

        :rtype: ``featureVec`` is the result of the function
    """
    featureVec = np.zeros((num_features,),dtype="float32")
    num_words = 0.
    index2word_set = set(model.index2word)
    for word in words:
        if word in index2word_set:
            num_words += 1
            featureVec = np.add(featureVec,model[word])        
    featureVec = np.divide(featureVec,num_words)
    return featureVec

def getAvgFeatureVecs(essays, model, num_features):
    """Main function to generate the word vectors for word2vec model.
    
    :param essays: Input is essays 
    :param model: This input specifies the model to be used to generate Feature vec
    :param num_features:  This is a metric of number of columns in the matrix cols

    :rtype: Returns the essay feature vector
    """
    
    counter = 0
    essayFeatureVecs = np.zeros((len(essays),num_features),dtype="float32")
    for essay in essays:
        essayFeatureVecs[counter] = makeFeatureVec(essay, model, num_features)
        counter = counter + 1
    return essayFeatureVecs

def predict(essay):
    """
        This is the function which calculates the score given an essay 

        :param essay: This input is the essay that we got from the fronend.
        :rtype: We are returning the y_pred values
    """
    
    model = KeyedVectors.load_word2vec_format('models/word2vecmodel.bin', binary=True)
    essay_tokens = []

    essay_tokens.append(tokenizeEssay(essay))
    testEssayVec = getAvgFeatureVecs(essay_tokens, model, 300)

    testEssayVec = np.array(testEssayVec)
    testEssayVec = np.reshape(testEssayVec,(testEssayVec.shape[0], 1, testEssayVec.shape[1]))

    evaluator = keras.models.load_model('models/final_lstm.h5')
    y_pred = evaluator.predict(testEssayVec)
    y_pred = 0 if np.isnan(y_pred[0][0]) else np.around(y_pred[0][0])
    return str(y_pred)
import numpy as np
import re

class Model:
    def __init__(self, alpha=1):
        self.vocab = set() # словарь, содержащий все уникальные слова из набора train
        self.spam = {} # словарь, содержащий частоту слов в спам-сообщениях из набора данных train.
        self.ham = {} # словарь, содержащий частоту слов в не спам-сообщениях из набора данных train.
        self.alpha = alpha # сглаживание
        self.label2num = None # словарь, используемый для преобразования меток в числа
        self.num2label = None # словарь, используемый для преобразования числа в метки
        self.Nvoc = None # общее количество уникальных слов в наборе данных train
        self.Nspam = None # общее количество уникальных слов в спам-сообщениях в наборе данных train
        self.Nham = None # общее количество уникальных слов в не спам-сообщениях в наборе данных train
        self._train_X, self._train_y = None, None
        self._val_X, self._val_y = None, None
        self._test_X, self._test_y = None, None
        
        # Вероятности
        self.prob_spam_prior = 0.0
        self.prob_ham_prior = 0.0

    def fit(self, dataset):
        '''
        dataset - объект класса Dataset
        Функция использует входной аргумент "dataset", 
        чтобы заполнить все атрибуты данного класса.
        '''
        self._train_X, self._train_y = dataset.train
        self._val_X, self._val_y = dataset.val
        self._test_X, self._test_y = dataset.test
        self.label2num = dataset.label2num
        self.num2label = dataset.num2label
        
        # Reset counts
        self.vocab = set()
        self.spam = {}
        self.ham = {}
        self.Nspam = 0
        self.Nham = 0
        
        # Identify label IDs
        spam_id = self.label2num.get('spam')
        ham_id = self.label2num.get('ham')
        
        # Calculate Priors (P(Spam) and P(Ham))
        total_docs = len(self._train_y)
        spam_docs = np.sum(self._train_y == spam_id)
        ham_docs = total_docs - spam_docs
        
        self.prob_spam_prior = spam_docs / total_docs
        self.prob_ham_prior = ham_docs / total_docs
        
        # Fill Dictionaries
        for i, text in enumerate(self._train_X):
            label = self._train_y[i]
            words = text.split()
            
            for word in words:
                self.vocab.add(word)
                if label == spam_id:
                    self.spam[word] = self.spam.get(word, 0) + 1
                    self.Nspam += 1
                else:
                    self.ham[word] = self.ham.get(word, 0) + 1
                    self.Nham += 1
                    
        self.Nvoc = len(self.vocab)
    
    def inference(self, message):
        '''
        Determines if a message is spam or ham using Naive Bayes.
        '''
        # Preprocess the single message (same cleaning as dataset)
        message = message.lower()
        message = re.sub(r'[^\w\s]', '', message)
        words = message.split()
        
        # Use Log Probabilities to avoid underflow
        # log(P(Spam|Message)) ~ log(P(Spam)) + sum(log(P(word|Spam)))
        
        spam_score = np.log(self.prob_spam_prior)
        ham_score = np.log(self.prob_ham_prior)
        
        for word in words:
            # Check if word exists in our vocabulary (ignore unknown words)
            if word in self.vocab:
                # P(w|spam) with Laplace Smoothing
                p_w_spam = (self.spam.get(word, 0) + self.alpha) / (self.Nspam + self.alpha * self.Nvoc)
                spam_score += np.log(p_w_spam)
                
                # P(w|ham) with Laplace Smoothing
                p_w_ham = (self.ham.get(word, 0) + self.alpha) / (self.Nham + self.alpha * self.Nvoc)
                ham_score += np.log(p_w_ham)
        
        if spam_score > ham_score:
            return "spam"
        return "ham"
    
    def validation(self):
        '''
        Predicts labels for validation set and returns accuracy.
        '''
        correct = 0
        total = len(self._val_y)
        
        for i in range(total):
            msg = self._val_X[i]
            true_label_id = self._val_y[i]
            true_label = self.num2label[true_label_id]
            
            prediction = self.inference(msg)
            
            if prediction == true_label:
                correct += 1
                
        return correct / total

    def test(self):
        '''
        Predicts labels for test set and returns accuracy.
        '''
        correct = 0
        total = len(self._test_y)
        
        for i in range(total):
            msg = self._test_X[i]
            true_label_id = self._test_y[i]
            true_label = self.num2label[true_label_id]
            
            prediction = self.inference(msg)
            
            if prediction == true_label:
                correct += 1
                
        return correct / total
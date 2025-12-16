import numpy as np
import re

class Dataset:
    def __init__(self, X, y):
        self._x = X # сообщения 
        self._y = y # метки ["spam", "ham"]
        self.train = None # кортеж из (X_train, y_train)
        self.val = None # кортеж из (X_val, y_val)
        self.test = None # кортеж из (X_test, y_test)
        self.label2num = {} # словарь, используемый для преобразования меток в числа
        self.num2label = {} # словарь, используемый для преобразования числа в метки
        self._transform()
        
    def __len__(self):
        return len(self._x)
    
    def _transform(self):
        '''
        Функция очистки сообщения и преобразования меток в числа.
        '''
        # 1. Map labels to numbers (ham -> 0, spam -> 1)
        unique_labels = list(set(self._y))
        for idx, label in enumerate(unique_labels):
            self.label2num[label] = idx
            self.num2label[idx] = label
            
        # Transform y to numbers
        self._y = np.array([self.label2num[label] for label in self._y])
        
        # 2. Clean text (remove punctuation, lowercase)
        # We store the cleaned text back into self._x
        clean_x = []
        for text in self._x:
            text = text.lower()
            # Regex to remove non-alphanumeric characters (keep spaces)
            text = re.sub(r'[^\w\s]', '', text) 
            clean_x.append(text)
        self._x = np.array(clean_x)

    def split_dataset(self, val=0.1, test=0.1):
        '''
        Splits the dataset into train-validation-test.
        '''
        # Ensure randomness
        indices = np.arange(len(self._x))
        np.random.shuffle(indices)
        
        # Calculate split indices
        test_count = int(len(self._x) * test)
        val_count = int(len(self._x) * val)
        
        test_idx = indices[:test_count]
        val_idx = indices[test_count : test_count + val_count]
        train_idx = indices[test_count + val_count :]
        
        # Assign tuples (X, y)
        self.test = (self._x[test_idx], self._y[test_idx])
        self.val = (self._x[val_idx], self._y[val_idx])
        self.train = (self._x[train_idx], self._y[train_idx])
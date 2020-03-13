import numpy as np
import pandas as pd
from sklearn.preprocessing import Normalizer

class TrainData:
  def __init__(self, trainFile, testFile, dataset_id):
    super().__init__()
    self.traindata = pd.read_csv(trainFile, header=None)
    self.testdata = pd.read_csv(testFile, header=None)
    self.dataset_id = dataset_id
  
  def train_data(self):
    X = self.traindata.iloc[:,1:42]
    scaler = Normalizer().fit(X)
    trainX = scaler.transform(X)
    
    return np.array(trainX)

  def train_label(self):
    Y = self.traindata.iloc[:,0]
    return np.array(Y)
  
  def test_data(self):
    T = self.testdata.iloc[:,1:42]
    scaler = Normalizer().fit(T)
    testT = scaler.transform(T)
    return np.array(testT)

  def test_label(self):
    C = self.testdata.iloc[:,0]
    return np.array(C)
  
  def getID(self):
    return self.dataset_id


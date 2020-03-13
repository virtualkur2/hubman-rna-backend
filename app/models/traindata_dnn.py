import numpy as np
import pandas as pd
from sklearn.preprocessing import Normalizer

class TrainDataDNN:
  def __init__(self, trainFile, dataset_id):
    super().__init__()
    self.traindata = pd.read_csv(trainFile, header=None)
    self.dataset_id = dataset_id
  
  def XTrain(self):
    X = self.traindata.iloc[:,1:42]
    trainX = np.array(X)
    trainX.astype(float)
    scaler = Normalizer().fit(trainX)
    trainX = scaler.transform(trainX)
    return np.array(trainX)

  def YTrain(self):
    Y = self.traindata.iloc[:,0]
    return np.array(Y)

  def getIF(self):
    return self.dataset_id

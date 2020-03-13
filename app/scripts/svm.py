from sklearn.svm import SVC
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score)

def svm(data):

  traindata = data.train_data()
  trainlabel = data.train_label()
  testdata = data.test_data()
  testlabel = data.test_label()

  print("--------------------------------------SVM linear--------------------------------------")

  model = SVC(kernel='linear', C=1000,probability=True)
  model.fit(traindata, trainlabel)
  print(model)
  # make predictions
  expected = testlabel
  predicted = model.predict(testdata)
  proba = model.predict_proba(testdata)

  # np.savetxt('classical/predictedlabelSVM-linear.txt', predicted, fmt='%01d')
  # np.savetxt('classical/predictedprobaSVM-linear.txt', proba)

  # summarize the fit of the model

  y_train1 = expected
  y_pred = predicted
  accuracy = accuracy_score(y_train1, y_pred)
  recall = recall_score(y_train1, y_pred , average="binary")
  precision = precision_score(y_train1, y_pred , average="binary")
  f1 = f1_score(y_train1, y_pred, average="binary")

  results = {
    'dataset_id': data.getID(),
    'accuracy': accuracy,
    'precision': precision,
    'recall': recall,
    'f1score': f1
  }
  
  print("accuracy")
  print("%.3f" %accuracy)
  print("precision")
  print("%.3f" %precision)
  print("recall")
  print("%.3f" %recall)
  print("f1score")
  print("%.3f" %f1)

  return results


#Use the training result in Classifier.py (read the joblib file)
#to predict the result for other sets of data



import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from root_numpy import root2array, rec2array,array2root
#from sklearn import cross_validation
from sklearn.metrics import accuracy_score, log_loss, classification_report, roc_auc_score,confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
import pandas as pd
import numpy as np
from root_pandas import *
import sys, os, math
os.environ["CUDA_VISIBLE_DEVICES"] = ""   # Do not use GPU
from sklearn.model_selection import  train_test_split,KFold
from sklearn.utils.class_weight import compute_sample_weight

import joblib

import pandas.core.common as com
from pandas.core.index import Index

#from pandas.tools import plotting
#from pandas.tools.plotting import scatter_matrix


branch_names=['3pi_M',  'Tau_m12', 'Tau_m13','Tau_m23','Tau_FD','Tau_life_reco']   #We need the same variables as that we used to train

bdt = joblib.load('bdt.joblib')




feed = root2array("/home/ke/tmps/feed.root","DecayTree",branch_names)
feed = rec2array(feed)

y_predicted_feed = bdt.decision_function(feed)
y_predicted_feed.dtype = [('BDT', np.float64)]


prompt = root2array("/home/ke/tmps/prompt.root","DecayTree",branch_names)
prompt = rec2array(prompt)

y_predicted_prompt = bdt.decision_function(prompt)
y_predicted_prompt.dtype = [('BDT', np.float64)]


Ds = root2array("/home/ke/tmps/Ds.root","DecayTree",branch_names)
Ds = rec2array(Ds)

y_predicted_Ds = bdt.decision_function(Ds)
y_predicted_Ds.dtype = [('BDT', np.float64)]


Dplus = root2array("/home/ke/tmps/Dplus.root","DecayTree",branch_names)
Dplus = rec2array(Dplus)

y_predicted_Dplus = bdt.decision_function(Dplus)
y_predicted_Dplus.dtype = [('BDT', np.float64)]

D0 = root2array("/home/ke/tmps/D0.root","DecayTree",branch_names)
D0 = rec2array(D0)

y_predicted_D0 = bdt.decision_function(D0)
y_predicted_D0.dtype = [('BDT', np.float64)]



signal = root2array("/home/ke/tmps/signal.root","DecayTree",branch_names)
signal = rec2array(signal)

y_predicted_signal = bdt.decision_function(signal)
y_predicted_signal.dtype = [('BDT', np.float64)]



#Convert the prediction to an array
def returnBDT(pred):
  res=[]
  for element in pred:
    res.append(element[0])
  return res




BDTlist={'Ds':returnBDT(y_predicted_Ds),'Dplus':returnBDT(y_predicted_Dplus),'D0':returnBDT(y_predicted_D0),'prompt':returnBDT(y_predicted_prompt),'feed':returnBDT(y_predicted_feed),'signal':returnBDT(y_predicted_signal)}

file_names=['Ds','Dplus','D0','prompt','feed']

BDTlist={'signal':returnBDT(y_predicted_signal)}

for name in file_names:
  file="/home/ke/tmps/"+name+".root"
  df=read_root(file)
  df['BDT']=BDTlist[name]
  df.to_root("/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Merged_Bkg/"+name+"_BDT.root",'DecayTree')

dg=  read_root("/home/ke/tmps/signal.root")
dg['BDT']=BDTlist['signal']
dg.to_root("/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstTauNu/3pi_LHCb_Total/model_vars_weights_hammer_BDT.root",'DecayTree')




bins=30




#plot the histograms of the predicted values (BDT) for each dataset

plt.hist(returnBDT(y_predicted_signal), bins=bins,density=True,
             histtype='step', label='signal')

plt.hist(returnBDT(y_predicted_feed),  bins=bins,density=True,
             histtype='step', label='feed')


plt.hist(returnBDT(y_predicted_prompt),  bins=bins,density=True,
             histtype='step', label='prompt')


plt.hist(returnBDT(y_predicted_D0),  bins=bins,density=True,
             histtype='step', label=r'$D^0$')


plt.hist(returnBDT(y_predicted_Dplus), bins=bins,density=True,
             histtype='step', label=r'$D^+$')


plt.hist(returnBDT(y_predicted_Ds),  bins=bins,density=True,
             histtype='step',label=r'$D_s$')

plt.title('BDT distributions')
plt.legend()
plt.savefig('BDT.pdf')







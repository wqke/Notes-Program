#Divide two histograms in python using root2matplotlib



import matplotlib   
matplotlib.use('Agg')   #fix python2 Tkinter problem
from matplotlib import pyplot as plt
import pandas as pd
import os
from root_pandas import *
import pandas as pd
import numpy as np
from numpy import cos,sin,tan,sqrt,absolute,real,conjugate,imag,abs,max,min
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm,rc
from skhep.visual import MplPlotter as skh_plt
import rootplot.root2matplotlib as r2m   #plot errorbars on the histogram 
from ROOT import TH1F,TChain,TFile       #divide two histograms

#define a tree with an existing root file
tree = TChain("DecayTree")
tree.Add("/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstTauNu/3pi_LHCb_Total/model_vars_weights_hammer_BDT.root")
 
 
 
hist_SM = TH1F("hist_SM","",20,-4,3.5)     #name='hist_SM' , bins=20 , range=[-4,3.5]
tree.Draw("BDT>>hist_SM","hamweight_SM")

hist_T2 = TH1F("hist_T2","",20,-4,3.5)
tree.Draw("BDT>>hist_T2","hamweight_T2")

hist_SM.Scale(1.0/hist_SM.Integral())   #normalise two histograms before dividing
hist_T2.Scale(1.0/hist_T2.Integral())

hist_SM.Divide(hist_T2)

hist = r2m.Hist(hist_SM)

fig, ax = plt.subplots(figsize=(7,7))
hist.errorbar(fmt='o', yerr=True, color='blue')
plt.axhline(y=1.,linestyle='--',color='red')   #draw horizontal line
plt.title('BDT ratio')
#plt.yscale('log')
plt.xlabel('BDT')
plt.savefig('BDTratio_20.pdf')

plt.close()
plt.close()



#Same procedure



hist_SM = TH1F("hist_SM","",20,4000.,100000.)      
tree.Draw("Tau_FD>>hist_SM","hamweight_SM")

hist_T2 = TH1F("hist_T2","",20,4000.,100000.)
tree.Draw("Tau_FD>>hist_T2","hamweight_T2")
hist_SM.Scale(1.0/hist_SM.Integral())   #normalise two histograms before dividing
hist_T2.Scale(1.0/hist_T2.Integral())
hist_SM.Divide(hist_T2)


hist = r2m.Hist(hist_SM)

fig, ax = plt.subplots(figsize=(7,7))
hist.errorbar(fmt='o', yerr=True, color='blue')
plt.axhline(y=1.,linestyle='--',color='red') #draw horizontal line
plt.title('Tau_FD ratio')
#plt.yscale('log')
plt.xlabel('Tau_FD [mm]')
plt.xticks([4000,20000,40000,60000,80000,100000],['4','20','40','60','80','100'])
plt.savefig('FDratio_20.pdf')

plt.close()
plt.close()




""""""




#define a tree with an existing root file

df=read_root("/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstTauNu/3pi_LHCb_Total/merged_signal.root","DecayTree")

weights_I1c=df['w_I1c']
plt.hist(df['costheta_D_true'],weights=weights_I1c,bins=30,normed=True) 
 
 
 
hist_true = TH1F("hist_true","",30,-1.,1.)     #name='hist_SM' , bins=20 , range=[-4,3.5]
tree.Draw("BDT>>hist_true","hamweight_SM")



hist_math = TH1F("hist_math","",30,-1.,1.)
tree.Draw("BDT>>hist_math","hamweight_T2")

hist_SM.Scale(1.0/hist_SM.Integral())   #normalise two histograms before dividing
hist_T2.Scale(1.0/hist_T2.Integral())

hist_SM.Divide(hist_T2)

hist = r2m.Hist(hist_SM)

fig, ax = plt.subplots(figsize=(7,7))
hist.errorbar(fmt='o', yerr=True, color='blue')
plt.axhline(y=1.,linestyle='--',color='red')   #draw horizontal line
plt.title('BDT ratio')
#plt.yscale('log')
plt.xlabel('BDT')
plt.savefig('BDTratio_20.pdf')

plt.close()
plt.close()



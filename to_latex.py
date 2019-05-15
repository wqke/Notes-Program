import pandas as pd
import numpy as np
import json
from collections import OrderedDict
import sys, os, math
sys.path.append("../../TensorFlowAnalysis")
os.environ["CUDA_VISIBLE_DEVICES"] = ""   # Do not use GPU

num = sys.argv[1]
ham = sys.argv[2]
sub_mode='3pi'
geom='LHCb'
var_type='reco'

coeffs = OrderedDict()

coeffs["I9"] = "$I_{9}$"
coeffs["I8"] = "$I_{8}$"
coeffs["I7"] = "$I_{7}$"
coeffs["I6s"] = "$I_{6s}$"
coeffs["I6c"] = "$I_{6c}$"
coeffs["I5"] = "$I_{5}$"
coeffs["I4"] = "$I_{4}$"
coeffs["I3"] = "$I_{3}$"
coeffs["I2s"] = "$I_{2s}$"
coeffs["I2c"] = "$I_{2c}$"
coeffs["I1s"] = "$I_{1s}$"
coeffs["I1c"] = "$I_{1c}$"
coeffs["frac_signal"] = "$frac_signal$"
coeffs["frac_Ds"] = "$frac_Ds$"
coeffs["frac_Dplus"] = "$frac_Dplus$"



columns1=['tot bkg frac','BDT','wI','fit'] 
columns2=['int frac prompt','int frac feed','int frac Ds','int frac Dplus','int frac D0']    #compare systematics of internal frac
columns3=['ext frac prompt','ext frac feed','ext frac Ds','ext frac Dplus','ext frac D0']    #compare systematics of external frac

column_list=[columns1,columns2,columns3]


def ChooseData(elem):  #choose one of the systematics files
  syst=[]
  if elem=='BDT':
    with open('results/%s/syst_3pi_LHCb_reco_%s_%s_D0_%s.json' %(elem,num,ham,elem), "r") as read_file:
      result = json.load(read_file)
    for c in coeffs :
      syst.append(result[c])
    
  elif elem=='wI' :
    with open('results/%s/syst_3pi_LHCb_reco_%s_%s_D0_%s.json' %(elem,num,ham,elem), "r") as read_file:
      result = json.load(read_file)
    for c in coeffs :
      syst.append(result[c+'_sigma'])

  elif elem=='tot bkg frac':
    with open('results/tot_syst_3pi_LHCb_reco_%s_%s.json' %(num,ham), "r") as read_file:
      result = json.load(read_file)
    for c in coeffs :
      syst.append(result[c])
      
  elif elem=='fit':
    df_reco_all = pd.read_csv("results/result_Lifetime_%s_%s_%s_%s_Hammer_%s.txt" % (sub_mode,geom,var_type,num,ham), header = None, sep=" ")
    df_p_reco_all = pd.read_csv("results/param_Lifetime_%s_%s_%s_%s_Hammer_%s.txt" % (sub_mode,geom,var_type,num,ham), header = None, sep=" ")
    df_reco={}
    for c in coeffs :
      if(c=="I1c"):
        df_reco["%s" % c] = df_p_reco_all[df_p_reco_all[0].str.contains("%s" % c)]
      else:
        df_reco["%s" % c] = df_reco_all[df_reco_all[0].str.contains("%s" % c)]
      err = df_reco["%s" % c].iat[0,2]
      with open('results/toy_pulls_%s_%s_%s_%s_%s.json' % (sub_mode,geom,var_type,num,ham), "r") as read_file:
        toy_pulls = json.load(read_file)
      syst.append(err*toy_pulls["%s_sigma" % c])  #corrected fit error

  else:   #columns2 or 3
    bkg=elem.split(' ')[-1]
    systtype=elem.split(' ')[0]  #int or ext
    with open('results/%s/syst_3pi_LHCb_reco_%s_%s_%s_%s.json' %(systtype,num,ham,bkg,systtype), "r") as read_file:
      result = json.load(read_file)
    for c in coeffs :
      syst.append(result[c+'_sigma'])
  
  return syst
  



for column in column_list:
  data={}
  for elem in column:
    data[elem]=ChooseData(elem)
  df=pd.DataFrame(data)
  df=df[column]
  df.index=list(coeffs)
  print(df.to_latex(encoding='utf-8',index=True))
  with open('%s.tex' %str(column),'w') as tf:
    tf.write(df.to_latex())







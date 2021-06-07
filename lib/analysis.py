import pandas as pd
import re
import math
#Extraer el Diccionario

def down(Documento):
  Doc = []
  for i in range(len(Documento)):
    d1 = Documento[i]
    d1 = str(d1)
    d1 = d1.lower()
    Doc.append(d1)
  return Doc



#------ Limpieza ------
def Limpieza(Documento):
  Doc = []
  for i in range(len(Documento)):
    d1 = Documento[i]
    d1 = str(d1)
    d1 = re.sub('[^A-Za-z0-9]+', ' ', d1)
    d1 = d1.lower()
    d1 = d1.split()
    Doc.append(d1)
  return Doc
#------ Diccionario ------
def Diccionario(documento1,documento2,sentimiento):
  Diccionario = []
  for i in range(len(documento1)):
    if documento2[i] == sentimiento:
      Diccionario.append(documento1[i])
  return Diccionario
#------ Coseno Vectorial ------
def Coseno_Vec(d3,Diccionario):
  #Bag words
  V_Abstract = []
  for i in range(len(d3)):
    var = d3[i]
    cont = []
    for word in Diccionario:
      cont.append(var.count(word))
    V_Abstract.append(cont)
  #WTF
  V_W_Abstract = []
  for i in range(len(V_Abstract)):
    var = V_Abstract[i]
    cont = []
    for j in var:
      if j != 0:
        cont.append(1 + math.log(j,10))
      else:
        cont.append(0)
    V_W_Abstract.append(cont)
  #DF
  V_DF_Abstract = []
  for word in Diccionario:
    cont = 0
    for i in d3:
      if word in i:
        cont += 1
    V_DF_Abstract.append(cont)
  #IDF
  V_IDF_Abstract = []
  for i in V_DF_Abstract:
    if i != 0:
      V_IDF_Abstract.append(math.log(len(d3) / i,10))
    else:
      V_IDF_Abstract.append(0)
  #TF-IDF
  V_TF_IDF_Abstract = []
  for i in range(len(V_Abstract)):
    var = V_Abstract[i]
    cont = []
    for j in range(len(var)):
      cont.append(var[j] * V_IDF_Abstract[j])
    V_TF_IDF_Abstract.append(cont)

  #Modulo
  V_Mod_Abstract = []
  for i in range(len(V_W_Abstract)):
    var = V_W_Abstract[i]
    sum = 0
    for j in range(len(var)):
      sum = sum + var[j]**2
    V_Mod_Abstract.append(math.sqrt(sum))
  #Vector Unitario
  V_Uni_Abstract = []
  for i in range(len(V_W_Abstract)):
    var = V_W_Abstract[i]
    cont = []
    for j in range(len(var)):
      if  V_Mod_Abstract[i] != 0:
        cont.append(var[j] / V_Mod_Abstract[i])
      else:
        cont.append(0)
    V_Uni_Abstract.append(cont)
  #Coseno Vectorial
  V_Co_Abstract = []
  for i in range(len(V_Uni_Abstract)):
    var = V_Uni_Abstract[i]
    cont = []
    for j in range(len(V_Uni_Abstract)):
      sum = 0
      var2 = V_Uni_Abstract[j]
      for k in range(len(var2)):
        sum = sum + (var[k] * var2[k])
      cont.append(round(sum,4))
    V_Co_Abstract.append(cont)
  C = V_Co_Abstract[-3:]
  for i in range(len(C)):
    for j in range(3):
      C[i].pop()
  return C
#------ Jacard ------
def Jacard(Documento,Diccionario):
  vec = []
  for i in range(len(Documento)):
    t = list(set(Documento[i]+Diccionario))
    tot = len(t)
    cont = 0
    for word in list(set(Documento[i])):
      if word in Diccionario:
        cont += 1
    j = cont / tot
    vec.append(round(j, 4))
  return vec
#------ Sentimiento ------
def Senti(Pos,Neu,Neg,D):
  Po = Pos
  Nu = Neu
  Ng = Neg
  sentimiento = ''
  may = 0
  if Po[D] > may:
    sentimiento = 'Positivo'
    may = Po[D]
  if Nu[D] > may:
    sentimiento = 'Neutral'
    may = Nu[D]
  if Ng[D] > may:
    sentimiento = 'Negativo'
    may = Ng[D]
  return sentimiento



def ObtenerValores(n):
  # url = "https://drive.google.com/uc?export=download&id=1Fa7MnSX5Av_VBOMis0TkOUibLPjCvY4C" ## Diccionario
  DataSet = pd.read_csv('data/Diccionario.csv',encoding="utf8")

  Kichwa = DataSet.iloc[:, 1]
  Spanish = DataSet.iloc[:, 2]
  Sentimiento = DataSet.iloc[:, 3]
  Kichwa = list(Kichwa)
  Spanish = list(Spanish)
  Sentimiento = list(Sentimiento)

  # Sentimiento = down(Sentimiento)

  # url1 = "https://drive.google.com/uc?export=download&id=198XFsoEj-WnB6o5k1D_hht0u_YqdT9G6" #Frases
  DataSet1 = pd.read_csv('data/Frases.csv',encoding="utf8",sep=';')
  frase = DataSet1.iloc[:, 0]
  tradu = DataSet1.iloc[:, 1]
  frase = frase[:9]
  tradu = tradu[:9]

  frase = Limpieza(frase)

  texto_kichwa, texto_esp = DataSet1.to_numpy()[n, :]

  Dic_Pos = Diccionario(Kichwa,Sentimiento,'positivo')
  Dic_Neu = Diccionario(Kichwa,Sentimiento,'neutro')
  Dic_Neg = Diccionario(Kichwa,Sentimiento,'negativo')

  Jac_Pos = Jacard(frase,Dic_Pos)
  Jac_Neg = Jacard(frase,Dic_Neu)
  Jac_Neu = Jacard(frase,Dic_Neg)

  fr_dic = frase
  fr_dic.append(Dic_Pos)
  fr_dic.append(Dic_Neu)
  fr_dic.append(Dic_Neg)
  Cos = Coseno_Vec(fr_dic,Kichwa)

  s = Senti(Cos[0],Cos[1],Cos[2],n)
  jacard_values = {
    "positivo": Jac_Pos[n],
    "negativo": Jac_Neg[n],
    "neutro": Jac_Neu[n]
  }
  cos_values = {
    "positivo": Cos[0][n],
    "negativo": Cos[1][n],
    "neutro": Cos[2][n]
  }
  return texto_kichwa, texto_esp, jacard_values, cos_values, s


def ObtenerDict():
  DataSet = pd.read_csv('data/Diccionario.csv',encoding="utf8")

  Kichwa = DataSet.iloc[:, 1]
  Spanish = DataSet.iloc[:, 2]
  Sentimiento = DataSet.iloc[:, 3]
  Kichwa = list(Kichwa)
  Spanish = list(Spanish)
  Sentimiento = list(Sentimiento)


  Dic_Pos = Diccionario(Kichwa,Sentimiento,'positivo')
  Dic_Neu = Diccionario(Kichwa,Sentimiento,'neutro')
  Dic_Neg = Diccionario(Kichwa,Sentimiento,'negativo')

  return Dic_Pos, Dic_Neu, Dic_Neg, Kichwa

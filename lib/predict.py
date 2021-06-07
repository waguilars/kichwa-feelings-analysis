from lib.analysis import Limpieza, Jacard, Coseno_Vec, ObtenerDict

def Texto_On(texto):
  Dic_Pos, Dic_Neu, Dic_Neg, Kichwa = ObtenerDict()
  jac = [texto]
  jac = Limpieza(jac)

  cos = [texto]
  cos = Limpieza(cos)
  cos.append(Dic_Pos)
  cos.append(Dic_Neu)
  cos.append(Dic_Neg)

  print('-- Jaccard Positivo -- ')
  Pos = Jacard(jac,Dic_Pos)
  print(Pos)
  print('-- Jaccard Neutral-- ')
  Neu = Jacard(jac,Dic_Neu)
  print(Neu)
  print('-- Jaccard Negativo -- ')
  Neg = Jacard(jac,Dic_Neg)
  print(Neg)

  Cos = Coseno_Vec(cos,Kichwa)
  print('-- Coseno Positivo-- ')
  print(Cos[0])
  print('-- Coseno Neutral -- ')
  print(Cos[1])
  print('-- Coseno Negativo -- ')
  print(Cos[2])

  Cos_Po = Cos[0]
  Cos_Nu = Cos[1]
  Cos_Ng = Cos[2]

  sentimiento = ''
  may = 0
  if Cos_Po[0] > may:
    sentimiento = 'Positivo'
    may = Cos_Po[0]
  if Cos_Nu[0] > may:
    sentimiento = 'Neutral'
    may = Cos_Nu[0]
  if Cos_Ng[0] > may:
    sentimiento = 'Negativo'
    may = Cos_Ng[0]

  jac_values = {
    "positivo": Pos[0],
    "negativo": Neu[0],
    "neutro": Neg[0]
  }
  cos_values = {
    "positivo": Cos[0][0],
    "negativo": Cos[1][0],
    "neutro": Cos[2][0]
  }
  return jac_values, cos_values,sentimiento

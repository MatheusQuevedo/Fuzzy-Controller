import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from skfuzzy import control as ctrl

np.random.seed(42)
"""
Sensores laterais e angulo do volante
"""
df = pd.read_csv('dataSteering.csv')
out = df.to_numpy()
min(out)
out = out.transpose()
out
bla=[]
for i in out[0]:
    bla.append(i)
out=np.array(bla)
out

df = pd.read_csv('dataSensores.csv')
res = df.to_numpy()

b = res[:,1]
a = res[:,2]
error = b-a
max(error)
print(out.shape)
print(error.shape)
alldata = np.vstack((error, out))
alldata = alldata.transpose()
scaler = MinMaxScaler()
scaler.fit(alldata)
alldata = scaler.transform(alldata)
alldata = alldata.transpose()
alldata

print(alldata.shape)

"""
Sensor frontal e velocidade
"""
df = pd.read_csv('dataVelocidade.csv')
out = df.to_numpy()
out
out = out.transpose()
out
bla=[]
for i in out[0]:
    bla.append(i)
vel=np.array(bla)
vel

df = pd.read_csv('dataSensores.csv')
res = df.to_numpy()

frontal = res[:,0]



print(vel.shape)
print(frontal.shape)
alldata_frontal_vel = np.vstack((frontal, vel))
alldata_frontal_vel = alldata_frontal_vel.transpose()
alldata_frontal_vel.shape
scaler_frontal_vel = MinMaxScaler()
scaler_frontal_vel.fit(alldata_frontal_vel)
alldata_frontal_vel = scaler_frontal_vel.transform(alldata_frontal_vel)

alldata_frontal_vel = alldata_frontal_vel.transpose()
alldata_frontal_vel
print(alldata.shape)

"""
Sensor frontal, lateral e ângulo
"""
df = pd.read_csv('dataSteering.csv')
out = df.to_numpy()
out
out = out.transpose()
out
bla=[]
for i in out[0]:
    bla.append(i)
steer=np.array(bla)
steer

df = pd.read_csv('dataSensores.csv')
res = df.to_numpy()
frontal = res[:,0]
b = res[:,1]
a = res[:,2]
laterais = b-a
min(laterais)

print(steer.shape)
print(laterais.shape)
alldata_frontlat_ang = np.vstack((frontal, laterais))
alldata_frontlat_ang = np.vstack((alldata_frontlat_ang, steer))
alldata_frontlat_ang = alldata_frontlat_ang.transpose()
alldata_frontlat_ang.shape
scaler_frontlat_ang = MinMaxScaler()
scaler_frontlat_ang.fit(alldata_frontlat_ang)
alldata_frontlat_ang = scaler_frontlat_ang.transform(alldata_frontlat_ang)

alldata_frontlat_ang = alldata_frontlat_ang.transpose()
alldata_frontlat_ang
print(alldata_frontlat_ang.shape)

"""
cmeans para relacionar os sensores laterais com o ângulo do volante
"""
c = []
for i in range(2,20):
    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(alldata, i, 2, error=0.005, maxiter=1000, seed=42)
    c.append(fpc)


plt.plot(range(2,20), c)
plt.show()

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(alldata, 3, 2, error=0.005, maxiter=1000, seed=42)

#Show 3-cluster model
fig2, ax2 = plt.subplots()
ax2.set_title('Sensores laterais versus ângulo do volante')
for j in range(3):
    ax2.plot(alldata[0, u.argmax(axis=0) == j],
             alldata[1, u.argmax(axis=0) == j], 'o',
              label='series ' + str(j))

ax2.legend()
plt.show()

#como resgatar os valores originais
cntr.shape
bleuris.shape

bleuris=cntr.transpose()
scaler.inverse_transform(cntr)



"""
cmeans para relacionar o sensor frontal com a velocidade
"""
c = []
for i in range(2,20):
    cntr_frontal_vel, u_frontal_vel, u0, d, jm, p, fpc = fuzz.cluster.cmeans(alldata_frontal_vel, i, 2, error=0.005, maxiter=1000, seed=42)
    c.append(fpc)


plt.plot(range(2,20), c)
plt.show()

cntr_frontal_vel, u_frontal_vel, u0, d, jm, p, fpc = fuzz.cluster.cmeans(alldata_frontal_vel, 2, 2, error=0.005, maxiter=1000, seed=42)

#Show 3-cluster model
fig2, ax2 = plt.subplots()
ax2.set_title('Sensor frontal versus velocidade')
for j in range(2):
    ax2.plot(alldata_frontal_vel[0, u_frontal_vel.argmax(axis=0) == j],
             alldata_frontal_vel[1, u_frontal_vel.argmax(axis=0) == j], 'o',
              label='series ' + str(j))

ax2.legend()
plt.show()

#como resgatar os valores originais
bleuris=cntr_frontal_vel.transpose()
scaler_frontal_vel.inverse_transform(bleuris)

"""
cmeans para relacionar os sensores frontal e laterais com o ângulo do volante
"""
c = []
for i in range(2,20):
    cntr_frontlat_ang, u_frontlat_ang, u0, d, jm, p, fpc = fuzz.cluster.cmeans(alldata_frontlat_ang, i, 2, error=0.005, maxiter=1000, seed=42)
    c.append(fpc)

c[1]
c[2]
c[3]

plt.plot(range(2,20), c)
plt.show()

cntr_frontlat_ang, u_frontlat_ang, u0, d, jm, p, fpc = fuzz.cluster.cmeans(alldata_frontlat_ang, 4, 2, error=0.005, maxiter=1000, seed=42)

#Show 3-cluster model
fig2, ax2 = plt.subplots()
ax2.set_title('Sensores laterais e frontais versus ângulo do volante')
for j in range(4):
    ax2.plot(alldata_frontlat_ang[0, u_frontlat_ang.argmax(axis=0) == j],
             alldata_frontlat_ang[1, u_frontlat_ang.argmax(axis=0) == j],
             alldata_frontlat_ang[2, u_frontlat_ang.argmax(axis=0) == j], 'o',
              label='series ' + str(j))

ax2.legend()
plt.show()

cntr_frontlat_ang.shape
#como resgatar os valores originais
scaler_frontlat_ang.inverse_transform(cntr_frontlat_ang)


u, u0, d, jm, p, fpc = fuzz.cluster.cmeans_predict(np.array([[0.53437889],[0.412]]), cntr, 2, error=0.005, maxiter=1000)
u



"""
teste de controlador fuzzy
"""
# New Antecedent/Consequent objects hold universe variables and membership
# functions
posicao_lateral = ctrl.Antecedent(np.arange(-600, 500, 0.1), 'Posicao Lateral')
posicao_frontal = ctrl.Antecedent(np.arange(0, 800, 0.1), 'Posicao Frontal')
angulo_volante = ctrl.Consequent(np.arange(-30, 30, 0.1), 'Angulo Volante')
velocidade = ctrl.Consequent(np.arange(0, 3, 0.1), 'Velocidade')

# Custom membership functions can be built interactively with a familiar,
# Funções de pertinência para os sensores laterais
posicao_lateral['Esquerda'] = fuzz.trapmf(posicao_lateral.universe, [-610, -600, -13.2, -5])
posicao_lateral['Meio'] = fuzz.trimf(posicao_lateral.universe, [-10 , -3.8, 1.5])
posicao_lateral['Direita'] = fuzz.trapmf(posicao_lateral.universe, [1, 1.2, 500, 510])
# Funções de pertinência para o sensor frontal
posicao_frontal['Perto'] = fuzz.trapmf(posicao_frontal.universe, [-1, 0, 402, 600])
posicao_frontal['Longe'] = fuzz.trapmf(posicao_frontal.universe, [450, 704, 800, 810])
# Funções de pertinência para os sensores laterais
angulo_volante['Esquerda'] = fuzz.trapmf(angulo_volante.universe, [-33, -30, -25,-9])
angulo_volante['Meio'] = fuzz.trimf(angulo_volante.universe, [-10, -0.9, 10])
angulo_volante['Direita'] = fuzz.trapmf(angulo_volante.universe, [9, 25, 30, 35])
# Funções de pertinência para o sensor frontal
velocidade['Devagar'] = fuzz.trapmf(velocidade.universe, [-1, 0, 0.4, 1.5])
velocidade['Rapido'] = fuzz.trapmf(velocidade.universe, [1, 2.9, 3, 3.5])
# You can see how these look with .view()
posicao_frontal['Longe'].view()
velocidade['Devagar'].view()
posicao_lateral['Direita'].view()
angulo_volante['Meio'].view()

#Regras
rule1 = ctrl.Rule(posicao_lateral['Meio'] & posicao_frontal['Longe'], angulo_volante['Meio'])
rule1_2 = ctrl.Rule(posicao_lateral['Meio'] & posicao_frontal['Longe'], velocidade['Rapido'])
rule2 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Perto'], angulo_volante['Direita'])
rule2_2 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Perto'], velocidade['Devagar'])
rule3 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Perto'], angulo_volante['Esquerda'])
rule3_2 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Perto'], velocidade['Devagar'])
rule4 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Longe'], angulo_volante['Direita'])
rule4_2 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Longe'], velocidade['Rapido'])
rule5 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Longe'], angulo_volante['Esquerda'])
rule5_2 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Longe'], velocidade['Rapido'])
rule1.view()


car_ctrl = ctrl.ControlSystem([rule1, rule1_2, rule2, rule2_2, rule3, rule3_2, rule4, rule4_2, rule5, rule5_2])
carro = ctrl.ControlSystemSimulation(car_ctrl)
carro.input['Posicao Lateral'] = 30
carro.input['Posicao Frontal'] = 400
carro.compute()
type(carro.output['Angulo Volante'])

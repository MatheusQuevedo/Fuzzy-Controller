import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import pandas as pd

np.random.seed(42)

df = pd.read_csv('dataSteering.csv')
df = df.drop(1)
df = df.drop(2)
df = df.drop(3)
out = df.to_numpy()

df = pd.read_csv('dataSensores.csv')
res = df.to_numpy()

b = res[:,1]
a = res[:,2]
error = b-a

out = out.reshape(out.size,1)
error = error.reshape(error.size,1)

#print(a)
#print(b)
#print(error)
# print(error)
print(out.shape)
print(error.shape)

alldata = np.vstack((error, out))
print(alldata.shape)
# alldata = pd.DataFrame(alldata)
# alldata = alldata.transpose()
# alldata = alldata.to_numpy()

#print(alldata.head())


c = []
for i in range(2,20):
    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(alldata, i, 2, error=0.005, maxiter=1000)
    c.append(fpc)

plt.plot(range(2,20), c)
plt.show()

cntr, u, _, _, _, _, _ = fuzz.cluster.cmeans(alldata, 4, 2, error=0.005, maxiter=1000)

#Show 3-cluster model
fig2, ax2 = plt.subplots()
ax2.set_title('Trained model for sensor 1')
for j in range(4):
    ax2.plot(alldata[0, u.argmax(axis=0) == j],
             alldata[1, u.argmax(axis=0) == j], 'o',
              label='series ' + str(j))

ax2.legend()
plt.show()

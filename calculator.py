#Libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

#Create output file
output = open("Output_langevin.txt",'w')   

#Create data structure
data = []
blkavg = []
p = []

#Define functions
def avg(a):																#Average function
	return float(sum(a)) * 1.0 / float(len(a))
def std(a):																#Sample standard deviation function
	return (sum((x - avg(a))**2 for x in a) / (len(a) - 1))**0.5
def avgsqr(a):
	return sum([k**2 for k in a]) / len(a)

#Extract data
file = open("log.lammps",'r')							#Open DataFile
for line in file:
	if line[0] == "T" and line[1] == "o" and line[2] == "t" and line[3] == "E":		#Find the line to get data
		for line in file:
			if line[0] == " " and line[1] == " ":									#Check if this line is data point
				line_s = line.split()								#Split string
				data.append(float(line_s[0]))					#Get data from Integer			
file.close()
														#Close DateFile
#Create time block and number of block
tb=range(10,300,1)
nb=[len(data)/k for k in tb]

for i in range(len(tb)):
	for j in range(nb[i]):
		if len(data[0+j*tb[i]:tb[i]+j*tb[i]]) >= tb[i]:
			a=data[0+j*tb[i]:tb[i]+j*tb[i]]
			blkavg.append(float(sum(a))/float(tb[i]))
	e=sum([(k-avg(data))**2 for k in blkavg])/float(nb[i])
	p.append(e*tb[i]/(avgsqr(data)-avg(data)**2))
	blkavg=[]
x = [1./k for k in tb]
y = [1./k for k in p] 
linregress(x,y)
fit = np.polyfit(x,y,1)
fit_fn = np.poly1d(fit) #fit_fn is now a function which takes in x and returns an estimate for y

tc = 200.0/fit_fn(0) #each data point is 200 fs
err = tc*(avgsqr(data)-avg(data)**2)/10400000.0

reg = linregress(x,y)
plt.plot(x,y, 'o', x, fit_fn(x), '--k')
plt.legend( ('data', 'trend line') )
plt.ylabel('1/P')
plt.xlabel('1/tb')
plt.title('Langevin')
plt.savefig('Langevin.pdf')
plt.show()

#Output results
output.write('"FileName", "AVG", "AVGSQR", "STDEV", "tc", "STDERROR"\n')
output.write('lammps.out  %0.2f  %0.2f  %0.2f  %0.2f  %0.2f\n' %(avg(data), avgsqr(data), std(data), tc, err))
output.close()
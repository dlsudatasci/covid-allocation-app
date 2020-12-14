# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 12:23:19 2020

@author: tapiaj
"""

import matplotlib.pyplot as plt
import numpy as np

from pyomo.environ import *

class VACModel():

    def __init__(self):
        #initial data
        self.Group = ["A", "B", "C", "D", "E"]
        self.N0= {"A":77, "B":241, "C":375, "D":204, "E":103}
        self.fn0= {"A":0.5, "B":0.5, "C":0.5, "D":0.5, "E":0.5}
        self.Kmatval = [
            0.6, 0.1, 0.1, 0.1, 0.1,
            0.2, 1.7, 0.3, 0.2, 0.2,
            0.4, 0.3, 0.5, 0.4, 0.3,
            0.2, 0.1, 0.3, 0.2, 0.1,
            0.1, 0.1, 0.1, 0.1, 0.1
            ]
        self.H = 0.98

    def run(self):
        Group = self.Group
        N0 = self.N0
        fn0 = self.fn0
        Kmatval = self.Kmatval
        H = self.H

        vac = ConcreteModel()
        vac.g = Set(initialize=Group)
        vac.mat = vac.g *vac.g
        
        Kmat00 = dict(zip([ij for ij in vac.mat],Kmatval))
        
        #parameters
        vac.K = Param(vac.mat, initialize=Kmat00, mutable=True)
        vac.n = Param(vac.g, initialize=N0)
        
        #variables
        vac.f = Var(vac.g, initialize=fn0, within=NonNegativeReals)
        vac.v = Var(vac.g, initialize=fn0, within=NonNegativeReals)
        
        #objective function
        def OBF(vac):
            return sum(vac.n[i]*vac.f[i] for i in vac.g)
        vac.obj = Objective(rule=OBF, sense=minimize)
        
        #constraints
        def Co1(vac):
            return sum(vac.v[i] for i in vac.g) == 1
        vac.C1 = Constraint(rule=Co1)
        
        def Co2(vac, i):
            return (1-H*vac.f[i])*sum(vac.K[i,j]*vac.v[j] for j in vac.g) <= vac.v[i]
        vac.C2 = Constraint(vac.g, rule=Co2)
        
        
        SolverFactory('ipopt').solve(vac)
        return [vac.f[j].value for j in Group], [vac.v[j].value for j in Group]

"""
Answer = []

x= list(np.arange(0.6,0.95,0.05))
xstr=[str('%.2f'%i) for i in x]

for i in np.arange(0.6, 0.95, 0.05):
        vac.K["A","A"]= i
        #SolverManagerFactory('neos').solve(vac, opt='bonmin')
        SolverFactory('ipopt').solve(vac)
        Answer.append([vac.f[j].value for j in Group])    
        
width =0.35       
fig, ax = plt.subplots()
ax.bar(xstr, [Answer[j][0] for j in range(len(x))], width, label= "A", color='#02dbce')
ax.bar(xstr, [Answer[j][1] for j in range(len(x))], width, bottom=[Answer[j][0] for j in range(len(x))], label= "B", color='#0a3466')
ax.set_facecolor("#f0f0f0")
ax.legend(loc=8, ncol=3, bbox_to_anchor=(0.5, -0.26))
ax.set_ylabel('% Distribution')
ax.set_xlabel('K Value between A-A')
ax.set_title("Sensitivity Analysis")
plt.show()
fig.savefig('Sensi.jpg', format='jpg', dpi=2000, bbox_inches='tight')

#vac.K.pprint()
#vac.mat.pprint()
"""
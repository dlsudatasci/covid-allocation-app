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
        self.Group = ["A", "B", "C", "D", "E"] #groups
        self.N0= {"A":77, "B":241, "C":375, "D":204, "E":103} #population per group
        #self.fn0= {"A":0.5, "B":0.5, "C":0.5, "D":0.5, "E":0.5} #default values for allocation variables
        self.vac_type = ["Vac A", "Vac B"] #vaccine types
        self.Kmatval = [
            0.6, 0.1, 0.1, 0.1, 0.1,
            0.2, 1.7, 0.3, 0.2, 0.2,
            0.4, 0.3, 0.5, 0.4, 0.3,
            0.2, 0.1, 0.3, 0.2, 0.1,
            0.1, 0.1, 0.1, 0.1, 0.1
            ] #contact rates between groups
        self.H = [0.98, 0.90] #vaccine efficacy values
        self.vac_avail = [30, 100] #available number of vaccines
        self.Hvac = dict(zip(self.vac_type, self.H)) #dictionary used for the model
        self.model_sub_type = "minR" #see below
        
        """
        subtype of model
         - minR - minimize spread of infection, measured by R - reproductive number
         - minV - minimize vaccines required, measured by V - vaccine requirements
        """

    def run(self):
        Group = self.Group
        N0 = self.N0
        #fn0 = self.fn0
        Kmatval = self.Kmatval
        Hvac = self.Hvac
        vac_type = self.vac_type
        vac_avail = self.vac_avail

        vac = ConcreteModel()
        vac.g = Set(initialize=Group)
        vac.mat = vac.g *vac.g
        vac.vtype = Set(initialize=vac_type)
        vac.gvtype = vac.g * vac.vtype
        
        Kmat00 = dict(zip([ij for ij in vac.mat],Kmatval))
        
        #parameters
        vac.K = Param(vac.mat, initialize=Kmat00, mutable=True)
        vac.n = Param(vac.g, initialize=N0)
        vac.H = Param(vac.vtype, initialize = Hvac)
        vac.avail = Param(vac.vtype, initialize = dict(zip(vac_type,vac_avail)))
        
        #variables
        vac.f = Var(vac.gvtype, within=NonNegativeReals) # percent of available vaccine to 
        vac.v = Var(vac.g, within=NonNegativeReals) # values in the eigenvector - determines R
        vac.R = Var(within=NonNegativeReals) #reproductive number
        
        #objective function
        def OBF(vac):
            if self.model_sub_type == "minV":
                return sum(vac.n[i]*vac.f[i,p] for i in vac.g for p in vac.vtype)
            elif self.model_sub_type == "minR":
                return vac.R
        vac.obj = Objective(rule=OBF, sense=minimize)
        
        #constraints
        def Co1(vac):
            return sum(vac.v[i] for i in vac.g) == vac.R
        vac.C1 = Constraint(rule=Co1)
        
        if self.model_sub_type == "minR":
            def Co2_minR(vac, p):
                return sum(vac.f[i,p] for i in vac.g) <= vac.avail[p]
            vac.C2p = Constraint(vac.vtype, rule=Co2_minR)        
        
        def Co2(vac, i):
            return (1-sum(vac.H[p]*vac.f[i,p] for p in vac.vtype))*sum(vac.K[i,j]*vac.v[j] for j in vac.g) <= vac.R*vac.v[i]
        vac.C2 = Constraint(vac.g, rule=Co2)
        
        def Co3(vac, i, p):
            return vac.f[i,p] <= 1
        vac.C3 = Constraint(vac.gvtype, rule=Co3)

        def Co4(vac,i):
            return sum(vac.f[i,p] for p in vac.vtype) <=1
        vac.C4 = Constraint(vac.g, rule= Co4)
        
        SolverFactory('ipopt').solve(vac)
        vac.pprint()
        return vac.R.value
        #return [vac.f[j].value for j in Group], [vac.v[j].value for j in Group]


#test
if __name__ == "__main__":
    model = VACModel();
    result = model.run()
    print(result)
    
    
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
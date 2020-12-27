from VACModel import VACModel

def vac(Group, N0, fn0, Kmatval, H):
    vm = VACModel()
    vm.Group = Group
    vm.N0 = N0
    vm.fn0= fn0
    vm.Kmatval = Kmatval
    vm.H = H
    return vm.run()

"""
- Group is the name of the group of people in a population and should be a string data. I suggest to restrict the length from 1 to 30 characters
- N0 is the number of population per group. This should be an integer.
- fn0 is an initial value used to solve fn in the model. fn doesn't represent anything useful for the user so it can hidden from them. 
     We keep all values to the default 0.5 values in each group. We can also remove it in the vac function?
- Kmatval is the contact rate between groups. It should be a decimal value greater than 0. 
- H is the efficacy of the vaccine. It should be between 0 to 1. 

If any of the conditions given above were not satisfied by the user, an error should be displayed, preventing the VACModel to be run. 
I am not sure if the error dialog should be displayed whenever an input violates the condition above or we just implement an error checking mechanism when the user tries to run the model. 
If we choose the second, is it possible for the error checking code to identify which field or cell (if it's in a table) has the incorrect input? 
 
The return value of the model that will be used for the result interface is vac.v which gives the % of the population in each group to be vaccinated. 
                                                                                                     
"""
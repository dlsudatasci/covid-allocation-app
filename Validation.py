def checkN0(N0):
    for val in N0:
        if(type(N0[val]) != int): # check type if integer 
            return False
        if(N0[val] < 0): # check if less than 0
            return False
    return True

def checkGroup(Group):
    for val in Group:
        if(type(val) != str): # check type if string
            return False
        if(len(val) < 1 or len(val) > 30): # check length if 1 to 30 characters
            return False
    return True

def checkKmatval(Kmatval):
    for val in Kmatval:
        if(type(val) != float): # check type if float 
            return False
        if(val <= 0): # check if greater than 0
            return False
    return True

def checkH(H):
    if(type(H) != float): # check type if float 
        return False
    if(H < 0 or H > 1): # check if in between 0 and 1
        return False
    return True

def checkfn0(fn0):
    for val in fn0:
        if(type(fn0[val]) != float): # check type if integer 
            return False
        if(fn0[val] != 0.5):
            return False
    return True

def validate(Group, N0, fn0, Kmatval, H):
    validation = {}
    validation['values'] = [] 
    validation['errors'] = [] 
    validation['valid'] = True
    # Group = string, 1 to 30 characters
    if(not checkGroup(Group)):
        validation['values'].append('Group') 
        validation['errors'].append('Group should be a string that is 1 to 30 characters in length.')
        validation['valid'] = False

    # N0 = integer, not less than 0
    if(not checkN0(N0)):
        validation['values'].append('N0') 
        validation['errors'].append('N0 should be an integer that is not less than 0.')
        validation['valid'] = False

    # fn0 = 0.5
    if(not checkfn0(fn0)):
        validation['values'].append('fn0') 
        validation['errors'].append('fn0 is invalid.')
        validation['valid'] = False

    # Kmatval > 0
    if(not checkKmatval(Kmatval)):
        validation['values'].append('Kmatval') 
        validation['errors'].append('Kmatval should be a float greater than 0.')
        validation['valid'] = False

    # 1 < H > 0
    if(not checkH(H)):
        validation['values'].append('H') 
        validation['errors'].append('H should be a float between 0 to 1.')
        validation['valid'] = False

    return validation

"""
- Group is the name of the group of people in a population and should be a string data. I suggest to restrict the length from 1 to 30 characters
- N0 is the number of population per group. This should be an integer.
- fn0 is an initial value used to solve fn in the model.
     We keep all values to the default 0.5 values in each group. 
- Kmatval is the contact rate between groups. It should be a decimal value greater than 0. 
- H is the efficacy of the vaccine. It should be between 0 to 1. (Percentage)

If any of the conditions given above were not satisfied by the user, an error should be displayed, preventing the VACModel to be run. 
I am not sure if the error dialog should be displayed whenever an input violates the condition above or we just implement an error checking mechanism when the user tries to run the model. 
If we choose the second, is it possible for the error checking code to identify which field or cell (if it's in a table) has the incorrect input? 
 
The return value of the model that will be used for the result interface is vac.fn which gives the % of the population in each group to be vaccinated. 
                                                                                                     
"""
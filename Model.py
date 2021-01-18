from VACModel import VACModel
from Validation import validate

def run(model, group, n0, fn0, kmatval, h):
    validation = validate(group, n0, fn0, kmatval, h)
    if(validation['valid']):
        if(model == 'vac'):
            return {
                'status': True,
                'result': vac(group, n0, fn0, kmatval, h)
            }
        elif(model == 'vac2'):
            pass
    else:
        return {
            'status': False,
            'values': validation['values'],
            'errors': validation['errors']
        }

def vac(Group, N0, fn0, Kmatval, H):
    vm = VACModel()
    vm.Group = Group
    vm.N0 = N0
    vm.fn0= fn0
    vm.Kmatval = Kmatval
    vm.H = H
    return vm.run()
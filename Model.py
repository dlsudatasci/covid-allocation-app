from VACModel import VACModel

def vac(Group, N0, fn0, Kmatval, H):
    vm = VACModel()
    vm.Group = Group
    vm.N0 = N0
    vm.fn0= fn0
    vm.Kmatval = Kmatval
    vm.H = H
    return vm.run()
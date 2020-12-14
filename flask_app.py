from flask import Flask, request
from multiprocessing import Process, Lock, Queue
import Model as model
import json

app = Flask(__name__)

Q = Queue()

def runModel(Group,N0,fn0,Kmatval,H):
    solution = model.vac(Group,N0,fn0,Kmatval,H)
    print(solution)
    Q.put(solution)

@app.route('/', methods=['GET'])
# http://localhost:5000/?groups=[%22A%22,%22B%22]&N0=[100,200]&fn0=[0.5,0.5]&Kmatval=[0.8,0.9,0.8,0.9]&H=0.98
def vacmodel():
    Group = request.args.get('groups')
    N0 = request.args.get('N0')
    fn0 = request.args.get('fn0')
    Kmatval = request.args.get('Kmatval')
    H = request.args.get('H')
    Group = json.loads(Group) 
    N0= dict(zip(Group, json.loads(N0)))
    fn0 = {k:0.5 for k in Group}
    Kmatval = json.loads(Kmatval)
    H = float(H)
    print(type(Group))
    print(Group, N0, fn0, Kmatval, H)
    p = Process(target=runModel,args=(Group,N0,fn0,Kmatval,H))
    p.start()
    p.join()
    return json.dumps(Q.get())

if __name__ == "__main__":
    app.run()
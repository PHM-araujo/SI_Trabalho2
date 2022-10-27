from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random
import time

class Gerador(Agent):
    # randType = str(random.randint(1, 3)) + "grau"
    randType = "3grau"

    x = random.randint(-1000,1000)
    a=0
    while a == 0:
        a = random.randint(-100,100)

    if randType == "1grau":  
        b = -1 * (a*x)
    if randType == "2grau":  
        b = -1 * (a*x*x)
    #? Tem um jeito mlehor de fazer isso
    else:
        b = random.randint(-100,100)
        c = random.randint(-100,100)
   
    class funcao_1grau(CyclicBehaviour):
        async def run(self):

            # Fica esperando uma msg
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                x = float( Gerador.a*x + Gerador.b )
                print("Enviou para " + str(res.sender) + " f(",res.body,")= ",x,"=>",int(x))
                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "inform")  
                msg.body = str(int(x))
                await self.send(msg)

    class funcao_2grau(CyclicBehaviour):
        async def run(self):
            # Fica esperando uma msg
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                x = float( Gerador.a*(x*x) + Gerador.b )
                print("Enviou para " + str(res.sender) + " f(",res.body,")= ",x,"=>",int(x))
                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "inform")  
                msg.body = str(int(x))
                await self.send(msg)

    # TODO Implementar o comportamento para a função de 3 grau
    class funcao_3grau(CyclicBehaviour):
        async def run(self):
            # Fica esperando uma msg
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                x = float( Gerador.a*x + Gerador.b )
                print("Enviou para " + str(res.sender) + " f(",res.body,")= ",x,"=>",int(x))
                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "inform")  
                msg.body = str(int(x))
                await self.send(msg)
   
    class tipo_funcao(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "inform")

                msg.body = Gerador.randType

                await self.send(msg)
                print("Respondeu para " + str(msg.sender) + " com " + msg.body)
                

    async def setup(self):

        #-------Comportamento do calculo da função-------#
        t = Template()
        # Só aceita msg com performativa subscribe
        t.set_metadata("performative","subscribe")

        # Ajusta o comportanento de acordo com o tipo da função 
        if Gerador.randType == "1grau":
            tf = self.funcao_1grau()
            print("Funcao de 1o grau: ", Gerador.x)
            print("Funcao: ", Gerador.a, "x + (", Gerador.b, ")")

        if Gerador.randType == "2grau":
            tf = self.funcao_2grau()
            print("Funcao de 2o grau: +-", Gerador.x)
            print("Funcao: ", Gerador.a, "x² + (", Gerador.b, ")")

        else:
            tf = self.funcao_3grau()
            print("Funcao de 3o grau: -(", Gerador.a, "),", Gerador.b, " e ", Gerador.c)
            print("Funcao: -0.2*(x + (", Gerador.a, "))(x - (", Gerador.b, "))(x - (", Gerador.c,"))")

        # Adiciona um comportamento ao agente 
        self.add_behaviour(tf,t)

        #-------Comportamento do tipo da função-------#
        ft = self.tipo_funcao()
        template = Template()
        # Só aceita msg com performativa requets
        template.set_metadata("performative", "request")
        self.add_behaviour(ft, template)

gerador = Gerador("pedrosmas@jix.im", "sender-ufsc")
gerador.web.start(hostname="127.0.0.1", port="10000")
res = gerador.start()

res.result()

while gerador.is_alive():
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        gerador.stop()
        break
print("Agente encerrou!")
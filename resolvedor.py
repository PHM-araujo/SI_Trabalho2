from getpass import getpass
from re import template
from unittest import result
from xmlrpc.client import getparser
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random
import time
from math import sqrt, fabs

geradorID = ""

class Resolvedor(Agent):
    type = ""
    checkLixo = 1

    class AskFunctionType(OneShotBehaviour):
        async def run(self):

            #-------Pergunta o tipo da função-------#
            msg = Message(to="pedrosmas@jix.im")
            # Envia uma mensagem com a perfomativa request
            msg.set_metadata("performative", "request")
            await self.send(msg)
            print("Tipo da função?")

            #-------Escuta o tipo da função-------#
            res = await self.receive(timeout=5)

            if res:
                Resolvedor.type = res.body
                print("O tipo da função é " + str(Resolvedor.type))

            self.kill()

    class solveFuncion1grau(CyclicBehaviour):

        async def on_start(self):
            await self.agent.behav.join()  # Espera perguntar o tipo da função

            self.a = None 
            self.b = None 
            self.raiz = None
            self.counter = 0

            if Resolvedor.type != "1grau":
                self.kill()
            else: 
                print("Procurando zero da função de primeiro grau")

        async def run(self):
            chute = Message(to=geradorID)
            chute.set_metadata("performative","subscribe")

            if self.counter == 0:
                print("Enviou 0")
                chute.body = "0"
                await self.send(chute)
                
            if self.counter == 1:
                print("Enviou 1")
                chute.body = "1"
                await self.send(chute)

            if self.counter == 2: 
                print("Enviou ", self.raiz)
                chute.body = str(self.raiz)
                await self.send(chute)


            if Resolvedor.checkLixo == 1:
                lixo = await self.receive(timeout=5)
                Resolvedor.checkLixo = 0

            msgChute = await self.receive(timeout=5)

            if self.counter == 0:
                self.b = int(msgChute.body)

            if self.counter == 1:
                self.a = int(msgChute.body) - self.b
                self.raiz = -1*(self.b / self.a)

            self.counter = self.counter + 1

            if int(msgChute.body) == 0 or self.counter == 3:
                print("Achei raiz")
                self.kill()


        async def on_end(self):
            if Resolvedor.type == "1grau":
                await self.agent.stop()

    class solveFuncion2grau(CyclicBehaviour):

        async def on_start(self):
            await self.agent.behav.join()  # Espera perguntar o tipo da função

            self.a = None 
            self.b = None 
            self.raiz = None
            self.counter = 0

            if Resolvedor.type != "2grau":
                self.kill()
            else: 
                print("Procurando zero da função de segundo grau")

        async def run(self):
            chute = Message(to=geradorID)
            chute.set_metadata("performative","subscribe")  # Envia uma mensagem com a perfomativa subscribe


            if self.counter == 0:
                print("Enviei 0")
                chute.body = "0"
                await self.send(chute)
                
            if self.counter == 1:
                print("Enviei 1")
                chute.body = "1"
                await self.send(chute)

            if self.counter == 2: 
                print("Enviei ", self.raiz)
                chute.body = str(self.raiz)
                await self.send(chute)


            if Resolvedor.checkLixo == 1:
                lixo = await self.receive(timeout=5)
                Resolvedor.checkLixo = 0

            msgChute = await self.receive(timeout=5)

            if self.counter == 0:
                self.b = int(msgChute.body)

            if self.counter == 1:
                self.a = int(msgChute.body) - self.b
                self.raiz = sqrt(fabs((self.b / self.a)))

            self.counter = self.counter + 1

            if int(msgChute.body) == 0 or self.counter == 3:
                print("Achei raiz")
                self.kill()

        async def on_end(self):
            if Resolvedor.type == "2grau":
                await self.agent.stop()
    
    class solveFuncion3grau(CyclicBehaviour):
        async def on_start(self):
            await self.agent.behav.join()  # Espera perguntar o tipo da função

            self.counter = -1000

            if Resolvedor.type != "3grau":
                self.kill()
            else: 
                print("Procurando zero da função terceiro grau")

        async def run(self):
            chute = Message(to=geradorID)
            chute.set_metadata("performative","subscribe")  # Envia uma mensagem com a perfomativa subscribe
            chute.body = str(self.counter)
            print("Enviou ", self.counter)
            self.counter = self.counter + 1

            await self.send(chute)

            if Resolvedor.checkLixo == 1:
                lixo = await self.receive(timeout=5)
                Resolvedor.checkLixo = 0

            msgChute = await self.receive(timeout=5)

            if int(msgChute.body) == 0:
                print("Achei raiz")
                self.kill()

        async def on_end(self):
            if Resolvedor.type == "3grau":
                await self.agent.stop()


    async def setup(self):

        #-------Tipo da função-------#
        t = Template()
        # So recebe mensagens com performativa inform  
        t.set_metadata("performative", "inform")  
        self.behav = self.AskFunctionType()
        self.add_behaviour(self.behav, t)
        

        #-------Tenta resolver-------#
        t2 = Template()
        # So recebe mensagens com performativa inform  
        t2.set_metadata("performative", "inform")
        behav2 = self.solveFuncion1grau()
        self.add_behaviour(behav2, t2)

        t3 = Template()
        # So recebe mensagens com performativa inform  
        t3.set_metadata("performative", "inform")
        behav3 = self.solveFuncion2grau()
        self.add_behaviour(behav3, t3)

        t4 = Template()
        # So recebe mensagens com performativa inform  
        t4.set_metadata("performative", "inform")
        behav4 = self.solveFuncion3grau()
        self.add_behaviour(behav4, t4)


if __name__ == "__main__":

    geradorID = input("Conta do servidor JIX do gerador:")
    resolvedor_id = input("Conta do servidor JIX do resolvedor: ")
    passwd = getpass("Senha do resolvedor:")
    resolvedor = Resolvedor(resolvedor_id, passwd)
    resolvedor.web.start(hostname="127.0.0.1", port="10000")
    res = resolvedor.start()

    res.result()

    while resolvedor.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            resolvedor.stop()
            break
    print("Resolvedor encerrou!")
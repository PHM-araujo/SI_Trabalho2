from re import template
from unittest import result
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random
import time

class Resolvedor(Agent):
    type = ""
    checkLixo = 1

    #-------Função do primeiro grau-------#
    y = None
    a = None 

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
                type = res.body
                print("O tipo da função é " + str(type))

            self.kill()

    class solveFuncion(CyclicBehaviour):
        async def on_start(self):
            await self.agent.behav.join()  # Espera perguntar o tipo da função
            print("Começando a chutar ...")

        async def run(self):
            chute = Message(to="pedrosmas@jix.im")
            # Envia uma mensagem com a perfomativa subscribe
            chute.set_metadata("performative","subscribe")
            #! Encontrar um método númerico 
            #chute.body = str(random.randint(-1000, 1000))
            chute.body = str(-720)
            await self.send(chute)

            #? Tem um forma melhor de fazer isso
            if Resolvedor.checkLixo == 1:
                lixo = await self.receive(timeout=5)
                Resolvedor.checkLixo = 0

            msgChute = await self.receive(timeout=5)
            intChute = int(msgChute.body)

            print("O resultado do chute foi: ", intChute)
            if intChute == 0:
                print("Achei raiz")
                self.kill()

        async def on_end(self):
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
        behav2 = self.solveFuncion()
        self.add_behaviour(behav2, t2)




if __name__ == "__main__":
    resolvedor = Resolvedor("resolvedorphma@jix.im", "resolvedor-ufsc")
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
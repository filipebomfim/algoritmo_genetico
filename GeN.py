
#Importações
from random import random
from random import randint
import matplotlib.pyplot as plt
import csv

#Definição da Classe Objeto
class Objeto():
    def __init__(self,nome,peso,valor):
        self.nome = nome
        self.peso = peso
        self.valor = valor
    
    def getNome(self):
        return self.nome
    
    def getPeso(self):
        return self.peso
    
    def getValor(self):
        return self.valor

#Definição da Classe Individuo
class Individuo():
    def __init__(self,itens, limite, geracao=0):
        self.itens = itens #Lista de todos os Itens que o individuo pode carregar
        self.limite = limite #Tamanho da mochila
        self.geracao = geracao #Geração atual do indivíduo
        self.fitness = 0 #Avaliação do Indivíduo 
        self.mochilaIndividuo = 0 #Peso total carregado pelo Indivíduo
        self.cromossomo = [] #Cromossomo do indivíduo
        
        for i in range(len(itens)):
            if(random()) < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")
                
    
    #Função Heurística de Avaliação do Cromossomo                
    def avaliacao(self):
        self.fitness = 0
        self.mochilaIndividuo = 0
        for i in range(len(self.cromossomo)):
            if (self.cromossomo[i]=="1"):
                self.fitness += self.itens[i].getValor()
                self.mochilaIndividuo += self.itens[i].getPeso()        
                
        if self.mochilaIndividuo > self.limite:
           self.fitness = self.fitness * 0.001
           #self.fitness = 1
           
        
    #Função de Cruzamento de Dois Pontos        
    def cruzamento(self,segundoIndividuo):
        primeiroCorte = randint(1,4)
        segundoCorte = randint(primeiroCorte+1,8)        
        filho1 = self.cromossomo[0:primeiroCorte]+ segundoIndividuo.cromossomo[primeiroCorte:segundoCorte] + self.cromossomo[segundoCorte::] 
        filho2 = segundoIndividuo.cromossomo[0:primeiroCorte] + self.cromossomo[primeiroCorte:segundoCorte] + segundoIndividuo.cromossomo[segundoCorte::] 
        
        filhos = [Individuo(self.itens, self.limite,self.geracao+1),
                 Individuo(self.itens, self.limite,self.geracao+1)]
         
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        
        return filhos
    
    
    #Função de Mutação     
    def mutacao(self, txMutacao): #Função de Mutação
        for i in range(len(self.cromossomo)):
            if(random() < txMutacao):
                if(self.cromossomo[i]=='0'):
                    self.cromossomo[i]='1'
                else:
                    self.cromossomo[i]='0'
        return self
    

class Gen():
    def __init__(self,tamPopulacao):
        self.tamPopulacao = tamPopulacao #Tamanho da População da Geração
        fitnessTotal = 0 #Fitness Geral da População da Geração
        self.populacao = [] #Indivíduos da População da Geração
        self.geracaoPopulacao = 0 #Geração da População
        self.best = 0 #Melhor indivíduo de todas as Gerações
        self.elite = [] #Elite da População da Geração
        self.melhoresIndividuos = [] #Melhores Indivíduos de cada Geração
        self.fitnessGerais = [] #Fitness Gerais de cada Geração
        
        
    def initPopulacao(self,itens,limite): #Inicialização da população
        for i in range(self.tamPopulacao):
            self.populacao.append(Individuo(itens,limite)) 
        self.best = self.populacao[0]
        
        
    def classificarPopulacao(self): #Função de classificação dos indivíduos da população da geração      
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.fitness,
                                reverse = 1)
               
    def fitnessGen(self): #Função de calcular o fitness geral da população da geração
        self.fitnessTotal = 0
        for individuo in self.populacao:
            self.fitnessTotal += individuo.fitness
            
    def theBest(self): #Função para verificar o melhor indivíduo de todas as gerações já criadas
        if(self.populacao[0].fitness > self.best.fitness):
            self.best = self.populacao[0]
            self.best.geracao = self.geracaoPopulacao
        
    
    def selecao(self, fitnessTotal): #Função da roleta para selecionar 1 indivíduo da população
        selecionado = -1
        roleta = random() * fitnessTotal
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < roleta:
               soma += self.populacao[i].fitness
               selecionado+=1
               i+=1        
        return self.populacao[selecionado]
    
    
    def eliteGeracao(self, elitismo): #Função para selecionar os elites da população
        self.elite = list(self.populacao[0:elitismo])

    def execucao(self,txMutacao,elitismo,numGeracoes,itens,limite): #Executar o algoritmo genético
            self.initPopulacao(itens,limite) #Inicializa população inicial
            for individuo in self.populacao: #Avalia toda a população
                individuo.avaliacao()
            
            self.classificarPopulacao() #Classifica a população
            self.theBest() #Verifica o melhor indivíduo
            self.melhoresIndividuos.append(self.best.fitness) #Salva o melhor na lista de melhores indivíduos de todas as gerações
            self.fitnessGen() #Calcula o fitness geral
            self.fitnessGerais.append(self.fitnessTotal) #Salva o fitness na lista de fitness gerais de todas as gerações
            self.eliteGeracao(elitismo) #Gera os elites dessa populaçao
            
            #Laço para as próximas gerações
            for i in range(numGeracoes):
                novaPopulacao = [] #Lista para adicionar os novos indivíduos gerados
                
                for individuos_gerados in range(elitismo,self.tamPopulacao,2): #Laço para gerar os filhos
                    sel1 = self.selecao(self.fitnessTotal)#Primeiro indivíduo selecionado
                    sel2 = self.selecao(self.fitnessTotal)#Segundo indivíduo selecionado
                    
                    filhos = sel1.cruzamento(sel2)# Cruzamento entre os selecionados
                    novaPopulacao.append(filhos[0].mutacao(txMutacao))# Primeiro filho gerado a partir dos selecionados
                    novaPopulacao.append(filhos[1].mutacao(txMutacao))# Segundo filho gerado a partir dos selecionados
                    # Ao final do laço teremos uma nova população
                novaPopulacao = list(novaPopulacao + self.elite)#A nova população substitui a população da geração anterior + os melhores daquela geração      
                self.populacao = list(novaPopulacao)
    
                for individuo in self.populacao: # Cada novo indivíduo é avaliado novamente
                    individuo.avaliacao()
                
                #Repete todo o processo anterior ao laço das próximas gerações , excluindo claro o fato de já ter gerado os indivíduos
                
                self.classificarPopulacao() # A nova população também necessita de uma nova classificação do fitness (ordenar)
                self.geracaoPopulacao += 1 #Incrementa a geração da nova população
                self.theBest() # Verifica o melhor indivíduo
                self.melhoresIndividuos.append(self.best.fitness) # Lista contendo todos os melhores indíviduos já encontrados por geração
                self.fitnessGen()# Fitness total da população
                self.fitnessGerais.append(self.fitnessTotal) # Lista contendo todos os fitness totais de cada geração
                self.eliteGeracao(elitismo) # Gera os indivíduos considerados elites 
            
            self.printTheBest() # Mostra o melhor resultado encontrado após a execução de todas as gerações
                
                
    
    def printTheBest(self): #Impressão das informações do melhor Indivíduo
        print("\n\n----------------")
        print("Melhor Indivíduo: ")
        print("Cromossomo = %s" %str(self.best.cromossomo))
        print("Geração = %s" %self.best.geracao)
        print("----------------")

        print("Objetos na Mochila a serem levados:")
        for j in range(len(itens)):
            if((self.best.cromossomo[j])=='1'):
                print("Nome: %s, Preço: R$ %s, Peso: %s" %(itens[j].getNome(), itens[j].getValor(), itens[j].getPeso()))

        print("----------------")
        print(f"Valor Total na Mochila (Fitness): R$ {self.best.fitness:.2f}")
        print("Peso na Mochila: %s kg" % self.best.mochilaIndividuo)

#========================================================= Main ========================================================================
itens = [] #lista para os itens do arquivo

arquivo = open('GeN\objetos.csv') # Arquivo csv
objetos = csv.DictReader(arquivo) #leitura do arquivo

for objeto in objetos: #laço para adicionar na lista de itens os dados do arquivo
    itens.append(Objeto(objeto["nome"],float(objeto["peso"]),float(objeto["valor"])))# Passando os elementos do arquivo para uma lista
    
#----------------------------- VALORES A SE ALTERAR AQUI ---------------------------

mochila = 5   #limite máximo suportado pela mochila
tamPopulacao = 50 #Tamanho de indivíduos da população em cada geração
elitismo = 4 #Quantidade de elites da população por geração
txMutacao = 0.01 #Taxa de mutação
numGeracoes = 1000 #Quantidade de gerações a serem executadas

#-----------------------------------------------------------------------------------

ag = Gen(tamPopulacao) # Gerando população inicial
ag.execucao(txMutacao,elitismo,numGeracoes,itens,mochila) # Buscando as gerações a partir da inicial

plt.plot(ag.melhoresIndividuos) # Gerando gráfico dos melhores individuos
plt.title("Desenvolvimento dos Indivíduos")
plt.xlabel('Gerações')
plt.ylabel('Fitness dos Melhores Indivíduos')
plt.show()


input("Pressione <enter> para continuar")








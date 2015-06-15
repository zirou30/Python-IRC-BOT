from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time
  
class Minibot:
     
    def __init__(self, server, port, nick, name, email, channel):
        self.s = socket (AF_INET,SOCK_STREAM)  # cria um socket para conexao
        self.s.connect((server,port) ) #conecta no servidor e porta
        time.sleep(0.5) # espera 0.5 segundos
        self.s.recv(4096) # recebe 4kb do servidor 
         
        self.nick = nick  # atribui apelido
        self.name = name #atribui nome
        self.email = email #atribui email
         
        self.data = ''  #container dos dados vindo do servidor
        self.channel = channel #atribui canal
         
        self.command =  None
         
        self.close = False #flag de fechamento 
         
         
    def SendCommand(self, cmd):  # funcao de envio de comandos ao servidor
        comm = cmd + '\r\n' #o comando atribui \r\n (obrigatorio para o servidor responder com sucesso)
        self.s.send(comm)
     
         
    def SendPingResponse(self):  #funcao de envio de ping
         
        if self.data.find('PING') != -1:  #captura mensagem do servidor e verifica se contem PINNG
            self.SendCommand('PONG ' + self.data.split()[1]) # se tiver envia comando PONG + (numero do tempo em ms?)
            time.sleep(15) #espera 15 segundos pra enviar denovo (se tempo menor pode flooda ro server e te kikar) 
             
    def Parse(self, cmd):  #aqui voce adiciona os comandos pro bot
        tp = cmd.split(' ')
        numargs = len(tp)
        fmt = []
         
        if numargs == 0:
            self.SendCommand(cmd)
        else:
            for i in range(numargs):
                 
                fmt.append(tp[i] + ' ')
             
             
            fmt = ' '.join(fmt)
            self.SendCommand(fmt)
     
     
    def run(self):  #loop principal do bot  para manter vivo
         
        self.SendCommand('NICK ' + self.nick)  #envia pedido de nick
        self.SendCommand('USER ' + self.nick + ' ' + self.name + ' ' + self.email + ' :Irc Python') #cria uma credencial de usuario
        self.SendCommand('JOIN ' + self.channel) #entra no canal
         
        while self.close == False:
             
            self.data = self.s.recv(4096)  #data fica recebendo todos dados do servidor e guarda em data
             
            self.SendPingResponse()  #envio de ping e resposta d epong do servidor (se nao responder usuario cai)
            
            time.sleep(0.5) #espera meio segundo pra "respirar"
                     
            print self.data 
         
if __name__ == '__main__':
  
    servidor = '' #aqui digite seu servidor
    porta =  # aqui sua porta (6667)
    nick = '' #mude para seu nick
    name = '' #digite seu nome
    email =  '' #digite seu email
    canal = '#' # coloque seu canal
  
    bot = Minibot(servidor,porta, nick , name , email, canal)     #cria um bot
    bot.run() # roda o loop principal do bot

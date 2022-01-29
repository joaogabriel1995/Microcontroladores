from tkinter import *
from tkinter import ttk 
import paho.mqtt.client as mqtt


root = Tk()


class MQTT():


    def conectar_mqtt(self):
        broker = 'test.mosquitto.org'
        port = 1883
        client_id_0 = 'PC_1705'
        self.client = mqtt.Client(client_id=client_id_0)
        try:
            self.client.connect(broker, port)
            print("Conectado")
        except:
            print("Não foi possivel estabelecer conexão")
        return self.client
            

    def ligar(self):
        topic = "luminaria"
        self.cliente.publish(topic, "0")
        print("Ligou")


    def desligar(self):
        topic = "luminaria"
        self.cliente.publish(topic, "1")
        print("desligou")
   

    
         



class Aplicacao(MQTT):


    def __init__(self):
        self.root = root
        self.config_root()
        self.frames_da_tela()
        self.widgets_frame1()
        self.widgets_frame2()
        self.cliente = self.conectar_mqtt()
        root.mainloop()
    
    def config_root(self):
        self.root.title("Central de Controle")
        self.root.geometry("300x200")
        self.root.resizable(False,False)


    def frames_da_tela(self):
        self.frame1 = Frame(root, bd=4, bg="#dfe3ee")
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        self.frame2 = Frame(self.frame1, bd=4, bg="#dfe3ee")
        self.frame2.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.4)

    def widgets_frame1(self):
        self.label = Label(self.frame1, text="Luminária", bg="#dfe3ee")
        self.label.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.1)


    def widgets_frame2(self):
        self.botao_ligar = Button(self.frame2, text="Ligar", command=self.ligar)
        self.botao_ligar.pack(side="top", fill="x", expand=True)
        self.botao_desligar = Button(self.frame2, text="Desligar", command=self.desligar)
        self.botao_desligar.pack(side="top", fill="x", expand=True)
        










if __name__ == "__main__":
    Aplicacao()
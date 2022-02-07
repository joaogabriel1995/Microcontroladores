
from email import message
from tkinter import *
from tkinter import ttk
from matplotlib import animation
from matplotlib.figure import Figure 
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import random
import matplotlib
import paho.mqtt.client as mqtt

matplotlib.use("TkAgg")


root = Tk()
rect = [0.1,0.1,0.8,0.8]
figura = Figure(figsize=(10,6), dpi=100)
axes = Axes(figura, rect=rect)
figura.add_axes(axes)



class MQTT():
    def __init__(self):
        self.y = []
        self.conectar_mqtt()
        self.subscribe()



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

    def subscribe(self):
        def on_message(client, userdate, mensagem):
            #print("Mensagem Recebida: ", str(mensagem.payload.decode("utf-8")))
            self.y.append(int(mensagem.payload.decode("utf-8")))

        self.client.subscribe("ESP32")
        self.client.on_message = on_message
        self.x = [i for i in range(len(self.y))]





class Grafico(MQTT):

    def __init__(self, frame, figura, axes):
        self.mqtt = MQTT()
        self.figura = figura
        self.axes = axes
        self.figura.add_axes(self.axes)
        canvas = FigureCanvasTkAgg(self.figura, frame)
        canvas.get_tk_widget().pack(side="top")
        canvas.draw()
        self.config_graf()
        


    def config_graf(self):
        self.axes.set_title("João")
        self.axes.set_xlabel("Label x")
        self.axes.set_ylabel("Label y")


    def animate(self, i):
        self.axes.clear()
        self.axes.set_title("João")
        self.axes.set_xlabel("Label x")
        self.axes.set_ylabel("Label y")
        self.axes.plot(self.mqtt.y)



class App_grafico(Grafico):


    def __init__(self, figura, axes):
    
        self.root = root
        self.configuracao_tela()
        self.grafico = Grafico(self.root, figura, axes)
        mqtt = self.grafico.mqtt
        mqtt.subscribe()
        ani = animation.FuncAnimation(figura, self.grafico.animate, interval=500)
        mqtt.client.loop_start()
        self.root.mainloop()
        mqtt.client.loop_stop()

    
    def configuracao_tela(self):
        self.root.title("Gráfico em tempo Real")
        self.root.geometry("700x500")
        self.root.resizable(False, False)





if __name__ =="__main__":
    App_grafico(figura, axes)

    







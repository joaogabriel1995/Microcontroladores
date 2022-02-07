from tkinter import *
from tkinter import ttk
import paho.mqtt.client as mqtt
from PIL import ImageTk,Image 
from tkinter import ttk

root = Tk()


class MQTT():
    

    def __init__(self):
        self.conectar_mqtt()
        self.temp = ["0"]
        self.umid = ["0"]


    def conectar_mqtt(self):

        broker = "broker.hivemq.com"
        port = 1883
        client_id_0 = 'PC_1705'
        self.client = mqtt.Client(client_id=client_id_0)
        
        try:
            self.client.connect(broker, port)
            print("Conectado")
        except:
            print("Não foi possivel estabelecer conexão")
        return self.client
    
    def subscribe(self, client):

        def on_message(client, userdate, mensagem):

            self.y =str(mensagem.payload.decode("utf-8"))
            temp_valor = "{:.0f}".format(float(self.y[12:21]))
            umid_valor = "{:.0f}".format(float(self.y[31:]))
            self.temp.pop(0)
            self.umid.pop(0)
            self.temp.insert(0, temp_valor)
            self.umid.insert(0, umid_valor)
            print(self.temp, self.umid)
            temp_var.set(self.temp[0] + "°C")
            umidade_var.set(self.umid[0] + "%")
            

            

        self.client.subscribe("temperatura_esp32")
        self.client.on_message = on_message
        



    def ligar(self):
        topic = "luminaria"
        self.client.publish(topic, "0")
        print("Ligou")

    def desligar(self):
        topic = "luminaria"
        self.client.publish(topic, "1")
        print("desligou")
   
   
class CentralControle(MQTT):


    def __init__(self, cliente):
        self.root = root
        self.config_tela()
        self.frames_da_tela()
        self.canvas_tela()
        self.canvas_1()
        self.canvas_2()
        self.canvas_3()
        self.botao_on()
        self.cliente = cliente
        self.cliente.subscribe(self.cliente)
        self.temperatura()
        self.umidade()
        self.estado_lamp = False
        self.cliente.client.loop_start()
        self.root.mainloop()
        self.cliente.client.loop_stop()


    def config_tela(self):
        self.root.title("Central de Controle") 
        self.root.resizable(False, False)
        self.root.geometry("395x600")   

    def frames_da_tela(self):
        self.container_frames = Frame(root, bg="#dcdcdc")
        self.container_frames.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
    
    def canvas_tela(self):
        self.canvas1 = Canvas(self.container_frames, bg="#dcdcdc")
        self.canvas1.place(x=0,y=0, width=385, height=100)
        self.canvas2 = Canvas(self.container_frames, bg="#dcdcdc")
        self.canvas2.place(x=20,y=240, width=100, height=100)
        self.canvas3 = Canvas(self.container_frames, bg="#dcdcdc")
        self.canvas3.place(x=20,y=360, width=100, height=100)
        
    def canvas_1(self):
        self.canvas1.background = ImageTk.PhotoImage(Image.open("smarthome.png" ))  
        self.canvas1.create_image(395/2,40, image=self.canvas1.background, anchor=CENTER)
        self.canvas1.create_text(395/2,75, text="SMART HOME", font=('Helvetica 10 bold'))

    def canvas_2(self):
        self.canvas2.background = ImageTk.PhotoImage(Image.open("temperatura.png"))
        self.canvas2.create_image(50,50, image=self.canvas2.background, anchor=CENTER)

    def canvas_3(self):
        self.canvas3.background = ImageTk.PhotoImage(Image.open("umidade.png"))
        self.canvas3.create_image(50,50, image=self.canvas3.background, anchor=CENTER)



    def botao_on(self):
        self.luz_off = ImageTk.PhotoImage(Image.open("luz on 2.png"))
        self.luz_on = ImageTk.PhotoImage(Image.open("luz off.png"))
        self.botao_ligar = Button(self.container_frames,text = 'Ligar', image=self.luz_off, bd=0, compound="top", command=self.interruptor, borderwidth=0, bg="#dcdcdc")
        self.botao_ligar.image = self.luz_off
        self.botao_ligar.place(x=20, y=120, width=100, height=100)
        self.botao_var = StringVar()
        self.label_botao = Label(self.container_frames, textvariable = self.botao_var, font=('Helvetica 12 bold'), bg="#dcdcdc")
        self.label_botao.place(x=240, y=160, anchor=CENTER)
    

    def temperatura(self):
        global temp_var
        temp_var = StringVar()
        self.label_temp = Label(self.container_frames, textvariable = temp_var, font=('Helvetica 32 bold'), bg="#dcdcdc", text="  °C")
        temp_var.set(cliente.temp[0] + "°C")
        self.label_temp.place(x=240 , y=290, anchor=CENTER)
        
    def umidade(self):
        global umidade_var
        umidade_var = StringVar()
        self.label_umidade = Label(self.container_frames, textvariable = umidade_var, font=('Helvetica 32 bold'), bg="#dcdcdc", text="  %")
        umidade_var.set(self.cliente.temp[-1] + "%")
        self.label_umidade.place(x=240 , y=410, anchor=CENTER)



    def interruptor(self):
        if self.estado_lamp == False:
            self.botao_ligar.config(image=self.luz_on, text="Ligar")
            self.estado_lamp = True
            self.cliente.ligar()
            self.botao_var.set("Luz está Desligada!")
        else:
            self.botao_ligar.config(image=self.luz_off, text="Desligar")
            self.estado_lamp = False
            self.cliente.desligar()
            self.botao_var.set("Luz está Ligar!")



if __name__ == "__main__":
    cliente = MQTT()
    print(cliente.temp)
    CentralControle(cliente)
    


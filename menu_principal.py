import os
import random
import smtplib
import datetime
import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def verManual():
   os.system("src\\files\\manual.pdf")

TITULO = "ReviTec by Katerine"
ANCHO, ALTO = 1000, 650

#Variables con los colores para poder utilizarlos o modificarlos mas facilmente
COLOR1 = '#0b725f'
COLOR2 = 'white'
COLOR3 = '#f0bd88'
COLOR_FALLA = 'red'
TEXT_COLOR = 'black'

#Variable global para guardar en un diccionario las citas
citas = []
fallas = {}
tablero = []
tableroFallas = [[[], [], [], [], []],
                 [[], [], [], [], []],
                 [[], [], [], [], []],
                 [[], [], [], [], []],
                 [[], [], [], [], []],
                 [[], [], [], [], []]]
colaEspera = [[],
              [],
              [],
              [],
              [],
              []]

archivoCitas = ".\\src\\files\\citas.dat"
archivoFallas = ".\\src\\files\\listaFallas.dat"


def guardar(nombreArchivo, datos):
    # Se abre el archivo en modo escritura de bytes
    archivo = open(nombreArchivo, 'wb')
    # Se escribe la informacion en bytes
    archivo.write(str(datos).encode())
    # Se cierra el archivo
    archivo.close()             

def cargar(nombreArchivo, tipo):
    # Se abre el archivo en modo lectura de bytes
    archivo = open(nombreArchivo, 'rb')
    info = archivo.read()
    archivo.close()
    # Si no hay datos me devuelve el tipo de dato especificado como vacio
    if info == b'':
        return tipo()
    else:
        # Se decodifica en formato del abecedario normal 
        # Si no se transforma al tipo de dato original
        return eval(info.decode('utf-8'))

def existeFalla(falla):
    global fallas
    return falla in fallas

def estaEnRevision(cita):
    global tablero
    # tablero = tablero de revision
    # linea = linea de revision (puesto1, puesto2,..., puesto5)
    for linea in tablero:
        if cita in linea:
            return True
    return False

def estaEnRevisionPlaca(numeroPlaca):
    global tablero
    # tablero = tablero de revision
    # linea = linea de revision (puesto1, puesto2,..., puesto5)
    posLinea = 0
    for linea in tablero:
        posPuesto = 0
        for puesto in linea:
            if numeroPlaca == puesto['numeroPlaca']:
                return posLinea, posPuesto
            posPuesto += 1
        posLinea += 1
    return -1, -1

def estaEnColaEspera(cita):
    global colaEspera
    for cola in colaEspera:
        if cita in cola:
            return True
    return False

def hayFallaGrave(fallas):
    for falla in fallas:
        if falla[2] == "G":
            return True
    else:
        return False

# Se verifica cual cola tiene menos vehiculos para ingresar al nuevo
def obtenerColaMenor():
    largoColas = []
    # Saca el largo de cada cola de espera
    for cola in colaEspera:
        largoColas.append(len(cola))
    menor = min(largoColas)
    # Me devuele la fila con menos carros
    return largoColas.index(menor)

def crearTablero(filas, columnas):
    tablero = []
    # Me crea las filas
    for _ in range(filas):
        fila = []
        # Agrega comillas al tablero
        for _ in range(columnas):
            fila.append({'numeroPlaca': '', 'fallas': []})
        tablero.append(fila)
    return tablero

# Cuando empieza a correr el programa se llama la funcion de cargar
# citas, se carga la informacion y se se guarda en la variable citas
citas = cargar(archivoCitas, list)
fallas = cargar(archivoFallas, dict)
print(citas)
tablero = crearTablero(6, 5)
tablero[0][0] = citas[0]

# Crea la ventana principal y se configura
ventanaMenuPrincipal = tk.Tk()
anchoPantalla = ventanaMenuPrincipal.winfo_screenwidth()
altoPantalla = ventanaMenuPrincipal.winfo_screenheight()

POS_X = int((anchoPantalla / 2) - (ANCHO / 2))
POS_Y = int((altoPantalla / 2) - (ALTO / 2))

ventanaMenuPrincipal.title(TITULO)
ventanaMenuPrincipal.geometry("{}x{}+{}+{}".format(ANCHO, ALTO, POS_X, POS_Y)) 
ventanaMenuPrincipal.resizable(width=False, height=False)
ventanaMenuPrincipal.config(bg=COLOR1)

lblTitulo = tk.Label(ventanaMenuPrincipal, text="Menu Principal", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 24))
lblTitulo.place(x=ANCHO//2, y=30, anchor="center")

imagen = tk.PhotoImage(file="src\\imgs\\imagencarro.png")
fondo = tk.Label(ventanaMenuPrincipal, bg=COLOR1, image=imagen)
fondo.config(image=imagen)
fondo.place(x=250, y=50)


def enviarCorreo(to, subject, text):
    enviado = True
    # Gmail Sign In
    gmail_sender = 'guzka97@gmail.com'
    gmail_passwd = 'Happiness.97'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % to,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % subject,
                        '', text])

    try:
        server.sendmail(gmail_sender, [to], BODY)
        messagebox.showinfo("Envio de correo", "Correo enviado exitosamente")
    except:
        enviado = False
        messagebox.showerror("Envio de correo", "El correo no pudo enviarse")

    server.quit()
    return enviado

def salir():
    ventanaMenuPrincipal.destroy()
    
#Crea ventana acerca de y la configura
def acercaDe():
    ventanaMenuPrincipal.withdraw()
    ventanaAcercaDe = tk.Toplevel()
    ventanaAcercaDe.title (TITULO)
    ventanaAcercaDe.geometry ("{}x{}+{}+{}".format(ANCHO, ALTO, POS_X, POS_Y))

    ventanaAcercaDe.resizable(width=False, height=False)
    ventanaAcercaDe.config(bg=COLOR1)
   
    lblnombrePrograma=tk.Label(ventanaAcercaDe, text="Revision Tecnica de Vehiculos (ReviTec)", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 24))
    lblnombrePrograma.place(x=ANCHO//2, y=100, anchor="center")

    lblversion=tk.Label(ventanaAcercaDe, text="version v1.0.0", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 24))
    lblversion.place(x=ANCHO//2, y=175, anchor="center")

    lblfecha=tk.Label(ventanaAcercaDe, text="30/10/2019", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 24))
    lblfecha.place(x=ANCHO//2, y=250, anchor="center")

    lblautora=tk.Label(ventanaAcercaDe, text="Katerine Guzman Flores", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 24))
    lblautora.place(x=ANCHO//2, y=325, anchor="center")

    def regresar():
        ventanaMenuPrincipal.deiconify()
        ventanaAcercaDe.destroy()

    btnRegresar=tk.Button(ventanaAcercaDe, text= "   Regresar   ",
                            bg=COLOR3, fg=TEXT_COLOR,
                            font=("Ubunto Monospace", 12),
                            activebackground=COLOR3,
                            activeforeground=TEXT_COLOR,
                            command=regresar)
    btnRegresar.place(x=800, y=580)
    
#Creacion de botones en pantalla principal y la configuracion de los mismos
btnAyuda=tk.Button(ventanaMenuPrincipal, text= "                Ayuda                 ",
                            bg=COLOR3, fg=TEXT_COLOR,
                            font=("Ubunto Monospace", 12),
                            activebackground=COLOR3,
                            activeforeground=TEXT_COLOR,
                            command=verManual)
btnAyuda.place(x=130, y=580)

btnAcercaDe=tk.Button(ventanaMenuPrincipal, text= "              Acerca de              ",
                            bg=COLOR3, fg=TEXT_COLOR,
                            font=("Ubunto Monospace", 12),
                            activebackground=COLOR3,
                            activeforeground=TEXT_COLOR,
                            command=acercaDe)
btnAcercaDe.place(x=385, y=580)

btnSalir=tk.Button(ventanaMenuPrincipal, text= "                    Salir                   ",
                            bg=COLOR3, fg=TEXT_COLOR,
                            font=("Ubunto Monospace", 12),
                            activebackground=COLOR3,
                            activeforeground=TEXT_COLOR,
                            command=salir)
btnSalir.place(x=650, y=580)

# _________________                PROGRAMAR CITAS        _____________________  #
def ventanaProgramarCitas():
    ventanaMenuPrincipal.withdraw()
    #Crea ventana de programar citas
    ventanaProgramarCita = tk.Tk()
    anchoPantalla = ventanaProgramarCita.winfo_screenwidth()
    altoPantalla = ventanaProgramarCita.winfo_screenheight()

    #Configuracion de ventana programar citas
    POS_X = int((anchoPantalla / 2) - (ANCHO / 2))
    POS_Y = int((altoPantalla / 2) - (ALTO / 2))

    ventanaProgramarCita.title(TITULO)
    ventanaProgramarCita.geometry("{}x{}+{}+{}".format(ANCHO, ALTO, POS_X, POS_Y)) 
    ventanaProgramarCita.resizable(width=False, height=False)
    ventanaProgramarCita.config(bg=COLOR1)

    #Crea los labels en la ventana programar cita
    lblTitulo = tk.Label(ventanaProgramarCita, text="Programar citas", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 18))
    lblTitulo.place(x=ANCHO//2, y=20, anchor="center")

    lblNumeroCita = tk.Label(ventanaProgramarCita, text="Numero de Cita:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblNumeroCita.place(x=20, y=70)

    lblDireccionFisica = tk.Label(ventanaProgramarCita, text="Direccion Fisica:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblDireccionFisica.place(x=20, y=150)

    lblNumeroPlaca = tk.Label(ventanaProgramarCita, text="Numero de Placa:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblNumeroPlaca.place(x=20, y=230)

    lblMarcaVehiculo = tk.Label(ventanaProgramarCita, text="Marca del Vehiculo:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblMarcaVehiculo.place(x=20, y=310)

    lblModelo = tk.Label(ventanaProgramarCita, text="Modelo:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblModelo.place(x=20, y=390)

    lblPropietario = tk.Label(ventanaProgramarCita, text="Propietario:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblPropietario.place(x=20, y=470)

    lblTelefono = tk.Label(ventanaProgramarCita, text="Telefono:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblTelefono.place(x=20, y=550)

    lblCorreoElectronico = tk.Label(ventanaProgramarCita, text="Correo Electronico:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblCorreoElectronico.place(x=500, y=70)

    lblTipoCita = tk.Label(ventanaProgramarCita, text="Tipo de cita:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblTipoCita.place(x=500, y=150)

    lblFechaCita = tk.Label(ventanaProgramarCita, text="Fecha de la cita:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblFechaCita.place(x=500, y=230)

    lblHoraCita = tk.Label(ventanaProgramarCita, text="Hora de la cita:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblHoraCita.place(x=500, y=300)

    entryNumeroCita = tk.Entry(ventanaProgramarCita, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryNumeroCita.place(x=250, y=70)

    entryDireccionFisica = tk.Text(ventanaProgramarCita, bd=2, height=2, width=20, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryDireccionFisica.place(x=250, y=150)

    entryNumeroPlaca = tk.Entry(ventanaProgramarCita, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryNumeroPlaca.place(x=250, y=230)

    entryMarcaVehiculo = tk.Entry(ventanaProgramarCita, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryMarcaVehiculo.place(x=250, y=310)

    entryModelo = tk.Entry(ventanaProgramarCita, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryModelo.place(x=250, y=390)

    entryPropietario = tk.Text(ventanaProgramarCita, bd=2, height=2, width=20, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryPropietario.place(x=250, y=470)

    entryTelefono = tk.Entry(ventanaProgramarCita, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryTelefono.place(x=250, y=550)

    entryCorreoElectronico = tk.Entry(ventanaProgramarCita, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryCorreoElectronico.place(x=750, y=70)

    entryTipoCita = tk.Entry(ventanaProgramarCita, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryTipoCita.place(x=750, y=150)

    entryFechaCita = tk.Entry(ventanaProgramarCita, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryFechaCita.place(x=750, y=230)

    entryHoraCita = tk.Entry(ventanaProgramarCita, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryHoraCita.place(x=750, y=300)

    def esNumeroCitaValida(numeroCita):
        global citas
        # Si el numero de cita ya esta ccomo llave de mi diccionario retorna falso porque es invalida
        for cita in citas:
            if cita['numeroCita'] == numeroCita:
                return False
        return True
    
    #Verifica si existen mas de 7 citas en una misma hora con un contador
    def esCitasRepetida(fechaCita, horaCita):
        global citas
        repetidas = 0

        for cita in citas:
            #Cada vez que encuentra una fecha con una hora suma al contador
            if cita['fechaCita'] == fechaCita and cita['horaCita'] == horaCita:
                repetidas += 1
        #    
        return repetidas < 6

    def hayCarroMismoDia(fechaCita, numeroPlaca, tipoCita):
        global citas
        citasCarro = 1 
        for cita in citas:
            if cita['numeroPlaca'] == numeroPlaca and cita['fechaCita'] == fechaCita and tipoCita ==0:
                citasCarro += 1   
        return citasCarro < 2

    def esFormatoFechaValida(date):
        try:
            date_str = '{}-{}-{}'.format(date[4:], date[2:4], date[:2])
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
        
    def esFechaValida(fecha, hora):
        ahora = datetime.datetime.now()
        #Para saber mi hora actual
        horaActual = ahora.hour * 100 + ahora.minute
        anioActual = ahora.year
        diaActual = ahora.day 
        mesActual = ahora.month
        anioIngresado = fecha%10000
        mesIngresado = (fecha//10000)%100
        diaIngresado = fecha//1000000

        if anioIngresado > anioActual:
            return True
        elif anioIngresado < anioActual:
            return False
        else:
            if mesIngresado > mesActual:
                return True
            elif mesIngresado < mesActual:
                return False
            else:
                if diaIngresado > diaActual:
                    return True
                elif diaIngresado < diaActual:
                    return False
                else:
                    if hora > horaActual and 2200 > hora >= 600:
                        return True
                    else:
                        return False
       
    def validarCita():
        global citas
        numeroCita = entryNumeroCita.get()
        direccionFisica = entryDireccionFisica.get("1.0",'end-1c')
        numeroPlaca = entryNumeroPlaca.get() 
        marcaVehiculo = entryMarcaVehiculo.get() 
        modelo = entryModelo.get()
        propietario = entryPropietario.get("1.0",'end-1c')
        telefono = entryTelefono.get()
        correoElectronico = entryCorreoElectronico.get()
        tipoCita = entryTipoCita.get()
        fechaCita = entryFechaCita.get()
        horaCita = entryHoraCita.get()

        if numeroCita == '':
            messagebox.showerror("Numero de Cita", "Debe ingresar un numero de cita")
        elif direccionFisica == '':
            messagebox.showerror("Direccion Fisica", "Debe ingresar un numero de direccion")
        elif numeroPlaca == '':
            messagebox.showerror("Numero de Placa", "Debe ingresar un numero de placa")
        elif marcaVehiculo == '':
            messagebox.showerror("Marca del Vehiculo", "Debe ingresar un numero de marca del vehiculo")
        elif modelo == '':
            messagebox.showerror("Modelo", "Debe ingresar un numero de modelo")
        elif propietario == '':
            messagebox.showerror("Propietario", "Debe ingresar un nombre de Propietario")
        elif telefono == '':
            messagebox.showerror("Telefono", "Debe ingresar un numero de telefono")
        elif correoElectronico == '':
            messagebox.showerror("Correo Electronico", "Debe ingresar un correo electronico")
        elif tipoCita == '':
            messagebox.showerror("Tipo de Cita", "Debe ingresar un tipo de cita")
        elif fechaCita == '':
            messagebox.showerror("Fecha de Cita", "Debe ingresar una fecha")
        elif horaCita == '':
            messagebox.showerror("Hora de Cita", "Debe ingresar una hora")
        else:
            if not numeroCita.isnumeric():
                messagebox.showerror("Numero de Cita", "Debe ingresar un numero")
            elif not telefono.isnumeric():
                messagebox.showerror("Numero de Telefono", "Debe ingresar un numero")
            elif not tipoCita.isnumeric():
                messagebox.showerror("Tipo de Cita", "Debe ingresar un numero")
            elif not fechaCita.isnumeric():
                messagebox.showerror("Fecha de Cita", "Debe ingresar un numero")
            elif not horaCita.isnumeric():
                messagebox.showerror("Hora de Cita", "Debe ingresar un numero")
            elif len(horaCita) != 4:
                messagebox.showerror("Hora de Cita", "La hora de la cita debe contener 4 caracteres")
            else:
                numeroCita = int(numeroCita)
                telefono = int(telefono)
                tipoCita = int(tipoCita)
                horaCita = int(horaCita)
                
                if numeroCita < 0:
                    messagebox.showerror("Numero de Cita", "Debe ingresar un numero mayor que cero")
                elif not 0<=tipoCita<4:
                    messagebox.showerror("Tipo de Cita", "Debe ingresar un numero de 0 a 3")
                elif not (len(numeroPlaca) == 6):
                    messagebox.showerror("Numero de Placa", "El numero de placa debe contener 6 caracteres")
                elif not ((numeroPlaca[:3].isalpha() and numeroPlaca[3:].isnumeric() and numeroPlaca[:3].isupper()) or numeroPlaca.isnumeric()):
                    messagebox.showerror("Numero de Placa", "Debe ingresar una placa de seis numeros o tres letras mayusculas y tres numeros (VTH070)")
                elif len(marcaVehiculo) > 15:
                    messagebox.showerror("Marca del Vehiculo", "La marca del vehiculo no puede contener mas de 15 caracteres")
                elif len(modelo) > 15:
                    messagebox.showerror("Modelo del Vehiculo", "El modelo del vehiculo no puede contener mas de 15 caracteres")
                elif len(propietario) > 40:
                    messagebox.showerror("Nombre de Propietario", "El nombre del propietario no puede contener mas de 40 caracteres")
                elif len(direccionFisica) > 40:
                    messagebox.showerror("Direccion Fisica ", "La direccion debe contener menos de 40 caracteres")
                elif not esFormatoFechaValida(fechaCita):
                    messagebox.showerror("Fecha Cita", "La fecha es invalida. Verifique el formato -ddmmaaaa-")
                elif not(60 > (horaCita%100) >= 0 and 24 > (horaCita//100) >= 0):
                    messagebox.showerror("Hora Cita", "La hora es invalida. Verifique el formato -hhmm-")
                elif not (horaCita%100 == 0 or horaCita%100 == 20 or horaCita%100 == 40):
                    messagebox.showerror("Hora Cita", "La hora es invalida, las citas se programan cada 20 minutos")
                elif not esNumeroCitaValida(numeroCita):
                    messagebox.showerror("Numero Cita", "El numero de cita ya existe")
                elif not esCitasRepetida(fechaCita, horaCita):
                    messagebox.showerror("Numero Cita", "No pueden exister mas de seis citas en un mismo dia")
                elif not hayCarroMismoDia(fechaCita, numeroPlaca, tipoCita):
                    messagebox.showerror("Numero Cita", "Un vehiculo que ingresa por primera vez no puede tener dos citas en el mismo dia")
                elif not esFechaValida(int(fechaCita), horaCita):
                    messagebox.showerror("Fecha/Hora Cita", "La fecha u hora ingresada es menor a la actual")
                else:
                    cita = {}
                    cita['numeroCita'] = numeroCita
                    cita['tipoCita'] = tipoCita 
                    cita['direccionFisica']= direccionFisica
                    cita['numeroPlaca'] = numeroPlaca
                    cita['marcaVehiculo'] = marcaVehiculo
                    cita['modelo'] = modelo
                    cita['propietario'] = propietario
                    cita['telefono'] = telefono
                    cita['correoElectronico'] = correoElectronico
                    cita['fechaCita'] = fechaCita
                    cita['horaCita'] = horaCita
                    cita['estado'] = 'Pendiente'
                    cita['fallas'] = []
                    citas.append(cita)
                    
                    guardar(archivoCitas, citas)
                    
                    SUBJECT = 'Correo de confirmacion de cita'
                    TEXT = 'Su cita ha sido agendada\n' + \
                           'Numero de Cita: {} \n' + \
                           'Fecha: {} \n' + \
                           'Hora: {} \n' + \
                           'Tipo de Cita: {} \n' + \
                           'Direccion Fisica: {} \n' + \
                           'Marca del Vehiculo: {} \n' + \
                           'Modelo: {} \n' + \
                           'Propietario: {} \n' + \
                           'Telefono: {}\n' + \
                           'Numero de Placa: {}'
                    TEXT = TEXT.format(numeroCita, fechaCita, horaCita, tipoCita,
                                direccionFisica, marcaVehiculo, modelo,
                                propietario, telefono, numeroPlaca)
                    enviarCorreo(correoElectronico, SUBJECT, TEXT)
                    ventanaProgramarCita.destroy()
                    ventanaMenuPrincipal.deiconify()
    
    def generarFechaHora():
        ahora = datetime.datetime.now()
        
        horaCita = 600
        anioActual = ahora.year
        diaActual = ahora.day + 1
        mesActual = ahora.month
        
        fechaCita = str(int(diaActual*10e5 + mesActual*10e3 + anioActual))
        if len(fechaCita) == 7:
            fechaCita = '0' + fechaCita
        
        while not esCitasRepetida(fechaCita, horaCita):
            horaCita += 20
            if horaCita % 100 == 60:
                horaCita = (horaCita//100 + 1)*100
            if horaCita//100 == 24:
                fechaCita = int(fechaCita) + 1
                fechaCita = str(fechaCita)
                horaCita = 600

        horaCita = str(horaCita)
        if len(horaCita) == 3:
            horaCita = '0' + horaCita
        
        entryFechaCita.delete(0, tk.END)
        entryFechaCita.insert(0, fechaCita)
        entryHoraCita.delete(0, tk.END)
        entryHoraCita.insert(0, horaCita)
                   
    btnConfirmar=tk.Button(ventanaProgramarCita, text= "   Confirmar   ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command=validarCita)
    btnConfirmar.place(x=820, y=550)

    btnCitaAutomatica=tk.Button(ventanaProgramarCita, text= "   Generar hora y fecha   ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command=generarFechaHora)
    btnCitaAutomatica.place(x=750, y=400)

    
    #Destruye la ventana de citas y se abre la de menu principal
    def regresar():
        ventanaProgramarCita.destroy()
        ventanaMenuPrincipal.deiconify()
        
    btnRegresar=tk.Button(ventanaProgramarCita, text= "   Regresar   ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command=regresar)
    btnRegresar.place(x=500, y=550)

btnProgramarCitas=tk.Button(ventanaMenuPrincipal, text= "        Programar Citas       ",
                            bg=COLOR3, fg=TEXT_COLOR,
                            font=("Ubunto Monospace", 12),
                            activebackground=COLOR3,
                            activeforeground=TEXT_COLOR,
                            command=ventanaProgramarCitas)
btnProgramarCitas.place(x=130, y=420)

def coincideCitaPlaca(numeroCita, numeroPlaca):
    global citas
    for cita in citas:
        if cita['numeroCita'] == numeroCita and cita['numeroPlaca'] == numeroPlaca:
            return True, cita
    return False, None
# _____________          VENTANA CANCELAR _________________________#
def cancelarCitas():
    global citas
    ventanaMenuPrincipal.withdraw()
    ventanaCancelarCita = tk.Tk()
    anchoPantalla = ventanaCancelarCita.winfo_screenwidth()
    altoPantalla = ventanaCancelarCita.winfo_screenheight()

    POS_X = int((anchoPantalla / 2) - (ANCHO / 2))
    POS_Y = int((altoPantalla / 2) - (ALTO / 2))
        
    ventanaCancelarCita.title(TITULO)
    ventanaCancelarCita.geometry("{}x{}+{}+{}".format(ANCHO, ALTO, POS_X, POS_Y)) 
    ventanaCancelarCita.resizable(width=False, height=False)
    ventanaCancelarCita.config(bg=COLOR1)

    lblTitulo = tk.Label(ventanaCancelarCita, text="Cancelar citas", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 18))
    lblTitulo.place(x=ANCHO//2, y=40, anchor="center")

    lblNumeroCita = tk.Label(ventanaCancelarCita, text="Numero de Cita:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblNumeroCita.place(x=100, y=150)

    lblNumeroPlaca = tk.Label(ventanaCancelarCita, text="Numero de Placa:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblNumeroPlaca.place(x=100, y=300)

    entryNumeroCita = tk.Entry(ventanaCancelarCita, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryNumeroCita.place(x=350, y=150)

    entryNumeroPlaca = tk.Entry(ventanaCancelarCita, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryNumeroPlaca.place(x=350, y=300)

    def validarCancelarCita():
        global citas
        numeroCita = entryNumeroCita.get()
        numeroPlaca = entryNumeroPlaca.get()

        if numeroCita == '':
            messagebox.showerror("Numero de Cita", "Debe ingresar un numero de cita")
        elif numeroPlaca == '':
            messagebox.showerror("Numero de Placa", "Debe ingresar un numero de placa")
        else:
            coincide, cita = coincideCitaPlaca(numeroCita, numeroPlaca)
            if not numeroCita.isnumeric():
                messagebox.showerror("Numero de Cita", "Debe ingresar un numero")
            else:
                numeroCita = int(numeroCita)
                if numeroCita < 0:
                    messagebox.showerror("Numero de Cita", "Debe ingresar un numero mayor que cero")
                elif not ((numeroPlaca[:3].isalpha() and numeroPlaca[3:].isnumeric() and numeroPlaca[:3].isupper()) or numeroPlaca.isnumeric()):
                    messagebox.showerror("Numero de Placa", "Debe ingresar una placa de seis numeros o tres letras y tres numeros (VTH070)")
                elif not coincide:
                    messagebox.showerror("Cancelar Cita", "El numero de cita debe coincidir con el numero de placa del vehiculo")
                elif estaEnRevision(cita):
                    messagebox.showerror("Cancelar Cita", "El vehiculo se encuentra en revision")
                elif cita["estado"] == "CITA CANCELADA":
                    messagebox.showerror("Cancelar Cita", "La cita ya fue cancelada")
                elif cita["estado"] == "REVISION CANCELADA":
                    messagebox.showerror("Ingresar Vehiculo", "La revision fue cancelada")
                else:
                    MsgBox = messagebox.askquestion("Cancelación","¿Esta seguro que desea cancelar la cita?", icon="warning")
                    if MsgBox == "yes":
                        indiceCita = citas.index(cita)
                        cita["estado"] = "CITA CANCELADA"
                        citas[indiceCita] = cita
                        
                        guardar(archivoCitas, citas)
                        ventanaCancelarCita.destroy()
                        ventanaMenuPrincipal.deiconify()
    def regresar():
        ventanaCancelarCita.destroy()
        ventanaMenuPrincipal.deiconify()

    btnRegresar=tk.Button(ventanaCancelarCita, text= "   Regresar   ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command=regresar)
    btnRegresar.place(x=650, y=500)  

    btnConfirmar=tk.Button(ventanaCancelarCita, text= "   Confirmar   ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command=validarCancelarCita)
    btnConfirmar.place(x=100, y=500)

btnCancelarCitas=tk.Button(ventanaMenuPrincipal, text= "         Cancelar Citas         ",
                            bg=COLOR3, fg=TEXT_COLOR,
                            font=("Ubunto Monospace", 12),
                            activebackground=COLOR3,
                            activeforeground=TEXT_COLOR,
                            command=cancelarCitas)
btnCancelarCitas.place(x=130, y=500)

# ___________________________ Ingreso Vehiculo__________________________________#
def ingresoVehiculo():
    ventanaMenuPrincipal.withdraw()

    ventanaIngresoVehiculo = tk.Toplevel()
    ventanaIngresoVehiculo.title(TITULO)
    ventanaIngresoVehiculo.geometry("{}x{}+{}+{}".format(ANCHO, ALTO, POS_X, POS_Y)) 
    ventanaIngresoVehiculo.resizable(width=False, height=False)
    ventanaIngresoVehiculo.config(bg=COLOR1)

    lblTitulo = tk.Label(ventanaIngresoVehiculo, text="Ingreso del Vehiculo a la Estacion", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 18))
    lblTitulo.place(x=ANCHO//2, y=40, anchor="center")

    lblNumeroCita = tk.Label(ventanaIngresoVehiculo, text="Numero de Cita:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblNumeroCita.place(x=100, y=150)

    lblNumeroPlaca = tk.Label(ventanaIngresoVehiculo, text="Numero de Placa:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblNumeroPlaca.place(x=100, y=250)

    lblCobro = tk.Label(ventanaIngresoVehiculo, text="Monto de Cobro:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblCobro.place(x=100, y=350)

    entryNumeroCita = tk.Entry(ventanaIngresoVehiculo, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryNumeroCita.place(x=350, y=150)

    entryNumeroPlaca = tk.Entry(ventanaIngresoVehiculo, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryNumeroPlaca.place(x=350, y=250)

    entryCobro = tk.Entry(ventanaIngresoVehiculo, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryCobro.place(x=350, y=350)

    #Destruye la ventana de citas y se abre la de menu principal
    def regresar():
        ventanaIngresoVehiculo.destroy()
        ventanaMenuPrincipal.deiconify()

    btnRegresar=tk.Button(ventanaIngresoVehiculo, text= "   Regresar   ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command=regresar)
    btnRegresar.place(x=650, y=500)  

    def validarIngresoVehiculo():
        global citas, colaEspera
        numeroCita = entryNumeroCita.get()
        numeroPlaca = entryNumeroPlaca.get()
        cobro = entryCobro.get()

        if numeroCita == '':
            messagebox.showerror("Numero de Cita", "Debe ingresar un numero de cita")
        elif numeroPlaca == '':
            messagebox.showerror("Numero de Placa", "Debe ingresar un numero de placa")
        elif cobro == '':
            messagebox.showerror("Monto de Cobro", "Debe ingresar un monto de cobro")
        else:
            if not numeroCita.isnumeric():
                messagebox.showerror("Numero de Cita", "Debe ingresar un numero")
            elif not cobro.isnumeric():
                messagebox.showerror("Monto de Cobro", "Debe ingresar un numero")
            else:
                numeroCita = int(numeroCita)
                cobro = int(cobro)
                coincide, cita = coincideCitaPlaca(numeroCita, numeroPlaca)
                if numeroCita < 0:
                    messagebox.showerror("Numero de Cita", "Debe ingresar un numero mayor que cero")
                elif not ((numeroPlaca[:3].isalpha() and numeroPlaca[3:].isnumeric() and numeroPlaca[:3].isupper()) or numeroPlaca.isnumeric()):
                    messagebox.showerror("Numero de Placa", "Debe ingresar una placa de seis numeros o tres letras y tres numeros (VTH070)")
                elif not (12000 <= cobro <= 50000):
                    messagebox.showerror("Monto de Cobro", "Debe ingresar un monto mayor que 12000 y menor que 50000")
                elif not coincide:
                    messagebox.showerror("Ingresar Vehiculo", "El numero de cita debe coincidir con el numero de placa del vehiculo")
                elif estaEnColaEspera(cita):
                    messagebox.showerror("Ingresar Vehiculo", "El vehiculo se encuentra en cola de espera")
                elif estaEnRevision(cita):
                    messagebox.showerror("Ingresar Vehiculo", "El vehiculo se encuentra en revision")
                elif cita["estado"] == "CITA CANCELADA":
                    messagebox.showerror("Ingresar Vehiculo", "La cita ya fue cancelada")
                elif cita["estado"] == "REVISION CANCELADA":
                    messagebox.showerror("Ingresar Vehiculo", "La revision fue cancelada")
                else:
                    pos = obtenerColaMenor()
                    colaEspera[pos].append(cita)
                    ventanaIngresoVehiculo.destroy()
                    ventanaMenuPrincipal.deiconify()
        
    btnConfirmar=tk.Button(ventanaIngresoVehiculo, text= "   Confirmar   ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command=validarIngresoVehiculo)
    btnConfirmar.place(x=100, y=500)

btnIngresoVehiculo=tk.Button(ventanaMenuPrincipal, text= "      Ingreso del Vehiculo     ",
                        bg=COLOR3, fg=TEXT_COLOR,
                        font=("Ubunto Monospace", 12),
                        activebackground=COLOR3,
                        activeforeground=TEXT_COLOR,
                        command=ingresoVehiculo)
btnIngresoVehiculo.place(x=385, y=420)

#_______________________Tablero Revision ___________________________#
def mostrarTableroRevision():
    ventanaMenuPrincipal.withdraw()
    ventanaTableroRevision = tk.Toplevel()
    anchoPantalla = ventanaTableroRevision.winfo_screenwidth()
    altoPantalla = ventanaTableroRevision.winfo_screenheight()

    POS_X = int((anchoPantalla / 2) - (ANCHO / 2))
    POS_Y = int((altoPantalla / 2) - (ALTO / 2))

    ventanaTableroRevision.title(TITULO)
    ventanaTableroRevision.geometry("{}x{}+{}+{}".format(ANCHO, ALTO, POS_X, POS_Y)) 
    ventanaTableroRevision.resizable(width=False, height=False)
    ventanaTableroRevision.config(bg=COLOR1)

    lblTitulo = tk.Label(ventanaTableroRevision, text="Tablero de Revision", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 18))
    lblTitulo.place(x=ANCHO//2, y=20, anchor="center")

    lblComando = tk.Label(ventanaTableroRevision, text="Ingrese el comando:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblComando.place(x=50, y=580)

    entryComando = tk.Entry(ventanaTableroRevision, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryComando.place(x=300, y=580)

    lblLinea = tk.Label(ventanaTableroRevision, text="Linea", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblLinea.place(x=50, y=60)

    lblPuesto1= tk.Label(ventanaTableroRevision, text="Puesto 1", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblPuesto1.place(x=200, y=60)

    lblPuesto2 = tk.Label(ventanaTableroRevision, text="Puesto 2", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblPuesto2.place(x=350, y=60)

    lblPuesto3 = tk.Label(ventanaTableroRevision, text="Puesto 3", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblPuesto3.place(x=500, y=60)

    lblPuesto4 = tk.Label(ventanaTableroRevision, text="Puesto 4", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblPuesto4.place(x=650, y=60)

    lblPuesto5 = tk.Label(ventanaTableroRevision, text="Puesto 5", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblPuesto5.place(x=800, y=60)

    lbl1= tk.Label(ventanaTableroRevision, text="1", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lbl1.place(x=65, y=120)

    lbl2 = tk.Label(ventanaTableroRevision, text="2", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lbl2.place(x=65, y=190)

    lbl3 = tk.Label(ventanaTableroRevision, text="3", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lbl3.place(x=65, y=260)

    lbl4 = tk.Label(ventanaTableroRevision, text="4", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lbl4.place(x=65, y=330)

    lbl5 = tk.Label(ventanaTableroRevision, text="5", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lbl5.place(x=65, y=400)

    lbl6 = tk.Label(ventanaTableroRevision, text="6", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lbl6.place(x=65, y=470)

    def draw(tablero, matrix):
        global tableroFallas
        for x in range(5):
            for y in range(6):
                if hayFallaGrave(tableroFallas[y][x]):
                    tablero[x][y].config(text=matrix[y][x]['numeroPlaca'], bg=COLOR_FALLA)
                else:
                    # Si la matriz tiene un numero
                    tablero[x][y].config(text=matrix[y][x]['numeroPlaca'], bg=COLOR1)
                # Acomoda los labels y le va sumando 150 cada vez que recorre el ciclo para acomodarlos
                tablero[x][y].place(x=(195 + x*150), y=(120 + y*70))
    #Label que dibuja  la matriz
    lblTablero = [[tk.Label(ventanaTableroRevision, font=("Ubuntu Monospace", 18)) for i in range(6)] for j in range(5)]
    
    # Pos es la cola de espera numero "pos"
    def ejecutarLA(pos):
        global colaEspera, tablero
        # Si la linea esta vacia no hay vehiculos en la cola de espera
        if colaEspera[pos] == []:
            messagebox.showerror('LA', 'No hay vehiculos en la cola de espera seleccionada')
            # Si en esa linea hay un vehiculo en el primer puesto
        elif tablero[pos][0] != {'numeroPlaca': '', 'fallas': []}:
            messagebox.showerror('LA', 'Hay un vehiculo en el puesto 1')
        else: #Se elimina de la cola de espera y retorna toda la cita
            tablero[pos][0] = colaEspera[pos].pop(0)
            draw(lblTablero, tablero)

    def ejecutarU(numeroPlaca):
        global tablero, citas, tableroFallas
        posLinea, posPuesto = estaEnRevisionPlaca(numeroPlaca)
        if posLinea == -1:
            messagebox.showerror('U', 'No se encontro el vehiculo')
        else:
            if posPuesto == 4:
                cita = tablero[posLinea][posPuesto]
                fallas = tableroFallas[posLinea][posPuesto]
                posCita = citas.index(cita)
                cita["fallas"] = fallas
                if fallas != []:
                    if hayFallaGrave(fallas):
                        if cita["tipoCita"] == 3:
                            cita["estado"] = "SACAR DE CIRCULACION"
                        else:
                            cita["estado"] = "PARA REINSPECCION"
                    else:
                        cita["estado"] = "PARA REINSPECCION"
                else:
                    cita["estado"] = "APROBADA"
                citas[posCita] = cita
                guardar(archivoCitas, citas)
                tablero[posLinea][posPuesto] = {'numeroPlaca': '', 'fallas': []}
                tableroFallas[posLinea][posPuesto] = []
                if fallas == []:
                    messagebox.showinfo('Fin de la revision', 'El vehiculo con la placa ' + numeroPlaca + ' termino la revision sin fallas')
                else:
                    msj = "Estado del vehiculo placa " + numeroPlaca + ": " + cita["estado"] + "\n"
                    for falla in fallas:
                        msjFalla = 'Numero de falla: {}, tipo de falla: {}, descripcion: {}\n'
                        msj = msj + msjFalla.format(falla[0], falla[2], falla[1])
                    messagebox.showinfo('Fin de la revision', msj)
            elif tablero[posLinea][posPuesto + 1] != {'numeroPlaca': '', 'fallas': []}:
                messagebox.showerror('U', 'Hay un vehiculo en el puesto ' + str(posPuesto + 2))
            else:
                tablero[posLinea][posPuesto + 1] = tablero[posLinea][posPuesto]
                tableroFallas[posLinea][posPuesto + 1] = tableroFallas[posLinea][posPuesto]
                tablero[posLinea][posPuesto] = {'numeroPlaca': '', 'fallas': []}
                tableroFallas[posLinea][posPuesto] = []
            draw(lblTablero, tablero)

    def ejecutarT(numeroPlaca):
        global tablero
        posLinea, posPuesto = estaEnRevisionPlaca(numeroPlaca)
        if posLinea == -1:
            messagebox.showerror('T', 'No se encontro el vehiculo')
        else:
            if tablero[posLinea][-1] == {'numeroPlaca': '', 'fallas': []}:
                cita = tablero[posLinea][posPuesto]
                fallas = tableroFallas[posLinea][posPuesto]
                posCita = citas.index(cita)
                cita["fallas"] = fallas
                if hayFallaGrave(fallas):
                    if cita["tipoCita"] == 3:
                        cita["estado"] = "SACAR DE CIRCULACION"
                    else:
                        cita["estado"] = "PARA REINSPECCION"
                else:
                    cita["estado"] = "APROBADA"
                citas[posCita] = cita
                guardar(archivoCitas, citas)
                tablero[posLinea][-1] = {'numeroPlaca': '', 'fallas': []}
                if fallas == []:
                    messagebox.showinfo('Fin de la revision', 'El vehiculo con la placa ' + numeroPlaca + ' termino la revision sin fallas')
                else:
                    msj = "Estado del vehiculo placa " + numeroPlaca + ": " + cita["estado"] + "\n"
                    for falla in fallas:
                        msjFalla = 'Numero de falla: {}, tipo de falla: {}, descripcion: {}\n'
                        msj = msj + msjFalla.format(falla[0], falla[2], falla[1])
                    messagebox.showinfo('Fin de la revision', msj)
            for i in range(0, len(tablero[posLinea]) - 1):
                # Se mueve el vehiculo al siguiente puesto
                tablero[posLinea][-i - 1] = tablero[posLinea][-i - 2]
                tableroFallas[posLinea][-i - 1] = tableroFallas[posLinea][-i - 2]
            # Si en la cola de espera hay algun vehiculo, se pasa a la primera posicion del tablero    
            if colaEspera[posLinea] != []:
                tablero[posLinea][0] = colaEspera[posLinea].pop(0)
                tableroFallas[posLinea][0] = []
            else: #Si no hay un vehiculo en la cola de espera se vacia la primera posicion 
                tablero[posLinea][0] = {'numeroPlaca': '', 'fallas': []}
                tableroFallas[posLinea][0] = []
            draw(lblTablero, tablero)

    def ejecutarC(numeroPlaca):
        global tablero, citas
        posLinea, posPuesto = estaEnRevisionPlaca(numeroPlaca)
        if posLinea == -1:
            messagebox.showerror('C', 'No se encontro el vehiculo')
        else:
            cita = tablero[posLinea][posPuesto]
            posCita = citas.index(cita)
            cita["estado"] = "REVISION CANCELADA"
            citas[posCita] = cita
            guardar(archivoCitas, citas)
            tablero[posLinea][posPuesto] = {'numeroPlaca': '', 'fallas': []}
            tableroFallas[posLinea][posPuesto] = []
            draw(lblTablero, tablero)
        
    def ejecutarF(numeroPlaca, falla):
        global tablero, tableroFallas
        posLinea, posPuesto = estaEnRevisionPlaca(numeroPlaca)
        if posLinea == -1:
            messagebox.showerror('F', 'No se encontro el vehiculo')
            # Validar que el numero de falla sea numerico
        elif not (falla.isnumeric()):
            messagebox.showerror('F', 'La falla debe ser un numero')
        else:
            # Convertir a int
            falla = int(falla)
            # Validar que este en el rango valido
            if not (1 <= falla <= 9999):
                messagebox.showerror('F', 'La falla debe ser un numero entre 1 y 9999')
                # Que la falla este en el diccionario de fallas
            elif not (existeFalla(falla)):
                messagebox.showerror("F", "El numero de falla no existe") 
            else:
                tableroFallas[posLinea][posPuesto].append([falla] + list(fallas[falla]))
                messagebox.showinfo("F", "Falla agregada")
        draw(lblTablero, tablero)
                

    def confirmarComando():
        comando = entryComando.get()
        if comando == '':
            messagebox.showerror('Comando', 'Debe ingresar un comando')
        elif len(comando) == 7:
            letra = comando[0]
            placa = comando[1:]
            if letra in 'TUC':
                if ((placa[:3].isalpha() and placa[3:].isnumeric() and placa[:3].isupper()) or placa.isnumeric()):
                    if letra == 'T':
                        ejecutarT(placa)
                    elif letra == 'U':
                        ejecutarU(placa)
                    else:
                        ejecutarC(placa)
                else:
                    messagebox.showerror("Numero de Placa", "Debe ingresar una placa de seis numeros o tres letras y tres numeros (VTH070)")
            else:
                messagebox.showerror('Comando', 'No se reconoce el comando')
        elif len(comando) == 11:
            letra = comando[0]
            placa = comando[1:7]
            falla = comando[7:]
            if letra == 'F':
                if ((placa[:3].isalpha() and placa[3:].isnumeric() and placa[:3].isupper()) or placa.isnumeric()):
                    ejecutarF(placa, falla)
                else:
                    messagebox.showerror("Numero de Placa", "Debe ingresar una placa de seis numeros o tres letras y tres numeros (VTH070)")
            else:
                messagebox.showerror('Comando', 'No se reconoce el comando')
        elif comando == 'M':
            regresar()
        else:
            if len(comando) == 2 and comando[1] == 'A' and (comando[0] in '123456'):
                ejecutarLA(int(comando[0]) - 1)
            else:
                messagebox.showerror('Comando', 'No se reconoce el comando')

    def regresar():
        ventanaTableroRevision.destroy()
        ventanaMenuPrincipal.deiconify()

    draw(lblTablero, tablero)
    btnConfirmarComando=tk.Button(ventanaTableroRevision, text= "   Confirmar   ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command=confirmarComando)
    btnConfirmarComando.place(x=800, y=580) 

btnTableroRevision=tk.Button(ventanaMenuPrincipal, text= "    Tablero de la Revision    ",
                            bg=COLOR3, fg=TEXT_COLOR,
                            font=("Ubunto Monospace", 12),
                            activebackground=COLOR3,
                            activeforeground=TEXT_COLOR,
                            command=mostrarTableroRevision)
btnTableroRevision.place(x=385, y=500)

#   _____________________  Resultado de la Revision___________________________#
def ResultadoRevision():
    ventanaMenuPrincipal.withdraw()
    ventanaResultadoRevision = tk.Toplevel()
    anchoPantalla = ventanaResultadoRevision.winfo_screenwidth()
    altoPantalla = ventanaResultadoRevision.winfo_screenheight()

    POS_X = int((anchoPantalla / 2) - (ANCHO / 2))
    POS_Y = int((altoPantalla / 2) - (ALTO / 2))

    ventanaResultadoRevision.title(TITULO)
    ventanaResultadoRevision.geometry("{}x{}+{}+{}".format(ANCHO, ALTO, POS_X, POS_Y)) 
    ventanaResultadoRevision.resizable(width=False, height=False)
    ventanaResultadoRevision.config(bg=COLOR1)

    lblTitulo = tk.Label(ventanaResultadoRevision, text="Resultado de la Revision", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 18))
    lblTitulo.place(x=ANCHO//2, y=20, anchor="center")

    lblNumeroCita = tk.Label(ventanaResultadoRevision, text="Numero de Cita:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblNumeroCita.place(x=100, y=150)

    lblNumeroPlaca = tk.Label(ventanaResultadoRevision, text="Numero de Placa:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblNumeroPlaca.place(x=100, y=300)

    entryNumeroCita = tk.Entry(ventanaResultadoRevision, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryNumeroCita.place(x=350, y=150)

    entryNumeroPlaca = tk.Entry(ventanaResultadoRevision, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryNumeroPlaca.place(x=350, y=300)

    def crearPdf(cita):
        pdf = canvas.Canvas('Revitec_Cita_' + str(cita["numeroCita"]) + '.pdf')

        pdf.setFillColorRGB(0, 0, 255)
        pdf.setFont("Helvetica", 24)
        pdf.drawString(175, 790, "Certificado de la Revisión")
        pdf.line(175, 785, 449, 785)

        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica", 16)
        pdf.drawString(70, 700, "Numero de Cita: " + str(cita["numeroCita"]))
        pdf.drawString(70, 625, "Numero de Placa: " + cita["numeroPlaca"])
        pdf.drawString(70, 550, "Fecha de Cita: " + cita['fechaCita'][:2] + cita['fechaCita'][2:4] + cita['fechaCita'][4:])
        pdf.drawString(70, 475, "Hora de Cita: " + str(cita["horaCita"]//100) + ":" + str(cita["horaCita"])[2:])
        pdf.drawString(70, 395, "Resultado de la Revisión: ")
        if cita['estado'] == "APROBADA":
            pdf.setFillColorRGB(0, 255, 0)
            pdf.setFont("Helvetica", 18)
            pdf.drawString(270, 395, cita['estado'])

        else:
            pdf.setFont("Helvetica", 18)
            pdf.drawString(270, 395, cita['estado'])
            pdf.drawString(70, 320, "Fallas encontradas: ")
            pdf.line(70, 315, 230, 315)
            y = 275
            for falla in cita["fallas"]:
                pdf.drawString(70, y, str(falla[0]) + " - " + falla[2])
                pdf.drawString(70, y - 20, falla[1])
                y -= 40
                

        pdf.save()

        #destinatario = [cita['correoElectronico']]
        destinatario = ["guzka97@gmail.com"]
        cuerpo = "Resultado de la cita.\n-Revitec"
        ruta_adjunto = nombre_adjunto = 'Revitec_Cita_' + str(cita["numeroCita"]) + '.pdf'
        mensaje = MIMEMultipart()
        mensaje['From'] = "guzka97@gmail.com"
        mensaje['To'] = ", ".join(cita["correoElectronico"])
        mensaje['Subject'] = "Resultado revision"

        mensaje.attach(MIMEText(cuerpo, 'plain'))
        archivo_adjunto = open(ruta_adjunto, 'rb')
        adjunto_MIME = MIMEBase('application', 'octet-stream')
        adjunto_MIME.set_payload(archivo_adjunto.read())
        encoders.encode_base64(adjunto_MIME)
        adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
        mensaje.attach(adjunto_MIME)
        sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        sesion_smtp.starttls()
        sesion_smtp.login('guzka97@gmail.com', 'Happiness.97')
        texto = mensaje.as_string()
        sesion_smtp.sendmail("guzka97@gmail.com", destinatario, texto)
        sesion_smtp.quit()

        

    def validarRevision():
        global citas
        numeroCita = entryNumeroCita.get()
        numeroPlaca = entryNumeroPlaca.get()

        if numeroCita == '':
            messagebox.showerror("Numero de Cita", "Debe ingresar un numero de cita")
        elif numeroPlaca == '':
            messagebox.showerror("Numero de Placa", "Debe ingresar un numero de placa")
        else:
            if not numeroCita.isnumeric():
                messagebox.showerror("Numero de Cita", "Debe ingresar un numero")
            else:
                numeroCita = int(numeroCita)
                coincide, cita = coincideCitaPlaca(numeroCita, numeroPlaca)
                if numeroCita < 0:
                    messagebox.showerror("Numero de Cita", "Debe ingresar un numero mayor que cero")
                elif not ((numeroPlaca[:3].isalpha() and numeroPlaca[3:].isnumeric() and numeroPlaca[:3].isupper()) or numeroPlaca.isnumeric()):
                    messagebox.showerror("Numero de Placa", "Debe ingresar una placa de seis numeros o tres letras y tres numeros (VTH070)")
                elif not coincide:
                    messagebox.showerror("Resultado de la Revision", "El numero de cita debe coincidir con el numero de placa del vehiculo")
                elif not (cita["estado"] == "APROBADA" or cita["estado"] == "PARA REINSPECCION" or cita["estado"] == "SACAR DE CIRCULACION"):   
                    messagebox.showerror("Resultado de la Revision", "El vehiculo no ha sido revisado")    
                else:
                    crearPdf(cita)
                    ventanaResultadoRevision.destroy()
                    ventanaMenuPrincipal.deiconify()    
    
    def regresar():
        ventanaResultadoRevision.destroy()
        ventanaMenuPrincipal.deiconify()

    btnRegresar=tk.Button(ventanaResultadoRevision, text= "   Regresar   ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command=regresar)
    btnRegresar.place(x=800, y=500)  
                        
    btnConfirmar=tk.Button(ventanaResultadoRevision, text= "   Confirmar   ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command = validarRevision)
    btnConfirmar.place(x=100, y=500)

btnResultadoRevision=tk.Button(ventanaMenuPrincipal, text= "  Resultado de la Revision  ",
                            bg=COLOR3, fg=TEXT_COLOR,
                            font=("Ubunto Monospace", 12),
                            activebackground=COLOR3,
                            activeforeground=TEXT_COLOR,
                            command=ResultadoRevision)
btnResultadoRevision.place(x=650, y=500)  

#_______________________________ Lista de Fallas_________________________#
def listaFallas():
    ventanaMenuPrincipal.withdraw()
    ventanalistaFallas = tk.Toplevel()
    anchoPantalla = ventanalistaFallas.winfo_screenwidth()
    altoPantalla = ventanalistaFallas.winfo_screenheight()

    POS_X = int((anchoPantalla / 2) - (ANCHO / 2))
    POS_Y = int((altoPantalla / 2) - (ALTO / 2))

    ventanalistaFallas.title(TITULO)
    ventanalistaFallas.geometry("{}x{}+{}+{}".format(ANCHO, ALTO, POS_X, POS_Y)) 
    ventanalistaFallas.resizable(width=False, height=False)
    ventanalistaFallas.config(bg=COLOR1)

    lblNumeroFalla = tk.Label(ventanalistaFallas, text="Numero de Falla:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblNumeroFalla.place(x=25, y=50) 

    lblDescripcion = tk.Label(ventanalistaFallas, text="Descripcion:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblDescripcion.place(x=25, y=100)

    lblFalla= tk.Label(ventanalistaFallas, text="Tipo de Falla:", bg=COLOR1, fg=TEXT_COLOR, font=("Ubuntu Monospace", 14))
    lblFalla.place(x=450, y=50)

    entryNumeroFalla = tk.Entry(ventanalistaFallas, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryNumeroFalla.place(x=200, y=50)

    entryFalla = tk.Entry(ventanalistaFallas, bd=2, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryFalla.place(x=600, y=50)

    entryDescripcion = tk.Text(ventanalistaFallas, bd=2, height=2, width=20, bg=COLOR2, font=("Ubuntu Monospace", 13))
    entryDescripcion.place(x=200, y=100)

    frame = tk.Frame(ventanalistaFallas, bg=COLOR3)
    frame.place(x=400, y=250)
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    lbFallas = tk.Listbox(frame, font=("Ubunto Monospace", 12), yscrollcommand=scrollbar.set)
    lbFallas.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.config(command=lbFallas.yview)

    def llenarLbFallas():
        global fallas
        lbFallas.delete(0, tk.END)
        i = 0
        for numeroFalla in sorted(list(fallas.keys())):
            lbFallas.insert(i, str(numeroFalla) + ' - ' + fallas[numeroFalla][1] + ': ' + fallas[numeroFalla][0])
            i += 1

    llenarLbFallas()

    def agregarFalla():
        global fallas, archivoFallas
        numeroFalla = entryNumeroFalla.get()
        tipoFalla = entryFalla.get()
        descripcion = entryDescripcion.get("1.0",'end-1c')

        if numeroFalla == "":
            messagebox.showerror("Numero de Falla", "El numero de falla no puede estar vacio")
        elif tipoFalla == "":
            messagebox.showerror("Tipo de Falla", "El tipo de falla no puede estar vacio")
        elif descripcion  == "":
            messagebox.showerror("descripcion", "La descripcion de la falla no puede estar vacio")
        else:    
            if not (numeroFalla.isnumeric() and 1 <= int(numeroFalla) <= 9999):
                messagebox.showerror("Numero de Falla", "El numero de falla debe ser un numero entre 1 y 9999")
            elif len(descripcion) > 60:
                messagebox.showerror("Descripcion Falla",  "La descripcion de la falla no puede ser mas de 60 caracteres")
            elif not (tipoFalla == "L" or tipoFalla == "G"):
                messagebox.showerror("Tipo de Falla", "El tipo de falla debe ser L: falla leve o G: falla grave")
            else:
                numeroFalla = int(numeroFalla)
                if existeFalla(numeroFalla):
                    messagebox.showerror("Numero de Falla", "El Numero de falla ya existe")
                else:
                    fallas[numeroFalla] = (descripcion, tipoFalla)
                    guardar(archivoFallas, fallas)
                    llenarLbFallas()
                    entryNumeroFalla.delete(0, tk.END)
                    entryFalla.delete(0, tk.END)
                    entryDescripcion.delete("1.0",'end-1c')
                    messagebox.showinfo("Numero de Falla", "La falla se ha agregado correctamente")

    def modificar():
        global fallas, archivoFallas
        numeroFalla = entryNumeroFalla.get()
        tipoFalla = entryFalla.get()
        descripcion = entryDescripcion.get("1.0",'end-1c')

        if numeroFalla == "":
            messagebox.showerror("Numero de Falla", "El numero de falla no puede estar vacio")
        elif tipoFalla == "":
            messagebox.showerror("Tipo de Falla", "El tipo de falla no puede estar vacio")
        elif descripcion  == "":
            messagebox.showerror("descripcion", "La descripcion de la falla no puede estar vacio")
        else:    
            if not (numeroFalla.isnumeric() and 1 <= int(numeroFalla) <= 9999):
                messagebox.showerror("Numero de Falla", "El numero de falla debe ser un numero entre 1 y 9999")
            elif len(descripcion) > 60:
                messagebox.showerror("Descripcion Falla",  "La descripcion de la falla no puede ser mas de 60 caracteres")
            elif not (tipoFalla == "L" or tipoFalla == "G"):
                messagebox.showerror("Numero de Falla", "El numero de falla debe ser L: falla leve o G: falla grave")
            else:
                numeroFalla = int(numeroFalla)
                if existeFalla(numeroFalla):
                    fallas[numeroFalla] = (descripcion, tipoFalla)
                    guardar(archivoFallas, fallas)
                    llenarLbFallas()
                    entryNumeroFalla.delete(0, tk.END)
                    entryFalla.delete(0, tk.END)
                    entryDescripcion.delete("1.0",'end-1c')
                    messagebox.showinfo("Numero de Falla", "La falla se ha modificado correctamente") 
                else:
                    messagebox.showerror("Numero de Falla", "El numero de falla no existe")
    
    def eliminar():
        global fallas, archivoFallas
        numeroFalla = entryNumeroFalla.get()

        if numeroFalla == "":
            messagebox.showerror("Numero de Falla", "El numero de falla no puede estar vacio")
        elif not (numeroFalla.isnumeric() and 1 <= int(numeroFalla) <= 9999):
            messagebox.showerror("Numero de Falla", "El numero de falla debe ser un numero entre 1 y 9999")
        else:
            numeroFalla = int(numeroFalla)
            if existeFalla(numeroFalla):
                MsgBox = messagebox.askquestion("Eliminar la Falla","¿Esta seguro que desea eliminar la falla?", icon="warning")
                if MsgBox == "yes":
                    del fallas[numeroFalla]
                    guardar(archivoFallas, fallas)
                    llenarLbFallas()
                    entryNumeroFalla.delete(0, tk.END)
                    entryFalla.delete(0, tk.END)
                    entryDescripcion.delete("1.0",'end-1c')
                    messagebox.showinfo("Numero de Falla", "La falla se ha eliminado correctamente")
            else:
                messagebox.showerror("Numero de Falla", "El numero de falla no existe")
            

    def regresar():
        ventanalistaFallas.destroy()
        ventanaMenuPrincipal.deiconify()

    btnRegresar=tk.Button(ventanalistaFallas, text= "   Regresar   ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command=regresar)
    btnRegresar.place(x=800, y=555) 

    btnAgregar=tk.Button(ventanalistaFallas, text= "    Agregar    ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command=agregarFalla)
    btnAgregar.place(x=800, y=300) 

    btnModificar=tk.Button(ventanalistaFallas, text= "   Modificar   ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command=modificar)
    btnModificar.place(x=800, y=225) 

    btnEliminar=tk.Button(ventanalistaFallas, text= "    Eliminar    ",
                                bg=COLOR3, fg=TEXT_COLOR,
                                font=("Ubunto Monospace", 12),
                                activebackground=COLOR3,
                                activeforeground=TEXT_COLOR,
                                command=eliminar)
    btnEliminar.place(x=800, y=150)

btnListaFallas=tk.Button(ventanaMenuPrincipal, text= "            Lista de Fallas          ",
                            bg=COLOR3, fg=TEXT_COLOR, 
                            font=("Ubunto Monospace", 12),
                            activebackground=COLOR3,
                            activeforeground=TEXT_COLOR,
                            command = listaFallas)
btnListaFallas.place(x=650, y=420)

ventanaMenuPrincipal.mainloop()

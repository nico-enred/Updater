# We create the game of The hangman
import random
secret_word=''
result=''
list_guessing_letters=[]
list_fails=[]
list_ahorcado=['AHORCADO']
# *********************************Programa Viejo*******************************
import urllib.request
import sys
import subprocess
# **************Comprobar versión del programa*************
url_check_version=('https://raw.githubusercontent.com/nico-enred/Updater/refs/heads/main/Version_check')
def check_version():
    inside_url_origen=[]
    fhand=urllib.request.urlopen(url_check_version)
    for line in fhand:
        line=line.decode().strip()
        inside_url_origen.append(line)
    fhand.close()
    return inside_url_origen
in_url_origen=check_version()#llamamos la función para tener su return disponible como parametro

def extract_content_from_url_origin(in_url_origen):#extraígo el contenido de la url.
    new_version=in_url_origen[0]#La nueva versión que está en la primera línea
    downloading_new_file_url=in_url_origen[1]#La url del archivo nuevo para descargar
    modifications=in_url_origen[3:]#Las modificaciones que contiene el nuevo programa. De la tercera línea en adelante
    return new_version,downloading_new_file_url,modifications

new_version,downloading_new_file_url,modifications=extract_content_from_url_origin(in_url_origen)#Se llama la función para tener disponibles
                                                                                                #las variables
modifications_='\n'.join(modifications)

def get_current_version():#Obtenemos la versión actual del archivo del archivo current_version.txt
    with open('current_version.txt','r') as fhand2:
        for line in fhand2:
            return line.strip()#it exists after reading the first line. if ever were added more lines the return should move out of the loop.
        
current_version=get_current_version()

def change_to_new_version_in_currrent_version(new_version):#Cambiar version en current_version.txt
    with open('current_version.txt','w') as fhand3:
        fhand3.write(new_version)
def download_new_file(downloading_new_file_url):#Descargar archivo nuevo desde la url que hay en la segunda posición
    data=urllib.request.urlopen(downloading_new_file_url).read()
    with open('New_Ahorcado.py','wb') as fhand4:
        fhand4.write(data)
# ***************terminate program and start new one***************************************
def terminate_program(): #to be run on the program to delete after all the checks
    sys.exit()
    
def start_updater():
    subprocess.Popen(['python3','Updater_7.py'])#after checking there is a new version in the old program, it starts the updater
def actualizar():
    change_to_new_version_in_currrent_version(new_version)
    download_new_file(downloading_new_file_url)
    start_updater()
    terminate_program()
    
def no_actualizar():
    boton_yes.grid_remove()
    boton_no.grid_remove()
    
identificador=None
def brilli(boton):
    global identificador
    if boton.cget('fg_color')=='light green':
        boton.configure(fg_color='green')
    else:
        boton.configure(fg_color='light green')
    identificador=root.after(1000,brilli,boton)
# *************
def word_from_file():
    list=[]
    global secret_word
    with open('palabras.txt','r') as fhand:
        for line in fhand:
            line=line.rstrip()
            for word in line.split(','):
                list.append(word)
    secret_word=random.choice(list)
#     print(secret_word)
    return secret_word
# *************
def output_hyphens():
    global secret_word
    word_from_file()
    guess_it="_ "
    widget_label_1.configure(text=guess_it*len(secret_word))
    widget_boton_start_currrent_game.configure(state='disabled')
    widget_entrada_datos.configure(state='normal',placeholder_text='Introduce aquí la letra...')
    widget_boton_check_letras.configure(state='normal')
    widget_new_game.configure(state='normal')
# *************   
def display_letters():
    global result
    global secret_word
    global list_guessing_letters
    global list_fails
    global list_ahorcado
    result=''
    if not validate_entry():
        entry=widget_entrada_datos.get()
        widget_entrada_datos.delete(0,'end')
        if len(entry)!=1:
            widget_entrada_datos.configure(placeholder_text='Ni muchas letras ni ninguna letra...')
        elif not entry.isalpha():
            widget_entrada_datos.configure(placeholder_text='Solo valen letras...')
        elif entry in list_guessing_letters or entry in list_fails:
            widget_entrada_datos.configure(placeholder_text='¿Eso no lo habías dicho ya...?')
        return
    list_guessing_letters.append(normalize(widget_entrada_datos.get()))
    for char in secret_word:
        char_no_accents=normalize(char)
        if char_no_accents in list_guessing_letters:
            result+=char+' '
        else:
            result+='_ '
        if not normalize(widget_entrada_datos.get()) in secret_word:
            list_fails.append(normalize(widget_entrada_datos.get()))
#             print(list_fails)
            widget_label_letras_falladas.configure(text=f"Letras falladas: {' '.join(list_fails)}",wraplength=600)
            for i in range(len(list_fails)):
                widget_label_hangman.configure(text=list_ahorcado[0][:i+1])
                if len(list_fails)>8:
                    widget_entrada_datos.configure(state='disabled')
                    widget_boton_check_letras.configure(state='disabled')
                    widget_label_1.configure(text='Has fallado')
                    widget_label_hangman.configure(text=f'Eres el A_H_O_R_C_A_D_O \n({secret_word.upper()})',wraplength=450)
                    
                    return
        widget_label_1.configure(text=result)
        widget_entrada_datos.delete(0,'end')
        widget_entrada_datos.configure(placeholder_text='Introduce aquí la letra')
    if '_' not in result:
        widget_label_hangman.configure(text='Eres el C_A_M_P_E_Ó_N')
        widget_entrada_datos.configure(state='disabled',placeholder_text='E_N_H_O_R_A_B_U_E_N_A')
        widget_boton_check_letras.configure(state='disabled')
        widget_label_letras_falladas.configure(text='')
       
        
    return result
# *************       
def reset():
    global secret_word
    global result
    secret_word=''
    result=''
    list_guessing_letters.clear()
    list_fails.clear()
    widget_entrada_datos.configure(state='normal',placeholder_text='Introduce aquí la letra')
    widget_label_hangman.configure(text='')
    widget_label_letras_falladas.configure(text='')
    output_hyphens()

# *************
def validate_entry():
    letra=normalize(widget_entrada_datos.get())
    if len(letra)!=1 or not letra.isalpha() or letra in list_guessing_letters or letra in list_fails:
        return False
    return True
# *************
def normalize(texto):
    return texto.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
# *************
import customtkinter as ctk
root=ctk.CTk()
root.title('The hangman')
root.geometry('500x500')
root.resizable(True,True)
ctk.set_appearance_mode('Dark')
# ctk.set_default_color_theme('blue') es el color que tendrían los widgets si no defino yo uno al crearlos
root.grid_columnconfigure(0,weight=1)
# widget boton de inicio de juego
widget_boton_start_currrent_game=ctk.CTkButton(root,text='Haz click para empezar este juego',fg_color='green',text_color='black',font=('Arial',24,'bold'),corner_radius=8,command=output_hyphens)
widget_boton_start_currrent_game.grid(row=0,column=0,sticky='we',padx=20,pady=10)
# widget para la etiqueta donde está la palabra secreta
widget_label_1=ctk.CTkLabel(root,text='Esperando a que inicies el juego...',fg_color='black',text_color='yellow',font=('Arial',24,'bold'),wraplength=550,corner_radius=8)
widget_label_1.grid(row=1,column=0,sticky='we',padx=20,pady=10)
# widget para introducir letras
widget_entrada_datos=ctk.CTkEntry(root,fg_color='white',text_color='red',font=('Arial',24,'bold'),corner_radius=8,state='disabled',placeholder_text='Introduce aquí la letra...')
widget_entrada_datos.grid(row=2,column=0,sticky='we',padx=20,pady=10)
# widget para el boton que comprueba si la letra es correcta o no
widget_boton_check_letras=ctk.CTkButton(root,text='Comprobar letra',fg_color='green',text_color='black',hover_color='orange',font=('Arial',30,'bold'),corner_radius=8,state='disabled',command=display_letters)
widget_boton_check_letras.grid(row=3,column=0,padx=20,pady=20)
# widget para ir poniendo las letras que se han fallado
widget_label_letras_falladas=ctk.CTkLabel(root,text='',font=('Arial',30,'bold'))
widget_label_letras_falladas.grid(row=4,column=0,padx=20,pady=10,sticky='we')
# widget etiqueta donde se va formando la palabra AHORCADO Y AL FORMARSE SE TRANSFORMA EN GAME OVER
widget_label_hangman=ctk.CTkLabel(root,text='',font=('Arial',30,'bold'))
widget_label_hangman.grid(row=5,column=0,padx=20,pady=10,sticky='we')
# boton de reiniciar juego
widget_new_game=ctk.CTkButton(root,command=reset,text='Juego nuevo',fg_color='black',text_color='red',font=('Arial',20,'bold'),corner_radius=8,state='disabled')
widget_new_game.grid(row=6,column=0, sticky='we',padx=150,pady=(100,0))
if current_version!=new_version: #si se cumple la condición empezamos la actualización
        frame_actualizar=ctk.CTkFrame(root,fg_color='light blue',border_color='blue',border_width=5)
        frame_actualizar.grid_configure(row=0,column=0,sticky='nswe')
        label_show_version=ctk.CTkLabel(frame_actualizar,text=f'La versión actual es:{current_version}. Hay una nueva versión disponible.\n¿Quiere actualizar?'
                                        ,fg_color='green',border_color='yellow',border_width=2)
        label_show_version.grid_configure(row=0,
                                          column=0,columnspan=3,sticky='nswe')
        label_show_modification=ctk.CTkLabel(frame_actualizar,text=f"Las modificaciones que se añadirán son:\n{modifications_}")
        label_show_modification.grid_configure(row=1,
                                               column=0,columnspan=3,sticky='nswe')
        boton_yes=ctk.CTkButton(frame_actualizar,text='Actualizar',fg_color='light green',hover_color='green',command=actualizar)
        boton_yes.grid_configure(row=2
                                 ,column=0)
        boton_no=ctk.CTkButton(frame_actualizar,text='No Actualizar',fg_color='pink',hover_color='red',command=no_actualizar)
        boton_no.grid_configure(row=2,
                                column=3)
        frame_actualizar.tkraise()
        brilli(boton_yes) 
root.mainloop()


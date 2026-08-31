# We create the game of The hangman
import random
secret_word=''
result=''
list_guessing_letters=[]
list_fails=[]
list_ahorcado=['AHORCADO']
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
root.resizable(False,False)
ctk.set_appearance_mode('light')
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
root.mainloop()

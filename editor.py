import tkinter as tk
import tkinter.filedialog as tkfd
import jsonhandler
import os
import cryptography.fernet as Fernet
import editorcrypt

#colors: white	#9da39d, green #90b061, black #292d34

acceptedfiletypes = (("Text Files", "*.txt"),("Quark crypted file", ".u2dc"),("All Files", "*.*"))
openFileLeft = 'Não salvo'
openFileRight = 'Não salvo'
Toggle = False
ToggleSecondText = True
focoEsquerdo = True
focoDireito = False

#Criar novos arquivos
def newFile(event = None):
    openFile = None
    if focoEsquerdo:
        applabel.delete('1.0', 'end-1c')
        root.title("Novo documento 1 - Proton")
        openFileLeft = None
    elif focoDireito:
        applabel2.delete('1.0', 'end-1c')
        root.title("Novo documento 2 - Proton")
        openFileRight = None

#Salvar arquivo atual  
def saveFile(event = None):
    if openFileLeft:
        if focoEsquerdo:
            openfile = open(openFile, 'wb')
            contenttosave = applabel.get('1.0', 'end-1c')
            openfile.write(contenttosave)
            openfile.close()

    elif openFileRight:
        if focoDireito:
            openfile = open(openFile, 'wb')
            contenttosave = applabel2.get('1.0', 'end-1c')
            openfile.write(contenttosave)
            openfile.close()

#Salvar novo arquivo em .txt
def saveAsFile(event = None):
    if focoEsquerdo:
        contenttosave = applabel.get('1.0', 'end-1c')

        if len(contenttosave) > 0:
            openfile = tkfd.asksaveasfile(mode='w', filetypes=acceptedfiletypes, defaultextension=".txt", title='Salve seu arquivo')
            global openFileLeft
            openFileLeft = os.path.basename(openfile.name)
            openfile.write(contenttosave)
            root.title(f"{openFileLeft} - Proton")
            openfile.close()
            
    elif focoDireito:
        contenttosave = applabel2.get('1.0', 'end-1c')

        if len(contenttosave) > 0:
            openfile = tkfd.asksaveasfile(mode='w', filetypes=acceptedfiletypes, defaultextension=".txt", title='Salve seu arquivo')
            global openFileRight
            openFileRight = os.path.basename(openfile.name)
            root.title(f"{openFileRight} - Proton")
            openfile.write(contenttosave)
            openfile.close()

#Salvar arquivo criptografado u2dc
def encryptSave(event = None):
    key = editorcrypt.cryp()

    if jsonhandler.loadSetting()['UseExperimentalEncrypting']:
        FC = Fernet.Fernet(key)

        #criptografar dados
        if focoEsquerdo:
            contenttosave = applabel.get('1.0', 'end-1c')
            if len(contenttosave) > 0:
                encryptedData = FC.encrypt(contenttosave.encode('utf-8'))
                openfile = tkfd.asksaveasfile(mode='wb', filetypes=acceptedfiletypes, defaultextension='.u2dc', title='Salve um arquivo criptografado')
                openfile.write(encryptedData)
                global openFileLeft
                openFileLeft = os.path.basename(openfile.name)
                root.title(f"{openFileLeft} - Proton (Experimental encrypting file)")
        elif focoDireito:
            contenttosave = applabel2.get('1.0', 'end-1c')
            if len(contenttosave) > 0:
                encryptedData = FC.encrypt(contenttosave.encode('utf-8'))
                openfile = tkfd.asksaveasfile(mode='wb', filetypes=acceptedfiletypes, defaultextension='.u2dc', title='Salve um arquivo criptografado')
                openfile.write(encryptedData)
                global openFileRight
                openFileRight = os.path.basename(openfile.name)
                root.title(f"{openFileRight} - Proton (Experimental encrypting file)")
    else:
        popup('Erro', 'UseExperimentalEncryption deve estar habilitado\n para essa função.\nAcesse settings.json')

#Abrir arquivos txt
def openFile(event = None):
    key = editorcrypt.cryp()
    
    if focoEsquerdo:
        openfile = tkfd.askopenfile(mode='rb', title='Abra um arquivo')
        splitedfile = os.path.splitext(openfile.name)

        if openfile:
            if splitedfile[-1] != '.u2dc':
                textdata = openfile.read()
                applabel.insert('1.0', textdata)
                global openFileLeft
                openFileLeft = os.path.basename(openfile.name)
                root.title(f"{openFileLeft} - Proton" )
            
            if splitedfile[-1] == '.u2dc':
                FC = Fernet.Fernet(key)

                textdatab = openfile.read()
                decrypteddata = FC.decrypt(textdatab)
                applabel.insert('1.0', decrypteddata.decode('utf-8'))
                openFileLeft = os.path.basename(openfile.name)
                root.title(f"{openFileLeft} - Proton" )

    elif focoDireito:
        openfile = tkfd.askopenfile(mode='r', title='Abra um arquivo')
        splitedfile = os.path.splitext(openfile.name)

        if openfile:
            if splitedfile[-1] != '.u2dc':
                textdata = openfile.read()
                applabel2.insert('1.0', textdata)
                global openFileRight
                openFileRight = os.path.basename(openfile.name)
                root.title(f"{openFileRight} - Proton" )
            
            if splitedfile[-1] == '.u2dc':
                FC = Fernet.Fernet(key)

                textdatab = openfile.read()
                decrypteddata = FC.decrypt(textdatab)
                applabel2.insert('1.0', decrypteddata.decode('utf-8'))
                openFileRight = os.path.basename(openfile.name)
                root.title(f"{openFileRight} - Proton" )

#habilitar/desabilitar a menubar
def toggleMenuBar(event = None):
    global Toggle
    fakebar = tk.Menu()

    if Toggle:
        Toggle = False
    else:
        Toggle = True
    
    if Toggle:
        root.config(menu=menubar)
    else:
        root.config(menu=fakebar)

#Detectar janela em foco
def on_focus_in(event):
    global focoDireito, focoEsquerdo

    if event.widget == applabel:
        focoEsquerdo = True
        focoDireito = False
        root.title(f"{openFileLeft} - Proton")

    elif event.widget == applabel2:
        focoDireito = True
        focoEsquerdo = False
        root.title(f"{openFileRight} - Proton")

def popup(title:str,texts:str):
    pop = tk.Toplevel(bg=jsonhandler.loadSetting()['PopUpBgColor'])
    pop.geometry("600x200")
    pop.title(title)
    l = tk.Label(pop,text=texts, padx=10, pady=50, bg=jsonhandler.loadSetting()['PopUpBgColor'], font='Consolas 16', fg=jsonhandler.loadSetting()['PopUpFontColor'])
    l.grid(row=0, column=0)

def main():
    global root, menubar, applabel, applabel2, panedwindow

    #Configurações da janela principal
    root = tk.Tk()
    root.iconbitmap('icon.ico')
    root.title("Novo Documento PyText")
    root.geometry('1280x720')

    #Definição da menubar
    menubar = tk.Menu(root, relief='flat')
    
    #comandos da menubar
    filemenu = tk.Menu(menubar, relief='flat', tearoff=0, fg=jsonhandler.loadSetting()['MenuBarTextColor'], bg=jsonhandler.loadSetting()['BgColor'], font=f"{jsonhandler.loadSetting()['EditorDefaultFont']} 9")
    #Novo
    filemenu.add_command(
    label='Novo',
    accelerator='Ctrl+N',
    command=newFile
    )
    root.bind("<Control-n>", newFile)
    root.bind("<Control-N>", newFile)
    #Salvar
    filemenu.add_command(
        label='Salvar',
        accelerator='Ctrl+S',
        command=saveFile
    )
    root.bind("<Control-s>", saveFile)
    root.bind("<Control-S>", saveFile)
    #Salvar como
    filemenu.add_command(
        label='Salvar Como',
        accelerator='Ctrl+Shift+S',
        command=saveAsFile
    )
    root.bind("<Control-Shift-KeyPress-s>", saveAsFile)
    root.bind("<Control-Shift-KeyPress-S>", saveAsFile)
    #Salvar em .u2dc
    filemenu.add_command(
        label='Encriptografar e salvar',
        accelerator='Control-Alt-S',
        command=encryptSave
    )
    root.bind("<Control-Alt-KeyPress-s>", encryptSave)
    root.bind("<Control-Alt-KeyPress-S>", encryptSave)
    #Abrir
    filemenu.add_command(
        label='Abrir',
        accelerator='Ctrl+O',
        command=openFile
    )
    root.bind("<Control-o>", openFile)
    root.bind("<Control-O>", openFile)

    #Adicionar a aba na menubar
    menubar.add_cascade(menu=filemenu, label='Arquivo', underline=0)

    #Definição do bloco de texto principal
    panedwindow = tk.PanedWindow(root, relief='flat', bd=0, orient=tk.HORIZONTAL, bg=jsonhandler.loadSetting()['ScreenDivisorColor'])
    panedwindow.pack(fill=tk.BOTH, expand=True)
    #Input de texto esquerdo
    applabel = tk.Text(panedwindow, selectbackground=jsonhandler.loadSetting()['TextSelectionColor'], undo=True, relief='flat', font=(f"{jsonhandler.loadSetting()['EditorDefaultFont']} {jsonhandler.loadSetting()['EditorFontSize']} bold"))
    applabel.config(wrap='word', padx=5, pady=5, insertbackground=jsonhandler.loadSetting()['CaretColor'], bg=jsonhandler.loadSetting()['BgColor'], fg=jsonhandler.loadSetting()['TextColor'])
    panedwindow.add(applabel)
    #Input de texto direito
    applabel2 = tk.Text(panedwindow, selectbackground=jsonhandler.loadSetting()['TextSelectionColor'], undo=True, font=(f"{jsonhandler.loadSetting()['EditorDefaultFont']} {jsonhandler.loadSetting()['EditorFontSize']} bold"))
    applabel2.config(wrap='word', padx=5, pady=5, insertbackground=jsonhandler.loadSetting()['CaretColor'], bg=jsonhandler.loadSetting()['BgColor'], fg=jsonhandler.loadSetting()['TextColor'])
    
    #Habilitar input direito a partir da config.json
    if jsonhandler.loadSetting()['DoubleTextInput']:
        panedwindow.add(applabel2)  

    #Associar eventos de foco a cada uma das janelas de edição de texto
    applabel.bind('<FocusIn>', on_focus_in)
    applabel2.bind('<FocusIn>', on_focus_in)

    #Habilitar/desabilitar a filebar usando ctrl+h
    root.bind("<Control-h>", toggleMenuBar)

    return root
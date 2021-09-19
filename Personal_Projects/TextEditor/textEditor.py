# Import tkinter for creating a GUI
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import messagebox
import os
import re

#Initialise a class for the text editor
class editor:
  
    #Constructor
    def __init__(self,root):
        #Set up the base window
        self.root = root
        self.root.title("Henry's Text Editor")
        self.root.geometry("800x600")

        #Set the title of the document based on the filename
        self.fileName = None
        self.setTitle()

        #Create the menu at the top of the app, remove tear off
        self.menu = Menu(self.root, font = ("Calibri",12))
        self.root.config(menu=self.menu)

        #Create all the shortcuts in the file section of the menu
        self.fileMenu = Menu(self.menu, font = ("Calibri",12),activebackground="black", activeforeground="white", tearoff = 0)
        self.fileMenu.add_command(label="New File", accelerator = "Ctrl+N", command = self.newFile)
        self.fileMenu.add_command(label="Open", accelerator="Ctrl+O", command=self.openFile)
        self.fileMenu.add_command(label="Save file", accelerator="Ctrl+S", command=self.saveFile)
        self.fileMenu.add_command(label="Save File As", accelerator="Ctrl+F", command =self.saveAsFile)

        self.menu.add_cascade(label="File", menu = self.fileMenu)

        #Create an about button
        self.aboutMenu = Menu(self.menu, font = ("Calibri",12),activebackground="black", activeforeground="white", tearoff = 0)
        self.aboutMenu.add_command(label="About Me", command = self.displayAboutMe)

        self.menu.add_cascade(label="About", menu = self.aboutMenu)


        #On scroll, it will use the scroll bar
        scroll = Scrollbar(self.root,orient=VERTICAL)

        #Generate a text area to contain the text.
        self.textarea = Text(self.root,yscrollcommand=scroll.set,font=("Calibri",15),state="normal",relief=FLAT)

        #Pack adds this to the application. Config applies the scroll to the text area not the whole application
        scroll.pack(side=RIGHT,fill=Y)
        scroll.config(command=self.textarea.yview)
        self.textarea.pack(fill=BOTH,expand=1)

        #Set up shortcuts
        self.keyboardShortcuts()

    #When a new window is loaded up, set the title as untitled
    def setTitle(self):
        if self.fileName:
            #Use delimiter to strip the full path so we only get the file name. This won't work for all OS's
            array = re.split("/", self.fileName)
            self.root.title("Henry's Text Editor - " + array[-1])
        else:
            self.root.title("Henry's Text Editor - New Document")

    def askToClose(self):
        MsgBox = messagebox.askquestion ('Losing unsaved progress','Are you sure you want to perform this action? All unsaved data will be lost',icon = 'warning')
        if MsgBox == 'yes':
            return True
        else:
            return False

    #Inform the user they will lose all unsaved progress if they continue
    def newFile(self,*args):
            if self.askToClose() == True:
                #Reset the text editor
                self.textarea.delete("1.0",END)
                self.filename = None
                self.settitle()

    #Opening a file to the editor
    def openFile(self, *args):

        if self.askToClose() == True:
            try:
                self.fileName = filedialog.askopenfilename(title = "Choose a file to open...", filetypes = (("All Files", "*.*"), ("Text Files","*.txt")))

                #Check the file name isn't empty
                if(self.fileName):
                    #We will clear the text area and then insert the lines from the file
                    file = open(self.fileName, "r")
                    #Delete all current content
                    self.textarea.delete("1.0",END)

                    #For every line, insert it at the end of the file
                    for line in file:
                        self.textarea.insert(END,line)
                    file.close()

                    self.setTitle()

            #If there is an exception, show the user as a messagebox
            except Exception as e:
                messagebox.showerror("Exception", e)
    
    #Very similar to openFile but we will be writing to a file instead
    def saveFile(self,*args):

        try:
            #Check the file name isn't empty
            if(self.fileName):
                #Prepare to write into a file
                file = open(self.fileName, "w")

                #Get all data from the first to last line
                content = self.textarea.get("1.0",END)
                file.write(content)
                file.close()

                self.setTitle()
                messagebox.showinfo("Success", "Your data has been successfully saved")

        #If there is an exception, show the user as a messagebox
        except Exception as e:
            messagebox.showerror("Exception", e)

    def saveAsFile(self, *args):

        try:
            fileName = filedialog.asksaveasfilename(title = "Save file as name:", defaultextension=".txt", initialfile = "Untitled.txt", filetypes = (("All Files", "*.*"), ("Text Files","*.txt")))
            #Prepare to write into a file
            file = open(fileName, "w")

            #Get all data from the first to last line
            content = self.textarea.get("1.0",END)
            file.write(content)
            file.close()

            self.fileName = fileName
            self.setTitle()
            messagebox.showinfo("Success", "Your data has been successfully saved")

        #If there is an exception, show the user as a messagebox
        except Exception as e:
            messagebox.showerror("Exception", e)

    def displayAboutMe(self):

        messagebox.showinfo('About Henry Gann','This text editor was developed over September 2021 by Henry Gann')

    #Bind all my shortcuts to the text area
    def keyboardShortcuts(self):
        root.bind("<Control-n>", self.newFile)
        root.bind("<Control-s>", self.saveFile)
        root.bind("<Control-f>", self.saveAsFile)
        root.bind("<Control-o>", self.openFile)

#Set up the root pane and pass it to the class for initialization
root = Tk()
editor(root)

#Keep the application running
root.mainloop()
from tkinter import *
from tkinter import font as tkFont
from bs4 import BeautifulSoup
import requests
import os
import random

#this is the main window
class Window1:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master
        #changing directories
        os.chdir(os.getcwd()+r"\files")
        # Upper Frame
        self.uframe=Frame(self.master, width=width_value, height=50)
        self.uframe.grid(row=0, column=0)
        self.uframe.grid_propagate(False)
        self.mainheading=Label(self.uframe, text="GRE WORDS", font=helv20)
        self.mainheading.place(relx=0.5, rely=0.5, anchor="center")
        # Lower Frame
        self.lframe=Frame(self.master, width=width_value, height=height_value-50)
        self.lframe.grid(row=1, column=0)
        self.lframe.grid_propagate(False)
        # Lower Frame - Add Frame
        self.addframe=Frame(self.lframe, width=width_value*0.6, height=height_value-50, relief=GROOVE, bd=3)
        self.addframe.grid(row=0, column=0)
        self.addframe.grid_propagate(False)
        # Add Frame widgets
        self.addheading=Label(self.addframe, text="ADD NEW WORDS", font=times15)
        self.addheading.grid(row=1, column=1, columnspan=2)
        self.decklabel=Label(self.addframe, text="Enter name of deck:", font=times15)
        self.decklabel.grid(row=2, column=1, sticky=NW, pady=20)
        self.deckentry=Entry(self.addframe, width=53)
        self.deckentry.grid(row=2, column=2, sticky=W, padx=40)
        self.wordlabel=Label(self.addframe, text="Words:", font=times15)
        self.wordlabel.grid(row=3, column=1, sticky=NW)
        self.wordtextbox=Text(self.addframe, height=15, width=40)
        self.wordtextbox.grid(row=3, column=2, sticky=NW, padx=40)
        self.add_button=Button(self.addframe, text="Add", width=20, command=self.get_items)
        self.add_button.grid(row=4, column=1, columnspan=2, pady=20)
        self.warning=Label(self.addframe)
        self.warning.grid(row=5, column=1, columnspan=2)

        self.addframe.grid_columnconfigure(0, weight=1)
        self.addframe.grid_columnconfigure(3, weight=1)

        #Lower Frame - Rev frame
        self.revframe=Frame(self.lframe, width=width_value*0.4, height=height_value-50, relief=GROOVE, bd=3)
        self.revframe.grid(row=0, column=1)
        self.revframe.grid_propagate(False)
        #heading frame in rev frame
        self.hframe2=Frame(self.revframe, width=width_value*0.4, height=25)
        self.hframe2.grid(row=0, column=0)
        self.hframe2.grid_propagate(FALSE)

        self.revlabel=Label(self.hframe2, text="REVISE WORDS", font=times15)
        self.revlabel.place(relx=0.5, rely=0.5, anchor="center")
        #content frame in rev frame
        self.cframe2=Frame(self.revframe, width=width_value*0.4, height=height_value-50-25)
        self.cframe2.grid(row=1, column=0)
        self.cframe2.grid_propagate(False)

        self.blframe=Frame(self.cframe2, bd=1, relief="sunken")                        # frame for listbox and scrollbar
        self.blframe.pack(pady=20)

        self.scrollbar=Scrollbar(self.blframe)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox=Listbox(self.blframe, width=50, height=30, borderwidth=0, highlightthickness=0, background=self.blframe.cget("bg"))
        self.listbox.pack(side=LEFT)
        # inserting data in listbox
        arr_files=os.listdir()
        for i in range(len(arr_files)):
            self.listbox.insert(END, arr_files[i].replace(".txt",""))

        #attach listbox to scrollbar
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.rev_button=Button(self.cframe2, text="Revise", width=20, command=self.revbut)
        self.rev_button.pack(side=BOTTOM, pady=20)

    def get_items(self):
        deckname=self.deckentry.get()
        textboxdata=self.wordtextbox.get("1.0", 'end-1c')       #1.0 means that the input should be read from line one, character zero
                                                                #The end part means to read until the end of the text box is reached and -1c deletes 1 character from end as by default the text box adds a newline at end.
        self.workonwords(textboxdata,deckname)

    def workonwords(self, textboxdata,deckname):
        if deckname!='':
            url='https://www.dictionary.com/browse/'
            word_list=textboxdata.split(',')
            dict={}
            notfound=[]                                            # array of words not found
            for word in word_list:
                page=requests.get(url+word)
                soup=BeautifulSoup(page.content, 'html.parser')
                meaning=soup.find(class_='css-1o58fj8 e1hk9ate4')
                try:
                    meaning=meaning.text         # Multiple meanings on the web are separated by '.'
                    dict[word]=meaning
                except:
                    notfound.append(word)
            filename=deckname+".txt"
            file_obj = open(filename, 'a')
            for key in dict:
                file_obj.write(key)
                file_obj.write('$')
                file_obj.write(dict[key])
                file_obj.write('\n')
            file_obj.close()
            if not notfound:
                self.warning.config(text="")
            else:
                nfwrds=""
                for i in notfound:
                    nfwrds=nfwrds+i+', '
                nfstr="**The following words were not found: "+nfwrds
                self.warning.config(text=nfstr, fg="red")
        else:
            self.warning.config(text="File name is missing!", fg="red")

    def revbut(self):
        try:
            # reverting to original working directory before going to next window
            original_dir=os.getcwd().replace(r"\files",'')
            os.chdir(original_dir)
            # getting the value of selected item in listbox
            clicked_item=self.listbox.curselection()                        # returns tuple containing indexes of selected items
            selected_file=self.listbox.get(clicked_item)
            #destroying all the elements
            elements=[self.uframe, self.lframe]
            for element in elements:
                element.destroy()
            # passing root and selected file to window2 class
            self.another = Window2(self.master, selected_file)
        except:
            pass

#this is the revision window
class Window2:
    ptr = -1
    def __init__(self, master, selected_file):
        self.selected_file=selected_file
        self.master=master
        # Images for the buttons
        os.chdir(os.getcwd()+r"\icons")
        self.previmg=PhotoImage(file="prev.png")
        self.previmg = self.previmg.subsample(3, 3)
        self.nextimg=PhotoImage(file="next.png")
        self.nextimg = self.nextimg.subsample(3, 3)

        # Key bindings
        self.master.bind("<space>", lambda event: self.meaningfunc())
        self.master.bind("<Left>", lambda event: self.prevfunc())
        self.master.bind("<Right>", lambda event: self.nextfunc())

        self.heading=Label(self.master, text=self.selected_file, font=helv20)
        self.heading.grid(row=0, column=2, pady=10)
        self.prev=Button(self.master, image=self.previmg, width=50, height=50, command=self.prevfunc)
        self.prev.grid(row=1, column=1)

        self.word_frame=Frame(self.master, bd=3, width=500, height=200, relief=GROOVE)
        self.word_frame.grid(row=1, column=2, pady=20, padx=30)
        self.word_frame.grid_propagate(False)
        self.wlb=Label(self.word_frame, text="Let's Begin...", font=helv20)
        self.wlb.place(relx=0.1, rely=0.5, anchor="w")

        self.next=Button(self.master, image=self.nextimg, width=50, height=50, command=self.nextfunc)
        self.next.grid(row=1, column=3)
        self.check=Button(self.master, text="Check Meaning", command=self.meaningfunc)
        self.check['font'] = helv15
        self.check.grid(row=2, column=2)
        self.meaning_frame=Frame(self.master, bd=3, width=500, height=300, relief=GROOVE)
        self.meaning_frame.grid(row=3, column=2, pady=20)
        self.meaning_frame.grid_propagate(False)
        note="**Key bindings: <- for previous, -> for next, space to see meaning."
        self.note=Label(self.master, text=note, fg="red")
        self.note.grid(row=4, column=1, columnspan=3)

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(4, weight=1)

        #Adding meaning text area
        self.tbscb=Scrollbar(self.meaning_frame)
        self.tbscb.pack(side=RIGHT, fill=Y)
        self.meaningtb=Text(self.meaning_frame, width=60, height=17)
        self.meaningtb.pack(side=LEFT)
        self.meaningtb.config(state=DISABLED)
        self.meaningtb.config(yscrollcommand=self.tbscb.set)
        self.tbscb.config(command=self.meaningtb.yview)

        self.extracting()

    def cleanup_textbox(self):
        self.meaningtb.config(state=NORMAL)
        self.meaningtb.delete('1.0', END)
        self.meaningtb.config(state=DISABLED)

    def extracting(self):
        original_dir=os.getcwd().replace(r"\icons",'')
        os.chdir(original_dir+r"\files")
        self.dict2={}
        file_name=self.selected_file + ".txt"
        file_obj=open(file_name,"r")
        l=file_obj.readlines()
        for element in l:
            temp=element.split('$')
            self.dict2[temp[0]]=temp[1]
        file_obj.close()
        # now self.dict2 has the words as keys and meanings as their meanings as the values
        self.listkeys=list(self.dict2.keys())
        random.shuffle(self.listkeys)

    def meaningfunc(self):
        '''
        1. enable state
        2. clear text area
        3. insert text
        4. disable state
        '''
        try:
            key=self.listkeys[Window2.ptr]
            meaning=self.dict2[key]
            meaning=meaning.replace('.','\n')
            self.meaningtb.config(state=NORMAL)
            self.meaningtb.delete('1.0', END)
            self.meaningtb.insert('1.0', meaning)
            self.meaningtb.config(state=DISABLED)
        except:
            self.meaningtb.insert('1.0', "No more words")

    def nextfunc(self):
        Window2.ptr= Window2.ptr + 1
        self.cleanup_textbox()
        try:
            word=self.listkeys[Window2.ptr]
            self.wlb.config(text=word)
        except:
            self.wlb.config(text="NO MORE WORDS !!")

    def prevfunc(self):
        Window2.ptr = Window2.ptr-1
        self.cleanup_textbox()
        try:
            word=self.listkeys[Window2.ptr]
            self.wlb.config(text=word)
        except:
            self.wlb.config(text="NO MORE WORDS !!")

root=Tk()
helv20 = tkFont.Font(family='Helvetica', size=20, weight=tkFont.BOLD)
helv15 = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)
times15 = tkFont.Font(family='Times', size=15, weight=tkFont.BOLD)
times15nb = tkFont.Font(family='Times', size=15)

width_value=root.winfo_screenwidth()
height_value=root.winfo_screenheight()
root.geometry("%dx%d"%(width_value, height_value))
run=Window1(root)
root.mainloop()

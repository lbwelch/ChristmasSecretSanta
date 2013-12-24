#!/usr/local/bin/python

from Tkinter import *
from donors import *
import tkFileDialog
import tkMessageBox
import re
import string
import tkSimpleDialog

NAMES = ["Name1", "Name2", "Name3", "Name4", "Name5", "Name6"]
SPOUSES = {"Name6":"Name4", "Name4":"Name6", "Name5":"Name3", "Name3":"Name5"}

class previousRecipientsDialog(tkSimpleDialog.Dialog):
    def body(self, master):
        self.lastRecipients = {}
        self.rows = range(len(NAMES))
        for (name, num) in zip(NAMES, self.rows):
            Label(master, text=name).grid(row=num, sticky=W)

        self.entries = []
        for name in NAMES:
            self.entries.append(Entry(master))

        for (entry, num) in zip(self.entries, self.rows):
            entry.grid(row=num, column=1)
        return self.entries[0]                  # initial focus

    def apply(self):
        self.lastRecipients = {}
        for (donor, entry, row) in zip(NAMES, self.entries, self.rows):
            self.lastRecipients[donor] = entry.get()
        for donor in self.lastRecipients:
            print donor, self.lastRecipients[donor]

class App(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.donors = Donors(NAMES, SPOUSES)
        self.grid()
        self.filename = None
        self.setupWidgets(master)
        self.setupMenus(master)
        self.setupDialogs()

    def setupWidgets(self, master):
        master.geometry("+100+100")
        master.update_idletasks()
        master.title("Merry Xmas!")
        master.grid()
        master.columnconfigure(0, pad=10)
        for num in range(len(NAMES)):
            master.rowconfigure(num, pad=5)

        # Create a button for each donor
        buttons = []
        for name in NAMES:
            buttonName = name.lower()
            buttons.append(Button(master, name=buttonName, text=name, width=13))
        for button in buttons:
            button.bind("<Button-1>", self.buttonClick)
            button.grid()
        
        # Create a label to reveal the recipient's name when a donor's
        # name button is clicked.
        self.recipientLabel = Label(master, width=15, relief="ridge", \
                                        text="Press a button")
        self.recipientLabel.grid(padx=10, pady=10)

    def setupMenus(self, master):
        self.menu = Menu(master)
        master.config(menu=self.menu)
        self.fileMenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="Open...", command=self.openDonorsFile)
        self.fileMenu.add_command(label="Save", command=self.saveDonorsFile)
        self.extrasMenu = Menu(self.menu)
        self.menu.add_cascade(label="Extras", menu=self.extrasMenu)
        self.extrasMenu.add_command(label="Edit Previous Recipients", 
                                    command=self.editPreviousRecipients)
        self.extrasMenu.add_command(label="Reshuffle", command=self.reshuffle)
        self.extrasMenu.add_command(label="Statistics", command=self.runStats)
        self.extrasMenu.add_command(label="View Data", command=self.viewData)

    def setupDialogs(self):
        print "in setupDialogs()"

    def resetRecipientLabel(self):
        self.recipientLabel.configure(text="Press a button")

    def openDonorsFile(self):
        self.filename = tkFileDialog.askopenfilename(\
            defaultextension="xmas", parent=self, initialdir=".")
        if (self.filename):
            self.inputFile = open(self.filename, 'r')
            donorRecipients = []
            for line in self.inputFile:
                donorRecipient = line.rstrip()
                donorRecipients.append(donorRecipient)
            self.donors.setRecipients(donorRecipients)
            self.inputFile.close()

    def saveDonorsFile(self):
        if (self.filename):
            self.filename = tkFileDialog.asksaveasfilename(
                defaultextension="xmas", parent=self, initialfile=self.filename)
        else:
            self.filename = tkFileDialog.asksaveasfilename(
                defaultextension="xmas", parent=self, initialdir=".")
        if (self.filename):
            print self.donors.str()
            self.outputFile = open(self.filename, 'w')
            self.outputFile.write(self.donors.str())
            self.outputFile.close() 

    def editPreviousRecipients(self):
        d = previousRecipientsDialog(root)
        if len(d.lastRecipients) == 6:
            self.donors.setLastRecipients(d.lastRecipients)

    def reshuffle(self):
        self.donors.shuffleRecipients()
        self.recipientLabel.configure(text="Shuffling")
        self.after(3000, self.resetRecipientLabel)

    def runStats(self):
        print "\nRunning Stats...\n"
        # Create stats grid
        annRow = {"Name1":0, "Name2":0, "Name3":0, "Name4":0, 
                  "Name5":0, "Name6":0}
        morsesRow = annRow.copy()
        lauraRow = annRow.copy()
        michelleRow = annRow.copy()
        jamesRow = annRow.copy()
        bradRow = annRow.copy()
        jonathanRow = annRow.copy()
        gridDict = {'Name1':Name1Row, 'Name2':Name2Row, 'Name3':Name3Row, 
                    'Name4':Name4Row, 'Name5':Name5Row, 'Name6':Name6Row}
                
        # Run the stats
        for i in range(1000):
            self.donors.shuffleRecipients()
            for donor in self.donors.donors.values():
                gridDict[donor.name][donor.recipient] += 1

        # Print the results
        names = gridDict.keys()

        print "   ",
        for name in names:
            print name[:3],
        print
        for name in names:
            print name[:3],
            for key in gridDict.keys():
                print "%3d" % gridDict[name][key],
            print

    def viewData(self):
        if tkMessageBox.askquestion(
                "View Data", "View the secret recipient data?", parent=self):
            tkMessageBox.showinfo("Current Data", self.donors.str())

        
    def buttonClick(self, event):
        # Create a regex to trim the word "Button" off of each button name
        nameTrim = re.compile(r'Button$')

        # Use the regex to get the name of the donor from the name of the
        # button that was clicked, capitalize the first letter, then use that
        # string to get the donor's recipient.
        donorName = event.widget.winfo_name()
        donorName = re.sub(nameTrim, '', donorName).capitalize()
        print donorName
        recipientName = self.donors.donors[donorName].recipient 

        # Display donor name for 3 seconds
        self.recipientLabel.configure(text=recipientName)
        self.after(3000, self.resetRecipientLabel)

root = Tk()
app = App(root)
root.mainloop()

#parent class can be initialized later then the derived class?

from GradeCalculator import create, Subject, print_all, add_subject, delete_sub
import tkinter as tk
from tkinter import Entry, W, E, Message, StringVar, Text, END
from tkinter import font  as tkfont
import sqlite3

#Application class inheriting from tkinter's Tk class
class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)    #initializing parent class
        self.title_font = tkfont.Font(family='Times', size=60,
                                      weight="bold")
        self._frame = None
        #calling shoe_frame function to show main page
        self.show_frame(MainPage)
        self.student_name=""
        self.title("Grade calculator")

        

    #this function takes the name of class and creates a frame and packs
    #it to the parent frame to display. If there is already another frame
    #in the parent frame then it destroys it
    def show_frame(self, frame_class):
        new_frame = frame_class(self,controller=self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    #this functions takes the name of the class name and creates the object
    #pf that class and lets access to the functions and variables
    def get_page(self, page_class):
        new_frame = page_class(self,controller=self)
        return new_frame

    def numValidate(self, P):
        if (P !=""):
            try:
                int(P)
                return True
            except:
                self.bell()
                return False
        else:
            return false

#First page to be displayed in the parent frame 
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #initializing parent class
        self.controller = controller

        #Labels to be displayed
        label = tk.Label(self, text="Welcome to the Grade Calculator", anchor="center", bg="lavender",
                         font = controller.title_font)
        label1 = tk.Label(self, text="Please enter your name to start:",
                          font="times 30", bg="lavender")

        #entry 
        self.entry = Entry(self,bg = "yellow")
        button1 = tk.Button(self, text="Save and Continue",
                            command= lambda: self.cmmd(), height =3,
                             bg="green")

        #gridding
        label.grid(row=3, column=0, rowspan=2, columnspan=10, sticky="EW")
        label1.grid(row=14, rowspan=3, column=0, sticky=E)
        self.entry.grid(row=14,rowspan=3,column=1, sticky="E")
        button1.grid(row = 19,column=1, sticky=W+E)


    #this function saves the typed name into student_name and displays the menupage frame
    def cmmd(self):
        self.controller.student_name = self.entry.get()
        print(self.controller.student_name)
        create(self.controller.student_name)
        self.controller.show_frame(MenuPage)

#menu page to be displayed
class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        
        #labels and buttons to be displayed
        label = tk.Label(self, text="Here is the options for you", bg="lavender",
                        font=controller.title_font)
        button1 = tk.Button(self, text="Print your progress so far",
                            command= lambda: controller.show_frame(PrintPage),
                            height=2)
        button2 = tk.Button(self, text="Add a subject with Grades only",
                            command= lambda: controller.show_frame(AddPage),
                            height=2)
        button3 = tk.Button(self, text="Add subject with full information",
                            command=lambda: controller.show_frame(FullAddPage),
                            height=2)
        button5 = tk.Button(self, text="Delete a subject",
                            command=lambda:controller.show_frame(Delete),
                            height=2)
        button6 = tk.Button(self, text="Go to main Page",
                            command= lambda: controller.show_frame(MainPage),
                            height=2)

        #gridding
        label.grid()
        button1.grid(row=1, rowspan=2, sticky=W+E)
        button2.grid(row=3, sticky=W+E)
        button3.grid(row=5, sticky=W+E)
        button5.grid(row=7, sticky=W+E)
        button6.grid(row=9, sticky=W+E)

#print page to be displayed along with the data of user
class PrintPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        
        label = tk.Label(self, text="Your progess so far:")

        #getting data as a string from database using print_all function
        whole_data= print_all(controller.student_name)

        text = Text(self, height=20, width=80)
        text.insert(END, whole_data)

        button = tk.Button(self, text ="Home Page",
                           command=lambda:controller.show_frame(MenuPage),
                           height=2)

        #gridding
        label.grid()
        text.grid(row=1)
        button.grid(row=3,column=0,sticky=W+E)
        print(whole_data)
        
        
#full add page for adding subject with full information
class FullAddPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #labels and entry
        label = tk.Label(self, text="Please enter all your details carefully",
                         font=controller.title_font, bg="lavender")
        vcmd = (self.register(controller.numValidate), '%P')
        
        label_subject = tk.Label(self, text="Name of the subject: ",bg="lavender")
        self.subject = Entry(self)
        
        label_credit = tk.Label(self,text="Credit hours:",bg="lavender")
        self.credit = Entry(self, validate="key", validatecommand=vcmd)

        label_exam = tk.Label(self, text="Percentage in exam:",bg="lavender")
        self.exam = Entry(self, validate="key", validatecommand=vcmd)
        label_weight = tk.Label(self, text="Weight in it:",bg="lavender")
        self.weight_exam = Entry(self, validate="key", validatecommand=vcmd)

        label_weight1 = tk.Label(self, text="Weight in it:",bg="lavender")
        label_weight2 = tk.Label(self, text="Weight in it:",bg="lavender")
        label_weight3 = tk.Label(self, text="Weight in it:",bg="lavender")
        
        label_final = tk.Label(self, text="Percentage in final:",bg="lavender")
        self.final = Entry(self,validate="key", validatecommand=vcmd)
        self.weight_final = Entry(self, validate="key", validatecommand=vcmd)

        label_assignment = tk.Label(self, text="Percentage in assignment:"
                                    ,bg="lavender")
        self.assignment = Entry(self, validate="key", validatecommand=vcmd)
        self.weight_assignment = Entry(self, validate="key", validatecommand=vcmd)
        label_others = tk.Label(self, text="Percentage in others:",bg="lavender")
        self.others = Entry(self, validate="key", validatecommand=vcmd)
        self.weight_others = Entry(self, validate="key", validatecommand=vcmd)

        button1 = tk.Button(self, text="Save and Continue",
                            command=lambda: self.save_all(),bg="lavender",
                            height = 2)
        
                            
        #gridding
        label.grid(columnspan=5)
        label_subject.grid(row=19, column=0, sticky=E)
        self.subject.grid(row=19,column=1, sticky=W)

        label_credit.grid(row=20,column=0, sticky=E)
        self.credit.grid(row=20,column=1, sticky=W)

        label_exam.grid(row=21,column=0)
        self.exam.grid(row=21, column=1)
        label_weight.grid(row=21, column=2)
        self.weight_exam.grid(row=21,column=3)

        label_final.grid(row=22,column=0)
        self.final.grid(row=22, column=1)
        label_weight1.grid(row=22, column=2)
        self.weight_final.grid(row=22,column=3)

        label_assignment.grid(row=23,column=0)
        self.assignment.grid(row=23, column=1)
        label_weight2.grid(row=23, column=2)
        self.weight_assignment.grid(row=23,column=3)

        label_others.grid(row=24,column=0)
        self.others.grid(row=24, column=1)
        label_weight3.grid(row=24, column=2)
        self.weight_others.grid(row=24,column=3)

        button1.grid(column = 2, row=25, sticky="EW")

    #this function creates tuple from the data entered by user and updates the db with it
    def save_all(self):
        try:
            sub = Subject(self.subject.get(), self.credit.get())
            
            sub.exams, sub.exams_weight, sub.final, sub.final_weight, sub.assignment, \
            sub.assignment_weight, sub.others, sub.others_weight = int(self.exam.get()), \
            int(self.weight_exam.get()), int(self.final.get()), int(self.weight_final.get()), int(self.assignment.get()), \
            int(self.weight_assignment.get()), int(self.others.get()), int(self.weight_others.get())
            data = (sub._name, sub.percentCalc(), sub._hour,
               sub.gradeCalc(), sub.weightCalc(sub.exams, sub.exams_weight), sub.weightCalc(sub.final,sub.final_weight),
                    sub.weightCalc(sub.assignment, sub.assignment_weight), sub.weightCalc(sub.others,sub.others_weight))
            add_subject(self.controller.student_name, data)
        except (ValueError, sqlite3.OperationalError) as e:
            print("wrong information")
        #show the menu page after subject is added
        self.controller.show_frame(MenuPage)


class AddPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_main = tk.Label(self, text="Enter all your details carefully",
                              font=controller.title_font)

        label1 =tk.Label(self, text="Name of the subject")
        self.name = Entry(self)

        vcmd = (self.register(controller.numValidate), '%P')
        label2 = tk.Label(self,text="Credit Hours")
        self.hours = Entry(self, validate="key", validatecommand=vcmd)

        label3 = tk.Label(self, text="Grade")
        self.grade = Entry(self)

        button1 = tk.Button(self, text="Save and Continue", command=lambda: self.save_all())


        #gridding
        label_main.grid()
        label1.grid(row=1)
        self.name.grid(row=1,column=1)
        label2.grid(row=2)
        self.hours.grid(row=2,column=1)
        label3.grid(row=3)
        self.grade.grid(row=3,column=1)
        button1.grid(row=5)


    def save_all(self):
        sub = Subject(self.name.get(), self.hours.get())
        row = (sub._name, 0, sub._hour, self.grade.get().upper(), 0,0,0,0)
        try:
            add_subject(self.controller.student_name, row)
        except (ValueError, sqlite3.OperationalError) as e:
            print("wrong information!!")
            
        self.controller.show_frame(MenuPage)

class Delete(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label= tk.Label(self, text="Please enter the name of the subject you want to delete",
                        font="times 28", bg="lavender")
        self.name = Entry(self)
        button1 = tk.Button(self, text="Save and Continue", command=lambda: self.save_all())

        
        label.grid(row=0,column=0, rowspan=100)
        self.name.grid(row=2)
        button1.grid(row=3)
        
    def save_all(self):
        delete_sub(self.controller.student_name, self.name.get())
        self.controller.show_frame(MenuPage)
        

app = Application()
app.geometry("1000x500")
app.configure(bg="lavender")
app.mainloop()

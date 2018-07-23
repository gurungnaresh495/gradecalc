import sqlite3

#creating connection with the database
conn = sqlite3.connect('data3.db')
c = conn.cursor()

#Subject class for all the prompted data
class Subject():
    #Constructor
    def __init__(self, name, hour):
        self._name = name
        self._hour = hour

    #variables
    sub_no  = 0
    grade = " "
    percent = 0
    exams = 0
    exams_weight = 0
    final = 0
    final_weight = 0
    assignment = 0
    assignment_weight = 0
    others = 0
    others_weight = 0

    #variables for grade
    A, B, C, D = 90, 80, 70, 60
    

    #this function takes percentage on the subject and its weight to calculate
    #the weight it contributes
    def weightCalc(self, percentage, weight):
        return (percentage * weight) / 100

    #this function calculates the percentage so far
    def percentCalc(self):
        self.percent = self.exams + self.final + self.assignment + self.others
        return self.percent

    #this function calculates the grade according to the percentage on that subject
    def gradeCalc(self):
            if (self.percent >= self.A):
                    self.grade = 'A'
            elif (self.percent >= self.B):
                    self.grade = 'B'
            elif (self.percent >= self.C):
                    self.grade = 'C'
            elif (self.percent >= self.D):
                    self.grade = 'D'
            else:
                    self.grade = 'F'
            return self.grade




#this function prompts the user for the information of the subjects
#creates a tuple with it and inserts in the database
def add_subject(name_stud, data):
    c.execute("INSERT INTO " + name_stud + " VALUES (?,?,?,?,?,?,?,?)", data)
    conn.commit()

def delete_sub(name_stud, sub):
    data = c.execute("DELETE FROM " + name_stud + " WHERE Subject=?", (sub,))
    conn.commit()

#this function calculates the G.P.A. from the grade and credit hours from databse
def calc_gpa(name_stud):
    c.execute("SELECT Grade, Credit_hours  from " + name_stud)
    grades = (c.fetchall())
    runningTotal = credit_count = 0

    for row in grades:
        (grade, hour) = tuple(row)
        if (grade == 'A'):
                runningTotal += hour * 4
                credit_count += hour
        elif (grade == 'B'):
                runningTotal += 3 * hour
                credit_count += hour
        elif (grade == 'C'):
                runningTotal += 2 * hour
                credit_count += hour
        elif (grade == 'D'):
                runningTotal += 1 * hour
                credit_count += hour

    return(runningTotal / credit_count)
        
#this function prints the gpa as well as the the list of grades     
def print_result(name_stud):
    gpa = calc_gpa(name_stud)
    print("\nYour G.P.A so far is {}.\n\n".format(gpa))
    

def print_all(name_stud):
    whole_data = ("\n{:^15}|{:^8}|{:^8}|{:^5}|{:^8}|{:^8}|{:^12}|{:^8} ".format("Subject", "Percent",
                                                                "Credit", "Grade", "Exam",
                                                                "Final", "Assignment", "Others"))
    
    try:
        c.execute("SELECT * FROM " + name_stud)
        grades = c.fetchall()
        for row in grades:
            (subject, percentage, credit, grade, exam, final, assignment, others) = tuple(row)
            chunk = ("{:^15}|{:^8}|{:^8}|{:^5}|{:^8}|{:^8}|{:^12}|{:^8}\n".format(subject, percentage, credit,
                                                  grade, exam, final, assignment, others))
            whole_data += chunk
    except sqlite3.OperationalError:
        print("nothing")
    return whole_data

def create(student_name):
    try:
        c.execute("CREATE TABLE " + student_name + " (Subject text,\
                    Percentage real, Credit_hours real, Grade text, Exams real, Final real,\
                    Assignment real, others real)")
        
        conn.commit()
        message = "Looks like its your first time"
    except sqlite3.OperationalError:
        message = "Looks like we already met (^_^)"
    return message

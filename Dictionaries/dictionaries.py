#example of dictionrie
friend_ages = {"Rolf":24,"Adam":30,"Anne":27}

friend_ages["Bob"] = 20

#print(friend_ages["Bob"])

###
#list of dicionaries

friends =[
    {"Name ": "Rolf", "age":24},
    {"Name":"Adam", "age":30},
    {"Name":"Anne","age":27}
]

print(friends[1]["Name"]) #this way we access the item in the dic, and the second [] gives what value we want.


###
#Using loops

student_attendance = {"Rolf":96,"Bob":80,"Anne":100}

for student in student_attendance:
    #print(student)
    #print(f"{student}: {student_attendance[student]}") # gives the key and the student togther/
    print("")

#second loop-using mulitp var
for student,attendance in student_attendance.items():
    print(f"{student}:{attendance}")


#using if statments
if "Bob" in student_attendance:
    print(f"Bob:{student_attendance['Bob']}")
else:
    print("Bob is not a student in this class.")

#functions
attendance_values = student_attendance.values() #will give the sum of all the values.
print(sum(attendance_values)/len(student_attendance))
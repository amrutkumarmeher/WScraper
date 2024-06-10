import requests
import pyinputplus as pyin
import json as js
import pandas as pd

print(r"""
         ████████                                   ___====-_  _-====___
     ██▀▀▀░░░░░░░▀▀▀██                        _--^^^#####//      \\#####^^^--_
   █▀░░░░░░░░░░░░░░░░░▀█                   _-^##########// (    ) \\##########^-_
  █│░░░░░░░░░░░░░░░░░░░│██                -############//  |\^^/|  \\############-
 █▌│░░░░░░░░░░░░░░░░░░░│▐██             _/############//   (@::@)   \\############\_
 █░└┐░░░░░░░░░░░░░░░░░┌┘░██            /#############((     \\//     ))#############\\
 █░░└┐░░░░░░░░░░░░░░░┌┘░░██           -###############\\    (oo)    //###############-
 █░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██          -#################\\  / VV \  //#################-
  ▌░│██████▌░░░▐██████│░▐█          -###################\\/      \//###################-
  █░│▐███▀▀░░▄░░▀▀███▌│░██         _#/|##########/\######(   /\   )######/\##########|\#_
 █▀─┘░░░░░░░▐█▌░░░░░░░└─▀██        |/ |#/\#/\#/\/  \#/\##\  |  |  /##/\#/  \/\#/\#/\#| \|
 █▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██        `  |/  V  V  `   V  \#\| |  | |/#/  V   '  V  V  \|  '
  ██▄─┘██▌░░░░░░░▐██└─▄██             `   `  `      `   / | |  | | \   '      '  '   '
   ██░░▐█─┬┬┬┬┬┬┬─█▌░░██                               (  | |  | |  )
   █▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐█                              __\ | |  | | /__
    █▄░░░└┴┴┴┴┴┴┴┘░░░▄█                              (vvv(VVV)(VVV)vvv)
     ██▄░░░░░░░░░░░▄██     
       ███▄▄▄▄▄▄▄███
                          

                    
                       ╭━━━┳━━━┳━━━━┳╮╱╱╭┳━━━┳━━━━╮  ╭━━━┳━━━╮
                       ┃╭━╮┃╭━╮┃╭╮╭╮┃╰╮╭╯┃╭━━┫╭╮╭╮┃  ┃╭━╮┃╭━╮┃
                       ┃╰━━┫┃╱╰┻╯┃┃╰┻╮┃┃╭┫╰━━╋╯┃┃╰╯  ┃╰━╯┃╰━╯┃
                       ╰━━╮┃┃╱╭╮╱┃┃╱╱┃╰╯┃┃╭━━╯╱┃┃╱╱  ┃╭╮╭┫╭╮╭╯
                       ┃╰━╯┃╰━╯┃╱┃┃╱╱╰╮╭╯┃╰━━╮╱┃┃╱╱  ┃┃┃╰┫┃┃╰╮
                       ╰━━━┻━━━╯╱╰╯╱╱╱╰╯╱╰━━━╯╱╰╯╱╱  ╰╯╰━┻╯╰━╯
                       
                       
                       made by:
                           Amrut Kumar Meher
                           CSE batch - 2023-26
                           Govt. Polytechnic, Bargarh

""")

class RegistrationFormatError(Exception):
    def __init__(self, rege, *args: object) -> None:
        message = f"Incorrect format of Registration no {rege}!"
        super().__init__(message, *args)


class SemesterNoError(Exception):
    def __init__(self, semno, *args: object) -> None:
        message = f"Incorrect semester no : {semno}"
        super().__init__(message, *args)


class ExamYearError(Exception):
    def __init__(self, year, *args: object) -> None:
        message = f"Incorrect Semester no: {year}"
        super().__init__(message, *args)


class WrongDirPath(Exception):
    def __init__(self,*args: object) -> None:
        message = f"Directory Path is wrong!"
        super().__init__(message,*args)

def validateRege(Rege: str):
    if len(Rege) == 12 and Rege.startswith(("F", "L")):
        no = Rege.replace("F", "")
        no = no.replace("L", "")
        if no.isnumeric():
            return Rege
        else:
            raise RegistrationFormatError(Rege)
    else:
        raise RegistrationFormatError(Rege)


def validate_sem(sem: str):
    if sem <= 6 and sem > 0:
        return sem
    else:
        raise SemesterNoError(sem)


def validate_year(year: str):
    if year.startswith(("s", "w")):
        actual_year = year.replace("s", "")
        actual_year = actual_year.replace("w", "")
        if (
            actual_year.isnumeric()
            and int(actual_year) > 2000
            and int(actual_year) < 2050
        ):
            return year
        else:
            raise ExamYearError(year)
    else:
        raise ExamYearError(year)
    

def validate_dir(dir: str):
    if dir.endswith("/"):
        return dir
    else:
        raise WrongDirPath
    
    

rollno = validateRege(pyin.inputStr("Enter Redgistration No: "))
semester = validate_sem(pyin.inputNum("Enter semester no: "))
year = validate_year(input("Enter Examination year([s/w]<year>): "))
to_save_loc = input("Enter directory location where you wanna save(eg. \\hi\\): ")
api_link = (
    f"https://sctevtexams.in/student-result-{year}?sem=0{semester}&rollNo={rollno}"
)
result = requests.get(api_link).text
if len(result) < 100 : 
    print("The registration number not found!")
    exit()

result = js.loads(result)
student_Info = [
    ["Name", result["studentInfo"]["studentName"]],
    ["StudentID:", result["studentInfo"]["studentID"]],
    ["StudentRegdNo", result["studentInfo"]["registrationNumber"]],
    ["DateOfBirth", result["studentInfo"]["doa"]],
    ["Sex", result["studentInfo"]["gender"]],
    ["Address", result["studentInfo"]["presentAddress1"]],
    ["course", result["studentInfo"]["courseName"]],
    ["Result", result["result"]],
]


A = ["Subject Code"]
A.extend([i["paperTypeCode"] for i in result["marksData"]]),
B = ["Sudject Name"]
B.extend([i["subjectName"] for i in result["marksData"]]),
C = ["TH FullM"]
C.extend([i["semYearFullMark"] for i in result["marksData"]]),
D = ["IA FullM"]
D.extend([i["internalFullMark"] for i in result["marksData"]]),
E = ["Total Marks"]
E.extend([i["totalFullMark"] for i in result["marksData"]]),
F = ["PassMark"]
F.extend([i["totalPassMark"] for i in result["marksData"]]),
G = ["TH secured"]
G.extend([i["securedTH"] for i in result["marksData"]]),
H = ["IA secured"]
H.extend([i["securedIA"] for i in result["marksData"]]),
I = ["Total secured"]
I.extend([i["securedTotal"] for i in result["marksData"]])

Marksheet = [A, B, C, D, E, F, G, H, I]
studentinfo_df = pd.DataFrame(
    student_Info,
)

null_df = pd.DataFrame([[""],[""],[""]])

marksheet_df = pd.DataFrame(Marksheet)
main = pd.concat([studentinfo_df,null_df, marksheet_df.T])
with open(f"{to_save_loc}{rollno}-{year}.xlsx","x"):
    pass
main.to_excel(f"{to_save_loc}{rollno}-{year}.xlsx")
print(f"Successfully saved {rollno}")

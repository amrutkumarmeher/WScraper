import requests
import json
import pandas as pd
import curses as cu
import time
import threading

# initializing values
main_result_web = "https://sctevtodisha.nic.in/en/"
is_runtime = True
homepage_logo = r"""
                  ╭━━━┳━━━┳━━━━┳╮╱╱╭┳━━━┳━━━━╮╭━━━┳━━━╮
                  ┃╭━╮┃╭━╮┃╭╮╭╮┃╰╮╭╯┃╭━━┫╭╮╭╮┃┃╭━╮┃╭━╮┃
                  ┃╰━━┫┃╱╰┻╯┃┃╰┻╮┃┃╭┫╰━━╋╯┃┃╰╯┃╰━╯┃╰━╯┃
                  ╰━━╮┃┃╱╭╮╱┃┃╱╱┃╰╯┃┃╭━━╯╱┃┃╱╱┃╭╮╭┫╭╮╭╯
                  ┃╰━╯┃╰━╯┃╱┃┃╱╱╰╮╭╯┃╰━━╮╱┃┃╱╱┃┃┃╰┫┃┃╰╮
                  ╰━━━┻━━━╯╱╰╯╱╱╱╰╯╱╰━━━╯╱╰╯╱╱╰╯╰━┻╯╰━╯"""
student_face = """
▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▓▒▒▓▒▒▒▒
▒▒▒▒▓▒▒▓▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒
▒▓▒▒▒▒▒▒▒▒▓▒
▒▒▓▓▓▓▓▓▓▓▒▒
▒▒▒▒▒▒▒▒▒▒▒▒"""
server_status_good = False

# print something in the screen
def scrPrint(screen,prompt,pos1=None,pos2=None,attri=None):
    """It will print something in the screen"""
    if attri != None:
        if pos1 and pos2:
            screen.addstr(pos1,pos2,prompt,attri)
        else:
            screen.addstr(prompt,attri)
        screen.refresh()
    else:
        if pos1 and pos2:
            screen.addstr(pos1,pos2,prompt)
        else:
            screen.addstr(prompt)
        screen.refresh()
  
def checking_server_anima(screen,pos1,pos2,anima_attr):
    """function for thread to show animation while server is responding"""
    screen.clear()
    for i in range(1,4):
        scrPrint(screen,homepage_logo,0,0)
        screen.addstr(pos1,pos2,f"Checking Server Condition {"."*i}",anima_attr)
        if i >= 3:
            i=1
            screen.refresh()
        else:
            i += 1
            screen.refresh()
        screen.clear()
        time.sleep(1)

# check when it gets response from the server.
def check_and_tell(web:str,return_list):
    """ it will submit when it get response"""
    requests.get(web)
    return_list[0] = return_list[0] + 1

# show how many responses we are getting in a perticular time.
def finalize(TimeOutTime:float,conclu:list,return_list):
    """It will tell responses before server timeOut"""
    time.sleep(TimeOutTime)
    conclu[0] = return_list[0]

# tell server is good or not...
def server_status(main_web,return_list):
    """Check server is good or not, 0=good, 1=not good"""
    """if list[1] = 1, responded"""
    # check server status
    conclu = [0]
    first = threading.Thread(None,check_and_tell,"first",[main_web,return_list])
    second = threading.Thread(None,check_and_tell,"second",[main_web,return_list])
    third = threading.Thread(None,check_and_tell,"Third",[main_web,return_list])
    fourth = threading.Thread(None,check_and_tell,"Fourth",[main_web,return_list])
    fifth = threading.Thread(None,check_and_tell,"fifth",[main_web,return_list])
    timeout = threading.Thread(None,finalize,"timeout_finalizer",[8,conclu,return_list])
    timeout.start()
    first.start()
    second.start()
    third.start()
    fourth.start()
    fifth.start()
    timeout.join()
    main_conclusion_var = conclu[0]
    if main_conclusion_var>=4:
        return_list[0] = 0
        return_list[1] = 1
    else:
        return_list[0] = 1
        return_list[1] = 1

# initializing the functions
def retreve(regino: str, sem: str, session: str):
    """
    This function retreve the result in JSON format & also validate the details,
    inputs: regino=[F/L]<regiNo(12 digs), sem=[<digit 0<d<7], session=[w/s]<year>
    """
    # checking registration no
    if len(regino) == 12 and regino.startswith(("F", "L")):
        no = regino.replace("F", "")
        no = no.replace("L", "")
        if no.isnumeric():
            pass  # let it continue
        else:
            return "Error-Regino"
    else:
        return "Error-Regino"

    # checking semester
    if int(sem) <= 6 and int(sem) > 0:
        pass  # let it continue
    else:
        return "Error-sem"

    # checking session
    if session.startswith(("s", "w")):
        actual_session = session.replace("s", "")
        actual_session = actual_session.replace("w", "")
        if (
            actual_session.isnumeric()
            and int(actual_session) > 2000
            and int(actual_session) < 2050
        ):
            pass  # let it continue
        else:
            return "Error-session"
    else:
        return "Error-session"
    # api which can be used to fetch the result
    api_link = (
        f"https://sctevtexams.in/student-result-{session}?sem=0{sem}&rollNo={regino}"
    )
    return requests.get(api_link).text

# parsing response.text 
def parse_into_pandas(result_text: str):
    """
    This function process the json format result & produce a virtual spreadsheet to save.
    """
    result = json.loads(result_text)
    # list of data containing student info.
    student_Info = [
        ["Name", result["studentInfo"]["studentName"]],
        ["StudentID", result["studentInfo"]["studentID"]],
        ["StudentRegdNo", result["studentInfo"]["registrationNumber"]],
        ["DateOfBirth", result["studentInfo"]["doa"]],
        ["Sex", result["studentInfo"]["gender"]],
        ["Address", result["studentInfo"]["presentAddress1"]],
        ["course", result["studentInfo"]["courseName"]],
        ["Result", result["result"]],
    ]

    # initializing different fields(columns) of marksheet.
    A = ["Subject Code"]
    B = ["Sudject Name"]
    C = ["TH FullM"]
    D = ["IA FullM"]
    E = ["Total Marks"]
    F = ["PassMark"]
    G = ["TH secured"]
    H = ["IA secured"]
    I = ["Total secured"]

    # putting(rows) data in marksheet.
    A.extend([i["paperTypeCode"] for i in result["marksData"]]),  # type: ignore
    B.extend([i["subjectName"] for i in result["marksData"]]),  # type: ignore
    C.extend([i["semYearFullMark"] for i in result["marksData"]]),  # type: ignore
    D.extend([i["internalFullMark"] for i in result["marksData"]]),  # type: ignore
    E.extend([i["totalFullMark"] for i in result["marksData"]]),  # type: ignore
    F.extend([i["totalPassMark"] for i in result["marksData"]]),  # type: ignore
    G.extend([i["securedTH"] for i in result["marksData"]]),  # type: ignore
    H.extend([i["securedIA"] for i in result["marksData"]]),  # type: ignore
    I.extend([i["securedTotal"] for i in result["marksData"]])  # type: ignore
    # declaring Marksheet var
    Marksheet = [A, B, C, D, E, F, G, H, I]

    # Storing student_Info as as DataFrame to process it by pandas framework.
    studentinfo_df = pd.DataFrame(student_Info)
    # creating some gap to make the final main spreadsheet neat .
    null_df = pd.DataFrame([[""], [""], [""]])
    # Storing Marksheet as as DataFrame to process it by pandas framework.
    marksheet_df = pd.DataFrame(Marksheet)
    # Combining all to make a virtual spreadsheet.
    main = pd.concat([studentinfo_df, null_df, marksheet_df.T])
    # returning the final spreadsheet.
    return main


def save_result_as_xlsx(rollno, session, result: pd.DataFrame, to_save_loc):
    """
    This function saves the result in permanent memory as a files as xlsx(excel X)
    input: to_save_loc=<pathToDir>,rollno=[[F/W]<12-digs>],session=[[w/s]<year>],result=[<dfOfResult].
    """
    fileName = f"{rollno}-{session}.xlsx"
    try:  # if file saved without an error
        open(f"{to_save_loc}{fileName}", "x")
        result.to_excel(f"{to_save_loc}{fileName}")
        print(f" File successfully saved to {to_save_loc}{fileName}") # need to replace
    except Exception as e:  # Error during save
        if type(e) == FileExistsError:  # File found
            print(
                f"File {to_save_loc}{fileName} found to be exists. Over writing the file..."
            ) # need to replace
            result.to_excel(f"{to_save_loc}{fileName}")
        else:  # anything else
            print(f"There is an error [{e}]") # need to replace


while is_runtime:  # program starts

    #                                  ->    HOME SCREEN    <-

    # starting the curses screen & color mode
    screen = cu.initscr()  # initializing the console screen(Command User Interface)
    cu.start_color()  # initializing the color mode
    ## defining common color
    cu.init_color(111,235,0,0) # RED 255
    cu.init_color(222,0,0,255) # BLUE 255
    ## defining color pairs (foreground,background)
    cu.init_pair(1,cu.COLOR_WHITE , 111)  # Red on Black
    cu.init_pair(2,cu.COLOR_WHITE , 222)  # Blue on Black
    cu.init_pair(3,cu.COLOR_CYAN,cu.COLOR_BLACK)
    cu.init_pair(4,cu.COLOR_GREEN,cu.COLOR_BLACK)
    cu.init_pair(5,cu.COLOR_YELLOW,cu.COLOR_BLACK)
    ## add elements to screen.
    screen.addstr(
        0,
        0,
        "Warning: Don't change the size of the screen, the interface may crash!",
        cu.color_pair(1)
    )  # warning message
    screen.addstr(4, 0, homepage_logo)  # main logo
    screen.addstr(
        12, 29, "Press any key\n\n", cu.color_pair(2)
    )  # message to user how to continue
    cu.curs_set(0)  # removing cursor
    screen.keypad(True)  # enabeling key response(keyboard)
    screen.refresh()  # finally showing it to screen
    screen.getch()  # waiting for any response,
    # animation
    logo_pos_divider = 63.75
    for i in range(255):
        cu.init_color(112,345-i,0,0) # RED to BLACK
        cu.init_color(223,0,0,345-i) # BLUE TO BLACK
        cu.init_pair(1,cu.COLOR_WHITE,112) # RED to BLACK pair
        cu.init_pair(2,cu.COLOR_WHITE,223) # BLUE to BLACK pair
        screen.clear()
        # re-adding some new elements for animation
        screen.addstr(
            0,
            0,
            "Warning: Don't change the size of the screen, the interface may crash!",
            cu.color_pair(1)
        )  # warning message
        logo_pos_sub = i/logo_pos_divider
        screen.addstr(int(4-logo_pos_sub), 0, homepage_logo)  # main logo
        screen.addstr(
            12, 29, "Press any key\n\n", cu.color_pair(2)
        )  # message to user how to continue
        screen.refresh()
        time.sleep(.001)
        cou = i
    # checking server response
    screen.clear() # clearing everything
    scrPrint(screen,homepage_logo,0,0)
    time.sleep(1)
    server_status_response = [0,0]

    checking_server = threading.Thread(None,server_status,"Checking_S_status",[main_result_web,server_status_response])
    checking_server.start()
    while server_status_response[1] == 0:
        checking_server_anima(screen,10,24,cu.color_pair(4))
    if server_status_response[0] == 0:
        
        ##                              ->  Selecting server mode  <-

        screen.clear()
        scrPrint(screen,homepage_logo,0,0)
        mode_select = screen.subwin(10,60,8,6)
        mode_select.keypad(True)
        mode_select.border()
        screen.refresh()
        scrPrint(mode_select,"MODE SELECT",1,24,cu.color_pair(3))
        scrPrint(mode_select,"[1] NormalFetch mode",6,3,cu.color_pair(5))
        scrPrint(mode_select,"[2] ForceRetrever mode",6,34,cu.color_pair(5))
        mode_select.refresh()
        mode_key = mode_select.getkey()
        if mode_key=="1":
            pass # normal fetch mode
        else:
            pass # force retrever mode
    else:
        pass # force retrever mode
    is_runtime = False

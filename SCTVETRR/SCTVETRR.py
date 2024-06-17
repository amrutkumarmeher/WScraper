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
                  ┃╭━╮┃╭━╮┃╭╮╭╮┃╰╮╭╯┃╭━━┫╭╮╭╮┃┃╭━╮┃╭━╮┃   Made By
                  ┃╰━━┫┃╱╰┻╯┃┃╰┻╮┃┃╭┫╰━━╋╯┃┃╰╯┃╰━╯┃╰━╯┃   Amrut Kumar Meher
                  ╰━━╮┃┃╱╭╮╱┃┃╱╱┃╰╯┃┃╭━━╯╱┃┃╱╱┃╭╮╭┫╭╮╭╯   CSE  batch- 2023-26
                  ┃╰━╯┃╰━╯┃╱┃┃╱╱╰╮╭╯┃╰━━╮╱┃┃╱╱┃┃┃╰┫┃┃╰╮   GP BARGARH
                  ╰━━━┻━━━╯╱╰╯╱╱╱╰╯╱╰━━━╯╱╰╯╱╱╰╯╰━┻╯╰━╯"""
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

# for multi-thread animation
def anima(screen,msg,pos1,pos2,anima_attr):
    """function for thread to show animation"""
    screen.clear()
    for i in range(1,4):
        scrPrint(screen,homepage_logo,0,0)
        screen.addstr(pos1,pos2,f"{msg}{"."*i}",anima_attr)
        if i >= 3:
            i=1
            screen.refresh()
        else:
            i += 1
            screen.refresh()
        screen.clear()
        time.sleep(1)

# remove signs like b'hi' which came from curses.getchar() function
def remove_b(st:str):
    st = str(st)
    st = st.replace("'","")
    st = st.replace("b","")
    return st

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
def retreve(regino: str, sem: str, session: str,return_list:list):
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
            return_list[0] = "Error-Regino"
            return_list[1] = 1
    else:
        return_list[0] = "Error-Regino"
        return_list[1] = 1

    # checking semester
    if int(str(sem)) <= 6 and int(str(sem)) > 0:
        pass  # let it continue
    else:
        return_list[0] = "Error-sem"
        return_list[1] = 1

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
            return_list[0] = "Error-session"
            return_list[1] = 1
    else:
        return_list[0] = "Error-session"
        return_list[1] = 1
    # api which can be used to fetch the result
    api_link = (
        f"https://sctevtexams.in/student-result-{session}?sem=0{sem}&rollNo={regino}" # its not working
    )
    return_list[0]= requests.get(api_link).text
    return_list[1] = 1

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
    main = pd.concat([studentinfo_df, null_df, marksheet_df.T],ignore_index=True)
    main.reindex()
    # returning the final spreadsheet.
    return main

# saves result as excel
def save_result_as_xlsx(rollno, session, result: pd.DataFrame,screen):
    """
    This function saves the result in permanent memory as a files as xlsx(excel X)
    input: to_save_loc=<pathToDir>,rollno=[[F/W]<12-digs>],session=[[w/s]<year>],result=[<dfOfResult].
    """
    fileName = f"{rollno}-{session}.xlsx"
    try:  # if file saved without an error
        open(f"{fileName}", "x")
        result.to_excel(f"{fileName}")
        screen.clear()
        scrPrint(screen,homepage_logo,0,0)
        scrPrint(screen,f"The result sucessfully saved to {fileName}",10,13,cu.color_pair(4))
        time.sleep(8)
    except Exception as e:  # Error during save
        if type(e) == FileExistsError:  # File found
            screen.clear()
            scrPrint(screen,homepage_logo,0,0)
            scrPrint(screen,f"Over Writing the file...{fileName}",10,13,cu.color_pair(4))
            result.to_excel(f"{fileName}")
            time.sleep(8)
        else:  # anything else
            screen.clear()
            scrPrint(screen,homepage_logo,0,0)
            scrPrint(screen,f"An error found while saving the file: {e}",10,18,cu.color_pair(7))
            time.sleep(8)


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
    cu.init_pair(6,cu.COLOR_MAGENTA,cu.COLOR_BLACK)
    cu.init_pair(7,cu.COLOR_RED,cu.COLOR_BLACK)
    cu.init_pair(8,cu.COLOR_WHITE,cu.COLOR_RED)
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
    server_status_response = [0,0] # used to collect server response by any thread
    checking_server = threading.Thread(None,server_status,"Checking_S_status",[main_result_web,server_status_response])
    checking_server.start() # server status check is in a different thread from animation
    while server_status_response[1] == 0: # for animation
        anima(screen,"Checking Server status",10,24,cu.color_pair(4))
    if server_status_response[0] == 0:
        
        ##                              ->  Selecting server mode  <-

        screen.clear() # clear everything
        scrPrint(screen,homepage_logo,0,0)
        mode_select = screen.subwin(10,60,8,6) # mode select screen
        mode_select.keypad(True)
        mode_select.border()
        screen.refresh() # must do to make the screen appear
        scrPrint(mode_select,"MODE SELECT",1,24,cu.color_pair(3))
        scrPrint(mode_select,"[1] NormalFetch mode",6,3,cu.color_pair(5))
        scrPrint(mode_select,"[2] ForceRetrever mode",6,34,cu.color_pair(5))
        scrPrint(mode_select,"[Any Key] Exit",8,23,cu.color_pair(5))
        mode_select.refresh() # show options
        mode_key = mode_select.getkey()  # wait for a response...
        if mode_key=="1":

            #                           ->    Normal Fetch mode   <-

            #    Fetching Details
            screen.clear()
            screen.refresh()
            student_info = screen.subwin(15,50,6,10)
            student_info.keypad(True)
            student_info.border()
            scrPrint(student_info,"STUDENT INFO",1,19,cu.color_pair(6))
            scrPrint(student_info,"REGI NO([F/L]<12-dig>): ",5,2,cu.color_pair(7))
            regi_entry = student_info.getstr()
            student_info.border()
            scrPrint(student_info,"SEMESTER(1-6): ",7,2,cu.color_pair(7))
            sem_entry = student_info.getstr()
            student_info.border()
            scrPrint(student_info,"SESSION([w/s]<year>): ",9,2,cu.color_pair(7))
            session_entry = student_info.getstr()
            screen.clear()
            scrPrint(screen,homepage_logo,0,0)
            retreve_return_list = [0,0]
            retreve_info = threading.Thread(None,retreve,"retreve",[remove_b(str(regi_entry)),remove_b(str(sem_entry)),remove_b(str(session_entry)),retreve_return_list])
            retreve_info.start()
            while retreve_return_list[1] == 0:
               anima(screen,"Fetching Details",10,26,cu.color_pair(4))
            #   Saving details
            screen.clear()
            scrPrint(screen,homepage_logo,0,0)
            scrPrint(screen,"Saving Details...",10,22,cu.color_pair(4))
            if len(retreve_return_list[0]) > 50:
                result_df = parse_into_pandas(str(retreve_return_list[0]))
                save_result_as_xlsx(remove_b(regi_entry),remove_b(session_entry),result_df,screen)
            else:
                screen.clear()
                scrPrint(screen,homepage_logo,0,0)
                scrPrint(screen,f"There is a problem: {retreve_return_list[0]}",10,15)
                time.sleep(3)

        elif mode_key == "2":

            #                   ->   Force Retrever mode  <-

            # getting every important details
            screen.clear()
            screen.refresh()
            student_info = screen.subwin(15,50,6,10)
            student_info.keypad(True)
            student_info.border()
            scrPrint(student_info,"STUDENT INFO",1,19,cu.color_pair(6))
            scrPrint(student_info,"REGI NO([F/L]<12-dig>): ",5,2,cu.color_pair(7))
            regi_entry = student_info.getstr()
            student_info.border()
            scrPrint(student_info,"SEMESTER(1-6): ",7,2,cu.color_pair(7))
            sem_entry = student_info.getstr()
            student_info.border()
            scrPrint(student_info,"SESSION([w/s]<year>): ",9,2,cu.color_pair(7))
            session_entry = student_info.getstr()
            student_info.border()
            scrPrint(student_info,"No of Threads:",11,2,cu.color_pair(7))
            threads_entry = student_info.getstr()
            threads_entry = int(remove_b(str(threads_entry)))
            screen.clear()
            scrPrint(screen,homepage_logo,0,0)
            scrPrint(screen,"Initializing Retrever Engine...",10,22,cu.color_pair(6))
            retreve_return_list = [0,0] # for collecting output
            time.sleep(2)
            # force retrever
            while retreve_return_list[1] != 1: # till output is not collected...
                thread_list = []
                # initializing every thread
                screen.clear()
                scrPrint(screen,homepage_logo,0,0)
                scrPrint(screen,"Preparing threads...",10,26,cu.color_pair(3))
                scrPrint(screen,"Please Don't Turn your computer or this program off...",13,11,cu.color_pair(8))
                time.sleep(1)
                for i in range(threads_entry):
                    screen.clear()
                    scrPrint(screen,homepage_logo,0,0)
                    scrPrint(screen,"Please Don't Turn your computer or this program off...",13,11,cu.color_pair(8))
                    thread_list.append(threading.Thread(None,retreve,f"retreve{i}",[remove_b(str(regi_entry)),remove_b(str(sem_entry)),remove_b(str(session_entry)),retreve_return_list]))
                    time.sleep(4/threads_entry)
                screen.clear()
                scrPrint(screen,homepage_logo,0,0)
                scrPrint(screen,"Starting Threads...",10,26,cu.color_pair(4))
                scrPrint(screen,"Please Don't Turn your computer or this program off...",13,11,cu.color_pair(8))
                time.sleep(1)
                # starting every thread
                for i in thread_list:
                    i.start()
                screen.clear()
                scrPrint(screen,homepage_logo,0,0)
                scrPrint(screen,"Waiting For Response...",10,25,cu.color_pair(3))
                scrPrint(screen,"Please Don't Turn your computer or this program off...",13,11,cu.color_pair(8))
                time.sleep(7)
                screen.clear()
                scrPrint(screen,homepage_logo,0,0)
                if retreve_return_list[0] == 0:
                    scrPrint(screen,"First Thread Batch Failed",10,24,cu.color_pair(4))
                    time.sleep(1.5)
            #   Saving details
            screen.clear()
            scrPrint(screen,homepage_logo,0,0)
            scrPrint(screen,"Saving Details...",10,22,cu.color_pair(4))
            if len(retreve_return_list[0]) > 50:
                result_df = parse_into_pandas(str(retreve_return_list[0]))
                save_result_as_xlsx(remove_b(regi_entry),remove_b(session_entry),result_df,screen)
            else:
                screen.clear()
                scrPrint(screen,homepage_logo,0,0)
                scrPrint(screen,f"There is a problem: {retreve_return_list[0]}",10,15)
                time.sleep(3)
        else:
            is_runtime = False
            
    else:
        #                   ->   Force Retrever mode  <-

        # getting every important details
        screen.clear()
        screen.refresh()
        student_info = screen.subwin(15,50,6,10)
        student_info.keypad(True)
        student_info.border()
        scrPrint(student_info,"STUDENT INFO",1,19,cu.color_pair(6))
        scrPrint(student_info,"REGI NO([F/L]<12-dig>): ",5,2,cu.color_pair(7))
        regi_entry = student_info.getstr()
        student_info.border()
        scrPrint(student_info,"SEMESTER(1-6): ",7,2,cu.color_pair(7))
        sem_entry = student_info.getstr()
        student_info.border()
        scrPrint(student_info,"SESSION([w/s]<year>): ",9,2,cu.color_pair(7))
        session_entry = student_info.getstr()
        student_info.border()
        scrPrint(student_info,"No of Threads:",11,2,cu.color_pair(7))
        threads_entry = student_info.getstr()
        threads_entry = int(remove_b(str(threads_entry)))
        screen.clear()
        scrPrint(screen,homepage_logo,0,0)
        scrPrint(screen,"Initializing Retrever Engine...",10,22,cu.color_pair(6))
        retreve_return_list = [0,0] # for collecting output
        time.sleep(2)
        # force retrever
        while retreve_return_list[1] != 1: # till output is not collected...
            thread_list = []
            # initializing every thread
            screen.clear()
            scrPrint(screen,homepage_logo,0,0)
            scrPrint(screen,"Preparing threads...",10,26,cu.color_pair(3))
            scrPrint(screen,"Please Don't Turn your computer or this program off...",13,11,cu.color_pair(8))
            time.sleep(1)
            for i in range(threads_entry):
                screen.clear()
                scrPrint(screen,homepage_logo,0,0)
                scrPrint(screen,"Please Don't Turn your computer or this program off...",13,11,cu.color_pair(8))
                thread_list.append(threading.Thread(None,retreve,f"retreve{i}",[remove_b(str(regi_entry)),remove_b(str(sem_entry)),remove_b(str(session_entry)),retreve_return_list]))
                time.sleep(4/threads_entry)
            screen.clear()
            scrPrint(screen,homepage_logo,0,0)
            scrPrint(screen,"Starting Threads...",10,26,cu.color_pair(4))
            scrPrint(screen,"Please Don't Turn your computer or this program off...",13,11,cu.color_pair(8))
            time.sleep(1)
            # starting every thread
            for i in thread_list:
                i.start()
            screen.clear()
            scrPrint(screen,homepage_logo,0,0)
            scrPrint(screen,"Waiting For Response...",10,25,cu.color_pair(3))
            scrPrint(screen,"Please Don't Turn your computer or this program off...",13,11,cu.color_pair(8))
            time.sleep(7)
            screen.clear()
            scrPrint(screen,homepage_logo,0,0)
            if retreve_return_list[0] == 0:
                scrPrint(screen,"First Thread Batch Failed",10,24,cu.color_pair(4))
                time.sleep(1.5)
        #   Saving details
        screen.clear()
        scrPrint(screen,homepage_logo,0,0)
        scrPrint(screen,"Saving Details...",10,22,cu.color_pair(4))
        if len(retreve_return_list[0]) > 50:
            result_df = parse_into_pandas(str(retreve_return_list[0]))
            save_result_as_xlsx(remove_b(regi_entry),remove_b(session_entry),result_df,screen)
        else:
            screen.clear()
            scrPrint(screen,homepage_logo,0,0)
            scrPrint(screen,f"There is a problem: {retreve_return_list[0]}",10,15)
            screen.clear()
            time.sleep(3)
    

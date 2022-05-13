from __future__ import print_function
from ast import While
from asyncio import exceptions
from audioop import mul
from codecs import getencoder
from dis import Instruction
from email.mime import audio
from glob import glob
from lib2to3.pgen2.driver import Driver
import random
from shutil import move
import unittest
import os,errno,atexit,platform,subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tkinter import *
from functools import partial
from selenium.webdriver.support import expected_conditions as EC
import tracemalloc
import time
from selenium.common.exceptions import NoSuchElementException   
from selenium.common.exceptions import ElementClickInterceptedException
from googlesearch import search
import pyautogui
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import TimeoutException
from random import randint
tracemalloc.start()

if platform.system() == 'Windows':
    clear = lambda: os.system('cls') # For Windows
elif platform.system() == 'Linux':
    clear = lambda: os.system('clear') # For linux
quizletOptions = Options()
quizletOptions.headless = True
driver_path = 'chromedriver'
def document_initialised(driver):
    return driver.execute_script("return initialised")
def searchGoogle(query):
    for j in search(query, tld="co.in", num=10, stop=10, pause=1): 
        if "https://quizlet.com/" in j:
            return j
    return 'Not found'

def findAnswer(question):
    question = question.strip('\n')
    question = question.strip('\t')
    # Keep only first line unless multiple choice question (helps with search results)
    if question.find('A.') == -1:
        question = question.partition('\n')[0]
    question = question[:-3]
    # Search google for quizlet url
    quizletUrl = searchGoogle(question)
    if quizletUrl == 'Not found':
        print('Could not find quizlet url')
        return
    # Keep only first line for every question type (helps with parsing)
    question = question.partition('\n')[0]
    print('Googled!')
    # Download and parse quizlet data
    quizletDriver = webdriver.Chrome(options=quizletOptions, executable_path=driver_path)
    quizletDriver.get(quizletUrl)
    print('Loaded quizlet!')
    try:
        # Scroll to bottom of page (helps prevent missing elements)
        quizletDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        answerElement = quizletDriver.find_element_by_xpath("//span[contains(text(),'" + question + "')]/../../../..//a[@class='SetPageTerm-definitionText']/span")
        print('Parsed!')
        answer = answerElement.text
        # If answer and question are flipped
        if answer.find(question) != -1:
            answerElement = quizletDriver.find_element_by_xpath("//span[contains(text(),'" + question + "')]/../../../..//a[@class='SetPageTerm-wordText']/span")
            answer = answerElement.text
    except:
        answer = 'Failed to parse!'
    clear()
    print(answer)
    print('DEBUG INFO:')
    print('question: ' + question)
    print('quizletUrl: ' + quizletUrl)

def setup():
    global driver
    driver = webdriver.Chrome()
    driver.get("https://auth.edgenuity.com/Login/Login/Student")
    driver.maximize_window() # For maximizing window
    #pyautogui.keyDown('ctrl')
    #pyautogui.keyDown('-')
    #pyautogui.keyUp('ctrl')
    #pyautogui.keyUp('-')
    #pyautogui.click()
    time.sleep(2)
    global wait
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="LoginPassword"]')))
    driver.implicitly_wait(5) # gives an implicit wait for 20 seconds

def allCourseElements():
    nextAcitivties = driver.find_elements(By. XPATH, '//*[@title="Next Activity"]')
    print(len(nextAcitivties))
    tkWindow = Tk()  
    tkWindow.geometry('400x400')  
    tkWindow.title('Pick a course you want to complete')
    tkWindow.configure(background='#ffffff')
    """use tkinter to make a multiple choice question to pick a course"""
    courseList = []
    for i in range(len(nextAcitivties)):
        courseList.append(nextAcitivties[i].text)
        
    print(courseList)
    course = StringVar(tkWindow)
    course.set(courseList[0])
    courseMenu = OptionMenu(tkWindow, course, *courseList)
    courseMenu.pack()
    courseMenu.config(width=20)
    courseMenu.config(height=10)
    courseMenu.config(bg='#ffffff')

def moveToMiddle():
    width, length = pyautogui.size()
    global width2
    global length2
    width2 = width / 2
    length2 = length / 2
    pyautogui.moveTo(width2,length2)

def match():
    matchingActivity = driver.find_element(By.XPATH, '//*[@id="matchingActivity"]')
    matchLeftColumn = driver.find_elements(By.CLASS_NAME, 'matchLeftColumn')
    character = "\n\n"
    print(innerText(matchLeftColumn).split(character))
    
    #in the code the answer are there. Look in the matchMiddleColumn and from top to bottum analyze the place of each element. 
    #As you analzye the elements you would see that each box for the arrows to go is seperated by the line and they are correlated to each other.
    
def volumeVideo():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="frame_video_controls"]')))   
    volumeButton = driver.find_element(By.XPATH, '//*[@id="uid2_volumeButton"]')
    volumeButton.click()
    time.sleep(1)
    sliderMute = driver.find_element(By.XPATH, '//*[@id="slider-mute"]')
    sliderMute.click()
    
def iframeVideo():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="frame_video_controls"]')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="uid1_time"]')))
    moveToMiddle()
    time.sleep(1)
    volumeVideo()
    time.sleep(1)
    pause = driver.find_element(By.CLASS_NAME, 'pause')
        
    while pause.is_displayed():
        WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.CLASS_NAME, 'play')))
        time.sleep(1)
        footNavRightDisabled()
    
    """
    try:
        videoLength = driver.find_element(By.XPATH, '//*[@id="uid1_time"]')
    except NoSuchElementException or InvalidSessionIdException:
        print('Could not find video length')
    else:
        print("found video length")
    
    time.sleep(1)
    videoLength = driver.find_element(By.XPATH, '//*[@id="uid1_time"]').text
    print("###")
    print("Time = ", videoLength)
    print("###")
    string = videoLength # Get the text from the element
    character = "/"
    def skipCharacter(string, character):
        string = string.split(character)
        return string[1]
    print(skipCharacter(string, character).split(":"))
    splitString = skipCharacter(string, character).split(":")
    global minute
    global second
    minute = splitString[0]
    second = splitString[1]
    print(minute)
    print(second)
    global secondsTimer
    def secondsTimer(seconds):
        time.sleep(seconds)
        #print("Timer finished")
        return
    global convertMinutesToSeconds
    def convertMinutesToSeconds(minutes):
        minutes = minutes*60
        time.sleep(minutes)
        return 
    global secondsPlusSeconds
    def secondsPlusSeconds():
        seconds = secondsTimer(int(second))
        minutes = convertMinutesToSeconds(int(minute))
        print("finished timer")
    """
    moveToMiddle()
    time.sleep(1)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="uid1_volumeButton"]'))) 
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="uid1_volumeButton"]'))) 
    except TimeoutException or InvalidSessionIdException or NoSuchElementException or ElementClickInterceptedException:
        try:
            WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.XPATH, '//*[@id="uid1_volumeButton"]')))
        except:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="v_control"]')))
            volumeButton2 = driver.find_element(By.XPATH, '//*[@id="v_control"]')
            volumeButton2.click()
            time.sleep(1) #if to slow try .5
            sliderMute2 = driver.find_element(By.CLASS_NAME, 'icon-media-volume2')
            sliderMute2.click() # if this doesnt work try to click with sliderMute
            moveToMiddle()
        else:
            volumeButton.click()
            try:
                sliderMute.click()
            except:
                sliderMute2.click()
            else:
                print("muted video")
                moveToMiddle()
                #secondsPlusSeconds()
                footNavRightDisabled()
    else:
        volumeButton = driver.find_element(By.XPATH, '//*[@id="uid1_volumeButton"]')
        volumeButton.click()
        time.sleep(1)
        sliderMute = driver.find_element(By.XPATH, '//*[@id="slider-mute"]')
        sliderMute.click()
        print("muted video")
        #secondsPlusSeconds()
        footNavRightDisabled()
        
### overly compilcated finding the volume button because the volume button is blocked by another element issue ^^^^
global validateLogin
def validateLogin(username, password):
    print("username entered :", username.get())
    print("password entered :", password.get())
    print("course entered :", course.get())

def loginFrom():
    global tkWindow
    tkWindow = Tk()  
    tkWindow.geometry('400x150')  
    tkWindow.title('Edgenuity Login Form')

    #username label and text entry box
    usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
    global username
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)  

    #password label and password entry box
    passwordLabel = Label(tkWindow,text="Password").grid(row=1, column=0)  
    global password
    password = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)  

    #amount of courses available entry box
    courseLable = Label(tkWindow, text="Number of courses?").grid(row=2, column=0)
    global course
    course = IntVar()
    courseEntry = Entry(tkWindow, textvariable=course).grid(row=2, column=1)  
    global validateLogin
    validateLogin = partial(validateLogin, username, password)
    #login button

    #ask the user if they are graded on Warm-up, Instruction, and Summary.

    loginButton = Button(tkWindow, text="Save Info", command=validateLogin).grid(row=4, column=0)  
    tkWindow.mainloop()
    
def tryToLogin():
    print("finding username and password sections...")
    element = driver.find_element(By.XPATH, '//*[@id="LoginPassword"]')
    element.send_keys(password.get())
    print("found password and sent")
    
    element2 = driver.find_element(By.XPATH, '//*[@id="LoginUsername"]')
    element2.send_keys(username.get())
    print("found username and sent")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="LoginSubmit"]')))
    try:
        loginButton = driver.find_element(By.XPATH, '//*[@id="LoginSubmit"]')
    except:
        try:
            loginButton = driver.find_element(By.CLASS_NAME, 'btn-primary enrollment-card-btn-next btn d-flex align-items-baseline')
        except:
            print("failed to find login button")
        else:
            loginButton.click()
            print("found login button")
            try:
                errorMessage = driver.find_element(By.XPATH, '//*[@id="loginTrouble"]')
            except:
                print("no error message")
                time.sleep(1.5) 
            else:
                print("error message found")
                print(errorMessage.text)
                driver.close()
                tkWindow.mainloop()
    else: 
        loginButton.click()
        print("found login button and clicked")
        time.sleep(1.5)
        try:
            errorMessage = driver.find_element(By.XPATH, '//*[@id="loginTrouble"]')
        except:
            print("no error message")
            time.sleep(1.5) 
        else:
            print("error message found")
            print("Printing error message:")
            print(errorMessage.text)
            driver.close()
            time.sleep(1)
            tkWindow.mainloop()

def nextActivity():
    #check all of the courses with all elements thingy
    time.sleep(1)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@title="Next Activity"]')))
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="Next Activity"]')))
    except InvalidSessionIdException:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'class="btn-primary enrollment-card-btn-next btn d-flex align-items-baseline"')))
        try:
            nextActivity = driver.find_element(By.CLASS_NAME,'class="btn-primary enrollment-card-btn-next btn d-flex align-items-baseline"')
            nextActivity.click()
        except:
            print("coudnt find next activity")
        else:
            time.sleep(5)
    else:
        nextActivity = driver.find_element(By.XPATH, '//*[@title="Next Activity"]')
        nextActivity.click()
        print("clciked the next Activity button")
        time.sleep(5)

def activeSession():
    try:
        countinueButton = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="btnContinue"]')))
        countinueButton = driver.find_element(By.XPATH, '//*[@id="btnContinue"]')
        countinueButton.click()
        time.sleep(2.5)
    except:
        driver.close()
        print("couldnt find the continue button")
    else:
        print("no active sessions")



def footNavRightDisabled():
    #noFootNavRight = driver.find_element(By.CLASS_NAME, "footnav goRight disabled")
    switchToMainContent()
    if WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'footnav goRight disabled'))):
        switchBackToIframe()
        frameRight = driver.find_element(By.XPATH, 'FrameRight')
        frameRight.click()
        print("clicked right page")
    else:
        nextLesson = driver.find_element(By.CLASS_NAME, 'footnav goRight')
        nextLesson.click()
        print("clicked next lessson")
        time.sleep(2.5)

def switchToMainContent():
    try:
        driver.switch_to.default_content()
    except NoSuchElementException:
        print("no default content")
        driver.switch_to.parent_frame()
    else:
        print("switched to main content")

def switchBackToIframe():
    try:
        driver.switch_to.frame("stageFrame")
    except NoSuchElementException:
        print("no frame")
        driver.switch_to.frame('iFramePreview')
    else:
        print("switched iframe")

def clickDone():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="btnCheck"]')))
    done = driver.find_element(By.XPATH, '//*[@id="btnCheck"]')
    done.click()
    print("clicked done")

def RandomMultipleChoiceClicker():
    switchToMainContent()
    lessonName = driver.find_element(By.XPATH, '//*[@id="activity-title"]').text
    print("Lesson name is: ", lessonName)
    switchBackToIframe()
    ezLessons = ['Summary', 'Instruction', 'Warm-Up']
    hardLessons = ['Quiz', 'Test', 'Assingment', 'Unit Test Review', 'Unit Test', 'Cumulative Exam Review', 'Cumulative Exam' ]
    if lessonName in ezLessons:
        #click randomly
        print("This is a ezlesson...")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'answer-choice-button')))
        acb = driver.find_elements(By.CLASS_NAME, 'answer-choice-button').text
        print("There are ", len(acb), "options to choose from")
        try:
            random.randint(0, len(acb)).click()
        except:
            print("click didnt work")
        try:
            print(acb[random.randint(len(acb))].click())
            print("clicked")
        except:
            print(random.choice(acb).click())
            print("clicked")
        finally:
            clickDone()
            audioChecking()
            multipleChoiceCheckAnswer()
    else:
        #search google and get correct answers
        i = "Check all that apply"
        for i in innerText(pqb):
            print("Searching google") #beta
            searchGoogle(i)
            #after searching google go to the website and check for the "correct answer" (use the code on the computer)


def oneChoiceClicker(question):
    question = question.strip('\n')
    question = question.strip('\t')
    searchgoogle = searchGoogle(question)
    print("searching the question...")
    print(searchgoogle)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "SiteLogo")))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "SetPageTerm-wordText")))
    definition = driver.find_elements(By.CLASS_NAME, 'SetPageTerm-wordText')
    print("found definitions")
    innerText(definition)
    answer = driver.find_elements(By.CLASS_NAME, 'SetPageTerm-definitionText')    
    innerText(answer)
    print("found possible answers")
    innerTextDef = innerText(definition)
    innerTextAns = innerText(answer)
    acl = driver.find_elements(By.CLASS_NAME, 'answer-choice-label')
    innerText(acl) 
    if acl in innerTextDef or acl in innerTextAns:
        print("found the answer")
        acl.click() 

def audioChecking():
    global audioOff
    try:
        while audioOff.is_displayed():
            try:
                audioOff = driver.find_element(By.XPATH, '//*[@id="invis-o-div"]')
                print(audioOff.text)
            except NoSuchElementException:
                print("no audio")
    except:
        print("No audio is being played, go ahead and click an answer")
            

def multipleChoiceCheckAnswer():
    if start.is_displayed():
        start = driver.find_element(By.CLASS_NAME, 'done-start')
        print("that wasnt supposed to happen")
        clickDone()
        time.sleep(1)
    if retry.is_displayed():
        retry = driver.find_element(By.CLASS_NAME, 'done-retry')
        audioChecking()
        time.sleep(1)
        clickDone()
        multipleChoiceCheckAnswer()
    if complete.is_displayed():
        complete = driver.find_element(By.CLASS_NAME, 'done-complete')
        print("completed")
        time.sleep(1)
        footNavRightDisabled()

def oneChoiceAnswerChecker():
    correctAnswer = driver.find_element(By.CLASS_NAME, 'icon-qa-right2')
    incorrectAnswer = driver.find_element(By.CLASS_NAME, 'icon-qa-wrong2')

global innerText
def innerText(element):
     for i in element:
        print(i.text)
        #return element[0].text

def main():
    try:
        if WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="stageFrame"]'))): 
            print("found iframe")
    except NoSuchElementException:
        print("no iframe")
        driver.close()
    else:
        try:
        #check if its a video\
            while True:   
                print("locating video if possible")
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="home_video_js"]')))
                break
        except TimeoutException:
            print("No iframe/video located")
            ##if it isint a video check if its a question
            try:
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="iFramePreview"]' )))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'Practice_Question_Body')))
                questionBody = driver.find_element(By.CLASS_NAME,'Practice_Question_Body')
            except TimeoutException or NoSuchElementException:
                print("No questions found")
                switchToMainContent()
                footNavRightDisabled()
                print("Going to next lesson/assignment/deez nuts")
            else:
                try:
                    #check if its one choice question
                    questionContainer = driver.find_element(By.CLASS_NAME, 'QuestionContainer')
                    print("one choice question")
                    try:
                        global pqb
                        pqb = questionContainer.find_elements(By.CLASS_NAME, 'Practice_Question_Body')
                        audioChecking()
                        innerText(pqb)
                        print(innerText(pqb))
                        #get the first element of the list
                        """get the first element of the pqb list"""
                        oneChoiceClicker(pqb[0].text)
                        clickDone()
                        audioChecking()
                        #checkAnswer()
                    except NoSuchElementException:
                        print("no one choice question")

                except NoSuchElementException:
                    print("not a one choice question")
                    #check if it is a multiple choice question
                    try:
                        acl = driver.find_elements(By.CLASS_NAME, 'answer-choice-label')
                    except:
                        print("no multiple choice")
                        #check if its a drag and drop question
                        try:
                            questionContainer = driver.find_element(By.CLASS_NAME, 'DragAndDropQuestion') #place holder for rn

                        except NoSuchElementException:
                            #check if it is a drop down menu
                            try:
                                questionContainer = driver.find_element(By.CLASS_NAME, 'DropDownQuestion')
                            except NoSuchElementException:
                                print("no drop down menu")
                                try:
                                    textBox = driver.find_element(By.CLASSNAME, 'QuestionTextArea')
                                except:
                                    print("No text box")
                                    try:
                                        footNavRightDisabled()
                                        #if none of that is not found click lesson and yk 
                                    except:
                                        print("No assignment found")
                                    else:
                                        print("going to next lesson")
                                        #click next button
                                else:
                                    print("found text box, looking for plausable answer")
                                    """
                                    get all pqb and look for the one that has the keyword "Check all that apply"
                                    Search google and get answers 
                                    and then get answer choice label innerText and check which ones are the same
                                    """
                                    
                                #go to next lesson
                                #if no lesson go to next assignment
                            else:
                                print("doing drop down question")
                        else:
                            #if it is a drag and drop question    
                            print("yo mama")
                    else:
                        print("doing multiple choice")
                        audioChecking()
                        print("audio checked")
                        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'answer-choice-label')))
                        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'Practice_Question_Body')))
                        pqb = driver.find_elements(By.CLASS_NAME, 'Practice_Question_Body')
                        innerText(acl)
                        RandomMultipleChoiceClicker()
                        #always loop back
                        main()
                else:   
                    #if its a one choice question
                    #get the attributes of the question
                    print("idk just yet")
                    
        else:
            #if it is a video
            if WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="home_video_js"]'))):
                #WebDriverWait(driver,10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="home_video_js"]')))
                print("located video")
                iframeVideo()
                try:
                    driver.switch_to.default_content()
                except NoSuchElementException:
                    try: 
                        switchToMainContent()
                    except NoSuchElementException:
                        print("no default content")
                    driver.switch_to.parent_frame()
                else:
                    print("switched to default content")
                footNavRightDisabled()
                main()
            else:
                print("No video/dont know what happened")
                driver.close()



loginFrom()
setup()
#moveToMiddle()
time.sleep(1)
tryToLogin()
activeSession()
nextActivity()
pyautogui.keyDown('ctrl')
pyautogui.keyDown('-')
pyautogui.keyUp('ctrl')
pyautogui.keyUp('-')
pyautogui.click()
main()

#

from re import search
from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from time import sleep
from os import mkdir, getcwd, listdir, rmdir, remove, system
from os import path as get_path
from pyautogui import size as get_screen_size
from pyautogui import moveTo as move_mouse
from pyautogui import position as get_mouse_pos
from pyautogui import click
from pyautogui import typewrite
from pyautogui import hotkey
from pyautogui import Point
from html import unescape
from sys import maxunicode
import pyperclip

from io import TextIOWrapper

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

PY_LINE_LENGTH = 100

ENCODING_SHEBANG = """#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

TEST = True



EMAIL = input("Input Google email: ")
PASSWORD =  input("Input Google password: ")
CLASSROOM_URL = input("Enter URL of repl.it classroom to scrape: ")
CHROMEDRIVER_PATH = input("Enter path to chromedriver.exe: ")

LINE_BREAKERS = '''if
for
while
def
class
#
try'''.split('\n')

WIDTH, HEIGHT = get_screen_size()

PAGE_LOAD_TIME = 3
ACTION_TIME = 0.5

GSIGN_IN_COORDS = Point(x=391, y=494)
NEXT_BTN_COORDS = Point(x=639, y=732)


REPL_HOME = "https://repl.it/login"

if not CHROMEDRIVER_PATH:
     CHROMEDRIVER_PATH = input("Please enter the full path of chromedriver here or leave blank if you have an environment variable set up: ")

ASS_DATE_DELIM = "â€"
ASS_URL_STEM = "repl.it/teacher/assignments"
SUB_URL_STEM = "repl.it/teacher/submissions"
ILLEGAL_CHARS = "#<>$%!&*'\":/{}\\@+`|=,"

last_paste = ""

UNICODE_MAP = {"฿":"THB", "ณ":"%"}

EMOJI_MAP = dict.fromkeys(range(0x10000, maxunicode + 1), 0xfffd)

def my_write(f, text):
     text.translate(UNICODE_MAP)
     text.translate(EMOJI_MAP)
     f.write(text)
     return f
          

def clear_dir():
     for f in listdir():
          if f != get_path.basename(__file__):
               try:
                    rmdir(getcwd() + "\\" + f)
               except:
                    remove(getcwd() + "\\" + f)

def neatify(submission):
     date = search("[A-Z][a-z]{2}\.[0-9]*\.[0-9]*", submission)[0]
     student, status = submission.split(date)

     mon, day, year = date.split(".")

     date = "{}.{}.{}".format(year, 'Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec'.split(",").index(mon)+1, day.zfill(2))

     return " - " + date + " - " + student + " [" + status + "]"



def attempt_write_line(f, lines):
     written = False
     
     for line in lines.split("\n"):
          written = False
          line = line.translate(EMOJI_MAP)
          while not written:
               try:
                    f = my_write(f, line)
                    print("Just wrote: ", line)
                    written = True
                    
               except Exception as e:
                    print(e)
                    print("Problem writing line: ")
                    print(line)
                    line = input("Enter modified line below: ")
          f = my_write(f, "\n")

     return f
          
          

def wait_move_mouse(*point):
     sleep(ACTION_TIME)
     move_mouse(*point)


def wait_type(text):
     sleep(ACTION_TIME*2)
     typewrite(text)
     sleep(ACTION_TIME)


def wait_hotkey(*keys):
     sleep(ACTION_TIME)
     hotkey(*keys)


def wait_click():     
     sleep(ACTION_TIME)
     click()


def wait_for_page(url):
     
     driver.get(url)
     sleep(PAGE_LOAD_TIME)
     timeout = 5
     try:
         element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
         WebDriverWait(driver, timeout).until(element_present)
     except TimeoutException:
         print("Timed out waiting for page to load")
     finally:
         print("Page loaded")
     sleep(PAGE_LOAD_TIME)
   

def auto_login():
     sleep(PAGE_LOAD_TIME)
     wait_move_mouse(GSIGN_IN_COORDS)     
     wait_click()
     sleep(PAGE_LOAD_TIME)
     sleep(4)
     wait_type(EMAIL)          
     wait_move_mouse(NEXT_BTN_COORDS)
     wait_click()
     sleep(PAGE_LOAD_TIME)     
     wait_type(PASSWORD)
     wait_move_mouse(NEXT_BTN_COORDS)     
     wait_click()
     sleep(10)
     

def sanitise_filename(fn):
     fn = fn.replace(' ', '_')
     fn = fn.replace('/', '-')

     return "".join([char for char in fn if char not in ILLEGAL_CHARS])

def commentify(f, string):
     if string.strip() == "":
          f = my_write(f, string)
     else:
          f = my_write(f, "# ") 
          new_line = False
          for i, char in enumerate(string):

               if char.strip() == "" and new_line:
                    f = my_write(f, "\n#")
                    new_line = False
                              
               f = my_write(f, char)
               if i % PY_LINE_LENGTH == 0 and i > 0:
                    new_line = True
                    
          f = my_write(f, "\n")
     return f

def grab_text_editor(x, y):
     global last_paste
     # grab feedback
     wait_move_mouse(x, y)
     wait_click()
     wait_hotkey('ctrl', 'a')     
     sleep(0.5)
     wait_hotkey('ctrl', 'c')     
     text_editor = pyperclip.paste()
     
     if text_editor != last_paste:
          last_paste = text_editor     
          return text_editor
     else:
          return ""



def scrape_student_work(link, submission, assignment_path, assignment_name, assignment_brief):
     global last_paste
     file_name = assignment_name + neatify(submission)
     full_path = assignment_path + "//" + file_name + ".py"
     
     if get_path.exists(full_path):
          print("Already found", file_name)
          print("skipping")
          return
     
     wait_for_page(link)
     
     feedback_given = grab_text_editor(WIDTH//3, (HEIGHT//4)*2.75)

     feedback_given = feedback_given.replace(assignment_brief, "")
     
     if feedback_given:
          commented_lines = [line if line.strip() == "" else "# " + line for line in feedback_given.split("\n")]
          feedback_given = "# FEEDBACK GIVEN:\n\n" + "\n".join(commented_lines).replace("\n\n", "\n")

      
     print("feedback given is: ")
     print(feedback_given.translate(EMOJI_MAP).translate(UNICODE_MAP))
     
     student_code = grab_text_editor(WIDTH//5, HEIGHT//2)

     print("student code is: ")
     print(student_code.translate(EMOJI_MAP).translate(UNICODE_MAP))
     
     with open(full_path, "w", encoding="utf-8") as f:
          f = my_write(f, ENCODING_SHEBANG)
          f = commentify(f, feedback_given)
          f = my_write(f, "\n")
          f = attempt_write_line(f, student_code)
          
     
     #html = download_html(assignment_path, file_name)
     #parse_python_code(assignment_path + "//" + neatify(submission), html)     
     

def scrape_submission_roots(root, assignment, assignment_path):
     
     wait_for_page(root)
          
     html = download_html(assignment_path, assignment)
     
     return parse_repl_links(html_data=html, link_stem=SUB_URL_STEM, delim=ASS_DATE_DELIM)

def download_html(path, name):
     full_file_path = path + "\\" + name + ".html"
##     if get_path.exists(full_file_path):
##          with open(full_file_path) as f:
##               html_data = f.read()
##               return html_data
     
     wait_move_mouse(100, 100)
     wait_click()
     
     wait_hotkey("ctrl", "s")
     
     
     wait_type(full_file_path)
     
     wait_hotkey("enter")

     sleep(PAGE_LOAD_TIME)

     opened = False

     while not opened:
     
          try:
               with open(full_file_path) as f:
                    html_data = f.read()
                    opened = True
          except Exception as e:
               print(e)
               

     return html_data


def parse_python_code(submission_path, html_data):

     html = Soup(html_data, "html.parser")

     python = []

     for line_in in html.find_all('div', {"class":"ace_line"}):
          line_out = ""
          for element in line_in.children:
               try:
                    code = unescape(element.text)
               except AttributeError:
                    code = ' '
               if code.strip() == "":
                    code = code.replace("  ", "\t")                    
                    
               line_out += code
          if any(line_out.startswith(l) for l in LINE_BREAKERS):
               python.append('\n')
          python.append(line_out)
               

     with open(submission_path + ".py", "w", encoding="utf-8") as f:
          for line in python:
               f = attempt_write_line(f, line + '\n')
     

def parse_repl_links(html_data, link_stem, delim):


     links = {}
     
     html = Soup(html_data, "html.parser")
     

     for link in html.find_all('a'):
          url = link["href"]
          link_name = sanitise_filename(link.text.split(delim)[0])[:75]
          
          if link_stem in url and "undefined" not in url:
               links[link_name] = url

     return links
    
def scrape_assignment_brief(path, assignment, assignment_path):
     
     #html = download_html(assignment_path, assignment + "_Test Suite")

     if get_path.exists(assignment_path + "\\" + assignment + " - Assignment Brief.txt"):
          print("Already found", assignment)
          print("skipping")
          return ""

     wait_for_page(path+"/edit")

     with open(assignment_path + "\\" + assignment + " - Assignment Brief.txt", "w", encoding="utf-8") as f:

          brief = grab_text_editor(WIDTH//3, (HEIGHT//4)*3)
          
          for s in brief.split("\n"):
               f = attempt_write_line(f, s)


          
               
          starter_code = grab_text_editor(WIDTH//5, HEIGHT//2)

          f = attempt_write_line(f, starter_code)
               


     
     return brief
     

def scrape_unit_tests(path, assignment, assignment_path):

     buffer_depth = 0

     if get_path.exists(assignment_path + "\\" + assignment + " - Input_Output Matching.py"):
          print("Already found i/o matching for", assignment)
          print("skipping")
          return

     wait_for_page(path+"/edit/correction")
     #html = download_html(assignment_path, assignment + "_Test Suite")

     inputs = driver.find_elements_by_tag_name('input')

     if any([i.get_attribute("value") == "input_output" and i.get_property("checked") for i in inputs]):

          f = open(assignment_path + "\\" + assignment + " - Input_Output Matching.py", 'w')

          f = my_write(f, ENCODING_SHEBANG)

          f = attempt_write_line(f, "TESTS = [")
          
          spans = driver.find_elements_by_tag_name('span')
          y = [i for i in spans if i.get_attribute('style') == "color: rgb(63, 64, 63); margin-left: 22px; cursor: pointer;"]
          for i, modal in enumerate(y):
               modal.click()
               inputs = driver.find_elements_by_tag_name('input')
               test_name = [i.get_attribute("value") for i in inputs if i.get_attribute("placeholder") == "Name your test case"][0]
               
               
               text_areas = driver.find_elements_by_tag_name('textarea')

               test_inputs = [t.text for t in text_areas if t.get_attribute("placeholder") == """Inputs, separated by newlines,
that will be sent to your 
student's program (optional)"""][0]

               test_outputs = [t.text for t in text_areas if t.get_attribute("placeholder") == """Expected output from your
student's program"""][0]

               print(test_name)
               print(test_inputs)
               print(test_outputs)

               buttons = driver.find_elements_by_tag_name('button')

               cancel = [b for b in buttons if b.text == "Cancel"][0]

               cancel.click()
               f = attempt_write_line(f, '{')
               f = attempt_write_line(f, '''"name":"{}",
"inputs":"""{}""",
"outputs":"""{}""",
'''.format(test_name, test_inputs, test_outputs))
               f = attempt_write_line(f, '}')
               if i != len(y) - 1:
                    f = attempt_write_line(f, ",\n")

          f = attempt_write_line(f, "]")
          f.close()
               

     elif any([i.get_attribute("value") == "unit_test" and i.get_property("checked") for i in inputs]):
          codes = driver.find_elements_by_tag_name('code')

          full_path = assignment_path + "\\" + assignment + " - Unit Tests.py"
          

          if get_path.exists(full_path):
               print("Already found unit tests for", assignment)
               print("skipping")
               return

          f = open(full_path, 'w', encoding="utf-8")
          f = my_write(f, ENCODING_SHEBANG)
          class_def_start = False
          defs = 0
          buffer_up = False
          for code in codes:
               
               code_as_text = code.text
##               for span in code.find_elements_by_tag_name("span"):
##                    code_as_text += span.text                    
               
               for i, line in enumerate(code_as_text.split("\n")):
                    
                    

                    
    
                    if line.strip().startswith("def"): # this won't work if you have nested function definitions inside your testing functions. but why would you do that?
                         if defs > 0:
                              buffer_depth -= 1
                         defs += 1
                              
                         buffer_up = True
                         

                    if line.strip().startswith("class UnitTests(unittest.TestCase):"):
                         buffer_up = True
                         

                    f = attempt_write_line(f, (buffer_depth*"  ")+line+"\n")

                    if buffer_up:
                         buffer_up = False
                         buffer_depth += 1

               

               
                    
               f = my_write(f, "\n")  
                    
                    
                    
               
          f.close()
     
     
     


def scrape_assignment_roots():

     fn = "repl.it - Classroom"
     html = download_html(getcwd(), fn)
     
     return parse_repl_links(html_data=html, link_stem=ASS_URL_STEM, delim=ASS_DATE_DELIM)
     
     
     


if __name__ == "__main__":

     driver = webdriver.Chrome(CHROMEDRIVER_PATH)
     wait_for_page(REPL_HOME)
     
 

     if TEST:
          auto_login()
     
     #x = input("Please log into repl.it and navigate to your classroom. Right wait_click -> Save As html and save the html file in the same folder as this script. Enter any key when done.")

     if TEST:
          wait_for_page(CLASSROOM_URL)
     
     ass_links = scrape_assignment_roots()     

     for assignment, url in ass_links.items():
          
          assignment_path = getcwd() + "\\" + assignment
          
          print("Making local directory for {}".format(assignment))
          try:
               mkdir(assignment_path)
          except FileExistsError:
               print("Directory found..")
               
          
          print("Scraping {}".format(assignment))

          scrape_unit_tests(url, assignment, assignment_path)

          assignment_brief = scrape_assignment_brief(url, assignment, assignment_path)
          
          sub_links = scrape_submission_roots(url, assignment, assignment_path)

          for submission, url in sub_links.items():

               submission_path = getcwd() + "\\" + assignment + "\\" + submission

               scrape_student_work(url, submission, assignment_path, assignment, assignment_brief)


          
               


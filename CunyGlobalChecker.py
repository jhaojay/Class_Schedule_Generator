from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import os
import gmail

import CunyFirstEnroller


class CunyGlobalChecker:

    global_search_page = "https://globalsearch.cuny.edu/CFGlobalSearchTool/_search.jsp"
    term_box_id = "t_pd"
    next_buttom_name = "next_btn"
    subject_id = "subject_ld"
    career_id = "courseCareerId"
    open_class_id = "open_classId"
    additional_criteria_id = "imageDivLink"
    instructor_box_id = "instructorId"
    instructor_name_input_box_id = "instructorNameId"
    search_buttom_id = "btnGetAjax"
    result_expand_id = "imageDivLink_inst0"
    status_id = "SSR_CLS_DTL_WRK_SSR_DESCRSHORT"

    def __init__(self, head=None):
        chromedriver_path = os.getcwd() + r"\chrome\chromedriver.exe"
        if head == "headless":
            options = Options()
            options.binary_location = os.getcwd() + r'\chrome\chrome.exe'
            options.add_argument('--headless')
            self.browser = webdriver.Chrome(chromedriver_path, chrome_options=options)
        else:
            self.browser = webdriver.Chrome(chromedriver_path)

    def quit(self):
        self.browser.quit()

    def check_class(self, io, to, so, career, ln, cls_num, delay):
        try:
            self.browser.get(self.global_search_page)

            institution_check_box = self.browser.find_element_by_id(io)
            self.browser.execute_script("arguments[0].click();", institution_check_box)

            term_select = Select(self.browser.find_element_by_id(self.term_box_id))
            term_select.select_by_visible_text(to)

            next_buttom = self.browser.find_element_by_name(self.next_buttom_name)
            self.browser.execute_script("arguments[0].click();", next_buttom)

            subject_select = Select(self.browser.find_element_by_id(self.subject_id))
            subject_select.select_by_visible_text(so)

            career_select = Select(self.browser.find_element_by_id(self.career_id))
            career_select.select_by_visible_text(career)

            open_class_buttom = self.browser.find_element_by_id(self.open_class_id)
            self.browser.execute_script("arguments[0].click();", open_class_buttom)

            additional_criteria = self.browser.find_element_by_id(self.additional_criteria_id)
            self.browser.execute_script("arguments[0].click();", additional_criteria)

            instructor_select = Select(self.browser.find_element_by_id(self.instructor_box_id))
            instructor_select.select_by_visible_text("contains")

            instructor_name_input = self.browser.find_element_by_id(self.instructor_name_input_box_id)
            instructor_name_input.send_keys(ln)

            search_buttom = self.browser.find_element_by_id(self.search_buttom_id)
            self.browser.execute_script("arguments[0].click();", search_buttom)

            result_classes = self.browser.find_elements_by_xpath("//*[contains(@id, 'imageDivLink')]")
            for i in range(len(result_classes)):
                self.browser.execute_script("arguments[0].click();", result_classes[i])

            target_class = self.browser.find_element_by_link_text(cls_num)
            self.browser.execute_script("arguments[0].click();", target_class)

            while (1):
                status_ele = self.browser.find_element_by_id(self.status_id)
                status = status_ele.text

                if "Closed" in status:
                    print(time.asctime(time.localtime(time.time())) + "  (" + cls_num + ") --- Closed")
                    time.sleep(delay)

                    self.browser.refresh()
                elif "Open" in status:
                    print(time.asctime(time.localtime(time.time())) + "  (" + cls_num + ") --- Open")
                    return True
        except:
            return False




school = "CTY01"
term = "2020 Spring Term"
subject = "Electrical Engineering"
career = "Undergraduate"
email = "" # gmail to receive notification
last_name = "" # professor's last name, optional
class_number = "21852"
delay = 15 # how often you want to refresh the page

while(1):
    checker = CunyGlobalChecker("headles")
    availability = checker.check_class(school, term, subject, career, last_name, class_number, delay)

    if availability:
        gmail.send_email(email, "Class '{}' is available for register.".format(class_number))

        enroller = CunyFirstEnroller.CunyFirstEnroller()
        enroller.login(username, pw)
        enroller.enroll_cart(term)
        enroller.quit()
        checker.quit()
        break
    else:
        gmail.send_email(email, "Something Went Wrong With Your Program!     " + class_number)
        checker.quit()

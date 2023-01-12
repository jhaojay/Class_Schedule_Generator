from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import os
import errno
import shutil
# import sys
# from functools import partial
# from multiprocessing.dummy import Pool as ThreadPool


class CunyFirstScraper:

    login_id = username
    login_pw = pw
    home_page = "https://home.cunyfirst.cuny.edu"
    class_search_page = "https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL"
    class_search_page_id = "ACE_DERIVED_CLSRCH_GROUP2"
    loading_icon_id = "WAIT_win0"
    username_id = "CUNYfirstUsernameH"
    password_id = "CUNYfirstPassword"
    institution_box_id = "CLASS_SRCH_WRK2_INSTITUTION$31$"
    term_box_id = "CLASS_SRCH_WRK2_STRM$35$"
    subject_box_id = "SSR_CLSRCH_WRK_SUBJECT_SRCH$0"
    open_class_only_id = "SSR_CLSRCH_WRK_SSR_OPEN_ONLY$5"
    max_units_text_box_id = "SSR_CLSRCH_WRK_UNITS_MAXIMUM$12"
    class_search_button_id = "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"
    search_err_msg_id = "DERIVED_CLSMSG_ERROR_TEXT"
    search_button_id = "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"
    modify_search_button_id = "CLASS_SRCH_WRK2_SSR_PB_MODIFY$5$"
    clear_button_id = "CLASS_SRCH_WRK2_SSR_PB_CLEAR"
    search_result_table_id = "win0divDERIVED_CLSRCH_GROUP6"
    class_detail_page_id = "win0divSSR_CLS_DTL_WRK_GROUP1"
    course_num_text_box_id = "SSR_CLSRCH_WRK_CATALOG_NBR$1"
    view_search_result_button_id = "CLASS_SRCH_WRK2_SSR_PB_BACK"
    class_select_button_id = "SSR_PB_SELECT$"
    class_select_cancel_button_id = "DERIVED_CLS_DTL_CANCEL_PB"
    course_name_id = "win0divSSR_CLSRSLT_WRK_GROUPBOX2GP$"
    crs_nbr_box_id = "SSR_CLSRCH_WRK_CATALOG_NBR$1"

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

    def login(self, login_id, login_pw):
        self.browser.get(self.home_page)
        # self.browser.find_element_by_name(self.close_button_name).click()
        self.browser.find_element_by_id(self.username_id).send_keys(login_id)
        self.browser.find_element_by_id(self.password_id).send_keys(login_pw)
        self.browser.find_element_by_name('submit').click()
        if self.home_page in self.browser.current_url:
            self.browser.get(self.class_search_page)
            print("Login Success!")
            return True
        elif "portaldown" in self.browser.current_url:
            print("CUNYfirst System Unavailable")
            return False
        else:
            print("Login Failed")
            return False

    def loading(self):
        try:
            WebDriverWait(self.browser, 600).until(
                ec.invisibility_of_element_located((By.ID, self.loading_icon_id))
            )
            return True
        except TimeoutException:
            print("[!]TimeoutException")
            return False

    def get_institution_options(self):
        try:
            self.browser.find_element_by_id(self.institution_box_id)
        except (StaleElementReferenceException, NoSuchElementException):
            self.go_to_class_search_page()

        institution_options = []
        institution_select_box = self.browser.find_element_by_id(self.institution_box_id)
        for o in institution_select_box.find_elements_by_tag_name("option"):
            institution_options.append(o.text)
        if institution_options:
            del institution_options[0]
        return institution_options

    def get_term_options(self, io):
        try:
            self.browser.find_element_by_id(self.term_box_id)
        except (StaleElementReferenceException, NoSuchElementException):
            self.go_to_class_search_page()

        institution_select = Select(self.browser.find_element_by_id(self.institution_box_id))
        institution_select.select_by_visible_text(io)
        self.loading()

        term_options = []
        term_select_box = self.browser.find_element_by_id(self.term_box_id)
        for o in term_select_box.find_elements_by_tag_name("option"):
            term_options.append(o.text)
        if term_options:
            del term_options[0]
        return term_options

    def get_subject_options(self, io, to):
        try:
            self.browser.find_element_by_id(self.subject_box_id)
        except (StaleElementReferenceException, NoSuchElementException):
            self.go_to_class_search_page()

        institution_select = Select(self.browser.find_element_by_id(self.institution_box_id))
        institution_select.select_by_visible_text(io)
        self.loading()

        term_select = Select(self.browser.find_element_by_id(self.term_box_id))
        term_select.select_by_visible_text(to)
        self.loading()

        subject_options = []
        subject_select_box = self.browser.find_element_by_id(self.subject_box_id)
        for o in subject_select_box.find_elements_by_tag_name("option"):
            subject_options.append(o.text)
        if subject_options:
            del subject_options[0]
        return subject_options

    def get_classes_info(self, io, to, so, folder_name=None):
        try:
            self.browser.find_element_by_id(self.class_search_page_id)
        except (StaleElementReferenceException, NoSuchElementException):
            self.go_to_class_search_page()

        if folder_name is None:
            folder_name = "classes_info"

        institution_select = Select(self.browser.find_element_by_id(self.institution_box_id))
        institution_select.select_by_visible_text(io)
        self.loading()
        term_select = Select(self.browser.find_element_by_id(self.term_box_id))
        term_select.select_by_visible_text(to)
        self.loading()
        subject_select = Select(self.browser.find_element_by_id(self.subject_box_id))
        subject_select.select_by_visible_text(so)
        self.loading()

        # settings for Search Criteria
        if self.browser.find_element_by_id(self.open_class_only_id).is_selected():
            self.browser.find_element_by_id(self.open_class_only_id).click()
            max_units_input = self.browser.find_element_by_id(self.max_units_text_box_id)
            max_units_input.send_keys('99')

        # click on the search button
        search_button = self.browser.find_element_by_id(self.class_search_button_id)
        self.browser.execute_script("arguments[0].click();", search_button)
        self.loading()

        # two kinds of error might be presented
        search_error = 0
        try:
            my_elm = self.browser.find_element_by_id(self.search_err_msg_id)
            if "Your search will exceed the maximum limit of 350 sections" in my_elm.text:
                search_error = 1
            elif "The search returns no results that match the criteria specified." == my_elm.text:
                search_error = 2
            else:
                print(my_elm.text)
        except (StaleElementReferenceException, NoSuchElementException):
            pass

        if not search_error:  # no error, there is search result page
            # create folder
            path = os.getcwd() + "\\" + folder_name + "\\" + io + "\\" + to
            self.create_folder(path)

            # save page
            modified_subject_name = self.modify_name(so)
            course_file = path + "\\" + modified_subject_name + ".html"
            with open(course_file, 'w', encoding='utf-8') as file:
                file.write(self.browser.page_source)

            # click on Modify Search button to go back
            modify_search_button = self.browser.find_element_by_id(self.modify_search_button_id)
            self.browser.execute_script("arguments[0].click();", modify_search_button)
            self.loading()
        elif search_error == 1:  # search results exceed 350
            content = ''

            # create folder
            path = os.getcwd() + "\\" + folder_name + "\\" + io + "\\" + to
            self.create_folder(path)

            days = ['MON', 'TUES', 'WED', 'THURS', 'FRI', 'SAT', 'SUN']
            for d in days:
                # select each day
                day_check_box = self.browser.find_element_by_id('SSR_CLSRCH_WRK_%s$9' % d)
                self.browser.execute_script("arguments[0].click();", day_check_box)

                # click on SEARCH
                search_button = self.browser.find_element_by_id(self.search_button_id)
                self.browser.execute_script("arguments[0].click();", search_button)
                self.loading()
                try:
                    self.browser.find_element_by_id(self.modify_search_button_id)
                    content += self.browser.page_source

                    modify_search_button = self.browser.find_element_by_id(self.modify_search_button_id)
                    self.browser.execute_script("arguments[0].click();", modify_search_button)
                    self.loading()
                except (StaleElementReferenceException, NoSuchElementException):
                    pass

                # deselect each day
                day_check_box = self.browser.find_element_by_id('SSR_CLSRCH_WRK_%s$9' % d)
                self.browser.execute_script("arguments[0].click();", day_check_box)

            # save page
            modified_subject_name = self.modify_name(so)
            course_file = path + "\\" + modified_subject_name + ".html"
            with open(course_file, 'w', encoding='utf-8') as file:
                file.write(content)
        elif search_error == 2:  # no search results
            clear_button = self.browser.find_element_by_id(self.clear_button_id)
            self.browser.execute_script("arguments[0].click();", clear_button)
            self.loading()

    def get_course_details(self, io, to, so, folder_name=None):
        try:
            self.browser.find_element_by_id(self.class_search_page_id)
        except (StaleElementReferenceException, NoSuchElementException):
            self.go_to_class_search_page()

        if folder_name is None:
            folder_name = "course_details"

        # select institution, term, and subject
        institution_select = Select(self.browser.find_element_by_id(self.institution_box_id))
        institution_select.select_by_visible_text(io)
        self.loading()
        term_select = Select(self.browser.find_element_by_id(self.term_box_id))
        term_select.select_by_visible_text(to)
        self.loading()
        subject_select = Select(self.browser.find_element_by_id(self.subject_box_id))
        subject_select.select_by_visible_text(so)
        self.loading()

        # settings for Search Criteria
        if self.browser.find_element_by_id(self.open_class_only_id).is_selected():
            self.browser.find_element_by_id(self.open_class_only_id).click()
            max_units_input = self.browser.find_element_by_id(self.max_units_text_box_id)
            max_units_input.send_keys('99')

        # click on the search button
        search_button = self.browser.find_element_by_id(self.class_search_button_id)
        self.browser.execute_script("arguments[0].click();", search_button)
        self.loading()

        # two kinds of error might be presented
        search_error = 0
        try:
            my_elm = self.browser.find_element_by_id(self.search_err_msg_id)
            if "Your search will exceed the maximum limit of 350 sections" in my_elm.text:
                search_error = 1
            elif "The search returns no results that match the criteria specified." == my_elm.text:
                search_error = 2
            else:
                print(my_elm.text)
        except (StaleElementReferenceException, NoSuchElementException):
            pass

        if not search_error:  # no error, there is search result page
            # create folder
            modified_subject_name = self.modify_name(so)
            path = os.getcwd() + "\\" + folder_name + "\\" + io + "\\" + to + "\\" + modified_subject_name
            self.create_folder(path)

            # START: get course details
            groups = self.browser.find_elements_by_xpath(
                "//div[starts-with(@id, 'win0divSSR_CLSRSLT_WRK_GROUPBOX2$')]")
            for g in range(len(groups)):
                # get the name of each course
                course_name = self.browser.find_element_by_xpath(
                    "//div[@id='win0divSSR_CLSRSLT_WRK_GROUPBOX2GP$%s']" % g).text
                modified_course_name = self.modify_name(course_name)
                course_file = path + "\\" + modified_course_name + r'.html'

                # if same general info page exists, go to the next one
                if os.path.exists(course_file):
                    # sys.exit()
                    continue

                # click on the first class of each course
                first_cls_num = self.browser.find_element_by_xpath(
                    "//div[@id='win0divSSR_CLSRSLT_WRK_GROUPBOX2$%s']"
                    "//a[starts-with(@id, 'MTG_CLASS_NBR$')]" % g)
                self.browser.execute_script("arguments[0].click();", first_cls_num)
                self.loading()

                # store general info for each course
                with open(course_file, 'w', encoding='utf-8') as file:
                    file.write(self.browser.page_source)

                # click on View Search Results button
                view_results_button = self.browser.find_element_by_id(self.view_search_result_button_id)
                self.browser.execute_script("arguments[0].click();", view_results_button)
                self.loading()
            # END: get course details

            # click on Modify Search button to go back
            modify_search_button = self.browser.find_element_by_id(self.modify_search_button_id)
            self.browser.execute_script("arguments[0].click();", modify_search_button)
            self.loading()
        elif search_error == 1:  # search results exceed 350
            # create folder
            modified_subject_name = self.modify_name(so)
            path = os.getcwd() + "\\" + folder_name + "\\" + io + "\\" + to + "\\" + modified_subject_name
            self.create_folder(path)

            days = ['MON', 'TUES', 'WED', 'THURS', 'FRI', 'SAT', 'SUN']
            for d in days:
                # select each day
                day_check_box = self.browser.find_element_by_id('SSR_CLSRCH_WRK_%s$9' % d)
                self.browser.execute_script("arguments[0].click();", day_check_box)

                # click on SEARCH
                search_button = self.browser.find_element_by_id(self.search_button_id)
                self.browser.execute_script("arguments[0].click();", search_button)
                self.loading()
                try:
                    self.browser.find_element_by_id(self.modify_search_button_id)

                    # START: get course details
                    groups = self.browser.find_elements_by_xpath(
                        "//div[starts-with(@id, 'win0divSSR_CLSRSLT_WRK_GROUPBOX2$')]")
                    for g in range(len(groups)):
                        # get the name of each course
                        course_name = self.browser.find_element_by_xpath(
                            "//div[@id='win0divSSR_CLSRSLT_WRK_GROUPBOX2GP$%s']" % g).text
                        modified_course_name = self.modify_name(course_name)

                        course_file = path + "\\" + modified_course_name + r'.html'

                        # if same general info page exists, go to the next one
                        if os.path.exists(course_file):
                            # sys.exit()
                            continue

                        # click on the first class of each course
                        first_cls_num = self.browser.find_element_by_xpath(
                            "//div[@id='win0divSSR_CLSRSLT_WRK_GROUPBOX2$%s']"
                            "//a[starts-with(@id, 'MTG_CLASS_NBR$')]" % g)
                        self.browser.execute_script("arguments[0].click();", first_cls_num)
                        self.loading()

                        # store general info for each course
                        with open(course_file, 'w', encoding='utf-8') as file:
                            file.write(self.browser.page_source)

                        # click on View Search Results button
                        view_results_button = self.browser.find_element_by_id(self.view_search_result_button_id)
                        self.browser.execute_script("arguments[0].click();", view_results_button)
                        self.loading()
                    # END: get course details

                    modify_search_button = self.browser.find_element_by_id(self.modify_search_button_id)
                    self.browser.execute_script("arguments[0].click();", modify_search_button)
                    self.loading()
                except (StaleElementReferenceException, NoSuchElementException):
                    pass

                # deselect each day
                day_check_box = self.browser.find_element_by_id('SSR_CLSRCH_WRK_%s$9' % d)
                self.browser.execute_script("arguments[0].click();", day_check_box)
        elif search_error == 2:  # no search results
            clear_button = self.browser.find_element_by_id(self.clear_button_id)
            self.browser.execute_script("arguments[0].click();", clear_button)
            self.loading()

    def get_class_details(self, io, to, so, course_num, class_list, folder_name=None):
        try:
            self.browser.find_element_by_id(self.class_search_page_id)
        except (StaleElementReferenceException, NoSuchElementException):
            self.go_to_class_search_page()

        if folder_name is None:
            folder_name = "class_details"

        # select institution, term, and subject
        institution_select = Select(self.browser.find_element_by_id(self.institution_box_id))
        institution_select.select_by_visible_text(io)
        self.loading()
        term_select = Select(self.browser.find_element_by_id(self.term_box_id))
        term_select.select_by_visible_text(to)
        self.loading()
        subject_select = Select(self.browser.find_element_by_id(self.subject_box_id))
        subject_select.select_by_visible_text(so)
        self.loading()

        # settings for Search Criteria
        if self.browser.find_element_by_id(self.open_class_only_id).is_selected():
            self.browser.find_element_by_id(self.open_class_only_id).click()
            max_units_input = self.browser.find_element_by_id(self.max_units_text_box_id)
            max_units_input.send_keys('99')

        # input course number
        course_num_input = self.browser.find_element_by_id(self.course_num_text_box_id)
        course_num_input.clear()
        course_num_input.send_keys(course_num)

        # click on the search button
        search_button = self.browser.find_element_by_id(self.class_search_button_id)
        self.browser.execute_script("arguments[0].click();", search_button)
        self.loading()

        # get the name of the course
        course_name = self.browser.find_element_by_xpath(
            "//div[@id='{}0']".format(self.course_name_id)
        ).text
        modified_course_name = self.modify_name(course_name)

        # create folder
        path = os.getcwd() + "\\" + folder_name + "\\" + io + "\\" + to + "\\" + modified_course_name
        self.create_folder(path)

        class_left = class_list[:]
        for cls in class_list:
            try:
                # click on the class
                cls_num = self.browser.find_element_by_xpath("//*[text()='%s']" % cls)
                self.browser.execute_script("arguments[0].click();", cls_num)
                self.loading()

                # save class details file
                cls_detail_file = path + "\\" + cls + r'.html'
                with open(cls_detail_file, 'w', encoding='utf-8') as file:
                    file.write(self.browser.page_source)

                # click on View Search Results button
                view_results_button = self.browser.find_element_by_id(self.view_search_result_button_id)
                self.browser.execute_script("arguments[0].click();", view_results_button)
                self.loading()

                # delete retrieved class
                class_left.remove(cls)
            except (StaleElementReferenceException, NoSuchElementException):
                pass

        # click on Modify Search button to go back
        modify_search_button = self.browser.find_element_by_id(self.modify_search_button_id)
        self.browser.execute_script("arguments[0].click();", modify_search_button)
        self.loading()

        if not class_left:
            return True
        else:
            print("Can't retrieve some class: ", class_left)
            return False

    def get_related_class(self, io, to, so, course_num, class_list, folder_name=None):
        try:
            self.browser.find_element_by_id(self.class_search_page_id)
        except (StaleElementReferenceException, NoSuchElementException):
            self.go_to_class_search_page()

        if folder_name is None:
            folder_name = "related_class"

        # select institution, term, and subject
        institution_select = Select(self.browser.find_element_by_id(self.institution_box_id))
        institution_select.select_by_visible_text(io)
        self.loading()
        term_select = Select(self.browser.find_element_by_id(self.term_box_id))
        term_select.select_by_visible_text(to)
        self.loading()
        subject_select = Select(self.browser.find_element_by_id(self.subject_box_id))
        subject_select.select_by_visible_text(so)
        self.loading()

        # settings for Search Criteria
        if self.browser.find_element_by_id(self.open_class_only_id).is_selected():
            self.browser.find_element_by_id(self.open_class_only_id).click()
            max_units_input = self.browser.find_element_by_id(self.max_units_text_box_id)
            max_units_input.send_keys('99')

        # input course number
        course_num_input = self.browser.find_element_by_id(self.course_num_text_box_id)
        course_num_input.clear()
        course_num_input.send_keys(course_num)

        # click on the search button
        search_button = self.browser.find_element_by_id(self.class_search_button_id)
        self.browser.execute_script("arguments[0].click();", search_button)
        self.loading()

        # get the name of the course
        course_name = self.browser.find_element_by_xpath(
            "//div[@id='{}0']".format(self.course_name_id)
        ).text
        modified_course_name = self.modify_name(course_name)

        # create folder
        path = os.getcwd() + "\\" + folder_name + "\\" + io + "\\" + to + "\\" + modified_course_name
        self.create_folder(path)

        class_left = class_list[:]
        for cls in class_list:
            try:
                # get the last number of attribute
                cls_num = self.browser.find_element_by_xpath("//*[text()='%s']" % cls)
                last_num_of_attribute = cls_num.get_attribute('id')[-1:]

                # click Select button
                try:
                    class_select_button = self.browser.find_element_by_id(
                        self.class_select_button_id + last_num_of_attribute
                    )
                    self.browser.execute_script("arguments[0].click();", class_select_button)
                    self.loading()
                except (StaleElementReferenceException, NoSuchElementException):
                    print("This course is not selectable.")

                # save class linked class file
                cls_detail_file = path + "\\" + cls + r'_related_class.html'
                with open(cls_detail_file, 'w', encoding='utf-8') as file:
                    file.write(self.browser.page_source)

                # click on cancel button to return
                class_select_cancel_button = self.browser.find_element_by_id(self.class_select_cancel_button_id)
                self.browser.execute_script("arguments[0].click();", class_select_cancel_button)
                self.loading()

                # delete retrieved class
                class_left.remove(cls)
            except (StaleElementReferenceException, NoSuchElementException):
                pass

        # click on Modify Search button to go back
        modify_search_button = self.browser.find_element_by_id(self.modify_search_button_id)
        self.browser.execute_script("arguments[0].click();", modify_search_button)
        self.loading()

        if not class_left:
            return True
        else:
            print("Can't retrieve some class: ", class_left)
            return False

    def get_courses(self, io, to, subject_list, crs_nbr_list, folder_name=None):
        print("Start to obtain courses!")
        if folder_name is None:
            folder_name = "courses"
        try:
            self.browser.find_element_by_id(self.class_search_page_id)
        except (StaleElementReferenceException, NoSuchElementException):
            return False

        institution_select = Select(self.browser.find_element_by_id(self.institution_box_id))
        institution_select.select_by_visible_text(io)
        self.loading()
        term_select = Select(self.browser.find_element_by_id(self.term_box_id))
        term_select.select_by_visible_text(to)
        self.loading()

        for index in range(len(subject_list)):
            subject_select = Select(self.browser.find_element_by_id(self.subject_box_id))
            subject_select.select_by_value(subject_list[index])
            self.loading()

            crs_nbr_input = self.browser.find_element_by_id(self.crs_nbr_box_id)
            crs_nbr_input.clear()
            crs_nbr_input.send_keys(crs_nbr_list[index])

            # settings for Search Criteria
            if self.browser.find_element_by_id(self.open_class_only_id).is_selected():
                self.browser.find_element_by_id(self.open_class_only_id).click()

            # click on the search button
            search_button = self.browser.find_element_by_id(self.class_search_button_id)
            self.browser.execute_script("arguments[0].click();", search_button)
            self.loading()

            try:
                my_elm = self.browser.find_element_by_id(self.search_err_msg_id)
                if "Your search will exceed the maximum limit of 350 sections" in my_elm.text:
                    print(subject_list[index] + ' ' + crs_nbr_list[index] + " Fail!")
                    return False
                elif "The search returns no results that match the criteria specified." == my_elm.text:
                    print(subject_list[index] + ' ' + crs_nbr_list[index] + " Fail!")
                    return False
                else:
                    print(my_elm.text)
                    print(subject_list[index] + ' ' + crs_nbr_list[index] + " Fail!")
                    return False
            except (StaleElementReferenceException, NoSuchElementException):
                pass

            # create folder
                path = os.getcwd() + "\\" + folder_name
            self.create_folder(path)

            # save page
            course_file = path + "\\" + subject_list[index] + "_" + crs_nbr_list[index] + ".html"
            with open(course_file, 'w', encoding='utf-8') as file:
                file.write(self.browser.page_source)

            print(subject_list[index] + ' ' + crs_nbr_list[index] + " Done!")

            # click on Modify Search button to go back
            modify_search_button = self.browser.find_element_by_id(self.modify_search_button_id)
            self.browser.execute_script("arguments[0].click();", modify_search_button)
            self.loading()

        print("All Done!")



    @staticmethod
    def create_folder(path):
            try:
                os.makedirs(path)
                shutil.rmtree(path)
                os.makedirs(path)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

    @staticmethod
    def modify_name(s):
        return s.strip().replace('/', '_').replace(':', '..')\
            .replace('?', '').replace('\\', '_').replace('\\', '_')

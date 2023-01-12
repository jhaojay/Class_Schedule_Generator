from lxml import etree
import re


class CunyFirstParser:
    course_text_id = "DERIVED_CLSRCH_DESCR200"
    instruct_mode_id = "INSTRUCT_MODE_DESCR"
    total_seats_id = "SSR_CLS_DTL_WRK_ENRL_CAP"
    taken_seats_id = "SSR_CLS_DTL_WRK_ENRL_TOT"
    available_seats_id = "SSR_CLS_DTL_WRK_AVAILABLE_SEATS"
    units_id = "SSR_CLS_DTL_WRK_UNITS_RANGE"
    class_component_id = "win0divSSR_CLS_DTL_WRK_SSR_COMPONENT_LONG"
    career_id = "PSXLATITEM_XLATLONGNAME"
    enrollment_info_id = "win0divSSR_CLS_DTL_WRK_GROUP2"
    description_id = "DERIVED_CLSRCH_DESCRLONG"
    box1_id = "win0divSSR_CLSRSLT_WRK_GROUPBOX1"
    box2_id = "win0divSSR_CLSRSLT_WRK_GROUPBOX2$"
    course_name_id = "win0divSSR_CLSRSLT_WRK_GROUPBOX2GP$"
    box3_id = "win0divSSR_CLSRSLT_WRK_GROUPBOX3$"
    class_num_id = "MTG_CLASS_NBR$"
    class_section_id = "MTG_CLASSNAME$"
    days_times_id = "MTG_DAYTIME$"
    room_id = "MTG_ROOM$"
    instructor_id = "MTG_INSTR$"
    meeting_dates_id = "MTG_TOPIC$"
    status_id = "win0divDERIVED_CLSRCH_SSR_STATUS_LONG$"
    auto_enroll_sentence_id = "win0divSSR_CLS_TBL_R0GP$0"
    related_class_section_0_id = "R0_SECTION$"
    related_class_section_1_id = "R1_SECTION$"

    def __init__(self):
        self.parser = etree.HTMLParser()

    def parse_classes_info(self, file):
        result = {}
        html = etree.parse(file, self.parser)

        pages_of_search_results = html.xpath("//div[@id='{}']".format(self.box1_id))
        for i in range(len(pages_of_search_results)):
            page_str = etree.tostring(pages_of_search_results[i])
            page = etree.fromstring(page_str)
            groups_of_courses = page.xpath("//div[starts-with(@id, '{}')]".format(self.box2_id))
            for j in range(len(groups_of_courses)):
                raw_course_name = page.xpath(
                    "//div[@id='{}{}']/descendant::div[@id='{}{}']//text()"
                    .format(self.box2_id, j, self.course_name_id, j)
                )

                course_name = raw_course_name[0].split('-')[1].strip()

                course_abbreviation = raw_course_name[0].split('-')[0].strip()

                course_abbreviation = ' '.join(course_abbreviation.split())
                course_abbreviation = course_abbreviation.replace(' ', '_')
                class_num = page.xpath(
                    "//div[@id='{}{}']/descendant::div[starts-with(@id, '{}')]"
                    "/descendant::*[starts-with(@id, '{}')]/text()"
                    .format(self.box2_id, j, self.box3_id, self.class_num_id)
                )
                class_section = page.xpath(
                    "//div[@id='{}{}']/descendant::div[starts-with(@id, '{}')]"
                    "/descendant::*[starts-with(@id, '{}')]/text()"
                    .format(self.box2_id, j, self.box3_id, self.class_section_id)
                )
                days_times = page.xpath(
                    "//div[@id='{}{}']/descendant::div[starts-with(@id, '{}')]"
                    "/descendant::*[starts-with(@id, '{}')]/text()"
                    .format(self.box2_id, j, self.box3_id, self.days_times_id)
                )
                room = page.xpath(
                    "//div[@id='{}{}']/descendant::div[starts-with(@id, '{}')]"
                    "/descendant::*[starts-with(@id, '{}')]/text()"
                    .format(self.box2_id, j, self.box3_id, self.room_id)
                )
                instructor = page.xpath(
                    "//div[@id='{}{}']/descendant::div[starts-with(@id, '{}')]"
                    "/descendant::*[starts-with(@id, '{}')]/text()"
                    .format(self.box2_id, j, self.box3_id, self.instructor_id)
                )
                meeting_dates = page.xpath(
                    "//div[@id='{}{}']/descendant::div[starts-with(@id, '{}')]"
                    "/descendant::*[starts-with(@id, '{}')]/text()"
                    .format(self.box2_id, j, self.box3_id, self.meeting_dates_id)
                )
                status = page.xpath(
                    "//div[@id='{}{}']/descendant::div[starts-with(@id, '{}')]"
                    "/descendant::*[starts-with(@id, '{}')]/div/img/@alt"
                    .format(self.box2_id, j, self.box3_id, self.status_id)
                )

                class_info = []
                for k in range(len(class_num)):
                    class_info.append(course_abbreviation)
                    class_info.append(class_num[k])
                    class_info.append(self.process_new_line(class_section)[k])
                    class_info.append(self.process_new_line(days_times)[k])
                    class_info.append(self.process_new_line(room)[k])
                    class_info.append(self.process_new_line(instructor)[k])
                    class_info.append(self.process_new_line(meeting_dates)[k])
                    class_info.append(status[k])
                    result.setdefault(course_name, []).append(class_info[:])
                    class_info.clear()

        return result

    def parse_course_details(self, file):
        result = []
        html = etree.parse(file, self.parser)
        raw_course_text = html.xpath("//*[@id='{}']/text()".format(self.course_text_id))[0]
        course_text = ' '.join(raw_course_text.split())

        # get abbreviate course name
        abbreviate_course_name = course_text.split('-')[0]
        result.append(' '.join(abbreviate_course_name.split()).strip())

        # get full course name
        raw_course_name = course_text.split(abbreviate_course_name)[1]
        raw_course_name = raw_course_name[1:].strip()
        raw_course_name = raw_course_name.split()
        del raw_course_name[0]
        course_name = ' '.join(raw_course_name)
        result.append(course_name)
        print(course_name)

        # get units
        units = html.xpath("//*[@id='{}']/text()".format(self.units_id))[0]
        result.append(self.find_float_in_str(units)[0])

        # get class components
        components = html.xpath("//*[@id='{}']/descendant::td/text()".format(self.class_component_id))
        result.append(components[0])

        # get career
        career = html.xpath("//*[@id='{}']/text()".format(self.career_id))[0]
        result.append(career)

        raw_description = html.xpath("//*[@id='{}']/text()".format(self.description_id))
        description = ''
        for des in raw_description:
            if des != u'\r\n':
                description += des.replace('\r\n', '<br>')
        result.append(description.strip())
        return result

    def parse_class_details(self, file):
        result = []
        html = etree.parse(file, self.parser)

        # get instruction mode
        instruct_mode = html.xpath("//*[@id='{}']/text()".format(self.instruct_mode_id))[0]
        result.append(instruct_mode)

        # get enrollment information
        raw_enrollment_info = html.xpath("//*[@id='{}']/descendant::*/text()".format(self.enrollment_info_id))
        enrollment_info = []
        for info in raw_enrollment_info:
            if info != u'\r\n' and info != ' ':
                enrollment_info.append(info.replace('\r\n', '<br>'))
        if enrollment_info:
            del enrollment_info[0]
        result.append(enrollment_info)

        # get seats
        total_seats = html.xpath("//*[@id='{}']/text()".format(self.total_seats_id))[0]
        result.append(total_seats)

        taken_seats = html.xpath("//*[@id='{}']/text()".format(self.taken_seats_id))[0]
        result.append(taken_seats)

        available_seats = html.xpath("//*[@id='{}']/text()".format(self.available_seats_id))[0]
        result.append(available_seats)
        return result

    def parse_related_class(self, file):
        html = etree.parse(file, self.parser)

        auto_enroll_sentence = html.xpath("//div[@id='{}']/text()".format(self.auto_enroll_sentence_id))
        if auto_enroll_sentence:
            if auto_enroll_sentence[0] == "You will automatically be enrolled in the following related class:":
                related_class_section_list = html.xpath("//a[starts-with(@id, '{}')]/text()".format(self.related_class_section_0_id))
                return related_class_section_list
        else:
            related_class_section_list = html.xpath("//a[starts-with(@id, '{}')]/text()".format(self.related_class_section_1_id))
            return related_class_section_list

    @staticmethod
    def find_float_in_str(s):
        return re.findall(r"[-+]?\d*\.\d+|\d+", s)

    @staticmethod
    def process_new_line(my_list):
        # processing multiple lines into one lines separated by <br>
        new_list = []
        position = -1
        for e in my_list:
            if '\r\n' in e:
                new_list[position] += e.replace('\r\n', '<br>')
            else:
                new_list.append(e)
                position += 1
        return new_list

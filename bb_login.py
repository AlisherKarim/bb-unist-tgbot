import requests
import pprint
from bs4 import BeautifulSoup as BS
from models import Course


def get_course_list(user):
    try:
        response = [200]
        s = requests.session()
        auth_html = s.get("https://blackboard.unist.ac.kr/webapps/login/")
        auth_bs = BS(auth_html.content, "html.parser")
        token = auth_bs.find(attrs={"name": "blackboard.platform.security.NonceUtil.nonce"})["value"]
        data = {
            "user_id": user.bb_id,
            "password": user.psw,
            "login": "Login",
            "action": "login",
            "new_loc": "",
            "blackboard.platform.security.NonceUtil.nonce": token
        }

        answ = s.request("POST", "https://blackboard.unist.ac.kr/webapps/login/", data=data)
        if answ.status_code != 200:
            response[0] = answ.status_code
            return response
        else:
            try:
                data2 = {
                    "action": "refreshAjaxModule",
                    "modId": "_22_1",
                    "tabId": "_2_1",
                    "tab_tab_group_id": "_2_1"
                }

                x = s.post("https://blackboard.unist.ac.kr/webapps/portal/execute/tabs/tabAction", data=data2)
                main_page = BS(x.content, "lxml")
                # print("status code for main page: ", x.status_code)

                courses = []

                for li in main_page.find_all('li'):
                    course_id = parse_link(li.a.get("href"))
                    if course_id is not None:
                        courses.append(Course(li.a.string, course_id))
                    else:
                        courses.append(Course(li.a.string))

                response.append(courses)

            except Exception as e:
                print(e)
                response[0] = 400

            return response
    except Exception as e:
        print(e)
        return [400]


def parse_link(link):
    try:
        # print(link)
        i = link.find("id=")
        # print(i)
        i += 3
        j = 0
        course_id = ""
        while j < 10:
            if link[i+j] == '&' or link[i+j] == 'a':
                break
            course_id += link[i+j]
            j += 1
        return course_id
    except Exception as e:
        print(e)
        return None


def get_grades(user, course):
    try:
        response = [200]
        s = requests.session()
        auth_html = s.get("https://blackboard.unist.ac.kr/webapps/login/")
        auth_bs = BS(auth_html.content, "html.parser")
        token = auth_bs.find(attrs={"name": "blackboard.platform.security.NonceUtil.nonce"})["value"]
        data = {
            "user_id": user.bb_id,
            "password": user.psw,
            "login": "Login",
            "action": "login",
            "new_loc": "",
            "blackboard.platform.security.NonceUtil.nonce": token
        }

        answ = s.request("POST", "https://blackboard.unist.ac.kr/webapps/login/", data=data)

        grades = s.get(
            "https://blackboard.unist.ac.kr/webapps/bb-mygrades-BB5a8801a04ee83/myGrades?course_id=" + course.course_id + "&stream_name=mygrades&is_stream=false")
        grades_page = BS(grades.content, "html.parser")
        grades_list = []
        for grade in (grades_page.find_all(attrs={"class": "graded_item_row"})):
            name = grade.find(attrs={"class": "gradable"})
            grade_row = name.get_text().lstrip().rstrip() + ":   "
            score = grade.find(attrs={"class": "grade"})
            grade_row += score.get_text().lstrip().rstrip()
            grades_list.append(grade_row)
        return grades_list

    except Exception as e:
        print(e)
        return []

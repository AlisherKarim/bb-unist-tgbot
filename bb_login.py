import requests
import pprint
from bs4 import BeautifulSoup as BS
from models import Course


def get_course_list(user):
    response = []
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
        response.append(answ.status_code)
        return response
    else:
        response.append(answ.status_code)
        data2 = {
            "action": "refreshAjaxModule",
            "modId": "_22_1",
            "tabId": "_2_1",
            "tab_tab_group_id": "_2_1"
        }

        x = s.post("https://blackboard.unist.ac.kr/webapps/portal/execute/tabs/tabAction", data=data2)
        main_page = BS(x.content, "lxml")
        print("status code for main page: ", x.status_code)

        courses = []

        for li in main_page.find_all('li'):
            courses.append(Course(li.a.string))
            # instructors = li.find_all('span')
            # for i in range(1, len(instructors)):
            #     print(instructors[i].string, end="")
            # print(")")
            # i += 1

        response.append(courses)
        return response

import random
import string
import requests
from bs4 import BeautifulSoup
from utils.utils import get_logger
import urllib3

urllib3.disable_warnings()


class Domain:
    def __init__(self, domain) -> None:
        self.domain = domain
        self.logger = get_logger()
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        self.default_status_code = None
        self.default_title = None
        self.is_passed_checks = False
        self.headers = {"User-Agent" : USER_AGENT}
        self.preliminary_checks()

    def random_generater(self, length: int) -> str:
        random_string = ''.join(random.SystemRandom().choice(
            string.ascii_lowercase) for _ in range(length))
        return random_string

    def preliminary_checks(self):
        current_run = 1
        last_status_code = 0
        length = 8
        while True:
            random_string = self.random_generater(length)
            url = f"https://f{random_string}.{self.domain}"
            res = None
            try:
                res = requests.get(url=url, headers=self.headers, allow_redirects=False, verify=False, timeout=0.5)
            except Exception as e:
                self.logger.debug(f"\x1b[32m preliminary check passed, error on {url}, error: {e}")
                self.is_passed_check = True
                return
            if current_run == 1:
                last_status_code = res.status_code
            else:
                if last_status_code == res.status_code:
                    self.logger.debug(f"\x1b[32m last request and current request have same status code {url}, status code: {last_status_code} \x1b[0m")
                else:
                    self.logger.debug(f"\x1b[32m last request and current request have different status code {url}, last status code: {last_status_code} current status code {res.status_code} \x1b[0m")
                    self.is_passed_check = True
                    return
            if current_run >= 3:
                soup = BeautifulSoup(res.text, "html.parser")
                title_tag = soup.find("title")
                if title_tag:
                    self.default_title = title_tag.text
                self.logger.debug(f"\x1b[31m preliminary check failed domain: {self.domain} \x1b[0m")
                self.default_status_code = last_status_code
                return
            current_run = current_run + 1
            length = length + 1



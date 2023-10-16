import requests
import argparse
from src.domain import Domain
import urllib3
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
from tqdm import tqdm
from utils.utils import get_logger



urllib3.disable_warnings()


class SubBrute:
    def __init__(self, args) -> None:
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        self.headers = {"User-Agent" : USER_AGENT}
        self.args = args
        self.logger = get_logger()
        self.output = []
    
    def file_writer(self, filepath: str, content: list):
        with open(filepath, "a") as f:
            content = "\n".join(content)
            f.write(content)
    
    def file_reader(self, filepath:str) -> list:
        with open(filepath, "r") as f:
            content = f.readlines()
            output = []
            for i in content:
                output.append(i.strip("\n"))
            return output

    def process(self, domain: str, word: str, preliminary_data: Domain):
        word = word.strip()
        domain = domain.strip()
        subdomain = f"{word}.{domain}"
        http_url = f"https://{subdomain}"
        res = None
        status_code = None
        soup = None
        title_tag = None
        title = None
        try:
            res = requests.get(url=http_url, verify=False, allow_redirects=False, headers=self.headers, timeout=0.5)
            status_code = res.status_code
            soup = BeautifulSoup(res.text, "html.parser")
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.text
        except Exception as e:
            self.logger.debug(f"{subdomain} request failed, error: {e}")
            return
        if preliminary_data.is_passed_checks == True:
            self.logger.debug(f" As {domain} passed preliminary, No error in : {subdomain}, new sub identified")
            self.logger.info(f"new domain: {subdomain}, status: {res.status_code}, title: {title}")
            self.output.append(subdomain)
            print(subdomain)
            return
        else:
            if preliminary_data.default_status_code != status_code:
                self.logger.debug(f"preliminary status code and req status code different,{subdomain}, new sub identified")
                self.logger.info(f"new domain: {subdomain}, status: {res.status_code}, title: {title}")
                self.output.append(subdomain)
                print(subdomain)
                return
            if preliminary_data.default_title != title:
                self.logger.debug(f"preliminary title and req title different, new sub identified: {subdomain}")
                self.logger.info(f"new domain: {subdomain}, status: {res.status_code}, title: {title}")
                self.output.append(subdomain)
                print(subdomain)
                return        

    def main(self):
        domain_list = []
        if self.args.filename:
            domain_list = self.file_reader(self.args.filename)
        elif self.args.domains:
            domain_list = str(self.args.domains).split(",")
        else:
            raise ValueError("Either filename or domains input should be provided")
        wordlist = self.file_reader(self.args.wordlist)
        threads = self.args.threads
        self.logger.info(f"Staring enumurating with {threads} threads")
        for domain in domain_list: 
            preliminary_data = Domain(domain)
            Parallel(n_jobs=threads, prefer="threads")(
                delayed(self.process)(domain = domain, word = word, preliminary_data=preliminary_data) for word in tqdm(wordlist))
        if self.args.output:
            self.file_writer(self.args.output, self.output)

if __name__=="__main__":
    parser = argparse.ArgumentParser(
                    prog='SubBruteForce',
                    description='Bruteforce the subdomains')
    parser.add_argument('-f', '--filename', help="File that contains the domain list to bruteforce")
    parser.add_argument('-d', '--domains', help="Domain names to brute force, comma seperated")
    parser.add_argument('-w', '--wordlist', help="Wordlist to brute force", required=True)
    parser.add_argument('-o', '--output', help="Output filename to store the output")
    parser.add_argument('-t', '--threads', help="Number of threads to bruteforce, default=10", 
                        default=10, type=int)
    args = parser.parse_args()
    obj = SubBrute(args=args)
    obj.main()

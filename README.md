# sub-bruteforce
Brute Forcing subdomains with HTTP requests 


# Usage 
```
usage: SubBruteForce [-h] [-f FILENAME] [-d DOMAINS] -w WORDLIST [-o OUTPUT] [-t THREADS]

Bruteforce the subdomains

options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        File that contains the domain list to bruteforce
  -d DOMAINS, --domains DOMAINS
                        Domain names to brute force, comma seperated
  -w WORDLIST, --wordlist WORDLIST
                        Wordlist to brute force
  -o OUTPUT, --output OUTPUT
                        Output filename to store the output
  -t THREADS, --threads THREADS
                        Number of threads to bruteforce, default=10
```

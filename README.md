# statuskode
checking status kode from list site like httpx


# help
usage: python3 statuskode.py [-h] [-l LIST] [-mc MATCH_CODE] [-fc FILTER_CODE] [-t THREADS] [-o OUTPUT] [-r RATE]<br>
<br>
options:<br>
  -h, --help            show this help message and exit<br>
  -l LIST, --list LIST  File containing list of target URLs<br>
  -mc MATCH_CODE, --match-code MATCH_CODE<br>
                        Comma-separated list of status codes to match<br>
  -fc FILTER_CODE, --filter-code FILTER_CODE<br>
                        Comma-separated list of status codes to filter out<br>
  -t THREADS, --threads THREADS<br>
                        Number of threads to use<br>
  -o OUTPUT, --output OUTPUT<br>
                        File to save results<br>
  -r RATE, --rate RATE  Rate limit (requests per second)

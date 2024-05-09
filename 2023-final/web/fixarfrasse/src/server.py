import os
import subprocess
import tempfile
import urllib
from pathlib import Path

from flask import Flask, render_template, request, flash, redirect

app = Flask(__name__)
app.secret_key = bytes.fromhex('cc4b2b48fb8956644fc5abe2d3c16b3d')

SUDO = 'USE_SUDO' in os.environ
FLAG1='SSM{du_fixar_jag_betalar_med_flagga}'
FLAG2='SSM{man_saljer_den_till_dumbommar_och_sa_blir_man_rik_he_he}'

tests_directory = Path(__file__).parent / 'tests'

def run_test(submission_directory, get_params, post_data):
    get_params['testfile'] = submission_directory
    testenv = {}
    testenv['DOCUMENT_ROOT'] = submission_directory
    testenv['GATEWAY_INTERFACE'] = 'CGI/1.1'
    testenv['PWD'] = submission_directory
    testenv['QUERY_STRING'] = urllib.parse.urlencode(get_params)
    testenv['REDIRECT_STATUS'] = '200'
    testenv['REMOTE_ADDR'] = '127.0.0.1'
    testenv['REQUEST_URI'] = '/'
    testenv['SCRIPT_FILENAME'] = tests_directory / 'mock.php'
    testenv['SCRIPT_NAME'] = '/index.php'
    testenv['SERVER_NAME'] = '127.0.0.1'
    testenv['SERVER_PROTOCOL'] = 'HTTP/1.1'
    testenv['SERVER_SOFTWARE'] = 'SSM/1337'
    
    if len(post_data) > 0:
        testenv['CONTENT_LENGTH'] = f'{len(post_data)}'
        testenv['CONTENT_TYPE'] = 'application/x-www-form-urlencoded'
        testenv['REQUEST_METHOD'] = 'POST'
    else:
        testenv['REQUEST_METHOD'] = 'GET'

    try:
        #return subprocess.check_output(['php-cgi', '-C'], input=post_data.encode(), timeout=1, cwd=submission_directory, env=testenv).decode()
        return subprocess.check_output(
            (['sudo'] if SUDO else []) + ['nsjail', '-Mo',
            '--really_quiet',
            #'--keep_caps',
            '--cap', 'CAP_NET_RAW',
        ] + 
        [item for sublist in [('--env', f'{key}={value}') for key, value in testenv.items()] for item in sublist] +
        [
            '--user', '9999',
            '--group', '9999',
            '-T', '/tmp/',
            '-R', submission_directory,
            '-R', tests_directory,
            '-R', '/lib/x86_64-linux-gnu/',
            '-R', '/usr/bin/',
            '-R', '/bin/',
            '-R', '/usr/lib/',
            '-R', '/lib64/',
            '-R', '/usr/lib/x86_64-linux-gnu/',
            '-R', '/etc/',
            #'--', '/usr/bin/strace', '-f', '/usr/bin/php-cgi', '-C',
            '--', '/usr/bin/php-cgi', '-C',
        ], input=post_data.encode(), timeout=1, cwd=submission_directory, env=testenv).decode()
    except subprocess.CalledProcessError as e:
        print(e)
        return ''
    except Exception as e:
        print(e)
        return ''

def test_basic_layout(submission_directory):
    output = run_test(submission_directory, {}, '')
    if not output:
        return False
    if 'My really cool website' not in output:
        return False
    if '<html>' not in output:
        return False
    if '<head>' not in output:
        return False
    if '<body>' not in output:
        return False

    return True

def test_ping(submission_directory):
    output = run_test(submission_directory, {'p': 'ping', 'host':'127.0.0.1'}, '')
    if not output:
        return False
    if '127.0.0.1 ping statistics' not in output:
        return False
    if 'PING 127.0.0.1' not in output:
        return False
    if 'rtt min/avg/max/mdev' not in output:
        return False
    return True

def test_ping_vuln(submission_directory):
    output = run_test(submission_directory, {'p': 'ping', 'host':'127.0.0.1; id'}, '')
    if not output:
        return False
    if 'uid=' in output:
        return False
    if 'gid=' in output:
        return False

    output = run_test(submission_directory, {'p': 'ping', 'host':'127.0.0.1; uname -a'}, '')
    if not output:
        return False
    if 'GNU/Linux' in output:
        return False

    return True

def test_search(submission_directory):
    output = run_test(submission_directory, {'p': 'search', 'contact':'Bamse'}, '')
    if not output:
        return False
    tokens = ['Search results for "Bamse"', 'DUNDER-HONUNG', 'Bamses Hus']
    if any(x not in output for x in tokens):
        return False
    
    output = run_test(submission_directory, {'p': 'search', 'contact':'Berget'}, '')
    if not output:
        return False
    tokens = ['Search results for "Berget"', 'Farmor', 'Höga']
    if any(x not in output for x in tokens):
        return False

    return True

def test_search_xss(submission_directory):
    output = run_test(submission_directory, {'p': 'search', 'contact':'<script>alert(1)</script>'}, '')
    if not output:
        return False
    tokens = ['<script>', '</script>']
    if any(x in output for x in tokens):
        return False

    return True

def test_search_sqli(submission_directory):
    output = run_test(submission_directory, {'p': 'search', 'contact':'" UNION SELECT 1, 7*7, 8*8, recept FROM recept; --'}, '')
    if not output:
        return False
    tokens = ['EXTREMT', 'HEMLIGT', '49', '64']
    if any(x in output for x in tokens):
        return False

    output = run_test(submission_directory, {'p': 'search', 'contact':'" UNION SELECT 7*7, 8*8, 9*9, 11*11; --'}, '')
    if not output:
        return False
    tokens = ['49', '64', '81', '121']
    if any(x in output for x in tokens):
        return False

    return True

def test_stocks(submission_directory):
    output = run_test(submission_directory, {'p': 'stocks', 'stocks':''}, '')
    if not output:
        return False
    tokens = ['SECRET_CONTENT_784839078123643675']
    if any(x not in output for x in tokens):
        return False
    
    output = run_test(submission_directory, {'p': 'stocks', 'stocks':'http://stocks.potatis.se'}, '')
    if not output:
        return False
    tokens = ['SECRET_CONTENT_879123867345451236']
    if any(x not in output for x in tokens):
        return False

    return True

def test_stocks_ssrf(submission_directory):
    output = run_test(submission_directory, {'p': 'stocks', 'stocks':'file://etc/passwd'}, '')
    if not output:
        return False
    tokens = ['EXPLOITED']
    if any(x in output for x in tokens):
        return False

    output = run_test(submission_directory, {'p': 'stocks', 'stocks':'php://filter'}, '')
    if not output:
        return False
    tokens = ['EXPLOITED']
    if any(x in output for x in tokens):
        return False

    output = run_test(submission_directory, {'p': 'stocks', 'stocks':'http://127.0.0.1/?p=admin'}, '')
    if not output:
        return False
    tokens = ['EXPLOITED']
    if any(x in output for x in tokens):
        return False

    return True

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/evaluate", methods=['POST'])
def evaluate():
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect('/')
    
    with tempfile.TemporaryDirectory(prefix='solution_') as tmpdir:
        tmpdir_path = Path(tmpdir)
        tmpdir_path.chmod(0o755)
        submission_path = tmpdir_path / 'index.php'
        file.save(submission_path)

        test_cases_functionality = [
            test_basic_layout,
            test_ping,
            test_search,
            test_stocks,
        ]

        test_cases_vulnerabilities = [
            test_ping_vuln,
            test_search_xss,
            test_search_sqli,
            test_stocks_ssrf,
        ]

        score_functionality = sum(test_case(tmpdir_path) for test_case in test_cases_functionality)
        score_vulnerabilities = sum(test_case(tmpdir_path) for test_case in test_cases_vulnerabilities)

        win1 = score_functionality == len(test_cases_functionality) and score_vulnerabilities >= ((len(test_cases_vulnerabilities)+1)//2)
        win2 = score_functionality == len(test_cases_functionality) and score_vulnerabilities == len(test_cases_vulnerabilities)

        return render_template(
            'score.html',
            score_functionality=score_functionality,
            max_functionality=len(test_cases_functionality),
            score_vulnerabilities=score_vulnerabilities,
            max_vulnerabilities=len(test_cases_vulnerabilities),
            flag1=(FLAG1 if win1 else None),
            flag2=(FLAG2 if win2 else None)
        )

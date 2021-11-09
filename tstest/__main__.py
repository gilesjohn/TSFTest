#!/usr/bin/env python
from os import path
import subprocess
import sys
from tempfile import NamedTemporaryFile
from time import sleep
from typing import List, Union, Optional

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.wait import WebDriverWait

# Todo: setup command which tsconfig.json and webpack config to folder
# Todo: publish node package: https://docs.npmjs.com/creating-node-js-modules

name = 'tstest'
cmd = 'tstest'
cmd_help = f'''{name} - TypeScript frontend testing utility
    Usage:
        {cmd} help - Show helpful information
        {cmd} setup test_dir_path - Adds required default configs to test folder
        {cmd} test_dir_path - Compile all scripts in test_dir_path with webpack, result is \
included in test html page which will be opened in your web browser

    Options:
        --headed - Runs the test in a non headless browser allowing use of developer tools

    {name} requires webpack cli set up to work with TypeScript
'''

available_options = ('--headed',)


def main():
    options = [arg for arg in sys.argv[1:] if arg.startswith("--")]
    args = [arg for arg in sys.argv[1:] if arg not in options]
    invalid_options = [opt for opt in options if opt not in available_options]
    if len(args) != 1:
        return f'Incorrect number of args, try {cmd} help'
    elif len(invalid_options) > 0:
        return f'Invalid options: {", ".join(invalid_options)}'
    elif args[0] == 'help':
        print(cmd_help)
    elif args[0] == 'setup':
        return "Not implemented"
    else:
        headless = '--headed' not in options

        test_path = path.abspath(sys.argv[1])
        if not path.isdir(test_path):
            return f'Invalid path {sys.argv[1]}'

        p = subprocess.Popen('webpack', cwd=test_path, shell=True)
        p.wait()
        if p.returncode != 0:
            return f'Webpack failed with exit code: {p.returncode}'

        js_file_path = path.join(test_path, "dist/test.js")

        script_tag = f'<script>var headless = true;</script><script src="file://{js_file_path}"></script>'
        with open('tstest.html') as f:
            html_content = f.read()
            html_content = html_content.replace('<!load script here!>', script_tag)
            with NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
                temp_file.write(html_content.encode())
                temp_file.flush()
                url = f'file://{temp_file.name}'
                return open_url(url, headless)

    return 0


def document_complete(driver):
    script = 'return document.readyState'
    try:
        return driver.execute_script(script) == 'complete'
    except WebDriverException:
        return False


DISCONNECTED_MSG = 'Unable to evaluate script: disconnected: not connected to DevTools\n'


def browser_closed(driver):
    log = driver.get_log('driver')
    return len(log) > 0 and log[-1]['message'] == DISCONNECTED_MSG


def open_url(url, headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
    # chrome_options.headless = True # also works
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    if not headless:
        WebDriverWait(driver, 20).until(document_complete)
    results = driver.execute_script(f'return await runTests({str(headless).lower()});')
    tests = [Test.from_dict(result) for result in results]
    print()
    for test in tests:
        test.print()
    print(f'{len([test for test in tests if test.passed()])}/{len(tests)} tests passed')
    if headless:
        driver.quit()
    else:
        WebDriverWait(driver, 500).until(browser_closed)
    return 0 if all([test.passed() for test in tests]) else 1


class Assertion:
    message: str
    success: Optional[bool]

    def __init__(self, message: str, success: Optional[bool] = None):
        self.message = message
        self.success = success

    def print(self):
        if self.success is False:
            style_print(self.message, "fail")
        else:
            print(self.message)

    @staticmethod
    def from_dict(dic):
        return Assertion(dic["message"], dic["success"])


print_styles = {
    "header": '\033[95m',
    "blue": '\033[94m',
    "cyan": '\033[96m',
    "green": '\033[92m',
    "warning": '\033[93m',
    "fail": '\033[91m',
    "bold": '\033[1m',
    "underline": '\033[4m'
}


def style_print(text: str, style: str):
    ENDC = '\033[0m'
    if style not in print_styles:
        raise ValueError("Please use a valid style such as the keys for print_styles")
    print(f'{print_styles[style]}{text}{ENDC}')


class Description:
    text: str
    success: Optional[bool]

    def __init__(self, text: str, success: Optional[bool] = None):
        self.text = text
        self.success = success

    def print(self):
        if self.success is True:
            style_print(self.text, "green")
        elif self.success is False:
            style_print(self.text, "fail")
        else:
            print(self.text)

    @staticmethod
    def from_dict(dic):
        return Description(dic["text"], dic["success"])


class Test:
    def __init__(self, name: str, results: List[Union[Assertion, Description]]):
        self.name = name
        self.results = results

    def passed(self):
        return all([result.success is not False for result in self.results])

    def all_assertions(self):
        return [result for result in self.results if isinstance(result, Assertion)]

    def all_failed_assertions(self):
        return [result for result in self.results if isinstance(result, Assertion) and not result.success]

    def print(self):
        style_print(f'Test {self.name}', 'header')
        for result in self.results:
            result.print()
        if self.passed():
            style_print(f'Test {self.name} passed', 'green')
        else:
            style_print(f'Test {self.name} failed', 'fail')
        print()

    @staticmethod
    def from_dict(dic):
        results = []
        for result in dic["results"]:
            if "text" in result:
                results.append(Description.from_dict(result))
            else:
                results.append(Assertion.from_dict(result))
        return Test(dic["name"], results)


if __name__ == '__main__':
    sys.exit(main())

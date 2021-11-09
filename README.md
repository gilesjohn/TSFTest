# TsTest

Simple frontend TypeScript testing utility

STILL UNDER DEVELOPMENT. The following instructions are placeholders and may or may not work.
Do not run commands you don't understand.

I intend to rewrite or at least wrap the python in node.js to simplify installation.

## Installation

Install webpack in your project directory:

    npm install --save-dev webpack webpack-cli typescript ts-loader
    
NPM PACKAGE NOT YET PUBLISHED. Install the typescript functions also in your project directory:

    npm install --save-dev tsftest

Install chromedriver and add to path
https://chromedriver.chromium.org/getting-started

Use pip to install the tsftest command (where `path_to_dir` is the folder containing setup.py):

    pip install path_to_dir --user



## Usage

`tsftest` may not be recognised as a command, if so replace with:

    python -m tsftest

To add default required configuration files if the files don't exist, run:

    tsftest setup path_to_test_folder

To run the tests use:
 
    tsftest path_to_test_folder
    
You can make a browser window open with the tests allowing the use of browser developer tools with:

    tsftest --headed path_to_test_folder

## Example Test

```
import { Api, ApiCredentials, ApiRequest } from "../src/api";
import { test, Test } from "tsftest"

test("ApiRequest class",
    (t: Test) => {
        let request = new ApiRequest("GET", "/");

        t.describe("ApiRequest should have GET method");
        t.assert(request.method, "GET");
    }
)

test("Api class",
    async (t: Test) => {
        let api = new Api(new URL("https://sphere.type1.fun"), new ApiCredentials())
        let request = new ApiRequest("GET", "/");

        let response = await api.call(request)

        t.describe("Api.call should return an instance of Response");
        t.assertInstance(response, Response);

        t.describe("Testing successful Api.call to /");
        t.assert(response.ok, true);
    }
)
```
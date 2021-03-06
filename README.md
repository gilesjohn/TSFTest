# TSFTest

Simple frontend TypeScript testing utility.

## Installation

Install webpack in your project directory:

    npm install --save-dev webpack webpack-cli typescript ts-loader
    
Install the typescript functions also in your project directory:

    npm install --save-dev tsftest

Install chromedriver and add to path
https://chromedriver.chromium.org/getting-started

Use pip to install the tsftest command (where `path_to_dir` is the folder containing setup.py):

    pip install path_to_dir --user

Create a test folder in your project if you don't have one already.

Either:

- Add `tsconfig.json` and `webpack.config.js` files to the test folder with settings to compile to `test_dir/dist/test.js`.

OR
- See the setup command in the Usage section for a simple command to add these files with a default configuration.

## Usage

To add default required configuration files if the files don't exist, run:

    python -m tsftest setup path_to_test_folder

To run the tests use (consider setting this in your package.json->scripts.test):
 
    python -m tsftest path_to_test_folder
    
You can make a browser window open with the tests allowing the use of browser developer tools with:

    python -m tsftest --headed path_to_test_folder

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
        let api = new Api(new URL("http://127.0.0.1"), new ApiCredentials())
        let request = new ApiRequest("GET", "/");

        let response = await api.call(request)

        t.describe("Api.call should return an instance of Response");
        t.assertInstance(response, Response);

        t.describe("Testing successful Api.call to /");
        t.assert(response.ok, true);
    }
)
```
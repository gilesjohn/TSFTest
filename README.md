# TsTest

Simple frontend TypeScript testing utility

## Installation

Install webpack:

    npm install --global webpack webpack-cli typescript ts-loader
    
Install the typescript functions:

    npm install tstest

Install chromedriver and add to path
https://chromedriver.chromium.org/getting-started

Use pip install to install the python package


## Usage

To add default required configuration files if the files don't exist, run:

    tstest setup path_to_test_folder

To run the tests use:
 
    tstest path_to_test_folder
    
You can make a browser window open with the tests allowing the use of browser developer tools with:

    tstest --headed path_to_test_folder
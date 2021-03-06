[![Build Status](https://travis-ci.org/Kai-Striega/FuelwatchReader.svg?branch=master)](https://travis-ci.org/Kai-Striega/FuelwatchReader)
# Fuelwatch Price Reader
This script parses the Fuelwatch RSS feed, finds the lowest fuel price then sends an SMS to a designated mobile number containing the lowest fuel prices for a given list of suburbs.

## Example
To run the script execute `./fuelscanner.py` or `python fuelscanner.py` from the command line.
The expected output is an SMS message listing the two cheapest fuel prices of the form: {price} ({discount}) at {station-name}, {station-address}

![An example sms message](images/exampleSMSmessage.png) ![Another example sms message](images/exampleSMSmessage2.png)

## Getting Started
### Requirements
- Python 3.6 or higher.
- Twilio Account. Twilio offers a [trial account](https://www.twilio.com/try-twilio) which provides all required functions.

### Set Up
#### Clone or download the git repository
Github offers [full instructions](https://help.github.com/articles/cloning-a-repository/) on how to clone or download, however for linux.

- On the main page of the repository click on the Clone or download button.
- Copy the url to your clipboard.
- Open a terminal in the wanted directory.
- Enter `git clone REPOSITORY_URL` to clone the repository.

#### Accessing your Twilio account details
- To access the Sid and Auth Token go to: `"Console Dashboard" -> "Settings" -> "General" -> "API Credentials"`
- To access your account number you will need to purchase a number (this is included in your trial).
  - To purchase a number go to: `"Console Dashboard" -> "Phone Numbers" -> "Buy a Number"`.
  - Select any number with `sms` capability and select the `Buy` button.
  - To view your Twilio number go to: `"Console Dashboard" -> "Phone Numbers" -> "Verified Caller IDs"`

Note: Twilio strongly encourages using [E.164](https://en.wikipedia.org/wiki/E.164) formatting. The prefix for Australia is `+61`. If your mobile number is `04 1234 5678`, it should be written as `+61412345678`. For a more detailed explanation see the Twilio [article](https://support.twilio.com/hc/en-us/articles/223183008-Formatting-International-Phone-Numbers)

#### Update the config file
Open the config file `vi configfile.ini`
The required fields to run the script are:
- mobile_number: The number to which the text will be sent.
- sid: Twilio secure identifier.
- auth_token Twilio authentication.
- twilio_number: Number from which the text will be sent.

If you intend to run the tests also update `fixtures/test_configfile`, with your test account credentials.
- test_sid: Twilio test account secure identifier.
- test_auth_token: Twilio test account secure identifier.
- trial_account: Whether the Twilio account is a trial account.

#### Install Dependencies
- (Optional) Set up a python virtual environment
  - To create the venv: `python3.6 -m venv fuelparser-env`
  - Activate the virtual environment:
    - Unix / Mac: `source fuelparser-env/bin/activate`
    - Windows: `fuelparser-env\Scripts\activate.bat`
- Install the required python packages: `pip install -r requirements.txt`

#### Run the tests (Recommended)
- Ensure the test_sid, test_auth_token and trial_account values are set in the configuration file.
- Run the tests to ensure everything is functioning; `python tests.py -v`

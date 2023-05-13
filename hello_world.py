# Had to run the command below to ensure the interpreter 
# export PYTHONPATH="${PYTHONPATH}:/home/ubuntu/Code/Standalone/mintapi/"

import mintapi
import configparser
from pathlib import Path
import os
import logging
import shutil

SESSION_PATH = "/home/ubuntu/.config/google-chrome"
HEADLESS = True

def main():
    logging.basicConfig(level=logging.INFO)
    
    root_folder = str(Path(__file__).parent)
    
    # Config setup
    config = configparser.ConfigParser()
    config.read(root_folder + '/config.ini')

    
    
    
    shutil.rmtree(root_folder + "/DOMExport")
    os.makedirs(root_folder + "/DOMExport")

    shutil.rmtree(root_folder + "/Screenshots")
    os.makedirs(root_folder + "/Screenshots")
    
    mint = mintapi.Mint(
        config['Mint']['email'].lower(),  # Email used to log in to Mint
        config['Mint']['password'],  # Your password used to log in to mint
        # Optional parameters
        mfa_method='soft-token',  # See MFA Methods section        
        # Can be 'sms' (default), 'email', or 'soft-token'.
        # if mintapi detects an MFA request, it will trigger the requested method
        # and prompt on the command line.
        mfa_input_callback=None,  # see MFA Methods section
        # can be used with any mfa_method
        # A callback accepting a single argument (the prompt)
        # which returns the user-inputted 2FA code. By default
        # the default Python `input` function is used.
        mfa_token=config['Mint']['mfaToken'],   # see MFA Methods section
        # used with mfa_method='soft-token'
        # the token that is used to generate the TOTP
        # account name when multiple accounts are registered with this email.
        intuit_account=config['Mint']['email'].lower(),
        headless=HEADLESS,  # Whether the chromedriver should work without opening a
        # visible window (useful for server-side deployments)
        # None will use the default account.
        # Directory that the Chrome persistent session will be written/read from.
        # session_path=Path(__file__).parent / "Session",
        session_path = SESSION_PATH,
        # To avoid the 2FA code being asked for multiple times, you can either set
        # this parameter or log in by hand in Chrome under the same user this runs
        # as.
        imap_account=config['Gmail']['username'],  # account name used to log in to your IMAP server
        imap_password=config['Gmail']['password'],  # account password used to log in to your IMAP server
        imap_server="imap.gmail.com",  # IMAP server host name
        imap_folder="Intuit",  # IMAP folder that receives MFA email
        wait_for_sync=True,  # do not wait for accounts to sync
        wait_for_sync_timeout=500,  # number of seconds to wait for sync
        # True will use a system provided chromedriver binary that
        use_chromedriver_on_path=False,
        # is on the PATH (instead of downloading the latest version)
        # pre-configured driver. If None, Mint will initialize the WebDriver.
        driver=None,
        save_directory=str(Path(__file__).parent),
    )

    accounts = mint.get_account_data()
    print(f'Number of accounts = {len(accounts)}')
    
    
if __name__ == '__main__':
    main()

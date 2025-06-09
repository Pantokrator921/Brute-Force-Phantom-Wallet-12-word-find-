# Phantom Wallet - 12th Word Finder

This Python script is designed to recover the twelfth and final word of a 12-word seed phrase for a Phantom Wallet. It automates the process of testing every possible word from the BIP-39 wordlist as the twelfth word to regain access to a wallet where only this single word is missing.

**IMPORTANT: USE AT YOUR OWN RISK.** Automating wallet recovery is risky and should be handled with caution. Review the code carefully to ensure it does not perform any malicious actions. The author of this script assumes no liability for any loss of funds or other damages that may result from using this software.

## How It Works

The script uses the `Selenium` library to remotely control a Google Chrome browser. The process is automated as follows:

1.  **Starts Chrome with Extension:** The script opens a new Chrome browser window and automatically loads the Phantom Wallet extension (`.crx` file) that you provide.
2.  **Reads BIP-39 Wordlist:** It reads a local copy of the official BIP-39 wordlist (which contains 2048 English words). This file must be provided by the user.
3.  **Creates and Tests Phrases:** The script takes the 11 words entered by the user and combines them, one by one, with each of the 2048 possible words in the twelfth position.
4.  **Validates the Checksum:** To drastically speed up the process, a BIP-39 checksum is first calculated for each generated 12-word phrase. Only phrases with a valid checksum are tested further. This eliminates thousands of invalid attempts before they are even entered into the wallet.
5.  **Automated Input:** A valid seed phrase is typed into the recovery field of the Phantom Wallet interface.
6.  **Checks for a Balance:** After successfully importing an account, the script checks if the resulting wallet has a balance greater than $0.00. This serves as an indicator of a successful recovery.
7.  **Reports Success and Stops:** If a balance is found, the process is immediately halted. The complete, correct 12-word seed phrase is printed to the console, and the script terminates.

## Prerequisites

Before you begin, ensure you have the following software installed on your system:

* **Python 3.x**
* **Google Chrome Browser**
* **ChromeDriver**: The version must exactly match your installed Google Chrome version.
* The **`.crx` file** for the Phantom Wallet extension.

## Installation Guide

1.  **Clone or Download the Repository:**
    ```bash
    git clone [https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git](https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git)
    cd YOUR-REPOSITORY
    ```

2.  **Install Dependencies:**
    Install the `Selenium` library using pip.
    ```bash
    pip install selenium
    ```

3.  **Set up ChromeDriver:**
    * Download the appropriate [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/).
    * Unzip the file and place the executable (`chromedriver.exe` or `chromedriver`) either in the same folder as the Python script or in a directory that is included in your system's `PATH` variable.

4.  **Create Project Structure:**
    The script expects the BIP-39 wordlist to be in a specific subfolder.
    * Create a folder named `phantomBot` in the project's root directory.
    * Download the [English BIP-39 wordlist](https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt).
    * Save the list as `english.txt` inside the `phantomBot` folder. The structure should look like this:
        ```
        /YOUR-REPOSITORY
        |-- phantomBot.py
        |-- phantomBot/
        |   |-- english.txt
        ```

5.  **Find the Phantom `.crx` File:**
    * The `EXTENSION_PATH` variable in the script needs the path to the Phantom `.crx` file. You can find this in your Chrome/Chromium configuration folder. Look for the `.../Extensions/bfnaelmomeimhlpmgjnjophhpkkoljpa/...` folder in your user profile to find the `.crx` file. The exact path varies by operating system.

6.  **Configure the Script:**
    Open the `phantomBot.py` file in a text editor and adjust the following variables:

    * **`EXTENSION_PATH`**: Replace the example path with the **absolute path** to your `.crx` file.
        ```python
        # Example for Windows (note the 'r' prefix)
        EXTENSION_PATH = r'C:\Users\YourName\AppData\Local\Google\Chrome\User Data\Default\Extensions\bfnaelmomeimhlpmgjnjophhpkkoljpa\25.20.0_0.crx'
        
        # Example for Linux
        EXTENSION_PATH = r'/home/yourname/.config/chromium/Default/Extensions/bfnaelmomeimhlpmgjnjophhpkkoljpa/25.20.0_0.crx'
        ```

    * **`seed_words`**: Enter your **first 11 known words** in the exact correct order.
        ```python
        seed_words = [
            'awake', 'normal', 'identify', 'grid', 'cinnamon', 'arrest',
            'invite', 'salmon', 'crumble', 'protect', 'expose'
        ]
        ```

## Execution

Open a terminal or command prompt, navigate to the project directory, and run the script:

```bash
python phantomBot.py
```

The script will now open a Chrome window and begin the search. You can follow the progress live in the terminal. When the correct phrase is found, it will be printed in the terminal.

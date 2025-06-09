# phantomBot.py (Version 18 - Searches only for the 12th word)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import itertools
from hashlib import sha256
import binascii

# --- USER INPUT ---
# 1. Path to the Phantom .crx file
EXTENSION_PATH = r'YOUR EXTENSION PATH (CRX) FROM PHANTOM WALLET (ID)' #YOU MUST START CHROME BROWSER ON DEVELOPER MODE FOR THE ID FROM EXTENSION
# 2. Your FIRST 11 known words in the correct order
seed_words = [
    'awake', 'normal', 'identify', 'grid', 'cinnamon', 'arrest',
    'invite', 'salmon', 'crumble', 'protect', 'expose'
]
# -------------------------

# Open Chrome with the extension
OPT = webdriver.ChromeOptions()
OPT.add_extension(EXTENSION_PATH)
DRIVER = webdriver.Chrome(options=OPT)

def main():
    startup()

#___________________________
# HELPER FUNCTIONS
#___________________________

def startup(skip_count=0):
    possible_words = get_bip39_words_list()
    if not possible_words: return
    
    count = 0
    time.sleep(4)
    switchToCurrentTab()
    
    DRIVER.get('chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/onboarding.html?append=true')
    time.sleep(1)

    # --- SIMPLIFIED LOGIC ---
    # The loop now only tests the 12th word
    print(f"[INFO] Starting search for the 12th word...")
    for word in possible_words:
        # Create the test phrase with 12 words
        check_seed_words = seed_words.copy()
        check_seed_words.append(word)
        input_string = " ".join(check_seed_words)

        # Immediately skip phrases with an invalid checksum
        if not is_checksum_valid(check_seed_words):
            continue
        
        # Skip if desired
        if skip_count > 0:
            skip_count -= 1
            count += 1
            continue
        
        print(f"Attempt #{count + 1}: Testing '{word}' as the last word...", end='\r')
        inputSeedWords(input_string)
        
        if accountHasBalance():
            print(f"\n\n!!! SUCCESS !!! Wallet found with phrase: {input_string}")
            return # End the script on success
        else:
            # Return to the import page for the next attempt
            DRIVER.get('chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/onboarding.html?append=true')
            time.sleep(1)
        count += 1
    
    print("\nAll 2048 words have been searched as the 12th word.")


def inputSeedWords(seed_word_string):
    """Inputs the seed phrase into the Phantom wallet field."""
    elem = tryToLocateElement('/html/body/div/main/div[2]/form/div/div[2]/div[1]/input')
    if elem:
        # Clears the field before sending new words
        elem.clear()
        elem.send_keys(seed_word_string)
        time.sleep(0.5)
        button = tryToLocateElement('/html/body/div/main/div[2]/form/button')
        if button: button.click()
        time.sleep(0.5)
        try:
            view_accounts_button = tryToLocateElement('/html/body/div/main/div[2]/form/button[1]', timeout=1)
            if view_accounts_button: view_accounts_button.click()
        except:
            pass

def accountHasBalance():
    """Checks if the imported wallet has a balance."""
    try:
        balance_element = tryToLocateElement("//div[starts-with(text(), '$')]", timeout=10)
        if balance_element:
            balance_text = balance_element.text
            if balance_text != "$0.00":
                print(f"\n[INFO] Balance found: {balance_text}")
                return True
        return False
    except Exception:
        return False


def switchToCurrentTab():
    if len(DRIVER.window_handles) > 1:
        DRIVER.switch_to.window(DRIVER.window_handles[-1])

def get_bip39_words_list():
    try:
        with open('phantomBot/english.txt') as file:
            lines = [line.rstrip() for line in file]
        assert(len(lines) == 2048)
        return lines
    except FileNotFoundError:
        print("\nERROR: File 'phantomBot/english.txt' not found!")
        return None

def is_checksum_valid(seed_phrase_list):
    """Checks if a 12-word phrase has a valid checksum."""
    if len(seed_phrase_list) != 12: return False
    bip39_words = get_bip39_words_list()
    if not bip39_words: return False
    try:
        indices = [bip39_words.index(word) for word in seed_phrase_list]
        b = ''.join(bin(i)[2:].zfill(11) for i in indices)
        entropy, checksum = b[:128], b[128:]
        hashed_entropy = sha256(binascii.unhexlify('%032x' % int(entropy, 2))).hexdigest()
        expected_checksum = bin(int(hashed_entropy, 16))[2:].zfill(256)[:4]
        return checksum == expected_checksum
    except (ValueError, TypeError):
        return False

def tryToLocateElement(xpath, timeout=5):
    sleepTimer = 0
    while sleepTimer < timeout:
        try:
            elem = DRIVER.find_element(by=By.XPATH, value=xpath)
            return elem
        except NoSuchElementException:
            time.sleep(0.25)
            sleepTimer += 0.25
    return None

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nAn unexpected error has terminated the script: {e}")
    finally:
        print("\nClosing script.")
        if 'DRIVER' in locals():
            DRIVER.quit()

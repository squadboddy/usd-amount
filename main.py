from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configure Chrome options for headless mode
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")  # Set the window size

# Set up Chrome and open the webpage
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


def check_address(address):
    try:
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "input"))
        )

        # Locate the search box by input tag and input the address, then press Enter
        search_box = driver.find_element(By.TAG_NAME, "input")
        search_box.clear()
        search_box.send_keys(address + Keys.RETURN)

        # Wait for the result element to be visible
        amount_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "db-user-amount"))
        )

        # Extract the amount text and convert to a float after removing any formatting
        amount = float(amount_element.text.replace(',', '').replace('$', ''))
        print(f"Address: {address}")
        print(f"Amount: {amount}")
        return amount
    except Exception as e:
        print(f"Failed to check address {address}: {str(e)}")
        return 0
    finally:
        # Close the browser after processing all addresses
        print("\n")


def main():
    total_amount = 0
    with open('wallets.txt', 'r') as file:  # Open the file containing the addresses
        addresses = [line.strip() for line in file if line.strip()]  # Read and clean each line
    
    driver.get("https://debank.com/")

    for address in addresses:
        amount = check_address(address)
        total_amount += amount
        time.sleep(5)  # Sleep to avoid hitting the server too quickly

    driver.quit()

    print(f"Total amount across all addresses: {total_amount}")


if __name__ == "__main__":
    main()

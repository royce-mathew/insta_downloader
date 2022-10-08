import os
import time
import platform
import json

from os import path

from json.decoder import JSONDecodeError

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException



class InstagramDownloader(object):
	def __init__(self):
		current_path : str = os.path.dirname(os.path.realpath(__file__)) # Get Current path of file
		geckodriverpath : str = "" # Initialize gecko driver path string
		json_file_path : str = current_path + '/../assets/data.json'

		if not path.exists(json_file_path):
			with open(json_file_path, 'w') as datafile:
				json_data = {} # Initialize empty list
				
				# Prompt user for username, password
				print("It seems to be your first time running this program.")

				self.username, self.password = self.get_data()
				
				# Set username and password inside the json list
				json_data["username"] = self.username
				json_data["password"] = self.password


				# Dump json data to empty file
				json.dump(json_data, datafile)

		else:
			with open(json_file_path) as datafile:
				try:
					json_data = json.load(datafile)
					self.username = json_data["username"]
					self.password = json_data["password"]
				except Exception as e:
					if e == JSONDecodeError or e == KeyError or AttributeError:
						os.remove(json_file_path) # Remove file
						self.__init__() # Call the constructor 
						print("Json Decode error happened, deleting json file")
					else:
						print(e)
			

		# Match geckodriver path based on platform
		match platform.system():
			case "Linux":
				geckodriverpath = '/../assets/geckodriver_linux'
			case "Darwin":
				geckodriverpath = '/../assets/geckodriver_macos'
			case "Windows":
				geckodriverpath = '/../assets/geckodriver.exe'

		# Get full path of geckodriver
		self.gecko_path = current_path + geckodriverpath
		self.login_browser()

	@staticmethod
	def get_data():
		local_username: str = input("Please enter your username: ")
		local_pass: str = input("Please enter your username: ")

		# Display Data
		print("\nAre you happy with your current data?")
		print(f"Username: {local_username}")
		print(f"Password: {len(local_pass) * '*'}")

		happy_input = input("Enter y/n (default yes): ").lower().replace("\n", "") # Prompt user for input

		if happy_input == "y" or happy_input == "yes" or happy_input == "":
			return local_username, local_pass
		else:
			print("Please Re-Enter your data")
			return InstagramDownloader.get_data()

	@staticmethod
	def get_options():
		args : list[str] = [
			"--window-size=1920,1080",
			# "--headless",
			# "--disable-gpu",
			"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
		]
		firefox_options = webdriver.FirefoxOptions()
		for arg in args:
			firefox_options.add_argument(arg)

		return firefox_options


	# Log into the browser
	def login_browser(self):
		driver = webdriver.Firefox(service=Service(self.gecko_path), options=self.get_options())
		self.driver = driver

		try:
			# Wait max 10 seconds or present timeout exception
			wait = WebDriverWait(driver, 10)

			driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher") # Go to instagram homepage
			
			# Wait until username elements are located
			user_element = wait.until(expected_conditions.presence_of_element_located((By.NAME, "username")))
			passwd_element = wait.until(expected_conditions.presence_of_element_located((By.NAME, "password")))

			# Send values to the textboxes
			user_element.send_keys(self.username)
			passwd_element.send_keys(self.password)
			passwd_element.send_keys(Keys.RETURN)

			# Wait until not now element loads (Essentially waiting for data to be passed)
			wait.until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/div/button")))

		except (NoAlertPresentException, TimeoutException) as py_ex:
			print("Alert not present")
			print (py_ex)
			print (py_ex.args)
			driver.close()

	def download(self, url : str) -> None:
		driver = self.driver
		driver.get(url)
		# IMPLEMENTATION NOT YET DONE




# Main Method
def main():
	url = "https://www.instagram.com/p/CjAcfHKvmnp"#  Test case
	# Create a new instagram Downloader class and parse the args to it
	downloader = InstagramDownloader()
	downloader.download(url=url)
	# video_downloader(url)


if __name__ == '__main__':
    main()

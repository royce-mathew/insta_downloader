import os
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Get Current path of file
current_path = os.path.dirname(os.path.realpath(__file__))
# Get Path of geckodriver
exc_path = current_path + '../assets/geckodriver'

# Video Downloader Function, takes url String
def video_downloader(url : str):
	# Open the firefox webdriver
	driver = webdriver.Firefox(executable_path=r'%s' % exc_path)
	driver.get(url) # Open passed url
	elementName = driver.find_elements_by_class_name("tWeCl") # The tWeCl element contains the video data
	src_url = elementName[0].get_attribute("src") # Get video url for download

	# Get Video name using string formatting
	video_name = (url.split('/'))[4]

	# Download the Video using urlretrieve from urllib
	urllib.request.urlretrieve(src_url, video_name + '.mp4')

	driver.close() # Close Gecko Driver


# Main Method
def main():
    url = input("Please enter url_link> ") # Prompt user for url input
    video_downloader(url)


if __name__ == '__main__':
    main()

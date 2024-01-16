import boto3
import os
from selenium import webdriver
from time import sleep
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = os.environ.get('LOGIN_URL')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
IP_INTERFACE_DESCRIPTION = os.environ.get('IP_INTERFACE_DESCRIPTION')
FIRST_SERVER = os.environ.get('FIRST_SERVER')
SECOND_SERVER = os.environ.get('SECOND_SERVER')
THIRD_SERVER = os.environ.get('THIRD_SERVER')

def handler(event=None, context=None):
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = "/opt/chrome/chrome"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    browser = webdriver.Chrome(options=options, service=service)

    browser.get(LOGIN_URL)

    sleep(3)

    # Login
    username_input = browser.find_element(By.NAME, "username")
    password_input = browser.find_element(By.NAME, "password")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)

    password_input.submit()

    sleep(3)

    # Select Servers Page
    servers_button = browser.find_element(By.CLASS_NAME, "servers")
    servers_button.click()

    sleep(3)

    ec2_client = boto3.client('ec2')
    ip_interfaces = ec2_client.describe_network_interfaces(Filters=[{'Name': 'description', 'Values': [IP_INTERFACE_DESCRIPTION]}])

    ip_addrs = []
    for ip_interface in ip_interfaces['NetworkInterfaces']:
        ip_addrs.append(ip_interface['Association']['PublicIp'])

    for ip_route in ip_addrs:

        # Stop First Server
        stop_button_backend = browser.find_element(By.XPATH, "//div[@class='server'][1]/div[@class='server-header']/button[@class='server-stop btn btn-warning btn-sm no-select']")
        stop_button_backend.click()

        sleep(3)

        # Add route- First Server
        route_button = browser.find_element(By.XPATH, "//div[@class='servers-list-buttons']/button[@class='header-button servers-add-route btn btn-primary']")
        route_button.click()

        sleep(3)

        network_input = browser.find_element(By.XPATH, "//div[@class='route-network form-group']/input[@class='form-control']")
        service_select = browser.find_element(By.XPATH, "//div[@class='server form-group']/select[@class='form-control']")

        network_input.send_keys(ip_route)

        select = Select(service_select)
        select.select_by_visible_text(FIRST_SERVER)

        attach_button = browser.find_element(By.XPATH, "//div[@class='modal-footer']/button[@class='btn btn-primary ok']")
        attach_button.click()

        sleep(3)

        # Restart First Server
        start_button_backend = browser.find_element(By.XPATH, "//div[@class='server'][1]/div[@class='server-header']/button[@class='server-start btn btn-success btn-sm no-select']")
        start_button_backend.click()

        sleep(3)

        # Stop Second Server
        stop_button_devops = browser.find_element(By.XPATH, "//div[@class='server'][2]/div[@class='server-header']/button[@class='server-stop btn btn-warning btn-sm no-select']")
        stop_button_devops.click()

        sleep(3)

        # Add Route - Second Server
        route_button = browser.find_element(By.XPATH, "//div[@class='servers-list-buttons']/button[@class='header-button servers-add-route btn btn-primary']")
        route_button.click()

        sleep(3)

        network_input = browser.find_element(By.XPATH, "//div[@class='route-network form-group']/input[@class='form-control']")
        service_select = browser.find_element(By.XPATH, "//div[@class='server form-group']/select[@class='form-control']")

        network_input.send_keys(ip_route)

        select = Select(service_select)
        select.select_by_visible_text(SECOND_SERVER)

        attach_button = browser.find_element(By.XPATH, "//div[@class='modal-footer']/button[@class='btn btn-primary ok']")
        attach_button.click()

        sleep(3)

        # Restart Second Server
        start_button_devops = browser.find_element(By.XPATH, "//div[@class='server'][2]/div[@class='server-header']/button[@class='server-start btn btn-success btn-sm no-select']")
        start_button_devops.click()

        sleep(3)

        # Stop Third Server
        stop_button_front = browser.find_element(By.XPATH, "//div[@class='server'][3]/div[@class='server-header']/button[@class='server-stop btn btn-warning btn-sm no-select']")
        stop_button_front.click()

        sleep(3)

        # Add Route - Third Server
        route_button = browser.find_element(By.XPATH, "//div[@class='servers-list-buttons']/button[@class='header-button servers-add-route btn btn-primary']")
        route_button.click()

        sleep(3)

        network_input = browser.find_element(By.XPATH, "//div[@class='route-network form-group']/input[@class='form-control']")
        service_select = browser.find_element(By.XPATH, "//div[@class='server form-group']/select[@class='form-control']")

        network_input.send_keys(ip_route)

        select = Select(service_select)
        select.select_by_visible_text(THIRD_SERVER)

        attach_button = browser.find_element(By.XPATH, "//div[@class='modal-footer']/button[@class='btn btn-primary ok']")
        attach_button.click()

        sleep(3)

        # Restart Third Server
        start_button_front = browser.find_element(By.XPATH, "//div[@class='server'][3]/div[@class='server-header']/button[@class='server-start btn btn-success btn-sm no-select']")
        start_button_front.click()

    browser.quit()
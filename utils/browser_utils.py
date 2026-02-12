import os
import platform
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from fake_useragent import UserAgent

def get_browser_driver():
    # 获取项目根目录
    base_dir = Path(__file__).resolve().parent.parent
    driver_folder = os.path.join(base_dir, 'web_driver')

    # 检测系统平台
    system = platform.system()
    ua = UserAgent()
    chrome_executable_name = 'chrome.exe' if system == 'Windows' else 'google-chrome'
    chrome_executable = shutil.which(chrome_executable_name)
    if chrome_executable:
        chrome_driver_name = 'chromedriver.exe' if system == 'Windows' else 'chromedriver'
        chrome_driver_path = os.path.join(driver_folder, chrome_driver_name)
        if os.path.exists(chrome_driver_path):
            service = ChromeService(chrome_driver_path)
            chrome_user_agent = ua.chrome
            options = webdriver.ChromeOptions()
            options.add_argument(f'user-agent={chrome_user_agent}')
            options.add_argument('--headless')  # 无头模式
            return webdriver.Chrome(service=service, options=options)

    # 若 Chrome 不可用，尝试 Firefox 浏览器
    firefox_executable_name = 'firefox.exe' if system == 'Windows' else 'firefox'
    firefox_executable = shutil.which(firefox_executable_name)
    if firefox_executable:
        firefox_driver_name = 'geckodriver.exe' if system == 'Windows' else 'geckodriver'
        firefox_driver_path = os.path.join(driver_folder, firefox_driver_name)
        if os.path.exists(firefox_driver_path):
            service = FirefoxService(firefox_driver_path)
            firefox_user_agent = ua.chrome
            options = webdriver.FirefoxOptions()
            options.add_argument(f'user-agent={firefox_user_agent}')
            options.add_argument('--headless')  # 无头模式
            return webdriver.Firefox(service=service, options=options)

    # 若 Chrome 和 Firefox 都不可用，尝试 Edge 浏览器
    edge_executable_name = 'msedge.exe' if system == 'Windows' else 'microsoft-edge'
    edge_executable = shutil.which(edge_executable_name)
    if edge_executable:
        edge_driver_name = 'msedgedriver.exe' if system == 'Windows' else 'msedgedriver'
        edge_driver_path = os.path.join(driver_folder, edge_driver_name)
        if os.path.exists(edge_driver_path):
            service = EdgeService(edge_driver_path)
            edge_user_agent = ua.chrome
            options = webdriver.EdgeOptions()
            options.add_argument(f'user-agent={edge_user_agent}')
            options.add_argument('--headless')  # 无头模式
            return webdriver.Edge(service=service, options=options)
    # 若都不可用，抛出异常
    if chrome_executable is None and firefox_executable is None and edge_executable is None:
        raise Exception("No supported browser found or browser environment path is missing.")
    else:
        raise Exception("Web driver is missing.")
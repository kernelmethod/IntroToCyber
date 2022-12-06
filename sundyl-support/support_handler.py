#!/usr/bin/env python3

import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=Path(__file__).name,
        description="Support server handler",
    )
    parser.add_argument("url")

    args = parser.parse_args()

    options = webdriver.FirefoxOptions()
    # options.set_headless()
    options.headless = True
    options.add_argument("--headless")
    options.set_preference("dom.webnotifications.enabled", False)
    driver = webdriver.Firefox(
        options=options,
        service_log_path="/tmp/geckodriver.log",
        executable_path="/usr/local/bin/geckodriver",
    )

    with open("/run/secrets/STAFF_PASSWORD", "r") as f:
        password = f.read()

    # Log in as the support user
    driver.get("http://www.sundyl.lab/auth/login")
    driver.find_element(By.ID, "id_username").send_keys("freddy_obrzut")
    driver.find_element(By.ID, "id_password").send_keys(password)
    driver.find_element(By.ID, "id_submit").click()

    # Now go to the input URL
    driver.get(args.url)
    time.sleep(1)
    driver.quit()

import flask
from flask import request, jsonify, Flask
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
"""
import subprocess as sp
from pathlib import Path

app = Flask(__name__)

"""
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
"""

with open("/run/secrets/STAFF_PASSWORD", "r") as f:
    password = f.read()

@app.route("/visit")
def visit():
    if (url := request.json.get("url")) is None:
        return jsonify({"detail": "No URL was provided"}, 422)

    """
    print(f"Requested visit to {url = !r}")

    # Log in as the support user
    driver.get("http://www.sundyl.lab/auth/login")
    driver.find_element(By.ID, "id_username").send_keys("freddy_obrzut")
    driver.find_element(By.ID, "id_password").send_keys(password)
    driver.find_element(By.ID, "id_submit").click()

    # Now go to the input URL
    driver.get(url)
    driver.quit()
    """

    args = ["python3", "support_handler.py", url]
    sp.run(args)

    return "okay"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

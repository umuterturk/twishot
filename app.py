# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
import io

from flask import Flask
from flask import request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
from flask import send_file

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
DRIVER = 'chromedriver'
content = """<html lang="en"><body><blockquote class="twitter-tweet"><p lang="tr" dir="ltr"><a href="https://twitter.com/aliekbererturk/status/{}"></a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script></body></html>"""

# tweet_ids = [1402002164042682371, 1401958982068101121, 1401864593186738180, 1401863159644893186, 1401620068899995650]
tweet_ids = [1403262786629685251]


# browser.get('file:///home/umut/IdeaProjects/screenshot/index.html')
def get_img(tweet_id):
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1024, 1024)
    browser.set_window_position(0, 0)
    browser.implicitly_wait(1)  # seconds
    try:
        browser.execute_script(
            """
            document.location='about:blank';
            document.open();
            document.write(arguments[0]);
            document.close();
            """,
            content.format(tweet_id)
        )

        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "twitter-widget-0")))
        browser.switch_to.frame(0)
        d = browser.find_element_by_xpath('/html')
        return d.screenshot_as_png
        # screenshot = d.screenshot('{}.png'.format(tweet_id))
    except Exception as exp:
        print(tweet_id)
        print(exp)
    finally:
        browser.quit()
        pass


@app.route('/twishot')
def twishot():
    try:
        """Return a friendly HTTP greeting."""
        return send_file(io.BytesIO(get_img(request.args.get('tweet_id'))), mimetype='image/png')
    except Exception as ex:
        return str(ex)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]

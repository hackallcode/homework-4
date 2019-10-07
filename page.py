from selenium.common import exceptions as Ex
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class AuthPage:
    BASE_URL = 'https://e.mail.ru/login'

    def __init__(self, driver):
        self.driver = driver
        self.driver.get(self.BASE_URL)

    def quit(self):
        self.driver.quit()

    def wait(self, wait_until=None, timeout=5):
        return WebDriverWait(self.driver, timeout).until(wait_until)

    def switch_to_login_iframe(self):
        frame = self.driver.find_element_by_css_selector('#auth-form iframe')
        self.driver.switch_to.frame(frame)

    def enter_email(self, text):
        elem = self.driver.find_element_by_css_selector('input[name=Login]')
        elem.send_keys(text)

    def clear_email(self):
        elem = self.driver.find_element_by_css_selector('input[name=Login]')
        elem.clear()

    def enter_password(self, text):
        elem = self.wait_password_field()
        elem.send_keys(text)

    def submit(self):
        elem = self.driver.find_element_by_css_selector('button[type=submit]')
        elem.click()

    def click_remind_password(self):
        elem = self.driver.find_element_by_css_selector('a[data-test-id=remind]')
        url = elem.get_attribute('href')
        self.driver.get(url)

    def click_signup(self):
        elem = self.driver.find_element_by_css_selector('a[data-test-id="signup-link"]')
        url = elem.get_attribute('href')
        self.driver.get(url)

    def select_yandex_provider(self):
        elem = self.driver.find_element_by_css_selector('div[data-provider="yandex"]')
        elem.click()

    def select_google_provider(self):
        elem = self.driver.find_element_by_css_selector('div[data-provider="google"]')
        elem.click()

    def select_yahoo_provider(self):
        elem = self.driver.find_element_by_css_selector('div[data-provider="yahoo"]')
        elem.click()

    def select_other_provider(self):
        elem = self.driver.find_element_by_css_selector('div[data-provider="other"]')
        elem.click()

    def get_domain_list(self):
        try:
            return self.wait(EC.presence_of_element_located((By.CSS_SELECTOR, '.domain-select')))
        except Ex.TimeoutException:
            return None

    def get_domain(self):
        elem = self.driver.find_element_by_css_selector('span[data-test-id="domain-select-value"]')
        return elem.text

    def wait_password_field(self):
        return self.wait(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name=Password]')))

    def wait_redirect(self, url=None):
        if url is None:
            self.wait(EC.url_changes(self.driver.current_url))
        else:
            self.wait(EC.url_matches(url))

    def get_email_error(self):
        try:
            error_selector = 'div[data-test-id="error-footer-text"] > small'
            elem = self.wait(EC.presence_of_element_located((By.CSS_SELECTOR, error_selector)))
            return elem.text
        except Ex.TimeoutException:
            return ""

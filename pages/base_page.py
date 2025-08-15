import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    @allure.step('Поиск элемента по локатору: {locator}')
    def find(self, locator):
        return self.driver.find_element(*locator)

    @allure.step('Скролл до элемента')
    def scroll_to_element(self, locator):
        element = self.find(locator)
        self.driver.execute_script('arguments[0].scrollIntoView();', element)

    @allure.step('Подождать прогрузки элемента')
    def wait_visibility_of_element(self, locator):
        self._close_cookie_banner_if_present()
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step('Кликнуть на элемент')
    def click_on_element(self, locator):
        try:
            self.find(locator).click()
        except ElementClickInterceptedException:
            self._close_cookie_banner_if_present()
            self.find(locator).click()

    @allure.step('Ввести значение в поле ввода')
    def send_keys_to_field(self, locator, keys):
        self.find(locator).clear()
        self.find(locator).send_keys(keys)

    @allure.step('Получить текст на элементе')
    def get_text_on_element(self, locator):
        return self.find(locator).text

    @allure.step('Перейти на другую вкладку')
    def switch_to_next_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step('Проверить отображение элемента')
    def check_displaying_of_element(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        return element.is_displayed()

    @allure.step('Проверить текущий URL')
    def get_current_url(self):
        return self.driver.current_url

    def _close_cookie_banner_if_present(self):
        try:
            banner = self.driver.find_element(By.CLASS_NAME, "App_CookieConsent__1yUIN")
            close_button = banner.find_element(By.TAG_NAME, "button")
            close_button.click()
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "App_CookieConsent__1yUIN")))
        except:
            pass

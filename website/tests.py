from django.test import TestCase
from django.core import mail
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class EmailTest(TestCase):
    def test_send_email(self):
        # user = CustomUser.objects.filter(email="admin@admin.com").first()
        # Send message.
        mail.send_mail(
            'Test', 'Here is the message.',
            'a.ledain@ncpi.fr', ['a.ledain@ncpi.fr'],
            fail_silently=False,
        )

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)


class GoogleTestCase(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(r"C:/dev/atscash/selenium_drivers/chromedriver.exe")
        self.vars = {}
        self.addCleanup(self.driver.quit)

    def testPageTitle(self):
        self.driver.get("https://ncpi-test-site.fr/")
        self.driver.set_window_size(1936, 1056)
        self.driver.find_element(By.CSS_SELECTOR, ".my-1:nth-child(1) .pt-8:nth-child(3) .text-center").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".my-1:nth-child(1) .pt-8:nth-child(3) .text-center")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, ".h-6").click()
        self.driver.find_element(By.CSS_SELECTOR, ".my-1:nth-child(2) .pt-8:nth-child(3) .text-center").click()
        self.driver.find_element(By.CSS_SELECTOR, ".h-6").click()
        self.driver.find_element(By.CSS_SELECTOR, ".my-1:nth-child(3) .pt-8:nth-child(3) .text-center").click()
        self.driver.find_element(By.CSS_SELECTOR, ".h-6").click()
        self.driver.find_element(By.NAME, "q").click()
        self.driver.find_element(By.NAME, "q").send_keys("table")
        self.driver.find_element(By.CSS_SELECTOR, ".w-auto > .material-icons").click()
        self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(1) > .flex > .flex input").send_keys("9")
        self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(1) > .flex > .flex input").click()
        self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(1) > .flex .material-icons").click()
        self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(2) > .flex > .flex input").send_keys("1")
        self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(2) > .flex > .flex input").click()
        self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(2) > .flex > .flex input").send_keys("2")
        self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(2) > .flex > .flex input").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(2) > .flex > .flex input")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(2) .form-control").click()
        self.driver.find_element(By.CSS_SELECTOR, "#cartIcon > .hover\\3Atext-blue-500").click()
        self.driver.find_element(By.CSS_SELECTOR, ".relative > .hover\\3Atext-blue-500 > p").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".relative > .hover\\3Atext-blue-500 > p")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.ID, "email").send_keys("testUser")
        self.driver.find_element(By.ID, "password").send_keys("Daily365")
        self.driver.find_element(By.CSS_SELECTOR, ".inline-flex").click()
        self.driver.find_element(By.CSS_SELECTOR,
                                 ".hoverable:nth-child(1) .px-4:nth-child(1) > .flex:nth-child(3) .text-black").click()
        self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(1) > .flex > .flex input").send_keys("0")
        self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(1) > .flex > .flex input").click()
        self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(1) > .flex > .flex input").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(1) > .flex > .flex input")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(1) > .flex .material-icons").click()
        self.driver.find_element(By.CSS_SELECTOR, ".shadow:nth-child(1) > .px-6").click()
        self.driver.find_element(By.CSS_SELECTOR, ".items-center:nth-child(1) .object-scale-down").click()
        self.driver.find_element(By.CSS_SELECTOR, ".text-center > p:nth-child(2)").click()
        self.driver.find_element(By.CSS_SELECTOR, ".my-1:nth-child(1) .block").click()
        self.driver.find_element(By.LINK_TEXT, "27 mai 2021 10:20").click()
        self.driver.find_element(By.CSS_SELECTOR, ".bg-green-300 > .material-icons").click()
        self.driver.find_element(By.CSS_SELECTOR, ".text-center > p:nth-child(2)").click()
        self.driver.find_element(By.CSS_SELECTOR, "#modal_update_user > .block").click()
        self.driver.find_element(By.ID, "first_name_update").send_keys("aaaaatyyuy")
        self.driver.find_element(By.ID, "last_name_update").click()
        self.driver.find_element(By.ID, "last_name_update").send_keys("leeej")
        self.driver.find_element(By.CSS_SELECTOR, ".inline-flex").click()
        self.driver.find_element(By.CSS_SELECTOR, "#modal_update_user > .block").click()
        self.driver.find_element(By.ID, "phone_update").click()
        self.driver.find_element(By.ID, "phone_update").send_keys("062451236988")
        self.driver.find_element(By.CSS_SELECTOR, ".inline-flex").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".inline-flex")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.ID, "phone_update").click()
        self.driver.find_element(By.ID, "phone_update").send_keys("0624512369")
        self.driver.find_element(By.CSS_SELECTOR, ".inline-flex").click()
        self.driver.find_element(By.CSS_SELECTOR, ".my-1:nth-child(2) .block").click()
        self.driver.find_element(By.CSS_SELECTOR,
                                 ".flex:nth-child(3) > .items-center:nth-child(1) > .flex > .material-icons").click()
        self.driver.find_element(By.ID, "deleteBtn").click()
        self.driver.find_element(By.CSS_SELECTOR,
                                 ".flex:nth-child(3) > .items-center:nth-child(1) .flex > .flex > input").click()
        self.driver.find_element(By.CSS_SELECTOR,
                                 ".flex:nth-child(3) > .items-center:nth-child(1) .flex > .flex > input").send_keys("6")
        self.driver.find_element(By.CSS_SELECTOR,
                                 ".flex:nth-child(3) > .items-center:nth-child(1) > .px-6 .material-icons").click()
        self.driver.find_element(By.CSS_SELECTOR, ".hover\\3Atext-blue-500 > .block").click()
        self.driver.find_element(By.CSS_SELECTOR, ".p-2").click()
        dropdown = self.driver.find_element(By.CSS_SELECTOR, ".p-2")
        dropdown.find_element(By.XPATH, "//option[. = 'Drive']").click()
        self.driver.find_element(By.CSS_SELECTOR, ".p-2").click()
        self.driver.find_element(By.CSS_SELECTOR, ".hover\\3A bg-blue-500").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".hover\\3A bg-blue-500")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, ".h-6").click()
        self.driver.find_element(By.CSS_SELECTOR, ".mt-5").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".mt-5")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.ID, "msg").click()
        self.driver.find_element(By.ID, "msg").send_keys("attention")
        self.driver.find_element(By.CSS_SELECTOR, ".inline-flex").click()
        self.driver.find_element(By.CSS_SELECTOR, ".hover\\3A bg-green-400:nth-child(2)").click()
        self.driver.find_element(By.CSS_SELECTOR, ".ml-2").click()
        self.driver.find_element(By.CSS_SELECTOR, ".border-transparent").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".border-transparent")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.NAME, "VISA").click()
        self.driver.find_element(By.CSS_SELECTOR, ".sips_customer_return_button").click()



import unittest
import bell

from base_case import on_platforms
from base_case import browsers
from base_case import BaseCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

@on_platforms(browsers)
class LoginTest(BaseCase):

    def test_login(self):
        """ NoneType -> NoneType
        
        Test login, logout, and configuration.
        Login, find the landing page and, if needed, fill out 
        the configuration, ensuring it is correctly accepted.
        Then, ensure correct log out.
        """
        driver = self.driver
        
        # login
        bell.login_test(self.driver, "admin", "password")
        
        # wait for the next page, and fill the configuration only if needed
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard")))
            #self.logout_test()
            self.click_manager_test()
            self.click_publications_test()
            self.click_and_add_issue()
            self.click_manager_test()
            self.click_publications_test()
            self.click_and_add_issue()
            self.click_manager_test()
            self.click_publications_test()
            self.delete_test()
            self.delete_test()
            
        except:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'code')]")))
            self.configuration_test()
            self.logout_test()
                        

        
   
        
    def logout_test(self):
        """ NoneType -> NoneType
        
        Helper function testing a correct logout operation.
        """
        driver = self.driver
        # test logout
        bell.logout(driver)
        # ensure logout was successful
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login")))
        actual = driver.current_url
        expected = bell.get_url() + "#login"
        self.assertEqual(actual, expected)

    def click_manager_test(self):
        sleep(5)
        driver = self.driver
        inputElement = driver.find_element_by_id('NationManagerLink')
        inputElement.click()
        sleep(2)
        expected = 'http://127.0.0.1:5981/apps/_design/bell/nation/index.html#dashboard'
        actual = driver.current_url
        self.assertEqual(actual, expected)
        
    def click_publications_test(self):
        sleep(5)
        driver = self.driver
        inputElement = driver.find_element_by_partial_link_text('Publications')
        inputElement.click()
        sleep(2)
        expected = 'http://127.0.0.1:5981/apps/_design/bell/nation/index.html#publication'
        actual = driver.current_url
        self.assertEqual(actual, expected)
        
    def click_and_add_issue(self):
        sleep(5)
        driver = self.driver
        inputElement = driver.find_element_by_partial_link_text('Add Issue')
        inputElement.click()
        sleep(2)
        expected = 'http://127.0.0.1:5981/apps/_design/bell/nation/index.html#publication/add'
        actual = driver.current_url
        self.assertEqual(actual, expected)
        inputElement = driver.find_element_by_name('editorName')
        inputElement.send_keys('Test Name')
        inputElement = driver.find_element_by_name('editorEmail')
        inputElement.send_keys('Test@email.com')
        inputElement = driver.find_element_by_name('editorPhone')
        inputElement.send_keys('1111111')
        inputElement = driver.find_element_by_name('save')
        inputElement.click()
        sleep(3)
        alert = driver.switch_to_alert()
        alert.accept()
        sleep(3)
        inputElement = driver.find_element_by_partial_link_text('My Home')
        inputElement.click()
        sleep(3)    

    def delete_test(self):
        sleep(5)
        driver = self.driver
        inputElement = driver.find_element_by_xpath(".//*[contains(text(), 'Delete')]")
        inputElement.click()
        alert = driver.switch_to_alert()
        alert.accept()
        sleep(1)
        alert = driver.switch_to_alert()
        alert.accept()

    
        
    def configuration_test(self):
        """ NoneType -> NoneType
        
        Helper function filling out the configuration form and ensuring it
        is successfully added to a new nation.
        
        TODO: Check configuration values in CouchDB         
        """
        driver = self.driver
        
        fields = ["name", "code", "region", "nationName", "nationUrl", "notes"]
        # fill out all fields
        for field in fields:
            elem = driver.find_element_by_name(field)
            elem.send_keys("ole")

        # uncomment to test languages other than English
        # dropdown = Select(driver.find_element_by_name("selectLanguage"))
        # dropdown.select_by_value("Spanish")
        
        # submit the form
        submit = driver.find_element_by_id("formButton")
        submit.click()
        sleep(5)
        
        # if configuration was successful, accept confirmation alert
        actual = Alert(driver).text
        expected = "Configurations are successfully added."
        self.assertEqual(actual, expected)
        Alert(driver).accept()
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard")))
        
        # ensure configuration was submitted (TODO: check against CouchDB)
        actual = driver.current_url
        expected = bell.get_url() + "#dashboard"
        self.assertEqual(actual, expected)
         

if __name__ == "__main__":
    unittest.main()

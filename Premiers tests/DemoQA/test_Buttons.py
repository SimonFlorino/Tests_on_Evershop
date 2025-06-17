import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from Helper_test import Helper_test

class TestButtons():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_Buttons(self):

    self.driver.get("https://demoqa.com/buttons")
    self.driver.set_window_size(1460, 1040)

    # Fermeture des popups de pub
    ads = Helper_test.wait_for_ads_to_load(self , timeout=10)
    for ad in ads:
      self.driver.execute_script("arguments[0].remove();", ad)

    #double click
    element = self.driver.find_element(By.ID, "doubleClickBtn")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.ID, "doubleClickMessage")))
    assert "You have done a double click" == self.driver.find_element(By.ID, "doubleClickMessage").text 

    #click droit
    element = self.driver.find_element(By.ID, "rightClickBtn")
    actions = ActionChains(self.driver)
    actions.context_click(element).perform()
    WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.ID, "rightClickMessage")))
    assert "You have done a right click" == self.driver.find_element(By.ID, "rightClickMessage").text 

    #simple click
    # vu que l'ID est dynamique, je vais chercher un bouton parmis tous les boutons qui existent et qui possède le text "Click Me"
    buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button.btn.btn-primary')
    for b in buttons:
      if b.text == "Click Me":
        b.click()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.ID, "dynamicClickMessage")))
        assert "You have done a dynamic click" == self.driver.find_element(By.ID, "dynamicClickMessage").text 
        break

# if __name__ == "__main__":
#   test = TestButtons()
#   test.setup_method(None)
#   try:
#       test.test_Buttons()
#   finally:
#       test.teardown_method(None)
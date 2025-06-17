import time
from selenium.webdriver.common.by import By

class Helper_test():

    def wait_for_ads_to_load(self, timeout=10):
        end_time = time.time() + timeout
        previous_count = -1

        while time.time() < end_time:
            ads = self.driver.find_elements(By.CSS_SELECTOR, "iframe[id^='google_ads_iframe']")
            current_count = len(ads)
            if current_count == previous_count and current_count > 0:
                return ads
            previous_count = current_count
            time.sleep(0.5)
        return self.driver.find_elements(By.CSS_SELECTOR, "iframe[id^='google_ads_iframe']")
    
    def remove_all_google_ads(self):
        # Script JS pour cacher toutes les div avec un attribut contenant "google"
        js_code = """
        document.querySelectorAll('div').forEach(function(div) {
        for (var i = 0; i < div.attributes.length; i++) {
        if (div.attributes[i].value && div.attributes[i].value.toLowerCase().includes('google')) {
          div.style.display = 'none';
          break;
        }
        }
        });
        """
        # Exécute le script dans la page
        self.driver.execute_script(js_code)
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time

class SeleniumConfig:
    """Classe de configuration pour les tests Selenium"""

    # ===========================
    # 1. Initialisation et setup navigateur
    # ===========================
    def __init__(self, base_url, wait_timeout=10, disable_popups=False):
        """
        Initialise la configuration Selenium
        
        Args:
            base_url (str): URL de base pour les tests
            wait_timeout (int): Délai d'attente maximum en secondes
            disable_popups (bool): Désactive les popups du navigateur si True
        """
        self.base_url = base_url
        self.wait_timeout = wait_timeout
        self.driver = None
        self.disable_popups = disable_popups

    def setup_driver(self):
        """Configure et retourne une instance du driver Chrome"""
        options = webdriver.ChromeOptions()
        if self.disable_popups:
            # Désactive les popups, notifications, géolocalisation, etc.
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_setting_values.geolocation": 2,
                "profile.default_content_setting_values.popups": 2
            }
            options.add_argument("--incognito")
            options.add_experimental_option("prefs", prefs)
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        return self.driver

    def teardown_driver(self):
        """Ferme le driver Chrome"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    # ===========================
    # 2. Navigation et utilitaires généraux
    # ===========================
    def navigate_to(self, path=""):
        """
        Navigue vers une URL spécifique
        
        Args:
            path (str): Chemin à ajouter à l'URL de base
        """
        url = f"{self.base_url}{path}"
        self.driver.get(url)

    def get_current_url(self):
        """Retourne l'URL actuelle"""
        return self.driver.current_url

    def get_page_title(self):
        """Retourne le titre de la page"""
        return self.driver.title

    # ===========================
    # 3. Attente d’éléments dans le DOM
    # ===========================
    def wait_for_element(self, selector, timeout=None):
        """
        Attend qu'un élément soit présent dans la page
        
        Args:
            selector (tuple): Sélecteur de l'élément (By, value)
            timeout (int): Délai d'attente en secondes (utilise wait_timeout par défaut)
        
        Returns:
            WebElement: L'élément trouvé
        """
        timeout = timeout or self.wait_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(selector)
        )

    def wait_for_element_visible(self, selector, timeout=None):
        """
        Attend qu'un élément soit visible à l'écran
        
        Args:
            selector (tuple): Sélecteur de l'élément (By, value)
            timeout (int): Délai d'attente en secondes (utilise wait_timeout par défaut)
        
        Returns:
            WebElement: L'élément trouvé et visible
        
        Raises:
            TimeoutException: Si l'élément n'est pas visible dans le délai imparti
        """
        timeout = timeout or self.wait_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(selector)
        )

    def wait_for_element_presence(self, selector, timeout=None):
        """
        Attend qu'un élément soit présent dans la page
        
        Args:
            selector (tuple): Sélecteur de l'élément (By, value)
            timeout (int): Délai d'attente en secondes (utilise wait_timeout par défaut)
        
        Returns:
            WebElement: L'élément trouvé
        
        Raises:
            TimeoutException: Si l'élément n'est pas trouvé dans le délai imparti
        """
        timeout = timeout or self.wait_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(selector)
        )
    def wait_until(self, condition, timeout=10):
        """
        Attend qu'une condition soit vraie, sinon lève TimeoutException après le timeout
        """
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if condition():
                    return True
            except Exception:
                pass
            time.sleep(0.2)
        raise TimeoutException("La condition n'a pas été remplie dans le délai imparti.")

    # ===========================
    # 4. Actions sur les éléments du DOM
    # ===========================
    def find_element(self, selector):
        """
        Trouve un élément dans la page
        
        Args:
            selector (tuple): Sélecteur de l'élément (By, value)
        
        Returns:
            WebElement: L'élément trouvé
        """
        return self.driver.find_element(*selector)

    def find_elements(self, selector):
        """
        Trouve tous les éléments correspondant au sélecteur
        
        Args:
            selector (tuple): Sélecteur des éléments (By, value)
        
        Returns:
            list: Liste des éléments trouvés
        """
        return self.driver.find_elements(*selector)

    def wait_and_click(self, selector, timeout=None):
        """
        Attend qu'un élément soit cliquable et clique dessus
        
        Args:
            selector (tuple): Sélecteur de l'élément (By, value)
            timeout (int): Délai d'attente en secondes
        """
        timeout = timeout or self.wait_timeout
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(selector)
        )
        element.click()

    def wait_and_send_keys(self, selector, keys, timeout=None):
        """
        Attend qu'un élément soit présent et envoie des touches
        
        Args:
            selector (tuple): Sélecteur de l'élément (By, value)
            keys (str): Texte à envoyer
            timeout (int): Délai d'attente en secondes
        """
        element = self.wait_for_element(selector, timeout)
        element.send_keys(keys)

    def wait_and_clear_and_send_keys(self, locator, text, timeout=10):
        """Attend qu'un élément soit présent, le vide et envoie du texte"""
        element = self.wait_for_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    # ===========================
    # 5. Utilitaires avancés pour les tests
    # ===========================
    def scroll_down(self):
        self.driver.execute_script("window.scrollBy(0, 100);")


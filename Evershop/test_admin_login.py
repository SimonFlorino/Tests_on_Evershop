# test_admin_login.py
import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from base_login_test import BaseLoginTest

class TestLogin(BaseLoginTest):
    BASE_URL = "http://localhost:3000/admin/login"
    RUN_LOGIN_TESTS = False

    SELECTORS = {
        'email_input': (By.NAME, "email"),
        'password_input': (By.NAME, "password"),
        'submit_button': (By.CSS_SELECTOR, "button[type='submit']"),
        'error_message': (By.CSS_SELECTOR, "div.field-error span.text-critical"),
        'dashboard_title': (By.CSS_SELECTOR, "h1.page-heading-title")
    }

    VALID_CREDENTIALS = {
        'email': "admin@mail.com",
        'password': "admin123"
    }

    ERROR_MESSAGES = {
        'invalid_email': "Invalid email",
        'empty_password': "This field can not be empty"
    }

    def is_admin_dashboard(self, driver):
        current_url = driver.current_url
        return current_url.startswith("http://localhost:3000/admin") and "/login" not in current_url

    @pytest.mark.skipif(not RUN_LOGIN_TESTS, reason="Set RUN_LOGIN_TESTS=True to run login tests")
    def test_successful_login(self, selenium):
        selenium.driver.get(self.BASE_URL)
        self.fill_login_form(selenium, self.VALID_CREDENTIALS['email'], self.VALID_CREDENTIALS['password'])
        try:
            WebDriverWait(selenium.driver, 10).until(self.is_admin_dashboard)
            dashboard_title = selenium.wait_for_element(self.SELECTORS['dashboard_title'])
            assert dashboard_title.text == "Dashboard"
        except TimeoutException:
            pytest.fail("Failed to redirect to dashboard after login")

    @pytest.mark.skipif(not RUN_LOGIN_TESTS, reason="Set RUN_LOGIN_TESTS=True to run login tests")
    def test_invalid_email(self, selenium):
        selenium.navigate_to()
        self.fill_login_form(selenium, "invalid-email", "password123")
        try:
            error_message = selenium.wait_for_element(self.SELECTORS['error_message'])
            assert error_message.text == self.ERROR_MESSAGES['invalid_email']
        except TimeoutException:
            pytest.fail("Error message not found for invalid email")

    @pytest.mark.skipif(not RUN_LOGIN_TESTS, reason="Set RUN_LOGIN_TESTS=True to run login tests")
    def test_empty_password(self, selenium):
        selenium.navigate_to()
        self.fill_login_form(selenium, "test@email.com")
        try:
            error_message = selenium.wait_for_element(self.SELECTORS['error_message'])
            assert error_message.text == self.ERROR_MESSAGES['empty_password']
        except TimeoutException:
            pytest.fail("Error message not found for empty password")


# # Import des bibliothèques nécessaires pour les tests
# import pytest  # Framework de test Python
# from selenium.webdriver.common.by import By  # Pour localiser les éléments
# from selenium.common.exceptions import TimeoutException  # Pour gérer les erreurs de timeout
# from config import SeleniumConfig  # Import de notre classe de configuration
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class TestLogin:
#     # Constantes utilisées dans les tests
#     BASE_URL = "http://localhost:3000/admin/login"  # URL de la page de connexion
#     RUN_LOGIN_TESTS = False  # Variable pour contrôler l'exécution des tests
    
#     # Dictionnaire des sélecteurs pour localiser les éléments dans la page
#     SELECTORS = {
#         'email_input': (By.NAME, "email"),  # Champ de saisie email
#         'password_input': (By.NAME, "password"),  # Champ de saisie mot de passe
#         'submit_button': (By.CSS_SELECTOR, "button[type='submit']"),  # Bouton de soumission
#         'error_message': (By.CSS_SELECTOR, "div.field-error span.text-critical"),  # Message d'erreur
#         'dashboard_title': (By.CSS_SELECTOR, "h1.page-heading-title")  # Titre du tableau de bord
#     }
    
#     # Identifiants valides pour les tests de connexion réussie
#     VALID_CREDENTIALS = {
#         'email': "admin@mail.com",  # Email valide
#         'password': "admin123"  # Mot de passe valide
#     }
    
#     # Messages d'erreur attendus pour les différents cas de test
#     ERROR_MESSAGES = {
#         'invalid_email': "Invalid email",  # Message pour email invalide
#         'empty_password': "This field can not be empty"  # Message pour mot de passe vide
#     }

#     @pytest.fixture
#     def selenium(self):
#         """Initialise et configure Selenium pour les tests"""
#         config = SeleniumConfig(self.BASE_URL)  # Crée une instance de configuration
#         config.setup_driver()  # Configure le driver
#         yield config  # Fournit la configuration aux tests
#         config.teardown_driver()  # Nettoie après les tests

#     def fill_login_form(self, selenium, email, password=None):
#         """Remplit le formulaire de connexion avec les identifiants fournis"""
#         # S'assurer qu'on est sur la bonne page
#         if not selenium.driver.current_url.startswith(self.BASE_URL):
#             selenium.driver.get(self.BASE_URL)
            
#         selenium.wait_and_send_keys(self.SELECTORS['email_input'], email)  # Saisit l'email
        
#         if password:  # Si un mot de passe est fourni
#             selenium.wait_and_send_keys(self.SELECTORS['password_input'], password)  # Saisit le mot de passe
        
#         selenium.wait_and_click(self.SELECTORS['submit_button'])  # Clique sur le bouton

#     def is_admin_dashboard(self, driver):
#         """Vérifie si on est sur le dashboard admin"""
#         current_url = driver.current_url
#         return current_url.startswith("http://localhost:3000/admin") and "/login" not in current_url
    
#     @pytest.mark.skipif(
#         not RUN_LOGIN_TESTS,
#         reason="Set RUN_LOGIN_TESTS=True to run login tests"
#     )
#     def test_successful_login(self, selenium):
#         """Test de connexion réussie avec des identifiants valides"""
#         # S'assurer qu'on est sur la page de login
#         selenium.driver.get(self.BASE_URL)
        
#         # Remplit et soumet le formulaire avec les identifiants valides
#         self.fill_login_form(
#             selenium,
#             self.VALID_CREDENTIALS['email'],
#             self.VALID_CREDENTIALS['password']
#         )

#         # Vérifie d'abord la redirection
#         try:
#             WebDriverWait(selenium.driver, 10).until(self.is_admin_dashboard)
#             # Ensuite vérifie le titre du dashboard
#             dashboard_title = selenium.wait_for_element(self.SELECTORS['dashboard_title'])
#             assert dashboard_title.text == "Dashboard"
#         except TimeoutException:
#             pytest.fail("Failed to redirect to dashboard after login")

#     @pytest.mark.skipif(
#         not RUN_LOGIN_TESTS,
#         reason="Set RUN_LOGIN_TESTS=True to run login tests"
#     )
#     def test_invalid_email(self, selenium):
#         """Test de connexion avec un format d'email invalide"""
#         selenium.navigate_to()  # Accède à la page de connexion
        
#         # Remplit et soumet le formulaire avec un email invalide
#         self.fill_login_form(selenium, "invalid-email", "password123")

#         # Vérifie le message d'erreur
#         try:
#             error_message = selenium.wait_for_element(self.SELECTORS['error_message'])  # Attend le message d'erreur
#             assert error_message.text == self.ERROR_MESSAGES['invalid_email']  # Vérifie le texte du message
#         except TimeoutException:
#             pytest.fail("Error message not found for invalid email")  # Échoue si le message n'est pas trouvé

#     @pytest.mark.skipif(
#         not RUN_LOGIN_TESTS,
#         reason="Set RUN_LOGIN_TESTS=True to run login tests"
#     )
#     def test_empty_password(self, selenium):
#         """Test de connexion avec un mot de passe vide"""
#         selenium.navigate_to()  # Accède à la page de connexion
        
#         # Remplit et soumet le formulaire sans mot de passe
#         self.fill_login_form(selenium, "test@email.com")

#         # Vérifie le message d'erreur
#         try:
#             error_message = selenium.wait_for_element(self.SELECTORS['error_message'])  # Attend le message d'erreur
#             assert error_message.text == self.ERROR_MESSAGES['empty_password']  # Vérifie le texte du message
#         except TimeoutException:
#             pytest.fail("Error message not found for empty password")  # Échoue si le message n'est pas trouvé 
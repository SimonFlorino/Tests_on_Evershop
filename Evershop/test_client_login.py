# test_client_login.py
import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from base_login_test import BaseLoginTest
from selenium.webdriver.common.action_chains import ActionChains

class TestClientLogin(BaseLoginTest):
    BASE_URL = "http://localhost:3000/account/login"
    ACCOUNT_URL = "http://localhost:3000/account"

    SELECTORS = {
        'email_input': (By.NAME, "email"),
        'password_input': (By.NAME, "password"),
        'submit_button': (By.CSS_SELECTOR, "button[type='submit']"),
        'error_message': (By.CSS_SELECTOR, "div.field-error span.text-critical"),
        'account_title': (By.CSS_SELECTOR, "h1.page-heading-title"),
        'user_name': (By.CSS_SELECTOR, "div.account-details-name div:nth-child(2)")
    }

    VALID_CREDENTIALS = {
        'email': "simon@simon.com",
        'password': "simon123",
        'name': "Simon"
    }

    ERROR_MESSAGES = {
        'empty_field': "This field can not be empty",
        'invalid_email': "Invalid email"
    }

    def test_successful_login(self, selenium):
        selenium.navigate_to()
        self.fill_login_form(selenium, self.VALID_CREDENTIALS['email'], self.VALID_CREDENTIALS['password'])
        try:
            
            selenium.wait_for_element_visible((By.CSS_SELECTOR, "a[href*='/account']"))
            element = selenium.wait_for_element_visible((By.CSS_SELECTOR, "a[href*='/account']"))
            actions = ActionChains(selenium.driver)
            actions.move_to_element(element).click().perform()

            h1 = selenium.wait_for_element_visible((By.CSS_SELECTOR, "h1.text-center"))
            assert h1.text == "My Account", f"Texte inattendu : {h1.text}"

        except TimeoutException as e:
            pytest.fail(f"Timeout waiting for elements: {str(e)}")
        except AssertionError as e:
            pytest.fail(f"Assertion failed: {str(e)}")
        except Exception as e:
            pytest.fail(f"Unexpected error: {str(e)}")

    # def test_invalid_email(self, selenium):
    #     selenium.navigate_to()
    #     self.fill_login_form(selenium, "invalid-email", "test123")
    #     try:
    #         error_message = selenium.wait_for_element(self.SELECTORS['error_message'])
    #         assert error_message.text == self.ERROR_MESSAGES['invalid_email']
    #     except TimeoutException:
    #         pytest.fail("Error message not found for invalid email")

    # def test_empty_email(self, selenium):
    #     selenium.navigate_to()
    #     self.fill_login_form(selenium, password="test123")
    #     try:
    #         error_message = selenium.wait_for_element(self.SELECTORS['error_message'])
    #         assert error_message.text == self.ERROR_MESSAGES['empty_field']
    #     except TimeoutException:
    #         pytest.fail("Error message not found for empty email")

    # def test_empty_password(self, selenium):
    #     selenium.navigate_to()
    #     self.fill_login_form(selenium, email="test@email.com")
    #     try:
    #         error_message = selenium.wait_for_element(self.SELECTORS['error_message'])
    #         assert error_message.text == self.ERROR_MESSAGES['empty_field']
    #     except TimeoutException:
    #         pytest.fail("Error message not found for empty password")

    # def test_empty_fields(self, selenium):
    #     selenium.navigate_to()
    #     self.fill_login_form(selenium)
    #     try:
    #         error_message = selenium.wait_for_element(self.SELECTORS['error_message'])
    #         assert error_message.text == self.ERROR_MESSAGES['empty_field']
    #     except TimeoutException:
    #         pytest.fail("Error message not found for empty fields")






# from base_login_test import BaseLoginTest
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# import pytest

# class TestLogin(BaseLoginTest):
#     BASE_URL = "http://localhost:3000/admin/login"
#     RUN_LOGIN_TESTS = False

#     SELECTORS = {
#         'email_input': (By.NAME, "email"),
#         'password_input': (By.NAME, "password"),
#         'submit_button': (By.CSS_SELECTOR, "button[type='submit']"),
#         'error_message': (By.CSS_SELECTOR, "div.field-error span.text-critical"),
#         'dashboard_title': (By.CSS_SELECTOR, "h1.page-heading-title")
#     }

#     VALID_CREDENTIALS = {
#         'email': "admin@mail.com",
#         'password': "admin123"
#     }

#     ERROR_MESSAGES = {
#         'invalid_email': "Invalid email",
#         'empty_password': "This field can not be empty"
#     }

# # # Import des bibliothèques nécessaires pour les tests
# # import pytest  # Framework de test Python
# # from selenium.webdriver.common.by import By  # Pour localiser les éléments
# # from selenium.common.exceptions import TimeoutException  # Pour gérer les erreurs de timeout
# # from config import SeleniumConfig  # Import de notre classe de configuration

# # class TestClientLogin:
# #     # Constantes utilisées dans les tests
# #     BASE_URL = "http://localhost:3000/account/login"  # URL de la page de connexion client
# #     ACCOUNT_URL = "http://localhost:3000/account"  # URL de la page de profil
    
# #     # Dictionnaire des sélecteurs pour localiser les éléments dans la page
# #     SELECTORS = {
# #         'email_input': (By.NAME, "email"),  # Champ de saisie email
# #         'password_input': (By.NAME, "password"),  # Champ de saisie mot de passe
# #         'submit_button': (By.CSS_SELECTOR, "button[type='submit']"),  # Bouton de soumission
# #         'error_message': (By.CSS_SELECTOR, "div.field-error span.text-critical"),  # Message d'erreur
# #         'account_title': (By.CSS_SELECTOR, "h1.page-heading-title"),  # Titre de la page compte
# #         'user_name': (By.CSS_SELECTOR, "div.account-details-name div:nth-child(2)")  # Nom de l'utilisateur
# #     }
    
# #     # Messages d'erreur attendus pour les différents cas de test
# #     ERROR_MESSAGES = {
# #         'empty_field': "This field can not be empty",  # Message pour champ vide
# #         'invalid_email': "Invalid email"  # Message pour email invalide
# #     }

# #     # Identifiants valides pour les tests de connexion réussie
# #     VALID_CREDENTIALS = {
# #         'email': "simon@simon.com",  # Email valide
# #         'password': "simon123",  # Mot de passe valide
# #         'name': "Simon"  # Nom attendu dans le profil
# #     }

# #     @pytest.fixture
# #     def selenium(self):
# #         """Initialise et configure Selenium pour les tests"""
# #         config = SeleniumConfig(self.BASE_URL)  # Crée une instance de configuration
# #         config.setup_driver()  # Configure le driver
# #         yield config  # Fournit la configuration aux tests
# #         config.teardown_driver()  # Nettoie après les tests

# #     def fill_login_form(self, selenium, email=None, password=None):
# #         """Remplit le formulaire de connexion avec les identifiants fournis"""
# #         if email:
# #             selenium.wait_and_send_keys(self.SELECTORS['email_input'], email)  # Saisit l'email
        
# #         if password:
# #             selenium.wait_and_send_keys(self.SELECTORS['password_input'], password)  # Saisit le mot de passe
        
# #         selenium.wait_and_click(self.SELECTORS['submit_button'])  # Clique sur le bouton

# #     def test_successful_login(self, selenium):
# #         """Test de connexion réussie avec des identifiants valides"""
# #         selenium.navigate_to()  # Accède à la page de connexion
        
# #         # Remplit et soumet le formulaire avec les identifiants valides
# #         self.fill_login_form(
# #             selenium,
# #             self.VALID_CREDENTIALS['email'],
# #             self.VALID_CREDENTIALS['password']
# #         )

# #         # Vérifie que la connexion a réussi en cherchant le titre de la page compte
# #         try:
# #             # Vérifie d'abord que nous sommes sur la bonne URL
# #             current_url = selenium.get_current_url()
# #             assert self.ACCOUNT_URL in current_url, f"Expected URL {self.ACCOUNT_URL}, but got {current_url}"
            
# #             # Vérifie le titre de la page
# #             account_title = selenium.wait_for_element(self.SELECTORS['account_title'])  # Attend le titre
# #             assert "Account" in account_title.text, f"Expected 'Account' in title, but got '{account_title.text}'"
            
# #             # Vérifie que le nom de l'utilisateur est correct
# #             user_name = selenium.wait_for_element(self.SELECTORS['user_name'])  # Attend le nom d'utilisateur
# #             assert user_name.text == self.VALID_CREDENTIALS['name'], f"Expected name '{self.VALID_CREDENTIALS['name']}', but got '{user_name.text}'"
# #         except TimeoutException as e:
# #             pytest.fail(f"Timeout waiting for elements: {str(e)}")
# #         except AssertionError as e:
# #             pytest.fail(f"Assertion failed: {str(e)}")
# #         except Exception as e:
# #             pytest.fail(f"Unexpected error: {str(e)}")

# #     def test_invalid_email(self, selenium):
# #         """Test de connexion avec un email invalide"""
# #         selenium.navigate_to()  # Accède à la page de connexion
        
# #         # Remplit et soumet le formulaire avec un email invalide
# #         self.fill_login_form(selenium, "invalid-email", "test123")

# #         # Vérifie le message d'erreur
# #         try:
# #             error_message = selenium.wait_for_element(self.SELECTORS['error_message'])  # Attend le message d'erreur
# #             assert error_message.text == self.ERROR_MESSAGES['invalid_email']  # Vérifie le texte du message
# #         except TimeoutException:
# #             pytest.fail("Error message not found for invalid email")

# #     def test_empty_email(self, selenium):
# #         """Test de connexion avec un email vide"""
# #         selenium.navigate_to()  # Accède à la page de connexion
        
# #         # Soumet le formulaire sans email
# #         self.fill_login_form(selenium, password="test123")

# #         # Vérifie le message d'erreur
# #         try:
# #             error_message = selenium.wait_for_element(self.SELECTORS['error_message'])  # Attend le message d'erreur
# #             assert error_message.text == self.ERROR_MESSAGES['empty_field']  # Vérifie le texte du message
# #         except TimeoutException:
# #             pytest.fail("Error message not found for empty email")

# #     def test_empty_password(self, selenium):
# #         """Test de connexion avec un mot de passe vide"""
# #         selenium.navigate_to()  # Accède à la page de connexion
        
# #         # Soumet le formulaire sans mot de passe
# #         self.fill_login_form(selenium, email="test@email.com")

# #         # Vérifie le message d'erreur
# #         try:
# #             error_message = selenium.wait_for_element(self.SELECTORS['error_message'])  # Attend le message d'erreur
# #             assert error_message.text == self.ERROR_MESSAGES['empty_field']  # Vérifie le texte du message
# #         except TimeoutException:
# #             pytest.fail("Error message not found for empty password")

# #     def test_empty_fields(self, selenium):
# #         """Test de connexion avec tous les champs vides"""
# #         selenium.navigate_to()  # Accède à la page de connexion
        
# #         # Soumet le formulaire sans aucun champ rempli
# #         self.fill_login_form(selenium)

# #         # Vérifie le message d'erreur
# #         try:
# #             error_message = selenium.wait_for_element(self.SELECTORS['error_message'])  # Attend le message d'erreur
# #             assert error_message.text == self.ERROR_MESSAGES['empty_field']  # Vérifie le texte du message
# #         except TimeoutException:
# #             pytest.fail("Error message not found for empty fields") 
import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config import SeleniumConfig
from test_admin_login import TestLogin
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
    
class TestCategory:
    ADMIN_URL = "http://localhost:3000/admin/login"
    CATEGORIES_URL = "http://localhost:3000/admin/categories"
    NEW_CATEGORY_URL = "http://localhost:3000/admin/categories/new"
    
    # Sélecteurs
    NEW_CATEGORY_BUTTON = (By.CSS_SELECTOR, "a.button.primary")
    CATEGORY_NAME = (By.ID, "name")
    CATEGORY_URL_KEY = (By.ID, "urlKey")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button.button.primary")
    SUCCESS_TOAST = (By.CSS_SELECTOR, "div.Toastify__toast--success div[role='alert']")
    ERROR_TOAST = (By.CSS_SELECTOR, "div.Toastify__toast--error div[role='alert']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "span.text-critical")
    
    # Nouveaux sélecteurs
    CATEGORY_IMAGE_INPUT = (By.ID, "categoryImageUpload")
    META_TITLE = (By.ID, "metaTitle")
    META_KEYWORDS = (By.ID, "metakeywords")
    META_DESCRIPTION = (By.ID, "meta_description")
    UPLOADED_IMAGE = (By.CSS_SELECTOR, ".category-image img")  # <img> généré après upload
    EDIT_BUTTON = (By.CSS_SELECTOR, "a.button.secondary")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='name']")
    CATEGORY_LINK = (By.CSS_SELECTOR, "a.hover\\:underline.font-semibold")
    CATEGORY_CHECKBOX = (By.CSS_SELECTOR, "td input[type='checkbox']")
    ACTION_DELETE_BUTTON = (By.CSS_SELECTOR, "td[colspan] .inline-flex a:has(span:contains('Delete'))")
    MODAL_DELETE_BUTTON = (By.CSS_SELECTOR, ".modal .button.critical")
    TABLE_ROW = (By.CSS_SELECTOR, "table.listing tbody tr")
    ACTION_ROW = (By.CSS_SELECTOR, "table.listing thead tr")
    ACTION_DELETE_BUTTON_XPATH = (By.XPATH, ".//a[span[text()='Delete']]")
    MODAL_OVERLAY = (By.CSS_SELECTOR, ".modal-overlay")

    # Données de test pour la création
    CATEGORY_DATA = {
        'name': "Outfit",
        'url_key': "Outfit",
        'meta_title': "Tenue",
        'meta_keywords': "Outfit",
        'meta_description': "Outfit",
        'image_path': "images/outfit.png"
    }
    
    # Données de test pour la modification
    EDIT_CATEGORY_DATA = {
        'name': "Sportswear",
        'url_key': "sportswear",
        'meta_title': "Tenue de sport",
        'meta_keywords': "Sportswear",
        'meta_description': "Sportswear",
        'image_path': "images/outfit.png"  # Même image ou une nouvelle+
    }
    
    # Messages d'erreur attendus
    ERROR_MESSAGES = {
        'empty_field': "This field can not be empty",
        'duplicate_url_key': "duplicate key value"
    }

    @pytest.fixture
    def selenium(self):
        config = SeleniumConfig(self.ADMIN_URL)
        config.setup_driver()
        yield config
        config.teardown_driver()

    def login_admin(self, selenium):
        """Connexion en tant qu'admin"""
        login = TestLogin()
        selenium.driver.get(self.ADMIN_URL)
        login.fill_login_form(
            selenium,
            login.VALID_CREDENTIALS['email'],
            login.VALID_CREDENTIALS['password']
        )
        
        # Vérifier que la connexion a réussi
        try:
            selenium.wait_for_element_visible((By.CSS_SELECTOR, "h1.page-heading-title"))
        except TimeoutException:
            pytest.fail("Login failed - not redirected to dashboard")
    
    def test_create_category(self, selenium):
        # Se connecter en tant qu'admin
        self.login_admin(selenium)
        
        # Aller à la page des catégories
        selenium.driver.get(self.CATEGORIES_URL)
        
        # Cliquer sur le bouton New Category
        selenium.wait_and_click(self.NEW_CATEGORY_BUTTON)
        
        # Vérifier qu'on est sur la bonne page
        assert selenium.driver.current_url == self.NEW_CATEGORY_URL
        
        # Tester la validation du champ name
        selenium.wait_and_click(self.SAVE_BUTTON)
        error_message = selenium.wait_for_element_visible(self.ERROR_MESSAGE)
        assert error_message.text == self.ERROR_MESSAGES['empty_field']
        
        # Saisir le nom de la catégorie
        selenium.wait_and_send_keys(self.CATEGORY_NAME, self.CATEGORY_DATA['name'])
        
        # Tester la validation du champ url_key
        selenium.wait_and_click(self.SAVE_BUTTON)
        error_message = selenium.wait_for_element_visible(self.ERROR_MESSAGE)
        assert error_message.text == self.ERROR_MESSAGES['empty_field']
        
        # Saisir l'url key
        selenium.wait_and_send_keys(self.CATEGORY_URL_KEY, self.CATEGORY_DATA['url_key'])
        
        # Uploader l'image
        image_input = selenium.wait_for_element(self.CATEGORY_IMAGE_INPUT)
        image_path = os.path.abspath(self.CATEGORY_DATA['image_path'])
        image_input.send_keys(image_path)
        
        # Vérifier que l'image est bien visible
        try:
            uploaded_image = selenium.wait_for_element_visible(self.UPLOADED_IMAGE, timeout=10)
            assert uploaded_image.is_displayed(), "L'image uploadée n'est pas visible"
            image_name = os.path.basename(self.CATEGORY_DATA['image_path'])
            assert image_name in uploaded_image.get_attribute("src"), "L'image uploadée n'est pas la bonne"
        except TimeoutException:
            pytest.fail("L'image n'a pas été uploadée correctement")

        # Remplir les champs meta
        selenium.wait_and_send_keys(self.META_TITLE, self.CATEGORY_DATA['meta_title'])
        selenium.wait_and_send_keys(self.META_KEYWORDS, self.CATEGORY_DATA['meta_keywords'])
        selenium.wait_and_send_keys(self.META_DESCRIPTION, self.CATEGORY_DATA['meta_description'])
        
        # Sauvegarder la catégorie
        selenium.wait_and_click(self.SAVE_BUTTON)
        
        # Vérifier qu'une popup s'affiche (succès ou erreur)
        try:
            # Essayer d'abord de trouver un message de succès
            success_message = selenium.wait_for_element_visible(self.SUCCESS_TOAST, timeout=5)
            assert success_message.text in "Category saved successfully!"
        except TimeoutException:
            try:
                # Si pas de succès, vérifier s'il y a un message d'erreur
                error_message = selenium.wait_for_element_visible(self.ERROR_TOAST, timeout=5)
                assert error_message.text in self.ERROR_MESSAGES['duplicate_url_key']
            except TimeoutException:
                pytest.fail("Aucune popup (succès ou erreur) n'a été affichée")

    def test_edit_category(self, selenium):
        """Test la modification d'une catégorie existante"""
        # Se connecter en tant qu'admin
        self.login_admin(selenium)
        
        # Aller à la page des catégories
        selenium.driver.get(self.CATEGORIES_URL)
        
        # Rechercher la catégorie par son nom
        search_input = selenium.wait_for_element_visible(self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(self.CATEGORY_DATA['name'])
        search_input.send_keys(Keys.ENTER)
        
        # Attendre que les résultats soient filtrés et que le lien de la catégorie soit visible
        selenium.wait_for_element(self.CATEGORY_LINK)
        
        # Trouver et cliquer sur le lien de la catégorie
        category_link = selenium.wait_for_element_visible(self.CATEGORY_LINK)
        assert category_link.text in self.CATEGORY_DATA['name'], f"Catégorie {self.CATEGORY_DATA['name']} non trouvée"
        category_link.click()
        
        # Attendre que la page de modification soit chargée
        selenium.wait_until(lambda: "edit" in selenium.driver.current_url)
        
        # Attendre que les champs soient chargés
        selenium.wait_for_element(self.CATEGORY_NAME)
        
        # Modifier les champs
        selenium.wait_and_clear_and_send_keys(self.CATEGORY_NAME, self.EDIT_CATEGORY_DATA['name'])
        selenium.wait_and_clear_and_send_keys(self.CATEGORY_URL_KEY, self.EDIT_CATEGORY_DATA['url_key'])
        
        # Uploader la nouvelle image si nécessaire
        image_input = selenium.wait_for_element(self.CATEGORY_IMAGE_INPUT)
        image_path = os.path.abspath(self.EDIT_CATEGORY_DATA['image_path'])
        image_input.send_keys(image_path)
        
        # Modifier les champs meta
        selenium.wait_and_clear_and_send_keys(self.META_TITLE, self.EDIT_CATEGORY_DATA['meta_title'])
        selenium.wait_and_clear_and_send_keys(self.META_KEYWORDS, self.EDIT_CATEGORY_DATA['meta_keywords'])
        selenium.wait_and_clear_and_send_keys(self.META_DESCRIPTION, self.EDIT_CATEGORY_DATA['meta_description'])
        
        # Sauvegarder les modifications
        selenium.wait_and_click(self.SAVE_BUTTON)
        
        # Vérifier le message de succès
        try:
            success_message = selenium.wait_for_element_visible(self.SUCCESS_TOAST, timeout=5)
            assert success_message.text in "Category saved successfully!"
        except TimeoutException:
            try:
                # Si pas de succès, vérifier s'il y a un message d'erreur
                error_message = selenium.wait_for_element_visible(self.ERROR_TOAST, timeout=5)
                assert error_message.text in self.ERROR_MESSAGES['duplicate_url_key']
            except TimeoutException:
                pytest.fail("Aucune popup (succès ou erreur) n'a été affichée")

    def test_delete_category(self, selenium):
        """Test la suppression d'une catégorie existante"""
        self.login_admin(selenium)
        selenium.driver.get(self.CATEGORIES_URL)

        # Recherche de la catégorie
        search_input = selenium.wait_for_element_visible(self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(self.EDIT_CATEGORY_DATA['name'])
        search_input.send_keys(Keys.ENTER)

        # Sélectionner la checkbox de la catégorie
        rows = selenium.driver.find_elements(By.CSS_SELECTOR, "table.listing tbody tr")
        
        for row in rows:
            # Cherche le nom de la catégorie dans la 2e colonne
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 1:
                category_name = columns[1].text.strip()
                if category_name == self.EDIT_CATEGORY_DATA['name']:
                    # Clique sur le checkbox du premier <td>
                    checkbox = columns[0].find_element(By.CSS_SELECTOR, "input[type='checkbox']")                    
                    ActionChains(selenium.driver).move_to_element(checkbox).click().perform()
                    break

        # Cliquer sur le bouton Delete de la barre d'action (ligne d'action en haut du tableau)
        action_row = selenium.wait_for_element_visible(self.ACTION_ROW)
        delete_button = action_row.find_element(*self.ACTION_DELETE_BUTTON_XPATH)
        delete_button.click()

        # Attendre que l'overlay modal disparaisse avant de cliquer sur Delete        
        modal_delete = selenium.wait_for_element_visible(self.MODAL_DELETE_BUTTON)
        modal_delete.click() 

        # Reprendre une nouvelle référence sur le champ de recherche
        search_input = selenium.wait_for_element_visible(self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(Keys.ENTER)

        # Vérifier que la catégorie n'est plus présente dans le tableau
        rows = selenium.driver.find_elements(By.CSS_SELECTOR, "table.listing tbody tr")
        category_found = False
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 1:
                category_name = columns[1].text.strip()
                if category_name == self.EDIT_CATEGORY_DATA['name']:
                    category_found = True
                    break
        if category_found:
            pytest.fail(f"La catégorie '{self.EDIT_CATEGORY_DATA['name']}' est toujours présente après suppression !")
        else:
            print(f"[DEBUG] La catégorie '{self.EDIT_CATEGORY_DATA['name']}' a bien été supprimée du tableau.")

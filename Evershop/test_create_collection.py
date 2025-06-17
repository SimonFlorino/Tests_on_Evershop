import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config import SeleniumConfig
from test_admin_login import TestLogin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import os

class TestCreateCollection:
    ADMIN_URL = "http://localhost:3000/admin/login"
    COLLECTIONS_URL = "http://localhost:3000/admin/collections"
    NEW_COLLECTION_URL = "http://localhost:3000/admin/collections/new"
    DASHBOARD_TITLE = (By.CSS_SELECTOR, "h1.page-heading-title")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast-body")
    
    # Sélecteurs pour la création de collection
    NEW_COLLECTION_BUTTON = (By.CSS_SELECTOR, "a.button.primary")
    COLLECTION_NAME_INPUT = (By.ID, "name")
    COLLECTION_CODE_INPUT = (By.ID, "code")
    ROW_TEMPLATES = (By.CSS_SELECTOR, "div.row-templates a")
    CLOSE_BLOCK_BUTTON = (By.CSS_SELECTOR, "div.config a[href='#'] svg[color='#d72c0d']")
    
    # Sélecteurs pour les blocs de contenu
    BLOCK_EDITOR = (By.CSS_SELECTOR, "div.codex-editor__redactor")
    BLOCK_CONTENT = (By.CSS_SELECTOR, "div.ce-block__content")
    BLOCK_PARAGRAPH = (By.CSS_SELECTOR, "div.ce-paragraph[contenteditable='true']")
    BLOCK_PLUS_BUTTON = (By.CSS_SELECTOR, "div.ce-toolbar__plus")
    BLOCK_OPTIONS = (By.CSS_SELECTOR, "div.ce-popover__items")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.cdx-search-field__input")
    TEXT_BLOCK = (By.CSS_SELECTOR, "div.ce-popover-item[data-item-name='paragraph']")
    IMAGE_BLOCK = (By.CSS_SELECTOR, "div.ce-popover-item:not(.ce-popover-item--hidden)[data-item-name='image']")
    QUOTE_BLOCK = (By.CSS_SELECTOR, "div.ce-popover-item[data-item-name='quote']")
    IMAGE_UPLOAD_INPUT = (By.CSS_SELECTOR, "input[type='file']")
    
    # Identifiants admin valides (récupérés de TestLogin)
    ADMIN_CREDENTIALS = TestLogin.VALID_CREDENTIALS

    @pytest.fixture
    def selenium(self):
        config = SeleniumConfig(self.ADMIN_URL)
        config.setup_driver()
        yield config
        config.teardown_driver()

    def is_admin_dashboard(self, driver):
        """Vérifie si on est sur le dashboard admin"""
        current_url = driver.current_url
        return current_url.startswith("http://localhost:3000/admin") and "/login" not in current_url

    def is_collections_page(self, driver):
        """Vérifie si on est sur la page des collections"""
        return driver.current_url == self.COLLECTIONS_URL

    def is_new_collection_page(self, driver):
        """Vérifie si on est sur la page de création de collection"""
        return driver.current_url == self.NEW_COLLECTION_URL

    def login_admin(self, selenium):
        # Utilise directement la méthode fill_login_form de TestLogin
        login = TestLogin()
        selenium.driver.get(self.ADMIN_URL)
        login.fill_login_form(
            selenium,
            self.ADMIN_CREDENTIALS['email'],
            self.ADMIN_CREDENTIALS['password']
        )
        
        # Attendre que la redirection soit terminée et vérifier l'URL
        try:
            WebDriverWait(selenium.driver, 10).until(self.is_admin_dashboard)
            # Vérifier que nous sommes bien sur le dashboard
            dashboard = selenium.wait_for_element(self.DASHBOARD_TITLE)
            assert "Dashboard" in dashboard.text
        except Exception as e:
            pytest.fail(f"Login failed or incorrect redirection: {e}")

    def activate_all_blocks(self, selenium):
        """Active tous les blocs en cliquant sur leurs paragraphes"""
        # Attendre que les blocs soient chargés
        WebDriverWait(selenium.driver, 10).until(
            EC.presence_of_all_elements_located(self.BLOCK_EDITOR)
        )
        
        # Trouver tous les paragraphes éditables
        paragraphs = selenium.driver.find_elements(*self.BLOCK_PARAGRAPH)
        
        # Cliquer sur chaque paragraphe pour activer les blocs
        for paragraph in paragraphs:
            paragraph.click()
            # Attendre que le bouton plus soit visible pour ce bloc
            WebDriverWait(selenium.driver, 10).until(
                EC.visibility_of_element_located(self.BLOCK_PLUS_BUTTON)
            )

    def add_text_to_block(self, selenium, text):
        """Ajoute du texte dans un bloc éditable"""
        editable = selenium.wait_for_element_visible(self.BLOCK_PARAGRAPH)
        editable.clear()
        editable.send_keys(text)



    def select_block_type(self, selenium, block_index, block_type):
        """Sélectionne le type de bloc pour un bloc spécifique"""
        # Trouver tous les paragraphes éditables
        paragraphs = selenium.driver.find_elements(*self.BLOCK_PARAGRAPH)
        assert len(paragraphs) > block_index, f"Bloc {block_index} non trouvé"
        
        # Cliquer sur le paragraphe pour activer le bloc
        paragraphs[block_index].click()
        
        # Attendre un peu pour que le bloc soit bien activé
        time.sleep(1)
        
        # Envoyer la touche "/" pour ouvrir le menu de sélection
        paragraphs[block_index].send_keys("/")
        
        if block_type != self.IMAGE_BLOCK:
            # Attendre que le menu des options soit visible
            WebDriverWait(selenium.driver, 10).until(
                EC.visibility_of_element_located(self.BLOCK_OPTIONS)
            )
        
        # Attendre un peu pour que le menu soit complètement chargé
        time.sleep(0.5)
        
        # Sélectionner le type de bloc souhaité
        if block_type == self.IMAGE_BLOCK:
            # Trouver l'élément qui contient les options
            menu_elements = selenium.driver.find_elements(*self.BLOCK_OPTIONS)
            menu_items = None
            for element in menu_elements:
                if "Image" in element.text:
                    menu_items = element
                    break
            
            if menu_items:
                # Cliquer sur l'option Image
                image_option = menu_items.find_element(By.XPATH, ".//div[contains(text(), 'Image')]")
                image_option.click()
        else:
            # Pour les autres types de blocs, on utilise le sélecteur normal
            block_option = selenium.wait_for_element_visible(block_type)
            block_option.click()

    def test_create_new_collection(self, selenium):
        # Se connecter d'abord
        self.login_admin(selenium)
        
        # Naviguer vers la page des collections
        selenium.driver.get(self.COLLECTIONS_URL)
        
        # Vérifier que nous sommes bien sur la page des collections
        try:
            WebDriverWait(selenium.driver, 10).until(self.is_collections_page)
            title = selenium.wait_for_element(self.DASHBOARD_TITLE)
            assert "Collections" in title.text
        except Exception as e:
            pytest.fail(f"Failed to reach collections page: {e}")
            
        # Cliquer sur New Collection
        selenium.wait_and_click(self.NEW_COLLECTION_BUTTON)
        
        # Vérifier que nous sommes sur la page de création
        try:
            WebDriverWait(selenium.driver, 10).until(self.is_new_collection_page)
        except Exception as e:
            pytest.fail(f"Failed to reach new collection page: {e}")
            
        # Remplir les champs
        unique_id_from_time = int(time.time())
        selenium.wait_and_send_keys(self.COLLECTION_NAME_INPUT, "Fast Fashion")
        selenium.wait_and_send_keys(self.COLLECTION_CODE_INPUT, f"fast_fashion_{unique_id_from_time}")
        
        # Sélectionner le troisième élément des templates
        templates = selenium.driver.find_elements(*self.ROW_TEMPLATES)
        assert len(templates) >= 3, "Pas assez de templates disponibles"
        templates[2].click()  # Cliquer sur le troisième élément (index 2)
        
        # Fermer le bloc
        close_button = selenium.wait_for_element_visible(self.CLOSE_BLOCK_BUTTON)
        close_button.click()
        
        # Sélectionner l'avant-dernier élément des templates
        templates = selenium.driver.find_elements(*self.ROW_TEMPLATES)
        assert len(templates) >= 7, "Pas assez de templates disponibles"
        templates[-2].click()  # Cliquer sur l'avant-dernier élément

        # Attendre que les blocs soient chargés
        WebDriverWait(selenium.driver, 10).until(
            EC.presence_of_all_elements_located(self.BLOCK_EDITOR)
        )

        # Premier bloc : Ajouter du texte
        self.select_block_type(selenium, 0, self.TEXT_BLOCK)
        self.add_text_to_block(selenium, "Fast fashion, be ready")

        # Deuxième bloc : Ajouter une image
        self.select_block_type(selenium, 1, self.IMAGE_BLOCK)
        # A finir

        # Troisième bloc : Ajouter une citation
        self.select_block_type(selenium, 2, self.QUOTE_BLOCK)
        self.add_text_to_block(selenium, "Vous allez être magnifique")
        
        # Cliquer sur Save
        buttons = selenium.driver.find_elements(By.CSS_SELECTOR, "button.button.primary")
        save_button = None
        for btn in buttons:
            if btn.text.strip().lower() == "save":
                save_button = btn
                break
        assert save_button is not None, "Bouton Save introuvable"
        save_button.click()
        
        # Vérifier le message de succès
        try:
            assert "Collection saved successfully!" in selenium.wait_for_element_visible(self.SUCCESS_MESSAGE).text
        except Exception as e:
            pytest.fail(f"Success message not found: {e}") 
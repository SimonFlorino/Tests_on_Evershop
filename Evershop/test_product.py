import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config import SeleniumConfig
import os
from test_admin_login import TestLogin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

class TestProduct:
    ADMIN_URL = "http://localhost:3000/admin/login"
    PRODUCTS_URL = "http://localhost:3000/admin/products"
    NEW_PRODUCT_URL = "http://localhost:3000/admin/products/new"
    DASHBOARD_TITLE = (By.CSS_SELECTOR, "h1.page-heading-title")
    ERROR_LABEL = (By.CSS_SELECTOR, "div.field-error span.text-critical")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast-body")

    # Données de test pour la création
    CREATE_PRODUCT_DATA = {
        'name': 'Cravate',
        'sku': 'Tie_mickey',
        'price': '20',
        'weight': '0.1',
        'qty': '100',
        'url_key': 'ties',
        'image': 'images/tie.png',
        'meta_title': 'Belle cravate',
        'meta_keywords': 'tie',
        'meta_description': 'tie'
    }

    # Données de test pour la modification
    EDIT_PRODUCT_DATA = {
        'name': 'Cravate Mickey',
        'sku': 'Tie_mickey',
        'price': '25',
        'weight': '0.1',
        'qty': '100',
        'url_key': 'tie-mickey',
        'image': 'images/tie.png',
        'meta_title': 'Cravate Mickey',
        'meta_keywords': 'tie mickey',
        'meta_description': 'tie mickey'
    }

    # Sélecteurs pour la suppression par action-barre
    SEARCH_INPUT = (By.ID, "keyword")
    ACTION_ROW = (By.CSS_SELECTOR, "table.listing thead tr")
    MODAL_DELETE_BUTTON = (By.CSS_SELECTOR, ".modal .button.critical")
    ACTION_BAR = (By.CSS_SELECTOR, "table.listing tbody tr td[colspan] .inline-flex")
    PRODUCT_ROWS = (By.CSS_SELECTOR, "table.listing tbody tr")
    ROW_COLUMN = (By.TAG_NAME, "td")
    ACTION_LINK = (By.TAG_NAME, "a")
    ACTION_SPAN = (By.TAG_NAME, "span")

    
    # Sélecteurs pour la catégorie
    SELECT_CATEGORY_LINK = (By.LINK_TEXT, "Select category")
    CATEGORY_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search categories']")
    CATEGORY_SELECT_BUTTON = (By.CSS_SELECTOR, "button.button.secondary")
    SELECTED_CATEGORY = (By.CSS_SELECTOR, "div.border.rounded.border-\\[\\#c9cccf\\].mb-4.p-4 span.text-gray-500")
    CATEGORY_RESULT = (By.CSS_SELECTOR, "div.divide-y div.grid")
    
    # Sélecteurs pour l'image
    UPLOADED_IMAGE = (By.CSS_SELECTOR, "div.image-list div.image img")
    
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

    def test_create_new_product(self, selenium):
        # Se connecter d'abord
        self.login_admin(selenium)
        
        # Naviguer vers la page des produits
        selenium.driver.get(self.PRODUCTS_URL)
        
        # Cliquer sur New Product
        selenium.wait_and_click((By.LINK_TEXT, "New Product"))
            
        # Vérifier qu'on est sur la bonne page
        assert selenium.driver.current_url == self.NEW_PRODUCT_URL

        # Remplir les champs à partir du jeu de test
        product_data = self.CREATE_PRODUCT_DATA
        selenium.wait_and_send_keys((By.ID, "name"), product_data['name'])
        assert not self.has_field_error(selenium), "Erreur sur le champ name"
        selenium.wait_and_send_keys((By.ID, "sku"), product_data['sku'])
        assert not self.has_field_error(selenium), "Erreur sur le champ sku"
        selenium.wait_and_send_keys((By.ID, "price"), product_data['price'])
        assert not self.has_field_error(selenium), "Erreur sur le champ price"
        selenium.wait_and_send_keys((By.ID, "weight"), product_data['weight'])
        assert not self.has_field_error(selenium), "Erreur sur le champ weight"
        selenium.wait_and_send_keys((By.ID, "qty"), product_data['qty'])
        assert not self.has_field_error(selenium), "Erreur sur le champ qty"
        selenium.wait_and_send_keys((By.ID, "urlKey"), product_data['url_key'])
        assert not self.has_field_error(selenium), "Erreur sur le champ url_key"
        selenium.wait_and_send_keys((By.ID, "metaTitle"), product_data['meta_title'])
        selenium.wait_and_send_keys((By.ID, "metaKeywords"), product_data['meta_keywords'])
        selenium.wait_and_send_keys((By.ID, "meta_description"), product_data['meta_description'])

        #test git
        # Upload d'image
        image_path = os.path.abspath(product_data['image'])
        file_input = selenium.wait_for_element((By.CSS_SELECTOR, "input[type='file']"))
        file_input.send_keys(image_path)
        
        # Vérifier que l'image est bien visible
        try:
            uploaded_image = selenium.wait_for_element_visible(self.UPLOADED_IMAGE, timeout=10)
            assert uploaded_image.is_displayed(), "L'image uploadée n'est pas visible"
            image_name = os.path.basename(product_data['image'])  # "tie.png"
            assert image_name in uploaded_image.get_attribute("src"), "L'image uploadée n'est pas la bonne"
        except TimeoutException:
            pytest.fail("L'image n'a pas été uploadée correctement")
        
        selenium.scroll_down()

        # Cliquer sur Save
        buttons = selenium.driver.find_elements(By.CSS_SELECTOR, "button.button.primary")
        save_button = None
        for btn in buttons:
            if btn.text.strip().lower() == "save":
                save_button = btn
                break
        assert save_button is not None, "Bouton Save introuvable"
        save_button.click()
                
        # Vérifier qu'une popup s'affiche (succès ou erreur)
        try:
            selenium.wait_for_element_visible(self.SUCCESS_MESSAGE, timeout=5)
        except TimeoutException:
            try:
                selenium.wait_for_element_visible(self.ERROR_TOAST, timeout=5)
            except TimeoutException:
                pytest.fail("Aucune popup (succès ou erreur) n'a été affichée")

    def test_edit_product(self, selenium):
        """Test de modification d'un produit existant"""
        self.login_admin(selenium)
        selenium.driver.get(self.PRODUCTS_URL)

        # Rechercher le produit par nom dans la barre de recherche
        search_input = selenium.wait_for_element((By.ID, "keyword"))
        search_input.clear()
        search_input.send_keys(self.CREATE_PRODUCT_DATA['name'])

        # Trouver la ligne correspondant au produit et cliquer sur le nom
        product_rows = selenium.driver.find_elements(By.CSS_SELECTOR, "table.listing tbody tr")
        assert product_rows, "Aucun produit trouvé pour modification"
        found = False
        for row in product_rows:
            try:
                name_link = row.find_element(By.CSS_SELECTOR, "a.hover\\:underline.font-semibold")
                if name_link.text.strip().lower() == self.CREATE_PRODUCT_DATA['name'].lower():
                    name_link.click()
                    found = True
                    break
            except Exception:
                continue
        assert found, f"Le produit '{self.CREATE_PRODUCT_DATA['name']}' n'a pas été trouvé dans la liste"

        product_data = self.EDIT_PRODUCT_DATA
        # Modifier le nom et le prix
        selenium.wait_and_clear_and_send_keys((By.ID, "name"), product_data['name'])
        selenium.wait_and_clear_and_send_keys((By.ID, "sku"), product_data['sku'])
        selenium.wait_and_clear_and_send_keys((By.ID, "price"), product_data['price'])

        # Saisie des champs meta lors de la modification
        selenium.wait_and_clear_and_send_keys((By.ID, "urlKey"), product_data['url_key'])
        selenium.wait_and_clear_and_send_keys((By.ID, "metaTitle"), product_data['meta_title'])
        selenium.wait_and_clear_and_send_keys((By.ID, "metaKeywords"), product_data['meta_keywords'])
        selenium.wait_and_clear_and_send_keys((By.ID, "meta_description"), product_data['meta_description'])
        selenium.scroll_down()

        # Sauvegarder
        buttons = selenium.driver.find_elements(By.CSS_SELECTOR, "button.button.primary")
        save_button = None
        for btn in buttons:
            if btn.text.strip().lower() == "save":
                save_button = btn
                break
        assert save_button is not None, "Bouton Save introuvable pour modification"
        save_button.click()

        # Vérifier qu'une popup s'affiche (succès ou erreur)
        try:
            selenium.wait_for_element_visible(self.SUCCESS_MESSAGE, timeout=5)
        except TimeoutException:
            try:
                selenium.wait_for_element_visible(self.ERROR_TOAST, timeout=5)
            except TimeoutException:
                pytest.fail("Aucune popup (succès ou erreur) n'a été affichée")

    def test_delete_product(self, selenium):
        """Test de suppression d'un produit existant (avec sélection par checkbox/action-barre)"""
        self.login_admin(selenium)
        selenium.driver.get(self.PRODUCTS_URL)

        # Recherche du produit par nom
        search_input = selenium.wait_for_element_visible(self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(self.EDIT_PRODUCT_DATA['name'])
        search_input.send_keys(Keys.ENTER)

        # Sélectionner la checkbox du produit
        rows = selenium.driver.find_elements(By.CSS_SELECTOR, "table.listing tbody tr")
        checkbox_clicked = False
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 1:
                product_name = columns[2].text.strip() if len(columns) > 2 else ""
                if product_name == self.EDIT_PRODUCT_DATA['name']:
                    checkbox = columns[0].find_element(By.CSS_SELECTOR, "input[type='checkbox']")                    
                    ActionChains(selenium.driver).move_to_element(checkbox).click().perform()
                    checkbox_clicked = True
                    break
        assert checkbox_clicked, f"Le produit '{self.EDIT_PRODUCT_DATA['name']}' n'a pas été trouvé ou sélectionné."

        # Cliquer sur le bouton Delete de la barre d'action (dans la barre d'action du tableau)
        action_bar = selenium.driver.find_element(*self.ACTION_BAR)
        delete_button = None
        for a in action_bar.find_elements(*self.ACTION_LINK):
            try:
                span = a.find_element(*self.ACTION_SPAN)
                if span.text.strip().lower() == "delete":
                    delete_button = a
                    break
            except Exception:
                if a.text.strip().lower() == "delete":
                    delete_button = a
                    break
        assert delete_button is not None, "Bouton Delete introuvable dans la barre d'action"
        delete_button.click()

        # Confirmer la suppression dans la modale
        modal_delete = selenium.wait_for_element_visible(self.MODAL_DELETE_BUTTON)
        modal_delete.click()
        
        # Ensuite, manipuler le champ de recherche
        time.sleep(1) #le seul sleep que je n'ai pas réussi à remplacer
        search_input = selenium.wait_for_element_visible(self.SEARCH_INPUT)        
        search_input.clear()
        search_input.send_keys(Keys.ENTER)

        # Vérifier que le produit n'est plus présent dans le tableau
        rows = selenium.driver.find_elements(*self.PRODUCT_ROWS)
        product_found = False
        for row in rows:
            columns = row.find_elements(*self.ROW_COLUMN)
            if len(columns) > 1:
                product_name = columns[2].text.strip() if len(columns) > 2 else ""
                if product_name == self.EDIT_PRODUCT_DATA['name']:
                    product_found = True
                    break
        if product_found:
            pytest.fail(f"Le produit '{self.EDIT_PRODUCT_DATA['name']}' est toujours présent après suppression !")
        else:
            print(f"[DEBUG] Le produit '{self.EDIT_PRODUCT_DATA['name']}' a bien été supprimé du tableau.")


    def has_field_error(self, selenium):
        try:
            error = selenium.driver.find_element(*self.ERROR_LABEL)
            return error.is_displayed()
        except:
            return False 
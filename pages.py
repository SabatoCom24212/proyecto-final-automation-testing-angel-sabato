from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils import get_logger


class BasePage:
    """Clase base para todos los Page Objects"""
    
    DEFAULT_TIMEOUT = 10  
    SHORT_TIMEOUT = 5     
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)
        self.logger = get_logger(self.__class__.__name__)
    
    def find_element(self, locator, timeout=None):
        """Encuentra un elemento con espera explícita"""
        timeout = timeout or self.DEFAULT_TIMEOUT
        try:
            self.logger.debug(f"Buscando elemento: {locator}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Timeout al buscar: {locator}")
            raise
    
    def click_element(self, locator, timeout=None):
        """Click en elemento esperando que sea clickeable"""
        timeout = timeout or self.DEFAULT_TIMEOUT
        try:
            self.logger.debug(f"Click en: {locator}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            # Scroll al elemento para asegurar visibilidad
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
        except TimeoutException:
            self.logger.error(f"Timeout en click: {locator}")
            raise
    
    def send_keys_to_element(self, locator, text, timeout=None):
        """Envía texto a un elemento"""
        timeout = timeout or self.DEFAULT_TIMEOUT
        try:
            self.logger.debug(f"Enviando texto a: {locator}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            self.logger.error(f"Timeout al enviar texto: {locator}")
            raise
    
    def is_element_visible(self, locator, timeout=None):
        """Verifica si un elemento es visible"""
        timeout = timeout or self.SHORT_TIMEOUT
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def get_element_text(self, locator, timeout=None):
        """Obtiene el texto de un elemento"""
        timeout = timeout or self.DEFAULT_TIMEOUT
        element = self.find_element(locator, timeout)
        return element.text


class LoginPage(BasePage):
    """Página de Login"""
    
    URL = "https://www.saucedemo.com/"
    
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MSG = (By.CSS_SELECTOR, "h3[data-test='error']")
    
    def navigate(self):
        """Navegar a la página de login"""
        self.logger.info(f"Navegando a {self.URL}")
        self.driver.get(self.URL)
        self.logger.debug(f"URL actual: {self.driver.current_url}")
    
    def login(self, username, password):
        """Realizar login"""
        self.logger.info(f"Login con usuario: {username}")
        
        try:
            # Esperar a que la página cargue
            self.find_element(self.USERNAME, timeout=self.SHORT_TIMEOUT)
            
            # Ingresar credenciales
            self.send_keys_to_element(self.USERNAME, username)
            self.logger.debug("Usuario ingresado")
            
            self.send_keys_to_element(self.PASSWORD, password)
            self.logger.debug("Contraseña ingresada")
            
            # Click en login
            self.click_element(self.LOGIN_BTN)
            self.logger.debug("Botón login clickeado")
            
        except Exception as e:
            self.logger.error(f"Error en login: {str(e)}")
            raise
    
    def get_error_message(self):
        """Obtener mensaje de error"""
        return self.get_element_text(self.ERROR_MSG)
    
    def is_error_displayed(self):
        """Verificar si hay error visible"""
        return self.is_element_visible(self.ERROR_MSG)


class InventoryPage(BasePage):
    """Página de Inventario"""
    
    INVENTORY = (By.ID, "inventory_container")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    BURGER_MENU_BTN = (By.ID, "react-burger-menu-btn")
    RESET_APP_STATE_LINK = (By.ID, "reset_sidebar_link")
    CLOSE_MENU_BTN = (By.ID, "react-burger-cross-btn")
    MENU_ITEMS = (By.CLASS_NAME, "bm-item-list")
    
    def is_loaded(self):
        """Verificar que la página está cargada"""
        self.logger.debug("Verificando carga de inventario")
        is_loaded = self.is_element_visible(self.INVENTORY, timeout=self.DEFAULT_TIMEOUT)
        self.logger.info(f"Inventario cargado: {is_loaded}")
        return is_loaded
    
    def add_product_to_cart_by_id(self, product_id):
        """Agregar producto al carrito por ID"""
        locator = (By.ID, product_id)
        self.logger.info(f"Agregando producto: {product_id}")
        self.click_element(locator)
    
    def add_backpack_to_cart(self):
        """Agregar mochila al carrito (producto más usado en tests)"""
        self.add_product_to_cart_by_id("add-to-cart-sauce-labs-backpack")
    
    def get_cart_count(self):
        """Obtener cantidad de items en carrito"""
        try:
            badge = self.wait.until(
                EC.visibility_of_element_located(self.CART_BADGE)
            )
            badge_text = badge.text
            count = int(badge_text)
            self.logger.debug(f"Items en carrito: {count}")
            return count
            
        except TimeoutException:
            self.logger.debug("Carrito vacío (Badge no encontrado)")
            return 0
            
        except Exception as e:
            self.logger.error(f"Error inesperado al obtener conteo del carrito: {str(e)}")
            return 0
    
    def wait_for_cart_count(self, expected_count, timeout=10):
        """
        Espera a que el carrito tenga el número esperado de items.
        Helper para evitar duplicación de código en tests.
        
        Args:
            expected_count: Número esperado de items
            timeout: Tiempo máximo de espera en segundos
            
        Raises:
            AssertionError: Si no se alcanza el conteo esperado
        """
        self.logger.debug(f"Esperando que carrito tenga {expected_count} items...")
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(*self.CART_BADGE).is_displayed() and 
                         d.find_element(*self.CART_BADGE).text == str(expected_count)
            )
            self.logger.info(f"Carrito actualizado a {expected_count} items")
            return True
        except TimeoutException:
            actual = self.get_cart_count()
            error_msg = f"Carrito no alcanzó {expected_count} items en {timeout}s. Actual: {actual}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
    
    def go_to_cart(self):
        """Ir al carrito"""
        self.logger.info("Navegando al carrito")
        self.click_element(self.CART_LINK)

    def reset_app_state(self):
        """
        Resetea el estado de la aplicación limpiando el carrito.
        Implementa múltiples estrategias de respaldo.
        """
        self.logger.info("Reseteando estado de la aplicación")
        
        try:
            # Verificar si el carrito ya está vacío
            cart_count = self.get_cart_count()
            if cart_count == 0:
                self.logger.info("Carrito ya está vacío")
                return
            
            self.logger.info(f"Carrito tiene {cart_count} items, procediendo a resetear...")
            
            # Estrategia 1: Reset vía menú hamburguesa
            try:
                self._reset_via_menu()
                
                # Verificar que funcionó
                WebDriverWait(self.driver, self.SHORT_TIMEOUT).until(
                    lambda d: self.get_cart_count() == 0
                )
                new_count = self.get_cart_count()
                if new_count == 0:
                    self.logger.info("Reset exitoso vía menú")
                    return
                else:
                    self.logger.warning(f"Reset vía menú parcial ({new_count} items restantes)")
            
            except Exception as menu_error:
                self.logger.warning(f"Reset vía menú falló: {menu_error}")
            
            # Estrategia 2: Recarga de página
            self.logger.info("Intentando reset vía recarga de página...")
            self.driver.refresh()
            
            WebDriverWait(self.driver, self.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(self.INVENTORY)
            )
            
            final_count = self.get_cart_count()
            if final_count == 0:
                self.logger.info("Reset exitoso vía recarga")
            else:
                self.logger.error(f"No se pudo vaciar el carrito ({final_count} items)")
        
        except Exception as e:
            self.logger.error(f"Error crítico en reset_app_state: {str(e)}")

    def _reset_via_menu(self):
        """Método auxiliar para resetear vía menú hamburguesa"""
        self.logger.debug("Ejecutando reset vía menú...")
        
        # Verificar si el menú ya está abierto
        menu_abierto = self.is_element_visible(self.RESET_APP_STATE_LINK, timeout=1)
        
        if not menu_abierto:
            self.logger.debug("Abriendo menú hamburguesa")
            burger_btn = WebDriverWait(self.driver, self.SHORT_TIMEOUT).until(
                EC.element_to_be_clickable(self.BURGER_MENU_BTN)
            )
            burger_btn.click()
            
            self.logger.debug("Esperando apertura del menú...")
            WebDriverWait(self.driver, self.SHORT_TIMEOUT).until(
                EC.visibility_of_element_located(self.MENU_ITEMS)
            )
        
        # Click en reset
        self.logger.debug("Haciendo click en Reset App State")
        reset_link = WebDriverWait(self.driver, self.SHORT_TIMEOUT).until(
            EC.element_to_be_clickable(self.RESET_APP_STATE_LINK)
        )
        reset_link.click()
        
        # Cerrar menú
        if self.is_element_visible(self.CLOSE_MENU_BTN, timeout=2):
            self.logger.debug("Cerrando menú")
            close_btn = WebDriverWait(self.driver, self.SHORT_TIMEOUT).until(
                EC.element_to_be_clickable(self.CLOSE_MENU_BTN)
            )
            close_btn.click()
        
        self.logger.debug("Reset vía menú completado")


class CartPage(BasePage):
    """Página del Carrito"""
    
    CART_CONTAINER = (By.ID, "cart_contents_container")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BTN = (By.ID, "checkout")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    
    def is_loaded(self):
        """Verificar que el carrito está cargado"""
        is_loaded = self.is_element_visible(self.CART_CONTAINER, timeout=self.DEFAULT_TIMEOUT)
        self.logger.debug(f"Carrito cargado: {is_loaded}")
        return is_loaded
    
    def get_items_count(self):
        """Obtener cantidad de items en el carrito"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.CART_CONTAINER))
            self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEMS))
            items = self.driver.find_elements(*self.CART_ITEMS)
            count = len(items)
            self.logger.info(f"Items en carrito: {count}")
            return count
        except:
            return 0
    
    def get_item_names(self):
        """Obtener nombres de productos en el carrito"""
        self.logger.debug("Obteniendo nombres de productos")
        names = []
        
        try:
            items = self.wait.until(
                EC.visibility_of_all_elements_located(self.CART_ITEMS)
            )
            
            for item in items:
                try:
                    name = item.find_element(*self.ITEM_NAME).text
                    names.append(name)
                    self.logger.debug(f"  - {name}")
                except NoSuchElementException:
                    self.logger.warning("No se pudo encontrar el nombre de un item")
        except Exception as e:
            self.logger.warning(f"Error al obtener nombres: {e}")
        
        return names
    
    def checkout(self):
        """Ir a checkout"""
        self.logger.info("Iniciando checkout")
        self.click_element(self.CHECKOUT_BTN)


class CheckoutPage(BasePage):
    """Página de Checkout"""
    
    CHECKOUT_INFO = (By.ID, "checkout_info_container")
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    ZIP_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    FINISH_BTN = (By.ID, "finish")
    COMPLETE_CONTAINER = (By.ID, "checkout_complete_container")
    SUCCESS_MSG = (By.CLASS_NAME, "complete-header")
    ERROR_MSG = (By.CSS_SELECTOR, "h3[data-test='error']")
    
    def is_loaded(self):
        """Verificar que el checkout está cargado"""
        is_loaded = self.is_element_visible(self.CHECKOUT_INFO, timeout=self.DEFAULT_TIMEOUT)
        self.logger.debug(f"Checkout cargado: {is_loaded}")
        return is_loaded
    
    def fill_information(self, first_name, last_name, zip_code):
        """Completar información de checkout"""
        self.logger.info(f"Completando información: {first_name} {last_name}")
        
        self.send_keys_to_element(self.FIRST_NAME, first_name)
        self.send_keys_to_element(self.LAST_NAME, last_name)
        self.send_keys_to_element(self.ZIP_CODE, zip_code)
    
    def click_continue(self):
        """Continuar al siguiente paso"""
        self.logger.info("Continuando")
        self.click_element(self.CONTINUE_BTN)
    
    def click_finish(self):
        """Finalizar compra"""
        self.logger.info("Finalizando compra")
        self.click_element(self.FINISH_BTN)
    
    def get_success_message(self):
        """Obtener mensaje de éxito"""
        self.logger.debug("Obteniendo mensaje de confirmación")
        message = self.get_element_text(self.SUCCESS_MSG)
        self.logger.info(f"Mensaje: {message}")
        return message
    
    def is_checkout_complete(self):
        """Verificar si checkout se completó"""
        is_complete = self.is_element_visible(self.COMPLETE_CONTAINER, timeout=self.DEFAULT_TIMEOUT)
        self.logger.debug(f"Checkout completo: {is_complete}")
        return is_complete

    def get_error_message(self):
        """Obtener mensaje de error en la página de checkout"""
        return self.get_element_text(self.ERROR_MSG)

    def is_error_displayed(self):
        """Verificar si hay error visible en la página de checkout"""
        return self.is_element_visible(self.ERROR_MSG)
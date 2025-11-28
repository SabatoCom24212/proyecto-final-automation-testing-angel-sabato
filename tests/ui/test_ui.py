import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import LoginPage, InventoryPage, CartPage, CheckoutPage
from utils import get_logger, data_loader, capturar_pantalla

logger = get_logger(__name__)


@pytest.mark.ui
class TestUI:
    """Suite de tests de UI"""
    
    @pytest.mark.parametrize("usuario", data_loader.get_usuarios_validos())
    def test_01_login_exitoso(self, driver, usuario):
        """
        Test 1: Login exitoso con credenciales válidas (PARAMETRIZADO)
        """
        logger.test_start("test_01_login_exitoso")
        
        try:
            # Arrange
            logger.step("Inicializando páginas")
            login_page = LoginPage(driver)
            inventory_page = InventoryPage(driver)
            
            # Act
            logger.step(f"Navegando a {login_page.URL}")
            login_page.navigate()
            
            logger.step(f"Realizando login con usuario: {usuario['username']}")
            login_page.login(usuario['username'], usuario['password'])
            
            # Espera explícita para carga de inventario
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(inventory_page.INVENTORY)
            )
            
            # Assert
            logger.step("Verificando que se cargó la página de inventario")
            is_loaded = inventory_page.is_loaded()
            logger.assertion("Página de inventario cargada", is_loaded)
            assert is_loaded, "Debería cargar la página de inventario"
            
            url_check = "inventory.html" in driver.current_url
            logger.assertion("URL contiene 'inventory.html'", url_check)
            assert url_check
            
            logger.test_end("test_01_login_exitoso", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_01_login_exitoso", "FAIL")
            raise
    
    @pytest.mark.parametrize("usuario", data_loader.get_usuarios_invalidos())
    def test_02_login_fallido(self, driver, usuario):
        """
        Test 2: Login fallido con credenciales inválidas (ESCENARIO NEGATIVO PARAMETRIZADO)
        """
        logger.test_start("test_02_login_fallido")
        
        try:
            # Arrange
            logger.step("Inicializando página de login")
            login_page = LoginPage(driver)
            
            # Act
            logger.step("Navegando a la página de login")
            login_page.navigate()
            
            logger.step(f"Intentando login con credenciales inválidas: {usuario['username']}")
            login_page.login(usuario['username'], usuario['password'])
            
            # Assert
            logger.step("Verificando que se muestra mensaje de error")
            error_displayed = login_page.is_error_displayed()
            logger.assertion("Error visible en pantalla", error_displayed)
            assert error_displayed, "Debería mostrar mensaje de error"
            
            error_msg = login_page.get_error_message()
            logger.action(f"Mensaje de error obtenido: {error_msg}")
            
            expected_error = usuario.get('expected_error', '')
            error_check = expected_error in error_msg
            logger.assertion(f"Mensaje contiene '{expected_error}'", error_check)
            assert error_check
            
            logger.test_end("test_02_login_fallido", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_02_login_fallido", "FAIL")
            raise
    
    def test_03_agregar_producto_al_carrito(self, logged_in_driver):
        """
        Test 3: Agregar un producto al carrito
        """
        logger.test_start("test_03_agregar_producto_al_carrito")
        
        try:
            # Arrange
            logger.step("Inicializando páginas")
            inventory_page = InventoryPage(logged_in_driver)
            
            # Verificar estado inicial
            initial_count = inventory_page.get_cart_count()
            logger.action(f"Carrito inicial: {initial_count} items")
            assert initial_count == 0, f"Carrito debería estar vacío al inicio, pero tiene {initial_count} items"
            
            # Act
            logger.step("Agregando producto al carrito")
            inventory_page.add_backpack_to_cart()
            logger.action("Producto 'Backpack' agregado")
            
            inventory_page.wait_for_cart_count(expected_count=1)
            
            # Assert
            cart_count = inventory_page.get_cart_count()
            logger.action(f"Cantidad en carrito: {cart_count}")
            logger.assertion("Carrito tiene 1 item", cart_count == 1)
            assert cart_count == 1, f"El carrito debería tener 1 item, pero tiene {cart_count}"
            
            logger.test_end("test_03_agregar_producto_al_carrito", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            capturar_pantalla(logged_in_driver, "test_03_agregar_producto_al_carrito", "ERROR")
            logger.test_end("test_03_agregar_producto_al_carrito", "FAIL")
            raise
    
    @pytest.mark.parametrize("checkout_data", data_loader.get_checkout_info())
    def test_04_proceso_checkout_completo(self, logged_in_driver, checkout_data):
        """
        Test 4: Proceso completo de checkout (FLUJO COMPLETO PARAMETRIZADO)
        """
        logger.test_start("test_04_proceso_checkout_completo")
        
        try:
            # Arrange
            logger.step("Inicializando todas las páginas")
            inventory_page = InventoryPage(logged_in_driver)
            cart_page = CartPage(logged_in_driver)
            checkout_page = CheckoutPage(logged_in_driver)
            
            # Verificar estado inicial
            initial_count = inventory_page.get_cart_count()
            assert initial_count == 0, f"Carrito debe estar vacío, tiene {initial_count} items"
            
            # Act - Agregar producto
            logger.step("Fase 1: Agregar producto al carrito")
            inventory_page.add_backpack_to_cart()
            logger.action("Producto agregado")
            
            inventory_page.wait_for_cart_count(expected_count=1)

            logger.step("Navegando al carrito")
            inventory_page.go_to_cart()
            
            # Esperar a que la URL cambie a la página del carrito
            WebDriverWait(logged_in_driver, 15).until(
                EC.url_contains("cart.html")
            )
            
            # Esperar carga del carrito
            WebDriverWait(logged_in_driver, 15).until(
                EC.presence_of_element_located(cart_page.CART_CONTAINER)
            )
            
            # Act - Checkout
            logger.step("Fase 2: Proceso de checkout")
            cart_page.checkout()
            
            # Esperar carga de formulario
            WebDriverWait(logged_in_driver, 15).until(
                EC.presence_of_element_located(checkout_page.CHECKOUT_INFO)
            )
            
            logger.step(f"Completando información: {checkout_data['first_name']} {checkout_data['last_name']}")
            checkout_page.fill_information(
                checkout_data['first_name'],
                checkout_data['last_name'],
                checkout_data['postal_code']
            )
            logger.action("Información completada")
            
            logger.step("Continuando al resumen")
            checkout_page.click_continue()
            
            # Esperar botón finish
            WebDriverWait(logged_in_driver, 15).until(
                EC.element_to_be_clickable(checkout_page.FINISH_BTN)
            )
            
            logger.step("Finalizando compra")
            checkout_page.click_finish()
            
            # Esperar confirmación
            WebDriverWait(logged_in_driver, 15).until(
                EC.presence_of_element_located(checkout_page.COMPLETE_CONTAINER)
            )
            
            # Assert
            logger.step("Verificando confirmación de compra")
            success_msg = checkout_page.get_success_message()
            logger.action(f"Mensaje recibido: {success_msg}")
            
            success_check = "Thank you for your order" in success_msg
            logger.assertion("Mensaje de éxito presente", success_check)
            assert success_check, "Debería mostrar mensaje de confirmación"

            logger.test_end("test_04_proceso_checkout_completo", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_04_proceso_checkout_completo", "FAIL")
            raise
    
    def test_05_verificar_productos_en_carrito(self, logged_in_driver):
        """
        Test 5: Verificar que múltiples productos agregados aparecen correctamente en el carrito
        """
        logger.test_start("test_05_verificar_productos_en_carrito")
        
        try:
            # Arrange
            logger.step("Inicializando páginas")
            inventory_page = InventoryPage(logged_in_driver)
            cart_page = CartPage(logged_in_driver)
            
            # Verificar estado inicial
            initial_count = inventory_page.get_cart_count()
            assert initial_count == 0, f"Carrito debe estar vacío, tiene {initial_count} items"
            
            # Obtener lista de productos desde test_data.json
            productos = data_loader.get_productos()
            logger.action(f"Productos a agregar: {len(productos)}")
            
            # Act - Agregar todos los productos
            logger.step(f"Agregando {len(productos)} productos al carrito")
            for idx, producto in enumerate(productos, 1):
                logger.action(f"Agregando producto {idx}/{len(productos)}: {producto['nombre']}")
                inventory_page.add_product_to_cart_by_id(producto['id'])
                
                # Esperar que el carrito se actualice después de cada producto
                inventory_page.wait_for_cart_count(expected_count=idx)
                logger.action(f"Carrito actualizado: {idx} item(s)")
            
            # Verificar badge final antes de ir al carrito
            badge_count = inventory_page.get_cart_count()
            logger.action(f"Badge muestra: {badge_count} item(s)")
            
            logger.step("Navegando al carrito")
            inventory_page.go_to_cart()
            
            # Esperar carga del carrito
            WebDriverWait(logged_in_driver, 10).until(
                EC.presence_of_element_located(cart_page.CART_CONTAINER)
            )
            
            # Assert - Verificar cantidad
            cart_count = cart_page.get_items_count()
            logger.action(f"Carrito contiene: {cart_count} item(s)")
            
            expected_count = len(productos)
            logger.assertion(
                f"Badge y carrito coinciden ({expected_count} items)", 
                badge_count == cart_count == expected_count
            )
            assert badge_count == cart_count == expected_count, \
                f"Cantidad debería ser {expected_count}, badge={badge_count}, cart={cart_count}"
            
            # Assert - Verificar nombres de productos
            logger.step("Verificando que todos los productos están en el carrito")
            items_in_cart = cart_page.get_item_names()
            logger.action(f"Productos encontrados en carrito: {items_in_cart}")
            
            for producto in productos:
                product_found = producto['nombre'] in items_in_cart
                logger.assertion(
                    f"Producto '{producto['nombre']}' presente en carrito", 
                    product_found
                )
                assert product_found, \
                    f"Producto '{producto['nombre']}' no encontrado. Items en carrito: {items_in_cart}"
            
            logger.action(f"Todos los {expected_count} productos verificados correctamente")
            logger.test_end("test_05_verificar_productos_en_carrito", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_05_verificar_productos_en_carrito", "FAIL")
            raise
    
    def test_06_checkout_sin_informacion(self, logged_in_driver):
        """
        Test 6: Checkout sin completar información (ESCENARIO NEGATIVO)
        """
        logger.test_start("test_06_checkout_sin_informacion")
        
        try:
            # Arrange
            logger.step("Inicializando páginas")
            inventory_page = InventoryPage(logged_in_driver)
            cart_page = CartPage(logged_in_driver)
            checkout_page = CheckoutPage(logged_in_driver)
            
            # Verificar estado inicial
            initial_count = inventory_page.get_cart_count()
            assert initial_count == 0, f"Carrito debe estar vacío, tiene {initial_count} items"
            
            # Act
            inventory_page.add_backpack_to_cart()
            
            inventory_page.wait_for_cart_count(expected_count=1)
            
            inventory_page.go_to_cart()
            
            WebDriverWait(logged_in_driver, 10).until(
                EC.presence_of_element_located(cart_page.CART_CONTAINER)
            )
            
            cart_page.checkout()
            
            WebDriverWait(logged_in_driver, 10).until(
                EC.presence_of_element_located(checkout_page.CHECKOUT_INFO)
            )
            
            # Intentar continuar sin llenar información
            logger.step("Intentando continuar sin completar información")
            checkout_page.click_continue()
            logger.action("Botón 'Continue' clickeado sin datos")
            
            # Esperar mensaje de error
            WebDriverWait(logged_in_driver, 10).until(
                EC.presence_of_element_located(checkout_page.ERROR_MSG)
            )
            
            # Assert
            logger.step("Verificando que permanece en la misma página")
            current_url = logged_in_driver.current_url
            logger.action(f"URL actual: {current_url}")
            
            url_check = "checkout-step-one.html" in current_url
            logger.assertion("Permanece en la página de checkout", url_check)
            assert url_check, "Debería permanecer en checkout-step-one"
            
            # Verificar mensaje de error
            error_displayed = checkout_page.is_error_displayed()
            logger.assertion("Mensaje de error visible", error_displayed)
            assert error_displayed, "Debería mostrar mensaje de error"
            
            error_msg = checkout_page.get_error_message()
            logger.action(f"Mensaje de error: {error_msg}")
            assert "Error: First Name is required" in error_msg, f"Mensaje inesperado: {error_msg}"
            
            logger.test_end("test_06_checkout_sin_informacion", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_06_checkout_sin_informacion", "FAIL")
            raise
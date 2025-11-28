import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import base64
from pages import LoginPage, InventoryPage
from utils import get_logger, capturar_pantalla, config, limpiar_navegador

logger = get_logger(__name__)


def _configurar_chrome_options():
    """
    Configura las opciones de Chrome.
    Helper function para evitar duplicación.
    """
    options = Options()
    
    # Modo headless
    if config.is_headless():
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        logger.info("Modo: HEADLESS")
    else:
        options.add_argument("--start-maximized")
        logger.info("Modo: NORMAL")
    
    # Opciones de estabilidad y limpieza
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Deshabilitar cache y cookies persistentes
    options.add_argument("--disable-application-cache")
    options.add_argument("--disk-cache-size=0")
    
    # Deshabilitar administrador de contraseñas
    options.add_argument("--disable-features=PasswordManagerSafetyCheck")
    
    # Preferencias
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "autofill.profile_enabled": False,
        "profile.password_manager_leak_detection": False
    }
    options.add_experimental_option("prefs", prefs)
    
    # Excluir switches
    options.add_experimental_option('excludeSwitches', [
        'enable-logging',
        'enable-automation'
    ])
    
    options.add_experimental_option("useAutomationExtension", False)
    
    return options


@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture de WebDriver con scope FUNCTION para aislamiento total.
    Cada test obtiene un navegador completamente nuevo.
    """
    test_name = request.node.name
    logger.info(f"Iniciando test: {test_name}")
    
    # Configurar Chrome
    options = _configurar_chrome_options()
    
    # Inicializar WebDriver
    driver_instance = None
    try:
        logger.info("Inicializando WebDriver con Selenium Manager...")
        service = Service()
        driver_instance = webdriver.Chrome(service=service, options=options)
        
        # Configurar timeouts
        driver_instance.implicitly_wait(10)
        driver_instance.set_page_load_timeout(30)
        
        logger.info("WebDriver listo")
        
    except Exception as e:
        logger.error(f"Error al inicializar WebDriver: {e}")
        raise
    
    yield driver_instance
    
    # Teardown
    try:
        # Capturar screenshot si falló
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            logger.warning(f"Test FALLÓ")
            
            try:
                screenshot_path = capturar_pantalla(driver_instance, test_name, "FAILED")
                logger.info(f"Screenshot: {screenshot_path}")
                
                # Embeber en reporte HTML
                with open(screenshot_path, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode()
                
                html = f'<div><img src="data:image/png;base64,{img_data}" style="max-width:100%; border:2px solid red;"/></div>'
                
                extra = getattr(request.node, 'extra', [])
                extra.append(pytest.html.extras.html(html))
                request.node.extra = extra
            
            except Exception as e:
                logger.warning(f"No se pudo capturar screenshot: {e}")
        else:
            logger.info(f"Test EXITOSO")
    
    finally:
        # Cerrar WebDriver siempre
        if driver_instance:
            try:
                limpiar_navegador(driver_instance, logger)
                driver_instance.quit()
                logger.info("WebDriver cerrado y limpiado")
            except Exception as e:
                logger.warning(f"Error al cerrar driver: {e}")


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    Fixture que entrega un driver ya logueado con garantía de carrito vacío.
    """
    logger.info("Fixture 'logged_in_driver': Realizando login limpio...")
    
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    
    # PASO 1: Limpiar storage antes del login
    limpiar_navegador(driver, logger)
    
    # PASO 2: Navegar y hacer login
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    
    # PASO 3: Asegurar que estamos en la página de inventario
    assert inventory_page.is_loaded(), "No se pudo cargar la página de inventario después del login."
    logger.info("Login exitoso, página de inventario cargada")
    
    # PASO 4: Garantizar carrito vacío usando el método refactorizado
    logger.info("Garantizando carrito vacío...")
    inventory_page.reset_app_state()
    
    # Verificación final
    final_count = inventory_page.get_cart_count()
    if final_count > 0:
        logger.error(f"ADVERTENCIA: No se pudo vaciar el carrito completamente ({final_count} items)")
    else:
        logger.info("Carrito vacío confirmado")
    
    logger.info("Fixture 'logged_in_driver' listo para el test")
    
    yield driver
    
    # Teardown del fixture
    limpiar_navegador(driver, logger)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura resultado del test"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup de directorios"""
    logger_env = get_logger("test_environment")
    
    logger_env.info("="*80)
    logger_env.info("INICIANDO SUITE DE TESTS")
    logger_env.info("="*80)
    
    # Crear directorios
    for directory in ['screenshots', 'reports', 'logs']:
        os.makedirs(directory, exist_ok=True)
    
    yield
    
    logger_env.info("="*80)
    logger_env.info("SUITE FINALIZADA")
    logger_env.info("="*80)


def pytest_html_report_title(report):
    """Título del reporte"""
    report.title = "Test Automation Report"


def pytest_configure(config):
    """Metadata del reporte"""
    config._metadata = {
        'Sistema': 'Windows AMD64',
        'Python': '3.13.7',
        'Browser': 'Chrome',
        'Aislamiento': 'Function-scoped drivers'
    }
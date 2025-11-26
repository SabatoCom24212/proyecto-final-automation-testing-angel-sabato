import logging
import os
import json
from datetime import datetime
from pathlib import Path

# Variable global para almacenar los handlers ya configurados
_LOG_HANDLERS_CONFIGURED = False
_LOG_FILE_PATH = None



class TestLogger:
    """Clase para gestionar el logging de tests con un único archivo de log"""
    
    def __init__(self, name, level=logging.INFO):
        global _LOG_HANDLERS_CONFIGURED, _LOG_FILE_PATH
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Configurar handlers solo una vez para todos los loggers
        if not _LOG_HANDLERS_CONFIGURED:
            self._setup_handlers()
            _LOG_HANDLERS_CONFIGURED = True
    
    def _setup_handlers(self):
        """Configura los handlers de logging una sola vez"""
        global _LOG_FILE_PATH
        
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Archivo único para todo
        _LOG_FILE_PATH = log_dir / "pytest_execution.log"
        
        # Formatter común
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File Handler - MODO APPEND para acumular logs
        file_handler = logging.FileHandler(
            _LOG_FILE_PATH,
            mode='a', 
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Agregar handlers al logger ROOT para que TODOS los loggers los hereden
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # Limpiar handlers existentes del root logger para evitar duplicados
        root_logger.handlers.clear()
        
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        # Log de inicio de sesión
        root_logger.info(f"SESIÓN DE TESTS INICIADA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        root_logger.info(f"Archivo de log: {_LOG_FILE_PATH}")
    
    def info(self, message):
        self.logger.info(message)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def test_start(self, test_name):
        self.logger.info(f"INICIO DE TEST: {test_name}")
    
    def test_end(self, test_name, status):
        self.logger.info(f"FIN DE TEST: {test_name} - Estado: {status}")
    
    def step(self, step_description):
        self.logger.info(f"PASO: {step_description}")
    
    def action(self, action_description):
        self.logger.debug(f"ACCIÓN: {action_description}")
    
    def assertion(self, assertion_description, result):
        status = "PASS" if result else "FAIL"
        self.logger.info(f"{status} ASERCIÓN: {assertion_description}")
    
    def api_request(self, method, url, status_code=None):
        msg = f"API {method}: {url}"
        if status_code:
            msg += f" - Status: {status_code}"
        self.logger.info(msg)
    
    def screenshot_taken(self, path):
        self.logger.warning(f"Screenshot capturado: {path}")


def get_logger(name):
    """Factory function para obtener un logger"""
    return TestLogger(name)


def get_log_file_path():
    """Retorna la ruta del archivo de log actual"""
    global _LOG_FILE_PATH
    return str(_LOG_FILE_PATH) if _LOG_FILE_PATH else "No inicializado"


class Config:
    """Clase para gestionar configuración del framework"""
    
    SAUCEDEMO_URL = "https://www.saucedemo.com/"
    JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"
    
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 10
    PAGE_LOAD_TIMEOUT = 30
    
    SCREENSHOTS_DIR = "screenshots"
    REPORTS_DIR = "reports"
    LOGS_DIR = "logs"
    DATA_DIR = "data"
    
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    CI_MODE = os.getenv('CI', 'false').lower() == 'true'
    
    SCREENSHOT_ON_FAILURE = True
    
    @classmethod
    def get(cls, key, default=None):
        return getattr(cls, key, default)
    
    @classmethod
    def is_headless(cls):
        return cls.HEADLESS or cls.CI_MODE
    
    @classmethod
    def is_ci(cls):
        return cls.CI_MODE


config = Config()


def capturar_pantalla(driver, test_name, paso=""):
    """Captura una screenshot con nombre descriptivo"""
    screenshot_dir = Path("screenshots")
    screenshot_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    clean_test_name = test_name.replace("::", "_").replace(" ", "_")
    clean_paso = f"_{paso}" if paso else ""
    
    filename = f"{clean_test_name}{clean_paso}_{timestamp}.png"
    filepath = screenshot_dir / filename
    
    driver.save_screenshot(str(filepath))
    
    return str(filepath)


def limpiar_navegador(driver, logger=None):
    """
    Limpia cookies y storage del navegador.
    Helper function para evitar duplicación de código.
    """
    try:
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        if logger:
            logger.debug("Navegador limpiado (cookies + storage)")
    except Exception as e:
        if logger:
            logger.debug(f"Error al limpiar navegador: {e}")


class DataLoader:
    """Clase para cargar datos de test desde JSON"""
    
    def __init__(self, data_file="data/test_data.json"):
        self.data_file = Path(data_file)
        self._data = self._load_data()
    
    def _load_data(self):
        if not self.data_file.exists():
            raise FileNotFoundError(f"Archivo de datos no encontrado: {self.data_file}")
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_usuarios_validos(self):
        return self._data.get("usuarios_validos", [])
    
    def get_usuarios_invalidos(self):
        return self._data.get("usuarios_invalidos", [])
    
    def get_checkout_info(self):
        return self._data.get("checkout_info", [])
    
    def get_productos(self):
        return self._data.get("productos", [])
    
    def get(self, key, default=None):
        return self._data.get(key, default)


data_loader = DataLoader()
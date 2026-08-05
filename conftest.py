import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    # Configuración de Chrome
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Descomentar si deseas ejecutar en segundo plano
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()

# Hook para capturar pantalla automáticamente si una prueba falla (requisito de reportes)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            os.makedirs("reports/screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = f"reports/screenshots/{item.name}_{timestamp}.png"
            driver.save_screenshot(file_path)
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL_BASE = "https://tu-aplicacion-web.com" # Cambia esto por la URL de tu app

# --- HU01: INICIO DE SESIÓN ---
def test_login_camino_feliz(driver):
    driver.get(f"{URL_BASE}/login")
    driver.find_element(By.ID, "username").send_keys("admin_valido")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "login-btn").click()
    
    # Validación (Camino feliz)
    time.sleep(2)
    assert "dashboard" in driver.current_url

def test_login_prueba_negativa(driver):
    driver.get(f"{URL_BASE}/login")
    driver.find_element(By.ID, "username").send_keys("usuario_falso")
    driver.find_element(By.ID, "password").send_keys("clave_incorrecta")
    driver.find_element(By.ID, "login-btn").click()
    
    # Validación de mensaje de error (Prueba Negativa)
    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert error_msg.is_displayed()


# --- HU02: CREAR REGISTRO (CREATE) ---
def test_crear_registro_limites(driver):
    # Simulación de prueba de límites: intentar ingresar un texto que excede el límite de caracteres permitidos
    driver.get(f"{URL_BASE}/dashboard/create")
    campo_nombre = driver.find_element(By.ID, "item-name")
    
    # Texto extremadamente largo (Prueba de límites)
    texto_largo = "A" * 300 
    campo_nombre.send_keys(texto_largo)
    driver.find_element(By.ID, "save-btn").click()
    
    # Validar que aparezca una validación de límite o que el sistema rechace el exceso
    error_limite = driver.find_element(By.ID, "char-limit-error")
    assert error_limite.is_displayed()


# --- HU03: LEER REGISTRO (READ) ---
def test_leer_registro_negativo(driver):
    driver.get(f"{URL_BASE}/dashboard/search")
    # Buscar un ID o elemento que no existe
    driver.find_element(By.ID, "search-input").send_keys("99999999")
    driver.find_element(By.ID, "search-btn").click()
    
    mensaje_vacio = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "no-results"))
    )
    assert "No se encontraron resultados" in mensaje_vacio.text


# --- HU04 & HU05: ACTUALIZAR Y ELIMINAR (UPDATE / DELETE) ---
def test_actualizar_y_eliminar_camino_feliz(driver):
    # Asumimos que ya estamos logueados o accedemos directamente al módulo CRUD
    driver.get(f"{URL_BASE}/dashboard")
    
    # UPDATE
    driver.find_element(By.CLASS_NAME, "edit-btn").click()
    input_edit = driver.find_element(By.ID, "item-name")
    input_edit.clear()
    input_edit.send_keys("Dato Actualizado Exitosamente")
    driver.find_element(By.ID, "update-btn").click()
    
    success_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-alert"))
    )
    assert success_msg.is_displayed()

    # DELETE
    driver.find_element(By.CLASS_NAME, "delete-btn").click()
    # Confirmar en el modal de alerta si lo hay
    confirm_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "confirm-delete-btn"))
    )
    confirm_btn.click()
    
    # Verificar que el registro desapareció
    time.sleep(2)
    assert True # Ajusta esta aserción según el comportamiento visual de tu app
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def test_flujo_completo_saucedemo():
    # --- CONFIGURACIÓN DEL NAVEGADOR ---
    options = Options()
    options.add_argument('--start-maximized') # Pantalla grande para ver bien
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5) # Espera implícita: espera hasta 5s a que los elementos aparezcan (ADIÓS time.sleep)

    try:
        # ==========================================
        # ACTIVIDAD 1: SCRIPT DE LOGIN
        # ==========================================
        driver.get('https://www.saucedemo.com')

        # 1. Ingresamos credenciales usando By.ID (La mejor práctica)
        driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        driver.find_element(By.ID, 'password').send_keys('secret_sauce')
        
        # 2. Hacemos clic en Login
        driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        # 3. Verificamos URL
        assert '/inventory.html' in driver.current_url, "Error: No redirigió al inventario"
        
        # Reto extra: Validación del título justo después de la redirección
        assert driver.title == 'Swag Labs', "Error: El título de la pestaña no coincide"
        print("\n✅ Actividad 1 OK: Login exitoso y redirección correcta.")

        # ==========================================
        # ACTIVIDAD 2: EXPLORAR EL INVENTARIO
        # ==========================================
        # 1. Validar título de la sección "Products"
        titulo_seccion = driver.find_element(By.CSS_SELECTOR, 'div.header_secondary_container .title').text
        assert titulo_seccion == 'Products', f"Error: Se esperaba 'Products' pero se obtuvo '{titulo_seccion}'"

        # 2. Confirmar que aparece al menos un producto
        productos = driver.find_elements(By.CLASS_NAME, 'inventory_item')
        assert len(productos) > 0, "Error: No hay productos en el inventario"

        # 3. Mostrar nombre y precio del primer producto en consola
        # Buscamos DENTRO del primer elemento de la lista (productos[0])
        primer_producto = productos[0]
        nombre = primer_producto.find_element(By.CLASS_NAME, 'inventory_item_name').text
        precio = primer_producto.find_element(By.CLASS_NAME, 'inventory_item_price').text
        print(f"✅ Actividad 2 OK: Inventario cargado. Primer producto -> Nombre: {nombre} | Precio: {precio}")

        # ==========================================
        # ACTIVIDAD 3: CARRITO RÁPIDO
        # ==========================================
        # 1. Hacer clic en "Add to cart" del primer producto
        # Buscamos el botón DENTRO de la tarjeta del primer producto
        primer_producto.find_element(By.TAG_NAME, 'button').click()

        # 2. Verificar que el contador del carrito (badge) muestre "1"
        badge_carrito = driver.find_element(By.CLASS_NAME, 'shopping_cart_badge').text
        assert badge_carrito == '1', f"Error: Se esperaba 1 ítem en el carrito, pero hay {badge_carrito}"

        # 3. Navegar al carrito
        driver.find_element(By.CLASS_NAME, 'shopping_cart_link').click()
        assert '/cart.html' in driver.current_url, "Error: No redirigió al carrito"

        # 4. Comprobar que el producto añadido está listado en el carrito
        items_en_carrito = driver.find_elements(By.CLASS_NAME, 'cart_item')
        assert len(items_en_carrito) == 1, "Error: El carrito no tiene el producto esperado"
        
        # Validamos que sea exactamente el mismo producto que clickeamos
        nombre_en_carrito = items_en_carrito[0].find_element(By.CLASS_NAME, 'inventory_item_name').text
        assert nombre_en_carrito == nombre, f"Error: El producto en el carrito ({nombre_en_carrito}) no coincide con el agregado ({nombre})"
        
        print(f"✅ Actividad 3 OK: Producto '{nombre_en_carrito}' agregado y verificado en el carrito.")
        print("\n🚀 ¡TEST OK! Flujo completo exitoso.")

    finally:
        # --- CIERRE LIMPIO ---
        # No importa si el test pasa o falla, el navegador SIEMPRE se cerrará
        driver.quit()

        ## Para ejecutarlo > python test_flujo_saucedemo.py // pytest test_flujo_saucedemo.py -v
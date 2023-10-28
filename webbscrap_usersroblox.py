import time
import selenium.common.exceptions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By


# Función para iniciar el driver
def driver_initiate():

    # Configuración del driver
    print("Configurando driver...")
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    # Retornar el objeto de driver
    driver_initiated = webdriver.Edge(options=chrome_options)
    print("Driver iniciado.")
    return driver_initiated


# Función para escribir resultados en .csv
def escribir_csv(usuarios):
    archivo_csv = open("usuarios_roblox.csv", "w")
    archivo_csv.write(f"ID,Username\n")

    # Escribir el usuario en una nueva línea del CSV
    for usuario in usuarios:
        archivo_csv.write(f"{usuario[0]},{usuario[1]}\n")


# Búsqueda de usuario
if __name__ == '__main__':

    lista_usuarios = []
    numero_usuario = None

    # Contenedores con la información a extraer
    contenedor_username = '/html/body/div[3]/main/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[2]'
    contenedor_alias = '/html/body/div[3]/main/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[1]/h1[1]'

    # Iniciar driver
    print("Iniciando driver...")
    driver = driver_initiate()

    while True:

        # Perfil encontrado/existe
        try:

            # ID de usuario donde iniciar el web scrapping
            if numero_usuario is None:
                numero_usuario = int(input("\nIngrese la ID de usuario donde desea iniciar el Web Scrapping: "))

            # Ya existe un valor en la variable de numero_usuario
            else:
                pass

            # Ingresar al perfil
            url_usuario = f'https://www.roblox.com/users/{numero_usuario}/profile'
            driver.get(url_usuario)
            print(f"Ingresando al perfil ID {numero_usuario}")
            time.sleep(2)

            # Ubicar elementos con la información a buscar
            elemento_nombre_usuario = driver.find_element(By.XPATH, contenedor_username)
            elemento_alias_usuario = driver.find_element(By.XPATH, contenedor_alias)

            # Obtener el atributo
            nombre_usuario_raw = elemento_nombre_usuario.get_attribute('innerHTML')
            alias_usuario_raw = elemento_alias_usuario.get_attribute('innerHTML')

            # Convertir a str el atributo
            nombre_usuario = BeautifulSoup(nombre_usuario_raw, 'html.parser').text.strip()
            alias_usuario = BeautifulSoup(alias_usuario_raw, 'html.parser').text.strip()

            # Añadir usuario a lista
            lista_usuarios.append([numero_usuario, nombre_usuario, alias_usuario])

            # Siguiente usuario
            numero_usuario += 1
            print(lista_usuarios)

        # Valor inválido
        except ValueError as e:
            print("Ingrese un valor válido.")

        # Perfil no encontrado/inexistente
        except selenium.common.exceptions.NoSuchElementException:
            print(f"El usuario bajo ID {numero_usuario} no existe, reintentando...")
            time.sleep(0.95)
            numero_usuario += 1

        # Interrumpir la ejecución del código
        except KeyboardInterrupt:
            escribir_csv(lista_usuarios)

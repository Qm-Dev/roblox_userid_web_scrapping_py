import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class WebDriverManager:
    """Gestionar la inicialización del driver."""

    @staticmethod
    def initiate_driver():
        edge_options = Options()
        edge_options.add_argument('--no-sandbox')
        edge_options.add_argument('--disable-dev-shm-usage')
        edge_options.add_argument('--disable-gpu')
        edge_options.add_argument('--headless')
        return webdriver.Edge(options=edge_options)


class UserScraper:
    """
    Extrae datos de perfiles de usuarios.
    Por ahora, los datos extraídos son:
    * Nombre de usuario y alias
    * Fecha de ingreso
    * Cantidad de amigos y seguidores
    TODO: Extraer experiencias favoritas e insignias de Roblox específicas (Administrator y Builders Club).
    """

    def __init__(self, driver):
        self.driver = driver
        self.container_username = '//*[@id="profile-header-container"]/div/div/div/div[2]/div[1]/div[2]'
        self.container_alias = '//*[@id="profile-header-container"]/div/div/div/div[2]/div[1]/div[1]/h1[1]'
        self.container_join_date = '//*[@id="profile-statistics-container"]/div/div[2]/ul/li[1]/p[2]'
        self.container_friends = '//*[@id="profile-header-container"]/div/div/div/div[2]/div[2]/ul[1]/li[1]/a/span'
        self.container_followers = '//*[@id="profile-header-container"]/div/div/div/div[2]/div[2]/ul[1]/li[2]/a/span'

    def scrape_user(self, user_id):
        user_url = f'https://www.roblox.com/users/{user_id}/profile'
        self.driver.get(user_url)
        print(f"\nAccediendo al perfil con ID {user_id}")

        try:
            element_username = self.driver.find_element(By.XPATH, self.container_username)
            element_alias = self.driver.find_element(By.XPATH, self.container_alias)
            element_friends = self.driver.find_element(By.XPATH, self.container_friends)
            element_followers = self.driver.find_element(By.XPATH, self.container_followers)
            element_join_date = self.driver.find_element(By.XPATH, self.container_join_date)
            self.driver.execute_script("arguments[0].scrollIntoView();", element_join_date)
            time.sleep(1)

            user_name = BeautifulSoup(element_username.get_attribute('innerHTML'), 'html.parser').text.strip()
            user_alias = BeautifulSoup(element_alias.get_attribute('innerHTML'), 'html.parser').text.strip()
            user_friends = BeautifulSoup(element_friends.get_attribute('innerHTML'), 'html.parser').text.strip()
            user_followers = element_followers.get_attribute("title")
            user_join_date = BeautifulSoup(element_join_date.get_attribute('innerHTML'), 'html.parser').text.strip()

            print(f"Scraping finalizado.")

            return [user_id, user_name, user_alias, int(user_friends), int(user_followers), user_join_date]
        
        # Excepción temporal para perfiles inexistentes
        except selenium.common.exceptions.NoSuchElementException:
            print(f"Perfil con ID {user_id} no encontrado. Saltando...")
            time.sleep(1.5)
            return None


class ExperienceScraper:
    """TODO: Implementar el scraper para los juegos/experiencias."""

class GroupScraper:
    """TODO: Implementar el scraper para los grupos. Una vez implementado, buscar forma de juntar este con el de usuario para obtener más información de este."""

class CSVWriter:
    """
    Manejar la escritura en un archivo CSV.
    Cada línea corresponde a la información extraída de un usuario por parte del scraper.
    """

    @staticmethod
    def write_csv(users, filename="rus.csv"):
        with open(filename, "w") as archivo_csv:
            archivo_csv.write("ID,Username,Alias,Friends,Followers,Join Date\n")
            for user in users:
                archivo_csv.write(f"{user[0]},{user[1]},{user[2]},{user[3]}, {user[4]}, {user[5]}\n")


class ScraperManager:
    """Administra el scraping."""

    def __init__(self):
        self.driver = WebDriverManager.initiate_driver()
        self.scraper = UserScraper(self.driver)
        self.user_list = []

    def run(self):
        try:
            user_id = int(input("\nIngrese el ID del usuario donde comenzará el scraping: "))
            jump = int(input("Ingrese el parámetro de salto (min. 1): "))
            list_size = int(input("Ingrese cuántos usuarios desea guardar en el archivo CSV: "))
            jump = max(jump, 1)

            while len(self.user_list) < list_size:
                user_data = self.scraper.scrape_user(user_id)
                if user_data:
                    self.user_list.append(user_data)
                user_id += jump
            CSVWriter.write_csv(self.user_list)

        except ValueError:
            print("Por favor, ingrese valores válidos.")
        finally:
            self.driver.quit()


if __name__ == "__main__":
    ScraperManager().run()

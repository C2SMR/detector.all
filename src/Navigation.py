import time

import undetected_chromedriver as uc


class Navigation:
    def __init__(self):
        self.option = uc.ChromeOptions()
        self.driver = uc.Chrome(options=self.option)
        self.accept_cookie()

    def accept_cookie(self):
        self.driver.get("https://www.youtube.com/")
        self.driver.execute_script(
            'document.cookie = "SOCS=CAESEwgDEgk1NzY'
            '3NTAwMzcaAmZyIAEaBgiAwfapBg"')
        self.driver.execute_script('document.location.reload()')

    def full_screen(self):
        try:
            time.sleep(10)
            self.driver.execute_script(
                "document.querySelector('#movie_player').playVideo()"
            )
            time.sleep(4)
            print("full screen")
        except Exception:
            print("Error during fullscreen")

    def screen_shot(self, name: str) -> None:
        self.driver.save_screenshot(f'pictures/{name}.png')

    def run(self, name: str, url: str) -> None:
        self.driver.execute_script(f"document.location.href='{url}'")
        self.full_screen()
        self.screen_shot(name)

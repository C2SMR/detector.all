from roboflow import Roboflow
import time
import sys

from config import PROJECT_WORKSPACE_ROBOFLOW, \
    API_KEY_ROBOFLOW, FOLDER_PICTURE
from detector import Detector
from api import API
from alert import Alert
from Navigation import Navigation
from city import CITY


class Main:

    def __init__(self):
        self.url = None
        self.longitude = None
        self.detector = None
        self.alert = None
        self.actual_data_predict_picture: object = None
        self.cv2 = None
        self.latitude = None
        self.longitude = None
        self.city = None
        self.api = None
        self.one_hour: int = 0
        self.time_for_one_hour: float = time.time()
        self.rf = Roboflow(api_key=API_KEY_ROBOFLOW)
        self.project = self.rf.workspace().project(PROJECT_WORKSPACE_ROBOFLOW)
        self.model = self.project.version(int(sys.argv[1])).model
        self.api_key: str = sys.argv[2]
        self.sensors: Navigation = Navigation()
        self.run()

    def verif_time_one_hour(self) -> bool:
        if time.time() - self.time_for_one_hour > self.one_hour:
            self.one_hour = 60 * 60
            self.time_for_one_hour = time.time()
            return True
        return False

    def predict_picture(self):
        self.actual_data_predict_picture = self.model.predict(FOLDER_PICTURE +
                                                              self.city
                                                              + '.png',
                                                              confidence=40,
                                                              overlap=30) \
            .json()
        self.model.predict(FOLDER_PICTURE + self.city + '.png',
                           confidence=40,
                           overlap=30).save(FOLDER_PICTURE +
                                            self.city + '.png')

    def set_value_for_city(self, index):
        self.city: str = CITY[index][0]
        self.latitude: float = CITY[index][1]
        self.longitude: float = CITY[index][2]
        self.url: str = CITY[index][3]

    def run(self):
        while True:

            for i in range(len(CITY)):
                self.set_value_for_city(i)

                self.api: API = API(self.city, self.api_key,
                                    self.latitude, self.longitude)
                self.sensors.run(self.city, self.url)
                self.predict_picture()
                self.detector: Detector = Detector(
                    self.actual_data_predict_picture)

                self.api.set_number_people(self.detector.get_nb_beach(),
                                           self.detector.get_nb_sea())
                self.alert: Alert = Alert(self.latitude, self.longitude,
                                          self.actual_data_predict_picture,
                                          self.api)
                self.alert.run()

                if self.verif_time_one_hour():
                    for j in range(len(CITY)):
                        self.set_value_for_city(j)

                        self.api: API = API(self.city, self.api_key,
                                            self.latitude, self.longitude)
                        self.api.add_data_city(self.detector.get_nb_beach(),
                                               self.detector.get_nb_sea(),
                                               self.detector.get_visibility()),
                # self.api.add_picture_alert_or_moment(
                #    FOLDER_PICTURE + self.city + '.png')


if __name__ == '__main__':
    Main()

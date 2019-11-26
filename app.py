import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import firestore
from time import sleep
from math import sqrt

cred = credentials.Certificate('./areaAlert.json')
default_app = firebase_admin.initialize_app(cred)
DEFAULT_RADIUS = 0.005
ONE_KM_APPROXIMATE = 0.008162097402023085
#
# tokens = [  # 'feZjFPoN2x4:APA91bEekCxZEF1jOzyzWuZ5WtDrm4bNL9wf4kxhSMrH-LZ1enEOIu0tVLW5I7cilGIpi0qQEh4nPUf50-_khDbJVSFYwVMvH5cE1vhy2T9OSSxgu9Zr8gGqI-DKeV-MYJh-Uclv4cW3',
#     # 'f4zqyOqSwaU:APA91bE6fJ15W8uiQn1dMIkrNsBIZNDQwg9oFtHB7Xl0p2MCUVAMEAPJwB3F6gOUEIoEiadFOTB0Tg1Mgybgnz6eGAXDA35PGblRoT8K77OnLGPy2DsNZApbEyPqEQXW8zUAkLdwVNW3',
#     # 'cWd3unXIEss:APA91bHfNim0_OvZKy-o_8qMPPpN8Mgle59antarfd1rc8c7KZOiGiSJZArhpVvCtIVqekBjE0SCiFlc4d4N4qdkA8Utofz9ZvQEcReBxyBRyNPpZLq7heXVudKtrC9DS906kzrBF7hI',
#     # 'c7HcaJhM3Sg:APA91bHQoSV6CZLJKT9XmkQY-GxTC_DtJpQWMlKVVFYPVV0dltGuHef073bPUMrhsDpU4oS8HWI8wrUWc5QjoOcQluaIbK4dCXJ_IZCKQtbdcDe4I2t2drzPPpJI033lOSa2A6dtaGjh',
#     'c34TtdsfCVI:APA91bEp9frwzdKh-vQSl7zZ-PHPaNpR1MxO9wsDuaJoOEfKr1jm4RB5J8Sr4BmUlq1nAiHbDZgTMmSYdZZUSRWYY65V0jXBqWTvCdo2_6Ibiu0h6reIEcdGCXT8BaLEYbXNWMqspGU0',
#     'c34TtdsfCVI:APA91bEp9frwzdKh-vQSl7zZ-PHPaNpR1MxO9wsDuaJoOEfKr1jm4RB5J8Sr4BmUlq1nAiHbDZgTMmSYdZZUSRWYY65V0jXBqWTvCdo2_6Ibiu0h6reIEcdGCXT8BaLEYbXNWMqspGU0',
#     'c2KCi7uJdMI:APA91bFbZYAj1klVKYW9qq_IQgiaUqaxBIguOcOSjUGT9mLDiLcBDcILWQsCvzc-DRxoOrOobd24SOXiH7MD0wA_H1nWRcqET7fmipi_GRnH_lyaAWppQT-jixgoqMFpOQWTn8jRqEGQ',
#     'er4ScJyRrls:APA91bFgTvOL4LjANNvFBdmZPukEmTy1mu_WQEWp4I1h-kV8RL45ShDDb3FCaJdzSQ7cnNuwfmrvJEWiGhUQz-6xI8ubHYVvt7LXWV_5jPO2uaNBHxUTcDBpxgqQihaPj3gY3OkYE6VQ',
#     'cNwV2c6NPlE:APA91bGLPDtLF1Pe59jgFB2MWGyRVEx7IB-HBYf4SgPAYxuHVjruhXGeBuTAc77BPX69aJJKTfm5KokNchfByunCdOUVwh4kiQ2c6YFOYLhThTXgjb_3lJx2nZr4K25VikdmcV4MXCLt',
#     'ffQKzbpiyEE:APA91bH18u2aJXG7VQwRgMplw9XuscWsyUfBpRrluiQ2SRZwMw0q0qfK2zoYS425jxyIvD5UCvFRwp8ypI2LqyYtu8rTQE-02BhxEBkHfvxed32t_2qV1eyfnx-Gwrb7-tXvrUm4QXYV',
#
# ]
#
# for token in tokens:
#     try:
#         message = messaging.Message(
#             data={
#                 'title': "Flash Flood Warning",
#                 'body': 'Flash floods expected near your area, click to see what you can do',
#                 'priority': '5',
#                 'tag': 'Test'
#             },
#             token=token
#         )
#
#         response = messaging.send(message)
#         print('Successfully sent message:', response)
#     except Exception as e:
#         pass

db = firestore.client()


def is_user_in_report(user_doc, report_doc):
    report_data = report_doc.to_dict()
    user_data = user_doc.to_dict()

    try:  # fix db inconsistencies
        epicenter_lat, epicenter_lon = report_data["lat"], report_data["lon"]
    except Exception:
        epicenter_lat, epicenter_lon = report_data["location"].latitude, report_data["location"].longitude
    user_lat, user_lon = user_data["currentLocation"].latitude, user_data["currentLocation"].longitude

    # strength
    radius = report_data["radius"] if "radius" in report_data.keys() else ONE_KM_APPROXIMATE

    def distance_between(p1, p2):
        print(sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2), "--------disp----------",
              (epicenter_lat, epicenter_lon), (user_lat, user_lon), user_data["name"]) if sqrt(
            (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) <= radius else print(end="")
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    return True if distance_between(p1=(epicenter_lat, epicenter_lon), p2=(user_lat, user_lon)) <= radius else False


def get_in_reports(user_doc):
    # change to reports.where()
    # in_reports = [report for report in db.collection('verified_reports').stream() \
    #               if is_user_in_report(user_doc, report)]
    in_reports = [report for report in db.collection('reports').where("verified", u"==", True).stream() \
                  if is_user_in_report(user_doc, report)]

    return in_reports


def send_notification(to, about):
    print(to.to_dict(), "==================", about.to_dict())


def users_listener(collection_snapshot, changed_users_docs, read_time):  # initial call gets everything, duh.
    print("----CHANGE DETECTEDD -------")
    for changed_user_doc in changed_users_docs:  # changes has the doc snapshots of the docs that has changed
        try:
            # print(type(change), "----------------- Changeeeee------------- ", type(change.document), change.document.to_dict()["currentLocation"].latitude, change.document.to_dict()["currentLocation"].longitude)
            in_reports = get_in_reports(changed_user_doc.document)

            if len(in_reports) is not 0:
                for report in in_reports:
                    send_notification(to=changed_user_doc.document, about=report)
            else:
                continue
        except Exception as e:
            pass


db.collection('users').on_snapshot(users_listener)

while True:
    # to keep program running
    sleep(1000)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import firestore
from time import sleep

cred = credentials.Certificate('./areaAlert.json')
default_app = firebase_admin.initialize_app(cred)
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


def users_listener(collection_snapshot, changes, read_time):
    for change in changes:  # changes has the doc snapshots of the docs that has changed
        print(change.document, "----------------- Changeeeee------------- \n\n")
    for document in collection_snapshot:  # collection snapshot has all the docs
        print(document.id, "---------------DOC ID\n", document.to_dict(), "DOC ---------------------- \n")


db.collection('users').on_snapshot(users_listener)

while True:
    # to keep program running
    sleep(1000)

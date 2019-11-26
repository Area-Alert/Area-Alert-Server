import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import firestore
from time import sleep
from math import sqrt
import threading

cred = credentials.Certificate('./areaAlert.json')
default_app = firebase_admin.initialize_app(cred)
DEFAULT_RADIUS = 0.005
ONE_KM_APPROXIMATE = 0.008162097402023085
DEFAULT_PRIORITY = '3'

db = firestore.client()


def is_user_in_report(user_doc, report_doc):
    report_data = report_doc.to_dict()
    user_data = user_doc.to_dict()

    try:  # fix db inconsistencies
        epicenter_lat, epicenter_lon = report_data["location"].latitude, report_data["location"].longitude
    except Exception:
        epicenter_lat, epicenter_lon = report_data["lat"], report_data["lon"]
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
    to = to.to_dict()
    about = about.to_dict()
    
    notification = messaging.Message(
        data={
            'title': str(about["report_type"]),
            'body': f'Report about {about["report_type"]} nearby',
            'priority': str(about["priority"]) if "priority" in about.keys() else DEFAULT_PRIORITY,
            'tag': str(about["tag"]) if "tag" in about.keys() else 'test'
        },
        token=to["token"]
    )

    response = messaging.send(notification)
    print("Sent Notification", response)


def handle_changed_location(changed_user_doc):
    try:
        # print(type(change), "----------------- Changeeeee------------- ", type(change.document), change.document.to_dict()["currentLocation"].latitude, change.document.to_dict()["currentLocation"].longitude)
        in_reports = get_in_reports(changed_user_doc.document)

        if len(in_reports) is not 0:
            for report in in_reports:
                threading.Thread(target=send_notification(to=changed_user_doc.document, about=report)).start()
                # send_notification(to=changed_user_doc.document, about=report)
    except Exception as e:
        print("user listener", e)


def users_listener(collection_snapshot, changed_users_docs, read_time):  # initial call gets everything, duh.
    print("----CHANGE DETECTEDD -------")
    for changed_user_doc in changed_users_docs:  # changes has the doc snapshots of the docs that has changed
        threading.Thread(target=handle_changed_location(changed_user_doc)).start()


db.collection('users').on_snapshot(users_listener)

while True:
    # to keep program running
    sleep(1000)

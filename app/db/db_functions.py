from flask import abort

from app.db.db_connection import engine
from app import app, cache


def get_results(result, label="", type=None):
    ret = {}
    for i, row in enumerate(result):
        row_dict = {}
        for item in row:
            if isinstance(item, str):
                item = item.split(":", 1)
            else:
                # blob
                item = item.read()
            if len(item) > 1:
                row_dict[item[0]] = item[1]
            else:
                # if the result doesn't have key/value pairs
                # use a custom label
                row_dict[label] = item[0]

        ret[int(i)] = row_dict
    return ret


def get_splits(line):
    rows = []

    for item in line.split('|'):
        rows.append(item)

    return rows


def portal_profile(username):
    try:
        conn = engine.raw_connection()
        call_cursor = conn.cursor()
        result_cursor = conn.cursor()

        call_cursor.callproc('bth_portal_channel_api.bu_profile', (username, result_cursor))
        r = result_cursor.fetchall()
        conn.close()
        return get_results(r)
    except:
        if conn:
            conn.close()
        return abort(503)


def directory_search():
    if cache.get('directory_search') is None:
        directory_data = get_directory_data()
        # cache for 24 hours, as every 4 we clear it with reset_directory_data() via cron
        cache.set(key='directory_search', value=directory_data, timeout=86400)
        return directory_data
    else:
        return cache.get('directory_search')


def reset_directory_data():
    cache.set('directory_search', get_directory_data())


def get_directory_data():
    try:
        conn = engine.raw_connection()
        call_cursor = conn.cursor()
        result_cursor = conn.cursor()
        data = []
        results = []

        call_cursor.callproc('bth_websrv_api.web_directory', (result_cursor,))
        data = get_results(result_cursor.fetchall())
        # todo: change data[item] to be able to use item? Use .items() or something
        for item in data:

            last_name = data[item]['last_name']
            first_name = data[item]['pref_first_name']  # we have 'first_name' available to us, but pref is desired.
            housing = data[item]['housing_building_room'].encode('utf-8')
            # replacing blackhole emails with regular emails
            email = data[item]['email'].replace('=bethel.edu@blackhole.bethel.edu', '@bethel.edu')
            username = data[item]['username']
            bu_po = data[item]['bu_po']
            bu_id = data[item]['bu_id']
            phone = data[item]['home_phone']
            image_path = data[item]['photo']
            udc = data[item]['udc_id']
            addr_city = data[item]['addr_city']
            addr_state = data[item]['addr_state']
            addr_street1 = data[item]['addr_street1']
            addr_street2 = data[item]['addr_street2']
            addr_zip = data[item]['addr_zip']
            phone_ext = data[item]['phone_ext'].split('*', 1)[0]  # this split is to fix numbers like "123.123.123*1234"
            office_number = data[item]['office_building_room']
            dorm = data[item]['housing_building_room']
            class_standing = data[item]['stu_class']

            # the next ones potentially have multiple, split by a '|'

            # ensure the order for those who have multiple roles.
            # this snippet could be moved into derek's script on IS's side.
            bu_role_list = get_splits(data[item]['bu_role'])
            bu_role_sort_key = {
                "Staff":            1,
                "Faculty":          2,
                "Sponsored Staff":  3,
                "Student":          4
            }
            bu_role_data = sorted(bu_role_list, key=lambda x: bu_role_sort_key[x])
            bu_role = bu_role_data
            department = get_splits(data[item]['dept'])
            major = get_splits(data[item]['stu_majr'])
            minor = get_splits(data[item]['stu_minr'])
            college = get_splits(data[item]['stu_coll'])
            title = get_splits(data[item]['title'])

            results.append({'last_name': last_name,
                            'first_name': first_name,
                            'housing': housing,
                            'email': email,
                            'username': username,
                            'po': bu_po,
                            'id': bu_id,
                            'phone': phone,
                            'image_path': image_path,
                            'udc': udc,
                            'addr_city': addr_city,
                            'addr_state': addr_state,
                            'addr_street1': addr_street1,
                            'addr_street2': addr_street2,
                            'role': bu_role,
                            'department': department,
                            'major': major,
                            'minor': minor,
                            'college': college,
                            'title': title,
                            'addr_zip': addr_zip,
                            'phone_ext': phone_ext,
                            'office_number': office_number,
                            'dorm': dorm,
                            'class_standing': class_standing
                            })
        conn.close()
        return results
    except:
        if conn:
            conn.close()
        return abort(503)


# 4 hour cache = 14400
@cache.memoize(timeout=14400)
def departments():
    try:
        conn = engine.raw_connection()
        call_cursor = conn.cursor()
        result_cursor = conn.cursor()
        results = []

        call_cursor.callproc('bth_websrv_api.web_directory_dept', (result_cursor,))
        data = get_results(result_cursor.fetchall())

        for item in data:
            results.append(data[item]['dept'])

        conn.close()
        return results
    except:
        if conn:
            conn.close()
        return abort(503)

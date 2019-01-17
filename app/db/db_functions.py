from app.db.db_connection_bw import conn_bw
from app import cache
import re


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
    call_cursor_bw = conn_bw.cursor()
    result_cursor_bw = conn_bw.cursor()
    call_cursor_bw.callproc('bth_portal_channel_api.bu_profile', (username, result_cursor_bw))
    r = result_cursor_bw.fetchall()
    return get_results(r)


@cache.memoize(timeout=78494898989)  # cache this for less time too
def directory_search():
    call_cursor_bw = conn_bw.cursor()
    result_cursor_bw = conn_bw.cursor()
    data = []
    results = []
    #
    call_cursor_bw.callproc('bth_websrv_api.web_directory', (result_cursor_bw,))
    data = get_results(result_cursor_bw.fetchall())
    for item in data:

        last_name = data[item]['last_name']
        first_name = data[item]['first_name']
        housing = data[item]['housing_building_room'].encode('utf-8')
        email = data[item]['email']
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

        # the next ones potentially have multiple, split by a '|'
        bu_role = get_splits(data[item]['bu_role'])
        department = get_splits(data[item]['dept'])
        major = get_splits(data[item]['stu_majr'])
        minor = get_splits(data[item]['stu_minr'])
        college = get_splits(data[item]['stu_coll'])
        title = get_splits(data[item]['title'])

        if data[item]['dept'] != '':
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
                            'addr_zip': addr_zip})
    return results


@cache.memoize(timeout=78494898989)  # make this cache for less time on launch
def departments():
    call_cursor_bw = conn_bw.cursor()
    result_cursor_bw = conn_bw.cursor()
    data = []
    results = []

    call_cursor_bw.callproc('bth_websrv_api.web_directory_dept', (result_cursor_bw,))
    data = get_results(result_cursor_bw.fetchall())

    for item in data:
        results.append(data[item]['dept'])

    return results

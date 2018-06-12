from app.db.db_connection_bw import conn_bw
# from app import cache


def get_results(result, label="", type=None):
    ret = {}
    for i, row in enumerate(result):
        row_dict = {}
        for item in row:
            if isinstance(item, str) or isinstance(item, unicode):
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


def portal_profile(username):
    call_cursor_bw = conn_bw.cursor()
    result_cursor_bw = conn_bw.cursor()
    call_cursor_bw.callproc('bth_portal_channel_api.bu_profile', (username, result_cursor_bw))
    r = result_cursor_bw.fetchall()
    return get_results(r)


# @cache.memoize(timeout=78494898989)
def directory_search():
    call_cursor_bw = conn_bw.cursor()
    result_cursor_bw = conn_bw.cursor()
    data = []
    results = []

    call_cursor_bw.callproc('bth_websrv_api.web_directory', (result_cursor_bw,))
    data = get_results(result_cursor_bw.fetchall())
    for item in data:
        last_name = data[item]['last_name']
        first_name = data[item]['first_name']
        image_path = data[item]['image_path']
        po = data[item]['po']
        role = data[item]['role_category']
        results.append({'last_name': last_name,
                        'first_name': first_name,
                        'image_path': image_path,
                        'po': po,
                        'role': role})
    return results

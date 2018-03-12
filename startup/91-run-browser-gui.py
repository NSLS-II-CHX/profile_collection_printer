t = "{start[plan_name]} ['{start[uid]:.6}'] (scan num: {start[scan_id]})"

def f(header, factory):
    plan_name = header['start']['plan_name']
    if plan_name in ('dscan', 'relative_scan'):
        motor, = header['start']['motors']
        data_keys = header['descriptors'][0]['data_keys']
        for key in data_keys:
            if key.endswith('stats1_total'):
                break
        fig = factory("stats1_total vs {}".format(motor))
        ax = fig.gca()
        lp = LivePlot(key, motor, ax=ax)
        db.process(header, lp)


def browse():
    return BrowserWindow(db, f, t)

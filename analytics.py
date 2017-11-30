from main import app, PageData
from flask import jsonify, render_template, session
from views import login_required
import dbManager as dbm


@app.route('/analytics/avg_amt_per_transaction', methods=['GET'])
@login_required
def avg_amt():
    curs, conn = dbm.DBconnect()

    query = "SELECT user_id,amount from transaction where user_id = {}".format(session['id'])

    curs.execute(query)
    res = curs.fetchall()
    sum1 = 0
    count = 0
    for i in res:
        sum1 += i['amount']
        count += 1
    if (count == 0):
        avg = 0
    else:
        avg = sum1 / count;

    average = {'avg': avg}
    dbm.DBclose(curs, conn)
    return jsonify(average)


@app.route('/analytics/mean_ex_month', methods=['GET'])
@login_required
def mean_ex_month():
    curs, conn = dbm.DBconnect()

    query = "SELECT monthname(timestamp) as 'month' ,SUM(amount) as 'sum', COUNT(amount) as 'count' FROM transaction where user_id = {} GROUP BY monthname(timestamp)".format(
        session['id'])

    curs.execute(query)

    average_expenditures = dict()
    res = curs.fetchall()
    for i in res:
        average_expenditures[i['month']] = i['sum'] / i['count']
    dbm.DBclose(curs, conn)
    return jsonify(average_expenditures)


@app.route('/analytics/mean_ex_category', methods=['GET'])
@login_required
def mean_ex_category():
    curs, conn = dbm.DBconnect()

    query = "SELECT category ,SUM(amount) as 'sum', COUNT(amount) as 'count' FROM transaction where user_id = {} GROUP BY category".format(
        session['id']    )

    curs.execute(query)
    res = curs.fetchall()
    average_expenditures_cat = dict()

    for i in res:
        average_expenditures_cat[i['category']] = i['sum'] / i['count']
    dbm.DBclose(curs, conn)
    return jsonify(average_expenditures_cat)


@app.route('/analytics/expenditures', methods=['GET'])
@login_required
def expenditures():
    curs, conn = dbm.DBconnect()

    query = "SELECT monthname(timestamp) ,SUM(amount) FROM transaction where user_id = {} GROUP BY monthname(timestamp)".format(
        session['id'])

    curs.execute(query)

    month = []
    exps = []

    for i in curs:
        month.append(i[0])
        exps.append(i[1])

    trace1 = {'x': month, 'y': exps, 'type': 'scatter'}
    dbm.DBclose(curs, conn)
    return jsonify(trace1)


@app.route('/analytics/pie_chart', methods=['GET'])
@login_required
def pie_chart():
    curs, conn = dbm.DBconnect()

    query = "SELECT category ,SUM(amount) FROM transaction where user_id = {} GROUP BY category".format(session['id'])

    curs.execute(query)

    category = []
    exps = []

    for i in curs:
        category.append(i[0])
        exps.append(i[1])

    trace1 = {'values': exps, 'labels': category, 'type': 'pie'}
    dbm.DBclose(curs, conn)
    return jsonify(trace1)


@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html', page=PageData('analytics', 'Analytics'))

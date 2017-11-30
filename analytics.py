from main import app, PageData
from flask import jsonify, render_template, session
from views import login_required
import dbManager as dbm


@app.route('/analytics/avg_amt_per_transaction', defaults={'income': None}, methods=['GET'])
@app.route('/analytics/avg_amt_per_transaction/<int:income>', methods=['GET'])
@login_required
def avg_amt(income):
    curs, conn = dbm.DBconnect()
    if income == 1:
        income = 'true'
    elif income == 2:
        income = 'true or income= false'
    else:
        income = 'false'
    query = "SELECT user_id,amount from transaction where user_id = {} and income=false".format(session['id'])

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

    average = {'avg': float(avg)}
    dbm.DBclose(curs, conn)
    return jsonify(average)


@app.route('/analytics/mean_ex_month', defaults={'income': None}, methods=['GET'])
@app.route('/analytics/mean_ex_month/<int:income>', methods=['GET'])
@login_required
def mean_ex_month(income):
    curs, conn = dbm.DBconnect()
    if income == 1:
        income = 'true'
    elif income == 2:
        income = 'true or income= false'
    else:
        income = 'false'
    query = "SELECT monthname(timestamp) as 'month' ,SUM(amount) as 'sum', COUNT(amount) as 'count' FROM transaction where user_id = {} and (income={}) GROUP BY monthname(timestamp)".format(
        session['id'], income)

    curs.execute(query)

    average_expenditures = dict()
    res = curs.fetchall()
    for i in res:
        average_expenditures[i['month']] = float(i['sum'] / i['count'])
    dbm.DBclose(curs, conn)
    return jsonify(average_expenditures)


@app.route('/analytics/mean_ex_category', defaults={'income': None}, methods=['GET'])
@app.route('/analytics/mean_ex_category/<int:income>', methods=['GET'])
@login_required
def mean_ex_category(income):
    curs, conn = dbm.DBconnect()
    if income == 1:
        income = 'true'
    elif income == 2:
        income = 'true or income= false'
    else:
        income = 'false'
    query = "SELECT category ,SUM(amount) as 'sum', COUNT(amount) as 'count' FROM transaction where user_id = {} and (income={}) GROUP BY category".format(
        session['id'], income)

    curs.execute(query)
    res = curs.fetchall()
    average_expenditures_cat = dict()

    for i in res:
        average_expenditures_cat[i['category']] = float(i['sum'] / i['count'])
    dbm.DBclose(curs, conn)
    return jsonify(average_expenditures_cat)


@app.route('/analytics/expenditures/', defaults={'income': None}, methods=['GET'])
@app.route('/analytics/expenditures/<int:income>', methods=['GET'])
@login_required
def expenditures(income):
    curs, conn = dbm.DBconnect()
    if income == 1:
        income = 'true'
    elif income == 2:
        income = 'true or income= false'
    else:
        income = 'false'
    query = "SELECT monthname(timestamp) as 'month' ,SUM(amount) as 'sum' FROM transaction where user_id = {} and (income = {}) GROUP BY monthname(timestamp)".format(
        session['id'], income)

    curs.execute(query)

    month = []
    exps = []

    for i in curs:
        month.append(i['month'])
        exps.append(float(i['sum']))

    trace1 = {'x': month, 'y': exps, 'type': 'scatter'}
    dbm.DBclose(curs, conn)
    return jsonify(trace1)


@app.route('/analytics/pie_chart/', defaults={'income': None}, methods=['GET'])
@app.route('/analytics/pie_chart/<int:income>', methods=['GET'])
@login_required
def pie_chart(income):
    curs, conn = dbm.DBconnect()
    if income == 1:
        income = 'true'
    elif income == 2:
        income = 'true or income= false'
    else:
        income = 'false'
    query = "SELECT category ,SUM(amount)as 'sum' FROM transaction where user_id = {} and (income={}) GROUP BY category".format(
        session['id'], income)

    curs.execute(query)

    category = []
    exps = []

    for i in curs:
        category.append(i['category'])
        exps.append(float(i['sum']))

    trace1 = {'values': exps, 'labels': category, 'type': 'pie'}
    dbm.DBclose(curs, conn)
    return jsonify(trace1)


@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html', page=PageData('analytics', 'Analytics'))

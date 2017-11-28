from main import app, PageData
from flask import render_template, request, redirect, url_for, session, flash
import actions as act
from functools import wraps

@app.route('/taxes')
def tax():
    return render_template('taxes.html',page=PageData('taxes', 'Taxes'))


@app.route('/taxCalculator',methods=["POST"])
def taxCalculator():
    
    income=int(request.form.get('income'))
    age=int(request.form.get('age'))
    
    shortStockEq=int(request.form.get('shortStockEq'))
    shortDebtMF=int(request.form.get('shortDebtMF'))
    longDebtMF=int(request.form.get('longDebtMF'))
    businessIncome=int(request.form.get('businessIncome'))
    deductableExpenses=int(request.form.get('deductableExpenses'))
    otherSourcesTotal=int(request.form.get('otherSourcesTotal'))
    rentReceived=int(request.form.get('rentReceived'))
    municipalTaxesPaid=int(request.form.get('municipalTaxesPaid'))
    homeLoanInterestPaid=int(request.form.get('homeLoanInterestPaid'))
    isSelfOccupied=int(request.form.get('isSelfOccupied'))
    isAquiredConstructed=int(request.form.get('isAquiredConstructed'))
    

    finalTax = 0

    
    #Capital Gains
    finalTax += longDebtMF*0.2
    finalTax += shortStockEq*0.15
    income += shortDebtMF
    
    #Business and Profession
    if businessIncome!=0 and businessIncome<deductableExpenses:
        income += businessIncome - deductableExpenses
    
    #Other Sources
    income += otherSourcesTotal
    
    #House Property
    NAV = rentReceived - municipalTaxesPaid
    
    NAV = NAV*0.7

    limit = 200000
    if not isAquiredConstructed:
        limit = 30000
    
    if isSelfOccupied:
        NAV -= min(limit,homeLoanInterestPaid)
    else:
        NAV -= homeLoanInterestPaid
    
    income += max(NAV,-200000)

    #Salary and Final Tax Calc
    if age<60:
        if income > 250000:
            taxable = income - 250000
            if income > 500000:
                taxable = 500000 - 250000
            finalTax += 0.05 * taxable

        if income > 500000:
            taxable = income - 500000
            if income > 1000000:
                taxable = 1000000 - 500000
            finalTax += 0.2 * taxable

        if income > 1000000:
            taxable = income - 1000000
            finalTax += 0.3 * taxable


    elif age<80:
        if income > 300000:
            taxable = income - 300000
            if income > 500000:
                taxable = 500000 - 300000
            finalTax += 0.05 * taxable

        if income > 500000:
            taxable = income - 500000
            if income > 1000000:
                taxable = 1000000 - 500000
            finalTax += 0.2 * taxable

        if income > 1000000:
            taxable = income - 1000000
            finalTax += 0.3 * taxable


    else:
        if income > 500000:
            taxable = income - 500000
            if income > 1000000:
                taxable = 1000000 - 500000
            finalTax += 0.2 * taxable

        if income > 1000000:
            taxable = income - 1000000
            finalTax += 0.3 * taxable
    
    return render_template('taxes.html',page=PageData('taxes', 'Taxes'),tax=finalTax)

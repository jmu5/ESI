import mysql.connector
import pandas as pd
import math


date='2023-09-01'

cnx=mysql.connector.connect(user='*', password='*', host='localhost',  database='ESI')

countries=['EU', 'EA', 'BE', 'BG', 'CZ', 'DK', 'DE', 'EE', 'IE', 'EL', 'ES', 'FR', 'HR', 'IT', 'CY', 'LV', 'LT', 'LU', 'HU', 'MT', 'NL', 'AT', 'PL', 'PT', 'RO', 'SI', 'SK', 'FI', 'SE', 'UK', 'ME', 'MK', 'BS', 'RS', 'TR']


def industrial():

    print('Industrial:')

    for i in range(2, 26):
        sheet=pd.read_excel('data/industry_subsectors_sa_m_nace2.xlsx', sheet_name=i)

        print(i+8)
        lastrow=print(len(sheet))
        lastrow=int(len(sheet))

        for k in range(0, 35):
            print(countries[k])

            cof=float(sheet.loc[lastrow-1][k*8+1])
            if math.isnan(cof):
                cof=None
            q1=float(sheet.loc[lastrow-1][k*8+2])
            if math.isnan(q1):
                q1=None
            q2=float(sheet.loc[lastrow-1][k*8+3])
            if math.isnan(q2):
                q2=None
            q3=float(sheet.loc[lastrow-1][k*8+4])
            if math.isnan(q3):
                q3=None
            q4=float(sheet.loc[lastrow-1][k*8+5])
            if math.isnan(q4):
                q4=None
            q5=float(sheet.loc[lastrow-1][k*8+6])
            if math.isnan(q5):
                q5=None
            q6=float(sheet.loc[lastrow-1][k*8+7])
            if math.isnan(q6):
                q6=None
            q7=float(sheet.loc[lastrow-1][k*8+8])
            if math.isnan(q7):
                q7=None

            add_data=("INSERT INTO INDUSTRIAL" "(date, country, subsector, cof, Q1, Q2, Q3, Q4, Q5, Q6, Q7) " " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data=(date, countries[k], i+8, cof, q1, q2, q3, q4, q5, q6, q7)

            cursor=cnx.cursor()
            cursor.execute(add_data, data)
            cnx.commit()
            cursor.close()


def service():

    print('Service:')

    service_sectors=[49, 50, 51, 52, 53, 55, 56, 58, 59, 60, 61, 62, 63, 64, 65, 66, 68, 69, 70, 71, 72, 73, 74, 75, 77, 78, 79, 80, 81, 82, 90, 91, 92, 93, 94, 95, 96]

    for i in range(2, 39):
        sheet=pd.read_excel('data/services_subsectors_sa_m_nace2.xlsx', sheet_name=i)

        print(service_sectors[i-2])
        lastrow=print(len(sheet))
        lastrow=int(len(sheet))

        for k in range(0, 35):
            print(countries[k])

            cof=float(sheet.loc[lastrow-1][k*7+1])
            if math.isnan(cof):
                cof=None
            q1=float(sheet.loc[lastrow-1][k*7+2])
            if math.isnan(q1):
                q1=None
            q2=float(sheet.loc[lastrow-1][k*7+3])
            if math.isnan(q2):
                q2=None
            q3=float(sheet.loc[lastrow-1][k*7+4])
            if math.isnan(q3):
                q3=None
            q4=float(sheet.loc[lastrow-1][k*7+5])
            if math.isnan(q4):
                q4=None
            q5=float(sheet.loc[lastrow-1][k*7+6])
            if math.isnan(q5):
                q5=None
            q6=float(sheet.loc[lastrow-1][k*7+7])
            if math.isnan(q6):
                q6=None

            add_data=("INSERT INTO SERVICE " "(date, country, subsector, cof, Q1, Q2, Q3, Q4, Q5, Q6) " " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

            data=(date, countries[k], service_sectors[i-2], cof, q1, q2, q3, q4, q5, q6)

            cursor=cnx.cursor()
            cursor.execute(add_data, data)
            cnx.commit()
            cursor.close()


def retail():

    print('Retail:')

    retail_sectors=[45, 'MVS', 'MVRM', 47, 'FBT', 'FUEL', 'OTHERS']

    for i in range(2, 9):
        sheet=pd.read_excel('data/retail_subsectors_sa_m_nace2.xlsx', sheet_name=i)

        print(retail_sectors[i-2])
        lastrow=print(len(sheet))
        lastrow=int(len(sheet))

        for k in range(0, 35):
            print(countries[k])

            cof=float(sheet.loc[lastrow-1][k*7+1])
            if math.isnan(cof):
                cof=None
            q1=float(sheet.loc[lastrow-1][k*7+2])
            if math.isnan(q1):
                q1=None
            q2=float(sheet.loc[lastrow-1][k*7+3])
            if math.isnan(q2):
                q2=None
            q3=float(sheet.loc[lastrow-1][k*7+4])
            if math.isnan(q3):
                q3=None
            q4=float(sheet.loc[lastrow-1][k*7+5])
            if math.isnan(q4):
                q4=None
            q5=float(sheet.loc[lastrow-1][k*7+6])
            if math.isnan(q5):
                q5=None
            q6=float(sheet.loc[lastrow-1][k*7+7])
            if math.isnan(q6):
                q6=None

            add_data=("INSERT INTO RETAIL " "(date, country, subsector, cof, Q1, Q2, Q3, Q4, Q5, Q6) " " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

            data=(date, countries[k], retail_sectors[i-2], cof, q1, q2, q3, q4, q5, q6)


            cursor=cnx.cursor()
            cursor.execute(add_data, data)
            cnx.commit()
            cursor.close()


def construction():

    print('Construction:')

    construction_sectors=[41, 42, 43]

    for i in range(2, 5):
#    for i in range(4, 5):
        print("Sheet: ", i)
        sheet=pd.read_excel('data/building_subsectors_sa_m_nace2.xlsx', sheet_name=i)

        print(construction_sectors[i-2])
        lastrow=print(len(sheet))
        lastrow=int(len(sheet))

        for k in range(0, 35):
            print(countries[k])

            cof=float(sheet.loc[lastrow-1][k*13+1])
            if math.isnan(cof):
                cof=None
            q1=float(sheet.loc[lastrow-1][k*13+2])
            if math.isnan(q1):
                q1=None
            q3=float(sheet.loc[lastrow-1][k*13+10])
            if math.isnan(q3):
                q3=None
            q4=float(sheet.loc[lastrow-1][k*13+11])
            if math.isnan(q4):
                q4=None
            q5=float(sheet.loc[lastrow-1][k*13+12])
            if math.isnan(q5):
                q5=None

            add_data=("INSERT INTO CONSTRUCTION " "(date, country, subsector, cof, Q1, Q3, Q4, Q5)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            data=(date, countries[k], construction_sectors[i-2], cof, q1, q3, q4, q5)

            cursor=cnx.cursor()
            cursor.execute(add_data, data)
            cnx.commit()
            cursor.close()


industrial()
service()
retail()
construction()


cnx.close()

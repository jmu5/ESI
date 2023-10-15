#!/usr/bin/env python3
import numpy as np
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from matplotlib import pyplot as plt, colors
import cgitb
import cgi
import requests
import os
import mysql.connector
import datetime

cgitb.enable()


print("Content-Type: text/html;charset=utf-8")
print("Content-type:text/html\r\n")
print('<h1>ESI - Economic Sentiment Indicator</h1><h2>Eurostat</h2><h3>Subsector Heatmap:</h3><form method="get" action="ESI.py"><select name="subsector"><option value="10">10:Manufacture of food products</option><option value="11">11:Manufactures of beverages</option><option value="12">12:Manufactures of tobacco products</option><option value="13">13:Manufactures of textiles</option><option value="14">14:Manufactures of wearing apparel</option><option value="15">15:Manufactures of leather and related products</option><option value="16">16:Manufactures of wood and of prod of wood and cork, except furniture; manuf. of straw and plaiting materials</option><option value="17">17:Manufactures of paper and paper products</option><option value="18">18:Printing and reproduction of recorded media</option><option value="19">19:Manufactures of coke and refined petroleum products</option><option value="20">20:Manufactures of chemicals and chemical products</option><option value="21">21:Manufactures of basic pharmaceutical products and pharmaceutical preparations</option><option value="22">22:Manufacture of rubber and plastic products</option><option value="23">23:Manufactures of other non-metallic mineral products</option><option value="24">24:Manufactures of basic metals</option><option value="25">25:Manufactures of fabricated metal products, except machinery and equipment</option><option value="26">26:Manufactgures of computer, electronic and optical products</option><option value="27">27:Manufactures of electrical equipment</option><option value="28">28:Manufactures of machinery and equipment n.e.c.</option><option value="29">29:Manufactures of motor vehicles, trailers and semi-trailers</option><option value="30">30:Manufacture of other transport equipment</option><option value="31">31:Manufactures of furniture</option><option value="32">32:Other manufacturing</option><option value="33">33:Repair and installation of machinery and equipment</option></select><br><input type="submit" value="Get map"></form><br>')

fields=cgi.FieldStorage()

try:
    subsector=fields['subsector'].value

#    print('---'+subsector+'---')

    cnx = mysql.connector.connect(user='*', password='*',
                              host='localhost',
                              database='ESI')


### Map ###

    def make_bbox(long0, lat0, long1, lat1):
        return Polygon([[long0, lat0], [long1, lat0], [long1, lat1], [long0, lat1]])

    bbox=make_bbox(-36.210938, 28.304381, 35.226563, 81.361287)

    bbox_gdf=gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[bbox])

    europe=gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    europe=europe[europe.continent=='Europe']

    europe=europe.overlay(bbox_gdf, how="intersection")

    fig, ax=plt.subplots(figsize=(10,10))

    title='Subsector '+subsector+' COF indicator'

    europe.plot(linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
    ax.set_title(title, fontsize=16)
    ax.set_axis_off()
    ax.set_facecolor('#676767')


### Database ###

    cursor = cnx.cursor()

    query = ("SELECT country, cof FROM INDUSTRIAL "
         "WHERE date='2023-08-01' AND cof IS NOT NULL AND subsector=%s" %subsector)

    df=pd.read_sql(query, con=cnx)

### Countries ###

    codes=['AL', 'AT', 'BE', 'BG', 'DE', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'ME', 'MK', 'NL', 'PL', 'PT', 'RO', 'RS', 'SE', 'SI']
    countries=['Albania', 'Austria', 'Belgium', 'Bulgaria', 'Germany', 'Denmark', 'Estonia', 'Greece', 'Spain', 'Finland', 'France', 'Croatia', 'Hungary', 'Ireland', 'Italy', 'Lithuania', 'Luxembourg', 'Latvia', 'Montenegro', 'North Macedonia', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Serbia', 'Sweden', 'Slovenia']

    codepairs0={'codes': codes, 'countries': countries}

    codepairs=pd.DataFrame(codepairs0)


    cmap=plt.cm.RdYlGn
    norm=colors.Normalize(vmin=-100.0, vmax=100.0)

    for k in codepairs.index:
        found=False
        for l in df.index:
            if codepairs['codes'][k]==df['country'][l]:
#                print('|', codepairs['codes'][k], ':', df['cof'][l])
                europe[europe.name==codepairs['countries'][k]].plot(color=cmap(norm(float(df['cof'][l]))), ax=ax)
                found=True
                break


    sm=plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    fig.colorbar(sm)

    os.system('sudo rm ../ESI/python/images/europe.jpg')
    plt.savefig("../ESI/python/images/europe.jpeg")
    plt.show()
    os.chmod('../ESI/python/images/europe.jpeg', 0o0777)
    print('<img src="../ESI/python/images/europe.jpeg">')
    cnx.close()

except:
    print('No map')


### Database ###

print('<h3>Subsector Breakdown:</h3><form method="get" action="ESI.py">Country:<br><select name="countrybrk"><option value="AL">Albania</option><option value="AT">Austria</option><option value="BE">Belgium</option><option value="BG">Bulgaria</option><option value="DE">Germany</option><option value="DK">Denmark</option><option value="EE">Estonia</option><option value="EL">Greece</option><option value="ES">Spain</option><option value="FI">Finland</option><option value="FR">France</option><option value="HR">Croatia</option><option value="HU">Hungary</option><option value="IE">Ireland</option><option value="IT">Italy</option><option value="LT">Lithuania</option><option value="LU">Luxembourg</option><option value="LV">Latvia</option><option value="ME">Montenegro</option><option value="MK">North Macedonia</option><option value="NL">Netherlands</option><option value="PL">Poland</option><option value="PT">Portugarl</option><option value="RO">Romania</option><option value="RS">Serbia</option><option value="SE">Sweden</option><option value="SI">Slovenia</option></select><br>Subsector:<br><select name="subsectorbrk"><option value="10">10:Manufacture of food products</option><option value="11">11:Manufactures of beverages</option><option value="12">12:Manufactures of tobacco products</option><option value="13">13:Manufactures of textiles</option><option value="14">14:Manufactures of wearing apparel</option><option value="15">15:Manufactures of leather and related products</option><option value="16">16:Manufactures of wood and of prod of wood and cork, except furniture; manuf. of  of straw  and plaiting materials</option><option value="17">17:Manufactures of paper and paper products</option><option value="18">18:Printing and reproduction of recorded media</option><option value="19">19:Manufactures of coke and refined petroleum products</option><option value="20">20:Manufactures of chemicals and chemical products</option><option value="21">21:Manufactures of basic pharmaceutical products and pharmaceutical preparations</option><option value="22">22:Manufacture of rubber and plastic products</option><option value="23">23:Manufactures of other non-metallic mineral products</option><option value="24">24:Manufactures of basic metals</option><option value="25">25:Manufactures of fabricated metal products, except machinery and equipment</option><option value="26">26:Manufactgures of computer, electronic and optical products</option><option value="27">27:Manufactures of electrical equipment</option><option value="28">28:Manufactures of machinery and equipment n.e.c.</option><option value="29">29:Manufactures of motor vehicles, trailers and semi-trailers</option><option value="30">30:Manufacture of other transport equipment</option><option value="31">31:Manufactures of furniture</option><option value="32">32:Other manufacturing</option> <option value="33">33:Repair and installation of machinery and equipment</option></select><br><input type="submit" value="Get chart"></form>')

try:
    subsectorbrk=fields['subsectorbrk'].value
    countrybrk=fields['countrybrk'].value
    if subsectorbrk!=None and countrybrk!=None:

        cnx = mysql.connector.connect(user='*', password='*', host='localhost', database='ESI')

        subsectorbrk=fields['subsectorbrk'].value
        countrybrk=fields['countrybrk'].value

        cursor = cnx.cursor()

        query2 = ("SELECT date, cof, q1, q2, q3, q4, q5, q6, q7 FROM INDUSTRIAL WHERE date>='2021-01-01' AND country=%s AND subsector=%s ORDER BY date ASC")

        df2=pd.read_sql(query2, con=cnx, params=[countrybrk, subsectorbrk])


        print('<h3>Country:', countrybrk, ' Subsector:', subsectorbrk, '</h3>');

        df2.plot()


        os.system('sudo rm ../ESI/python/images/chart.jpg')
        plt.savefig("../ESI/python/images/chart.jpeg")
        os.system('sudo chmod 777 ../ESI/python/images/chart.jpeg')
        print('<img src="../ESI/python/images/chart.jpeg">')
        cnx.close()

    else:
        print('No chart')

        subsectorbrk=fields['subsectorbrk'].value
        countrybrk=fields['countrybrk'].value

        print(countrybrk, ':', subsectorbrk)

except:
    print('No chart')



print('<ul style="list-style: none;"><li>COF:Condidence indicator (Q2-Q4+Q5)/3</li>')
print('<li>Q1:Production trend observed in recent months</li>')
print('<li>Q2:Assessment of order-book levels</li>')
print('<li>Q3:Assessment of export order-book levels</li>')
print('<li>Q4:Assessment of stocks of finished products</li>')
print('<li>Q5:Production expectations for the months ahead</li>')
print('<li>Q6:Selling price expectations for the months ahead</li>')
print('<li>Q7:Employment expectations for the months ahead</li></ul>')



print('<ul style="list-style: none;"><li>10:Manufacture of food products</li>')
print('<li>11:Manufactures of beverages</li>')
print('<li>12:Manufactures of tobacco products</li>')
print('<li>13:Manufactures of textiles</li>')
print('<li>14:Manufactures of wearing apparel</li>')
print('<li>15:Manufactures of leather and related products</li>')
print('<li>16:Manufactures of wood and of prod. of wood and cork, except furniture; manuf. of straw and plaiting materials</li>')
print('<li>17:Manufactures of paper and paper products</li>')
print('<li>18:Printing and reproduction of recorded media</li>')
print('<li>19:Manufacture of coke and refined petroleum products</li>')
print('<li>20:Manufactures of chemicals and chemical products</li>')
print('<li>21:Manufactures of basic pharmaceutical products and pharmaceutical preparations</li>')
print('<li>22:Manufactures of rubber and plastic products</li>')
print('<li>23:Manufactures of other non-metallic mineral products</li>')
print('<li>24:Manufactures of basic metals</li>')
print('<li>25:Manufactures of fabricated metal products, except machinery and equipment</li>')
print('<li>26:Manufactures of computer, electronic and optical products</li>')
print('<li>27:Manufactures of electrical equipment</li>')
print('<li>28:Manufactures of machinery and equipment n.e.c.</li>')
print('<li>29:Manufactures of motor vehicles, trailers and semi-trailers</li>')
print('<li>30:Manufactures of other transport equipment</li>')
print('<li>31:Manufactures of furniture</li>')
print('<li>32:Other manufacturing</li>')
print('<li>33:Repair and installation of machinery and equipment</li></ul>')

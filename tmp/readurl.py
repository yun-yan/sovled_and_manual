#!/usr/bin/python
import urllib2, json
import MySQLdb
import matplotlib.pyplot as plt
import numpy 

#set the variable you want to restrict the boundary condition
global DEC_MIN,DEC_MAX,MAG_MIN,MAG_MAX
DEC_MIN=35
DEC_MAX=40
MAG_MIN=8
MAG_MAX=12
path="/home/yunyan/ZITFIG/"   #the path of saving figure


#This function catch the data from https://mars.lco.global and insert the data to database ALERT
def search(DEC_MIN,DEC_MAX,MAG_MIN,MAG_MAX):
    #connect the https://mars.lco.global
    url=urllib2.urlopen("https://mars.lco.global/?dec__gt={0}&dec__lt={1}&magpsf__gte={2}&magpsf__lte={3}&format=json".format(DEC_MIN,DEC_MAX,MAG_MIN,MAG_MAX))
    print(url)
    #change type of json to python
    data=json.load(url)
    #Let all page you set the boundary condition to python data
    for i in range(data['pages']):
        url=urllib2.urlopen("https://mars.lco.global/?dec__gt={0}&dec__lt={1}&magpsf__gte={2}&magpsf__lte={3}&page={4}&format=json".format(DEC_MIN,DEC_MAX,MAG_MIN,MAG_MAX,i+1))
        data=json.load(url)
        # Connect the Mysql and use the user "ALERT" .The form is (your localhost , username, password, name of database)
        db = MySQLdb.connect("localhost", "ALERT" ,"1234","ALERT")    
        cursor = db.cursor()                     # Create a Cursor object to execute queries.

        #Get some data you want to insert to database
        for result in data['results']:
            lco_id=result['lco_id']
            objectId=result['objectId']
            magpsf=result['candidate']['magpsf']
            sigmapsf=result['candidate']['sigmapsf']
            filter=result['candidate']['filter']
            ra=result['candidate']['ra']
            dec=result['candidate']['dec']
            jd=result['candidate']['jd']
            wall_time=result['candidate']['wall_time']

            #judge the data whether it repeats
            sql="select * from ZIT;"
            #try:
            cursor.execute(sql)
            figuredata=cursor.fetchall()
            try:
                if figuredata[0][1]==lco_id:
                    print("It has been processed")
                    return
            except:
                pass
            #insert to database
            sql="insert into ZIT (lco_id,objectId,magpsf,sigmapsf,filter,ra,`dec`,jd,wall_time) values ({0},'{1}',{2},{3},'{4}',{5},{6},{7},'{8}');".format(lco_id,objectId,magpsf,sigmapsf,filter,ra,dec,jd,wall_time)

            try:
                cursor.execute(sql)         #excute the "isnert into data_file...."
                db.commit()                 #do nothing
            except:
                db.rollback()               #skip if error
        db.close()
        print("A page has been finished")



if __name__== "__main__":

    search(DEC_MIN,DEC_MAX,MAG_MIN,MAG_MAX)

    # Connect the Mysql and use the user "ALERT" .The form is (your localhost , username, password, name of database)
    db = MySQLdb.connect("localhost", "ALERT" ,"1234","ALERT")    
    cursor = db.cursor()                     # Create a Cursor object to execute queries.

    #select all data from ZIT
    sql="select * from ZIT;"
    try:
        cursor.execute(sql)
        figuredata=cursor.fetchall()
        for row in figuredata:
            #separate the data with objectId
            sql="select * from ZIT where objectId='{0}';".format(row[2])
            
            cursor.execute(sql)
            figureofobjectId=cursor.fetchall()
            x=[item[9] for item in figureofobjectId]    #x is julian data
            y=[item[3] for item in figureofobjectId]    #y is mag
            error=[item[4] for item in figureofobjectId]#error bar is sigmamag
            
            #draw mag-JD with every objectId
            fig=plt.figure()
            plt.errorbar(x,y,error,fmt='o',ecolor='r',color='b',elinewidth=2,capsize=4)
            plt.title("{0}".format(row[2]))
            plt.ylabel('magnitude')
            plt.xlabel('JD')
            figurepath=path+"{0}.png".format(row[2])
            fig.savefig(figurepath)
            sql="UPDATE ZIT set `figurepath`= '{0}' WHERE `objectId`='{1}';".format(figurepath,row[2]) 
            try:
                cursor.execute(sql) 
                db.commit()
                print("{0}.png has finished".format(row[2])) 
            except:
                db.rollback()
    
    except:
        print "Error: unable to fetch data"
    db.close()



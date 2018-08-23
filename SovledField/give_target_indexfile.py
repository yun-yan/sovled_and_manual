#!/usr/bin/python
import MySQLdb                              #Let python use mysql
import math

# Connect the Mysql and use the user "TAT" .The form is (your localhost , username, password, name of database)
db = MySQLdb.connect("localhost","TAT","1234","TAT")     
cursor=db.cursor()       # Create a Cursor object to execute queries.


#Let RA(HH:MM:SS) to deg
def RA_to_deg(RA):
    RA_deg=0
    try:
        RA=RA.split(':')

        for i in range(len(RA)):
            RA[i]=float(RA[i])

        RA_deg=RA[0]*15.0+RA[1]*15.0/60.0+RA[2]*15.0/3600.0
    except:
        pass
    return RA_deg


#Let DEC(DEG:ARCMIN:ARCSEC) to deg
def DEC_to_deg(DEC):
    DEC_deg=0
    try:
        DEC=DEC.split(':')

        for i in range(len(DEC)):
            DEC[i]=float(DEC[i])

        DEC_deg=DEC[0]+DEC[1]/60.0+DEC[2]/3600.0
    except:
        pass
    return DEC_deg

#Find the healpix from (RA,DEC)

def deg_to_index(x,y):
    x=x%360
    index=0
    indexscope=[]
    scope=[(x+0.73,y),(x-0.73,y),(x,y+0.73),(x,y-0.73)]         # scope a limit value
    for seat in scope:
        for i in range(4):                                      #split four part
            if 90*i <= seat[0] < 90*(i+1):
                index=i
                #split up and down with abs function
                if seat[1] >= abs(math.asin(2.0/3.0)*180/math.pi/45.0*seat[0]-(2*i+1)*math.asin(2.0/3.0)*180/math.pi):
                    index=index%4
                elif seat[1] <= -abs(math.asin(2.0/3.0)*180/math.pi/45.0*seat[0]-(2*i+1)*math.asin(2.0/3.0)*180/math.pi):
                    index=8+index%4
                else:
                    if seat[0] <= 45+i*90:
                        index=4+index%4
                    else:
                        index=4+(index+1)%4
    #build the list of all index, and then elimate it.
        indexscope.append(index)
    indexscope=list(set(indexscope))
    return indexscope

if __name__ == "__main__":

    #Get `NAME`,`RA`,`DEC` from table target
    sql="select `NAME`,`RA`,`DEC`  from table targets;"
    try:
        cursor.execute(sql)
        results=cursor.fetchall()
        for i in results:
            #use the data from table targets to become deg and the healpix
            RAdeg=RA_to_deg(i[1])
            DECdeg=DEC_to_deg(i[2])
            indexyy=deg_to_index(RAdeg,DECdeg)
            sql="UPDATE targets set `RA(deg)`  = '{0}' WHERE `NAME`= '{1}';".format(RAdeg,i[0])
            #print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

            sql="UPDATE targets set `DEC(deg)`  = '{0}' WHERE `NAME`= '{1}';".format(DECdeg,i[0])
            #print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
            indexyy="{0}".format(indexyy)
            sql="UPDATE targets set `INDEXYY`  = '{0}' WHERE `NAME`='{1}';".format(indexyy[1:-1],i[0])
            #print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()


    except:
        print "Error: unable to fetch data"

db.close()

     

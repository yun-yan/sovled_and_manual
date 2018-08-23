#!/usr/bin/python
import os
import MySQLdb

global LOG
LOG="/home/yunyan/SovledField/log.txt"

global LOG_ERROR
LOG_ERROR="/home/yunyan/SovledField/log_error.txt"

global BACKUP_PATH_FILENAME                                                       
BACKUP_PATH = "/home/yunyan/test_healpix"



def insert(current_path,filename,name):
    temp="/opt/astrometry/bin/solve-field --cpulimit 60 --overwrite {0} > tmp".format(filename)
    os.system(temp)
    fo=open('tmp','r')
    line=fo.readlines()
    for i in range(len(line)):
        line[i]=line[i][:-1]
        if "(RA,Dec)" in line[i]:
            linesplit=line[i].split("=") 
            RADECdeg=linesplit[-1][:-5]
        if "(RA H:M:S, Dec D:M:S)" in line[i] :
            linesplit=line[i].split("=")
            RADEC=linesplit[-1][:-1]
        if "best" in line[i]: 
            linesplit=line[i-4].split("/")
            index=linesplit[-1][:-6]

    fo.close()
    os.remove("tmp")

    # Connect the Mysql and use the user "TAT" .The form is (your localhost , username, password, name of database)
    db = MySQLdb.connect("localhost", "TAT" ,"1234","INDEXFILE")    
    cursor = db.cursor()                     # Create a Cursor object to execute queries. 
    # Describe the data_file
    try: 
        sql="insert into INDEXFILE (`INDEX`,`FILENAME`,`FILEPATH`, `RA,DEC (deg)`,`(RA H:M:S, Dec D:M:S)`) values ('{0}','{1}','{2}','{3}','{4}');".format(index,name,current_path,RADECdeg,RADEC)
        try:
            print(sql)
            cursor.execute(sql)         #excute the "isnert into data_file...."
            db.commit()                 #do nothing
        except:
            db.rollback()               #skip if error
    except:
        fo=open(LOG_ERROR,"a")
        fo.write("{0} is fail \n".format(name))
        fo.close() 
    return 


if __name__ =="__main__":

    fo=open(LOG,"a")
    fo.close()

    for root, dirs, files in os.walk(BACKUP_PATH):
        for name in files:
            if 'fit' in name:
                filename=os.path.join(root, name)    # the current directory plus the one of sub directory.
                print(root)
                #read the log and elimate "\n"
                fo=open(LOG,"r")
                line=fo.readlines()
                for i in range(len(line)):
                    line[i]=line[i][:-1]
                fo.close()
            
                if filename in line:
                    print("{0} has already been deal ").format(filename)
                else:
                    try:
                        insert(root,filename,name)
                    except:
                        fo=open(LOG_ERROR,"a")
                        fo.write("{0} has some other problems".format(filename))
                        fo.close()
                    # Write the path dealed to log.txt
                    fo=open(LOG,"a")
                    fo.write(filename+'\n')
                    fo.close()
            else:
                pass





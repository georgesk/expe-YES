"""
Database management
"""

import sqlite3
import datetime, time, pytz, crypt

def adapt_datetime(ts):
    return time.mktime(ts.timetuple())

sqlite3.register_adapter(datetime.datetime, adapt_datetime)

class DB(object):
  "Create a SQLite datbase and manage it"
 
  def __init__(self, dbName, tables=None):
      """
      Constructor
      @param dbName filename for the database
      @param tables an otionale dictionary of tables to create
      """
      self.dbName = dbName
      if tables:
          self.creaTables(tables)
      return
  
  def execReq(self, req, param =()):
      """
      Exec the given request, detect errors eventually
      @param req the request
      @param param parameters
      @return a list of tuples when the request is a SELECT; 
              a string in case of an error;
              None by default
      """
      conn =sqlite3.connect(self.dbName)
      if req.upper().startswith("SELECT"):
          try:
              cursor=conn.cursor()
              cursor.execute(req, param)
              return cursor.fetchall() # returns a list of tuples
          except Exception as err:
              # feedback the request and the error message
              msg ="Incorrect SQL request :\n{}\nError:".format(req)
              return msg +str(err)
      else:
          try:
              conn.cursor().execute(req, param)
              conn.commit()
          except Exception as err:
              conn.rollback()
              # feedback the request and the error message
              msg ="Incorrect SQL request :\n{}\nError:".format(req)
              return msg +str(err)
      return
 
  def creaTables(self, dicTables):
      """
      Creates database tables if they don't already exist
      @param dicTables dictionary of tables
      """
      for table in dicTables:
          req = "CREATE TABLE {} (".format(table)
          pk =""
          for descr in dicTables[table]:
              fieldName = descr[0]
              ftype = descr[1]	    # type wanted for the field
              if ftype =="i":
                  fieldType ="INTEGER"
              elif ftype =="k":     # primary key
                  fieldType ="INTEGER PRIMARY KEY AUTOINCREMENT"
                  pk = fieldName
              elif ftype =="r":
                  fieldType ="REAL"
              else: 	            # to keep it simple, every other
                  fieldType ="TEXT" # field type is TEXT
              req += "{} {}, ".format(fieldName, fieldType)
          req = req[:-2] + ")"
          try:
              self.execReq(req)
          except:
              pass		   # The table probably exists already

class resaDB (DB):
    """
    database to deal with reservations of timeslots
    ======================================================
    @var resaTables define tables for a reservation database.
    Every user can make a reservation for the same resource, resources
    must not overlap each over along time.
    """

    resaTables={
      "user": [("id","k"),("name","t"),("passwd","t"),("email","t"),],
      "resa": [("id","k"),("beg","i"),("end","i"),],
      "user_resa": [("id","k"),("user_id","i"),("resa_id","i"),],
    }

    def __init__(self, dbName):
      """
      Constructor
      @param dbName filename for the database
      """
      DB.__init__(self, dbName, tables=resaDB.resaTables)
      return

    def resa4day(self, wantedDate):
      """
      gets reservations existing for a given date
      @param wantedDate the date for reservations, as string in
      format "mm/dd/yyy"
      @return an iterable with existing reservations, which gives
      explicitely the time and the username for each one.
      """
      m,d,y=wantedDate.split("/")
      m,d,y = int(m), int(d), int(y)
      today=time.mktime(datetime.datetime(y,m,d, tzinfo=pytz.utc).timetuple())
      req="SELECT beg, name FROM user, resa, user_resa WHERE resa.beg >= {today} AND resa.beg < {tomorrow} AND resa.id=user_resa.resa_id AND user.name=user_resa.user_id".format(today=today, tomorrow=today+24*3600)
      return self.execreq(req)
    
    def insUser(self, name, passwd, email, force=False):
      """
      insert a user in the database, or raise an error
      @param name user's name
      @param passwd user's password
      @param email user's e-mail
      @param force will modify the password and/or e-mail forcefully if True
      """
      found=False
      msg=""
      res=self.execReq("select * from user where name='{}'".format(name))
      if len(res):
        found=True
        msg="user {} already exists".format(name)
      res=self.execReq("select * from user where email='{}'".format(email))
      if len(res):
        found=True
        msg="the e-mail address {} is already in use".format(name)
      if force or not found:
        req="INSERT INTO user VALUES (?,?,?)"
        c=crypt.crypt(passwd, salt=crypt.mksalt(crypt.METHOD_MD5))
        print ("GRRRR req=",req, (name, c, email))
        self.execReq(req, (name, c, email))
      else:
        raise Exception('InsertError',msg)
      

  
if __name__=="__main__":
    print(resaDB("test.sq3"))
    

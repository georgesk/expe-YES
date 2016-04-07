"""
Database management
"""

import sqlite3

"""
tables for a reservation database.
Every user can make a reservation for the same resource, resources
must not overlap each over along time.
"""

resaTables={
    "user": [("id","k"),("name","t"),("passwd","t"),("email","t"),],
    "resa": [("id","k"),("beg","i"),("end","i"),],
    "user_resa": [("id","k"),("user_id","i"),("resa_id","i"),],
}

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

if __name__=="__main__":
    print(DB("test.sq3",resaTables))
    

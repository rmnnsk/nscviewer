import sqlite3
import time

class DBWorker:
	def __init__(self,database):
		self.connection = sqlite3.connect(database,check_same_thread=False)
		self.cursor = self.connection.cursor()

	def write_user(self,user,passw,AT,VER,):
		t = time.strftime(r"%Y %m %d %H:%M:%S",time.localtime())
		with self.connection:
			self.cursor.execute("INSERT INTO users(logins,password,AT1,VER1,time) VALUES(?,?,?,?,?)",(user,passw,AT,VER,t))
			self.connection.commit()

	def write_atver2(self,user,AT,VER2,_id):
		if mode == 1:
			with self.connection:
				self.cursor.execute("UPDATE users SET AT2 = '%s',VER2 = '%s' WHERE ID = '%s'"%AT,VER2,_id)
				self.connection.commit()
	def get_AT(self,user_id):
		with self.connection:
			self.cursor.execute("SELECT AT1 FROM users WHERE ID = ?",(user_id,))
			return self.cursor.fetchone()

	def get_VER(self,user_id):
		with self.connection:
			self.cursor.execute("SELECT VER1 FROM users WHERE ID = ?",(user_id,))
			return self.cursor.fetchone()

	def get_user_id(self,VER):
		with self.connection:
			self.cursor.execute("SELECT ID FROM users WHERE VER1 = ? ",(VER,))
			return self.cursor.fetchone()

	def del_user(self,AT):
		with self.connection:
			self.cursor.execute("DELETE FROM users WHERE AT1 = '%s'"%AT)
			self.connection.commit()

	def close(self):
		self.connection.close()

if __name__ == "__main__":
	dbw = DBWorker("users.db")
	print(dbw.get_VER(22))
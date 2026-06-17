from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv('DB_file'))
print(os.getenv('SHELL'))
user_id=19
print(f"SELECT * FROM users WHERE id = """,(user_id,))
s='[1,2,3]'
l=(int(i) for i in s.strip("[]").replace(',',''))
print(l,type(i for i in l))
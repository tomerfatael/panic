import plyvel
import sqlite3

# f = open('jstest.txt','w')
# for k,v in db:
# 	f.write(v.decode("utf-8"))
# 	break


if __name__ == "__main__":
	db = plyvel.DB('./datadir/levelDB', create_if_missing=True)
	conn = sqlite3.connect('./datadir/crawl-data.sqlite')
	cursor = conn.cursor()

	#creating new table for javascript content
	table = """ CREATE TABLE IF NOT EXISTS content (
	            js_content VARCHAR NOT NULL
	        ); """
	cursor.execute(table)

	keys_column = cursor.execute("SELECT content_hash FROM http_responses")
	keys = set(keys_column.fetchall())
	for key in keys:
		key = key[0]
		if key:
			content = db.get(key.encode("utf-8"))
			sqlite_insert_query = f"INSERT INTO content (js_content) VALUES ({content})"
			cursor.execute(sqlite_insert_query)
			print(content)
			print(key)
			break

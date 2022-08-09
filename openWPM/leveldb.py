import pandas as pd
#import plyvel
import sqlite3
import leveldb

if __name__ == "__main__":
    db = leveldb.LevelDB('./datadir/levelDB')
    #db = plyvel.DB('./datadir/levelDB', create_if_missing=True)
    conn = sqlite3.connect('./datadir/crawl-data.sqlite')
    cursor = conn.cursor()

    df = pd.DataFrame(columns=['url', 'js_content'])

    columns = cursor.execute("SELECT url, content_hash FROM http_responses")
    values = set(columns.fetchall())
    for value in values:
        key = value[1]
        url = value[0]
        if key:
            content = db.get(key.encode('utf-8'))
            df.append({'url': url, 'js_content': content}, ignore_index=True)
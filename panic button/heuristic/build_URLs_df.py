import re

import leveldb as leveldb
import pandas as pd
import sqlite3

COMMON_ALERTS_WORDS = ['techsupport', 'alert', 'pc', 'security', 'windows', 'address', 'financial', 'message', 'email',
					   'using', 'virus', 'breach', 'tracking', 'carry', 'communications', 'ancient', 'result', 'call',
					   'stalkers', 'thefts', 'administrator', 'exe', 'hacked', 'logs', 'services', 'suspended',
					   'restart', 'situation', 'attention', 'duped', 'contacting', 'webcam', 'oops', 'passwords',
					   'registry', 'prevent', 'technicians', 'connection', 'adware', 'disabled', 'block', 'pop',
					   'access', 'reserved', 'run', 'worm', 'program', 'frame', 'live', 'live', 'warning', 'unknown',
					   'wrong', 'classified', 'info', 'attack', 'actions', 'desk', 'details', 'computing', 'inject',
					   'something', 'malware', 'calling', 'copyright', 'especially', 'technical', 'vpn', 'follow',
					   'harmful', 'response', 'engineering', 'anonymous', 'significant', 'shut', 'browsing', 'location',
					   'containing', 'dear', 'installed', 'visit', 'current', 'continue', 'causing', 'caused',
					   'exposed', 'apply', 'acts', 'useful', 'warriors', 'leaked', 'often', 'concealed', 'reason',
					   'tcp', 'theft', 'social', 'rights', 'firewall', 'major', 'disk', 'logins', 'identity', 'removed',
					   'hard', 'locked', 'cause', 'viruses', 'password', 'deleted', 'fix', 'auto',
					   'based form', 'trick', 'software', 'harmful', 'crash', 'terms', 'tech support',
					   'contact', 'toll-free', 'toll free', 'error', 'access', 'problem', 'issue', 'phone']

COMMON_ALERTS_WORDS = list(set(COMMON_ALERTS_WORDS))

if __name__ == "__main__":
	# initializing databases from OpenWPM crawler
	db = leveldb.LevelDB('../assets/levelDB')
	conn = sqlite3.connect('../assets/crawl-data.sqlite')
	cursor = conn.cursor()

	# initializing data frame that we will work with
	df = pd.DataFrame(columns=['url', 'js_content', 'visit_id', 'top_level_url', 'alerts'] + COMMON_ALERTS_WORDS + ['phone'])

	columns = cursor.execute("SELECT id, url, content_hash, visit_id FROM http_responses")
	values = set(columns.fetchall())
	# iterating through the database and filling the data frame
	for value in values:
		id = value[0]
		url = value[1]
		key = value[2]  # will be used to retrieve the javascript content of the url from the leveldb database
		visit_id = value[3]  # will be used to retrieve the top level url
		try:
			cursor.execute(f"DELETE FROM http_responses WHERE id = {id}")
			conn.commit()
			if key:
				content = db.Get(key.encode('utf-8'))  # fetching the js content with the key
				if content:
					content = content.decode('utf-8')
					df = df.append({'url': url, 'js_content': content, 'visit_id': visit_id}, ignore_index=True)
		except Exception:
			continue

	# continue filling the data frame
	for _, row in df.iterrows():
		# retrieving top level url for each url
		visit_id = row['visit_id']
		columns = cursor.execute(f"SELECT top_level_url FROM javascript WHERE visit_id = {visit_id}")
		top_level_url = columns.fetchall()
		if top_level_url:
			top_level_url = top_level_url[0][0]
			row['top_level_url'] = top_level_url

		# filling the alert columns in the data frame by using js content
		content = row['js_content']
		if 'alert' in content:
			alerts = re.findall(r'(?<=alert\(\").+(?=\")', content)  # fetching the alerts functions from js content with regex
			if alerts:
				row['alerts'] = alerts
				# looking for instances common alert words given by the article in the founded alerts
				for alert in alerts:
					for risk_word in COMMON_ALERTS_WORDS:
						# marking the founded common alert words in the data frame
						if risk_word in alert.lower():
							row[risk_word] = int(1)
							continue

					# searching for US phone number patterns in the alert functions using regex
					phone_numbers = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', alert)
					if phone_numbers:
						row['phone'] = int(1)

	df = df.dropna(subset=COMMON_ALERTS_WORDS, how='all')  # deleting all the rows without alerts at all
	df.drop('js_content', axis=1, inplace=True)
	df.drop('alerts', axis=1, inplace=True)
	df.drop(['visit_id'], axis=1, inplace=True)

	df.to_csv('data_base_actual.csv')

import pandas as pd
from collections import defaultdict

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
					   'contact', 'toll-free', 'toll free', 'error', 'access', 'problem', 'issue']


if __name__ == "__main__":
	df = pd.read_csv('data_base_actual.csv')

	num_of_url = df.shape[0]

	alert_weight_mapping = defaultdict(int)
	for alert_column in df[COMMON_ALERTS_WORDS]:
		alert_weight_mapping[alert_column] = 0
		if num_of_url != 0:
			alert_weight_mapping[alert_column] += (df.loc[:, alert_column].sum() / num_of_url)

	# for alert in ['call', 'techsupport', 'tech support', 'contact', 'phone', 'toll-free', 'toll free']:
	# 	alert_weight_mapping[alert]

	max_weight = 0
	for alert in COMMON_ALERTS_WORDS:
		max_weight += alert_weight_mapping[alert]

	df['tech_support_scam_score'] = 0
	for row_number in range(df.shape[0]):
		for alert_column in COMMON_ALERTS_WORDS:
			alert_value = df.loc[row_number].at[alert_column]
			if pd.isnull(alert_value):
				continue
			new_value = df.at[row_number, 'tech_support_scam_score'] + (alert_value/max_weight * alert_weight_mapping[alert_column])
			df.loc[row_number, ['tech_support_scam_score']] = new_value

	df.to_csv('weights_actual.csv')


	avg_weight = df['tech_support_scam_score'].mean()
	x = 1
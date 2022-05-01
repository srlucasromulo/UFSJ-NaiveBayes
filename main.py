import pandas as pd

m_estimate = True  # set m-estimate True/False

df = pd.read_csv('dataset.csv')
entry = pd.read_csv('entry.csv')
columns = df.columns


def main():
	count_x = {i: None for i in columns[1:]}
	for i in columns[1:]:
		count_x[i] = df[i].value_counts().to_dict()

	# class probability
	probabilities_y = df[columns[0]].value_counts(normalize=True).to_dict()

	# m-estimate values
	m = 1
	p = 1 / len(probabilities_y)

	# xij probability
	probabilities_x = {i: {} for i in columns[1:]}
	for i in columns[1:]:
		for j in count_x[i].keys():
			probabilities_x[i].update({j: {}})
			for y in probabilities_y.keys():
				xij = df.loc[(df[columns[0]] == y) & (df[i] == j)]
				prop = len(xij) / count_x[i][j] if m_estimate is False \
					else (len(xij) + m * p) / (count_x[i][j] * m)
				probabilities_x[i][j].update({y: prop})

	# classify entries
	hit = 0
	for row in entry.iloc:
		result_entry = row[columns[0]]
		result = {}
		for y in probabilities_y.keys():
			result.update({y: None})
			calc = probabilities_y[y]
			for i in columns[1:]:
				j = row[i]
				calc *= probabilities_x[i][j][y]
			result[y] = calc
			if calc > 0:
				hit += 1

		# evaluates algorithm
		print(f'Entry: {dict(row)}')
		if hit == 0:
			print(f'Entry class: {result_entry}; Algorithm wasnt able to classify the entry.')
		else:
			higher = max(result, key=result.get)
			print(f'Entry class: {result_entry}; Classification result: {higher}; Classified right?: {result_entry == higher}')
		print()


if __name__ == '__main__':
	main()

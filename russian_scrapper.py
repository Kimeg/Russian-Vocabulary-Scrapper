from collections import defaultdict
from bs4 import BeautifulSoup

import pandas as pd
import requests

def main():
	dfs = []

	for i in range(1, 13):
		print(i)
		if i==1:
			resp = requests.get(f"http://masterrussian.com/vocabulary/most_common_words.htm")
		else:
			resp = requests.get(f"http://masterrussian.com/vocabulary/most_common_words_{i}.htm")

		resp.encoding = 'utf-8'

		html_doc = resp.text

		soup = BeautifulSoup(html_doc, "html.parser")

		table = soup.find('table', attrs={"class": "topwords"})

		rows = table.find_all('tr')

		_dict = defaultdict(list)
		for j, row in enumerate(rows):
			if j==0:
				continue

			cols = [ele.text.strip() for k, ele in enumerate(row.find_all('td')) if len(ele.text) and k>0]

			for ele, col_name in zip(cols, col_names):
				_dict[col_name].append(ele)

		dfs.append(pd.DataFrame(_dict))

	with pd.ExcelWriter('russian.xlsx') as writer:
		for i, df in enumerate(dfs):
			dfs[i].to_excel(writer, sheet_name=str(i+1), index=False)

	return

if __name__=="__main__":
	col_names = ["russian_word", "english_translation", "part_of_speech"]

	main()
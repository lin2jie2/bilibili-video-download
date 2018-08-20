#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

# bilibili video url

import sys
import json
import re
import subprocess
import requests

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print("python3 bilibili.py AV-ID [dl?]")
		sys.exit(-1)

	url = "https://www.bilibili.com/video/av{}/".format(sys.argv[1])
	regex = re.compile(r".*<script>window.__playinfo__=(.+?)<\/script>.*", re.S)
	print(url)

	r = requests.get(url)
	if r.status_code == requests.codes.OK:
		match = regex.match(r.text)
		if match:
			# print(match.group(1))
			data = json.loads(match.group(1))
			# print(json.dumps(data, indent=4))
			url = data['durl'][0]['url']
			quality = data['quality']
			search = "-{}.flv".format(quality)
			print("* {}\n".format(url))
			if len(sys.argv) > 2:
				print('downloading, please wait!')
				command = [
					'curl',
					'-s',
					'-C',
					'-',
					url,
					'-H',
					'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
					'-H',
					'Referer: https://www.bilibili.com/video/av{}/?spm_id_from=333.334.bili_douga.4'.format(sys.argv[1]),
					'-H',
					'Origin: https://www.bilibili.com',
					'-o',
					'av{}-q{}.mp4'.format(sys.argv[1], quality)
				]
				print("exec", ' '.join(command))
				subprocess.call(command)
		else:
			print("mismatch")
	else:
		print(r.status_code)

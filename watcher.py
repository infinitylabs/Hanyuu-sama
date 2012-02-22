#!/usr/bin/python

import pyinotify as pi
import webcom
import config
import logging
import updater
from os import path

def start_watcher():
	global notifier
	wm = pi.WatchManager()
	notifier = pi.ThreadedNotifier(wm, handler())
	notifier.start()
	wdd = wm.add_watch(config.watcher_path, pi.IN_MODIFY)
	
def stop_watcher():
	notifier.stop()
def parse_queue_file():
	queue = []
	remaining = 0
	with open(path.join(config.watcher_path, config.watcher_file)) as f:
		djid = f.readline().strip()
		firstline = f.readline().strip()
		
		if (djid != ''):
			remaining = int(firstline)
			current_djid = webcom.get_djid()
			if (current_djid == djid):
				for line in file:
					line = line.strip()
					if line == "":
						continue
					
					try:
						spacepos = line.index(' ')
					except:
						continue
					stime = int(line[:spacepos])
					song = line[spacepos+1:]
					
					song = webcom.fix_encoding(song)
					queue.append((None, song, stime, updater.TYPE_REGULAR))
			else:
				logging.info("Queue discarded because djid does not match")
	if (len(queue) > 0):
		updater.queue.appendmany(queue)
		updater.queue.send(remaining)
			
class handler(pi.ProcessEvent):
	def process_IN_MODIFY(self, event):
		if (event.name == 'queue.txt'):
			parse_queue_file()


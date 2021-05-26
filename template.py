#-*- coding: utf-8 -*-

import configparser
import datetime
import logging
import logging.handlers
import os
import sys

logger = None

class Logger :
	def __init__(self, size=0, backup_cnt=0, pid=False) :
		global logger
		logger = logging.getLogger("sample1")

		self.filename = "./log/crawl_logfile_{:%Y%m%d %H:%M}.log".format(datetime.datetime.now())
		self.filesize = size
		self.backup_count = backup_cnt
		self.enable_pid_postfix = pid
		self.file_handler = None

	def setLogger(self) :
		if self.file_handler :
			logger.removeHandler(self.file_handler)

		logger.setLevel(logging.DEBUG)

		formatter = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")

		stream_handler = logging.StreamHandler()
		stream_handler.setFormatter(formatter)
		logger.addHandler(stream_handler)

		self.file_handler = logging.handlers.RotatingFileHandler(self.filename, mode='a', maxBytes=self.filesize, backupCount=self.backup_count)
		self.file_handler.setFormatter(formatter)
		logger.addHandler(self.file_handler)


class Worker:
	def __init__(self, argv):
		if len(argv) != 2:
			print("Usage: %s config.ini" % argv[0])
			os.exit(0)

		self.logObj = Logger()
		self.config_file = argv[1]
		self.config = configparser.ConfigParser()
		self.config.read(self.config_file)


		self.server_ip = ''
		self.server_port = ''
		self.account = ''
		self.password = ''

		self.sleep = 0


	def setLog(self) :

		section = "LOGGER"
		filesize = self.config.getint(section, "filesize")
		backup_count = self.config.getint(section, "backup_count")
		enable_pid_postfix = self.config.getboolean(section, "enable_pid_postfix")

		self.logObj = Logger(filesize, backup_count, enable_pid_postfix)
		self.logObj.setLogger()


	def setDatas(self) :

		section = "SERVER"
		self.server_ip = self.config.get(section, "SERVER_IP")
		self.server_port = self.config.get(section, "SERVER_PORT")
		self.account = self.config.get(section, "ACCOUNT")
		self.password = self.config.get(section, "PASSWORD")

		section = "CONTROL"
		self.sleep = self.config.getfloat(section, "sleep_time")

	def runProcess(self) :	
		# 실행
		pass


	def run(self):
		self.setLog()
		self.setDatas()
		self.runProcess()
	



if __name__ == '__main__':
    processor = Worker(sys.argv)

    processor.run()
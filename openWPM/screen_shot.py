import os
from hashlib import md5

from selenium import webdriver

from openwpm.commands.types import BaseCommand
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

from openwpm.commands.types import BaseCommand
from openwpm.config import BrowserParams, ManagerParams
from openwpm.socket_interface import ClientSocket

class ScreenShotCommand(BaseCommand):
	def __init__(self, suffix):
		self.suffix = suffix

	def __repr__(self):
		return "SaveScreenshotCommand({})".format(self.suffix)

	def execute(
			self,
			webdriver,
			browser_params,
			manager_params,
			extension_socket,
	):
		if self.suffix != "":
			self.suffix = "-" + self.suffix

		urlhash = md5(webdriver.current_url.encode("utf-8")).hexdigest()
		outname = os.path.join(
			manager_params.screenshot_path,
			"%i-%s%s.png" % (self.visit_id, urlhash, self.suffix),
		)
		webdriver.save_screenshot(outname)


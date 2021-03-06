# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt 

from __future__ import unicode_literals
import frappe


class DocType:
	def __init__(self, doc, doclist=[]):
		self.doc = doc
		self.doclist = doclist
	
	def validate(self):
		self.set_as_default()
		
		# clear the cache so that the new letter head is uploaded
		frappe.clear_cache()
		
	def set_as_default(self):
		from frappe.utils import set_default
		if not self.doc.is_default:
			if not frappe.db.sql("""select count(*) from `tabLetter Head` where ifnull(is_default,0)=1"""):
				self.doc.is_default = 1
		if self.doc.is_default:
			frappe.db.sql("update `tabLetter Head` set is_default=0 where name != %s",
				self.doc.name)
			set_default('letter_head', self.doc.name)

			# update control panel - so it loads new letter directly
			frappe.db.set_value('Control Panel', None, 'letter_head', self.doc.content)
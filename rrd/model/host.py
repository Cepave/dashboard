#-*- coding:utf-8 -*-
from rrd.store import portal_db_conn as db_conn

"""
* @class name:      Host(object)
* @description:     This class implements search method for "host" table.
* @related issues:  OWL-295
* @param:           object
* @return:          void
* @author:          Don Hsieh
* @since:           01/25/2016
* @last modified:   01/25/2016
* @called by:       def api_get_counters()
*                    in rrd/view/api.py
*                   def chart()
*                    in rrd/view/chart.py
"""
class Host(object):
	def __init__(self, id, hostname):
		self.id = str(id)
		self.name = hostname

	def __repr__(self):
		return "<Host id=%s, name=%s>" %(self.id, self.name)
	__str__ = __repr__


	@classmethod
	def search(cls, host_ids):
		if not host_ids:
			return []

		holders = ["%s" for x in host_ids]
		placeholder = ",".join(holders)
		args = host_ids
		cursor = db_conn.execute('''select id, hostname from host where id in (''' + placeholder + ''')''', args)
		rows = cursor.fetchall()
		cursor and cursor.close()
		return [cls(*row) for row in rows]

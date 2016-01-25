#-*- coding:utf-8 -*-
from rrd.store import portal_db_conn as db_conn

"""
* @class name:      Group(object)
* @description:     This class implements search method for "grp" table.
* @related issues:  OWL-295
* @param:           object
* @return:          void
* @author:          Don Hsieh
* @since:           01/25/2016
* @last modified:   01/25/2016
* @called by:       def api_groups()
*                   def api_get_counters()
*                    in rrd/view/api.py
"""
class Group(object):
	def __init__(self, id, grp_name):
		self.id = str(id)
		self.name = grp_name

	def __repr__(self):
		return "<Group id=%s, name=%s>" %(self.id, self.name)
	__str__ = __repr__

	@classmethod
	def search(cls, qs):
		args = []
		for q in qs:
			args.append("%"+q+"%")

		sql = '''select id, grp_name from grp where id > 0'''
		for q in qs:
			sql += ''' and grp_name like %s'''

		cursor = db_conn.execute(sql, args)
		rows = cursor.fetchall()
		cursor and cursor.close()

		return [cls(*row) for row in rows]

	@classmethod
	def gets_by_group(cls, groups):
		if not groups:
			return []

		holders = ["%s" for x in groups]
		placeholder = ",".join(holders)
		args = groups

		cursor = db_conn.execute('''select id, grp_name from grp where grp_name in (''' + placeholder + ''')''', args)
		rows = cursor.fetchall()
		cursor and cursor.close()

		return [cls(*row) for row in rows]

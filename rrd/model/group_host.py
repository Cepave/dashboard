#-*- coding:utf-8 -*-
from rrd.store import portal_db_conn as db_conn

"""
* @class name:      GroupHost(object)
* @description:     This class implements search method for "grp_host" table.
* @related issues:  OWL-295
* @param:           object
* @return:          void
* @author:          Don Hsieh
* @since:           01/25/2016
* @last modified:   01/25/2016
* @called by:       def api_get_counters()
*                    in rrd/view/api.py
*                   def chart()
*                   def charts()
*                    in rrd/view/chart.py
"""
class GroupHost(object):
	def __init__(self, grp_id, host_id):
		self.groupId = str(grp_id)
		self.hostId = str(host_id)

	def __repr__(self):
		return "<GroupHost groupId=%s, hostId=%s>" %(self.groupId, self.hostId)
	__str__ = __repr__


	@classmethod
	def search(cls, group_ids):
		if not group_ids:
			return []

		holders = ["%s" for x in group_ids]
		placeholder = ",".join(holders)
		args = group_ids
		cursor = db_conn.execute('''select grp_id, host_id from grp_host where grp_id in (''' + placeholder + ''')''', args)
		rows = cursor.fetchall()
		cursor and cursor.close()
		return [cls(*row) for row in rows]

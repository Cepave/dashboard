#-*- coding:utf-8 -*-
from rrd.store import graph_db_conn as db_conn
import re

class EndpointCounter(object):
    def __init__(self, id, endpoint_id, counter, step, type_):
        self.id = str(id)
        self.endpoint_id = str(endpoint_id)
        self.counter = counter
        self.step = step
        self.type_ = type_

    def __repr__(self):
        return "<EndpointCounter id=%s, endpoint_id=%s, counter=%s>" %(self.id, self.endpoint_id, self.counter)
    __str__ = __repr__

    def tag_query(tags, args, tagname):
        if tagname in tags:
            sql += ''' and ('''
            for t in tags[tagname][:-1]:
                args.append("%"+t+"%")
                sql += ''' counter like %s or'''
            args.append("%"+tags[tagname][-1]+"%")
            sql += ''' counter like %s )'''

    @classmethod
    def search_in_endpoint_ids(cls, qs, endpoint_ids, start=0, limit=100):
        if not endpoint_ids:
            return []

        holders = ["%s" for x in endpoint_ids]
        placeholder = ",".join(holders)

        args = endpoint_ids

        sql = '''select id, endpoint_id, counter, step, type from endpoint_counter where endpoint_id in (''' +placeholder+ ''') '''
        tags = {}
        is_packet_loss_rate = False
        is_average = False

        for q in qs:
            match = re.match('([^\0]+)=([^\0]+)', q)
            if match:
                tags[match.group(1)] = match.group(2).split(',')
            else:
                if "packet-loss-rate" in q:
                    q = "packets-sent"
                    is_packet_loss_rate = True
                elif "average" in q:
                    q = "transmission-time"
                    is_average = True
                args.append("%"+q+"%")
                sql += ''' and counter like %s'''

        if 'isp' in tags:
            sql += tag_query(tags, args, 'isp')
        if 'province' in tags:
            sql += tag_query(tags, args, 'isp')
        if 'city' in tags:
            sql += tag_query(tags, args, 'isp')
        if 'tag' in tags:
            sql += tag_query(tags, args, 'isp')

        args += [start, limit]
        sql += ''' limit %s,%s'''

        cursor = db_conn.execute(sql, args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        if is_packet_loss_rate or is_average:
            rows = list(rows)
            # clone the first one and then set the filed of NQM
            row = list(rows[0]) 
            if is_packet_loss_rate:
                row[2] = 'packet-loss-rate'
            elif is_average:
                row[2] = 'average'
            rows = (rows + [(row)])

        return [cls(*row) for row in rows]

    @classmethod
    def gets_by_endpoint_ids(cls, endpoint_ids, start=0, limit=100):
        if not endpoint_ids:
            return []

        holders = ["%s" for x in endpoint_ids]
        placeholder = ",".join(holders)
        args = endpoint_ids + [start, limit]

        cursor = db_conn.execute('''select id, endpoint_id, counter, step, type from endpoint_counter where endpoint_id in ('''+placeholder+''') limit %s, %s''', args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

    @classmethod
    def gets(cls, ids, deadline=0):
        if not ids:
            return []

        holders = ["%s" for x in ids]
        placeholder = ",".join(holders)
        args = ids + [start, limit]

        cursor = db_conn.execute('''select id, endpoint, ts from endpoint where id in ('''+placeholder+''') and ts > %s''', args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

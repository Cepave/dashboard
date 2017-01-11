# -*- coding:utf-8 -*-
import json
from flask import Blueprint, request

from rrd.store import dashboard_db_conn as db_con
from rrd.model.endpoint import Endpoint
from rrd.model.endpoint_counter import EndpointCounter
from rrd.model.graph import TmpGraph
from rrd.model.group import Group
from rrd.model.group_host import GroupHost
from rrd.model.host import Host
from rrd.model.tag_endpoint import TagEndpoint

bp = Blueprint('api', __name__)


@bp.route("/api/health")
def health_check():
    resp = {
        "status": "ok",
        "msg": "system work well"
    }
    if str(db_con._conn) == "None":
	#reconnect again
	db_con.connect()
	if str(db_con._conn) == "None":
		resp = {"status": "failed",
			"msg": "dashboard got problem now, please contact system administrator"
		       }
    return json.dumps(resp)

"""
* @def name:        api_groups()
* @description:     This function returns hostgroup names filtered by keywords.
* @related issues:  OWL-295
* @param:           void
* @return:          JSON json.dumps(ret)
* @author:          Don Hsieh
* @since:           01/22/2016
* @last modified:   01/25/2016
* @called by:       function fn_list_endpoints()
*                    in rrd/static/js/xperf.js
"""
@bp.route("/api/groups")
def api_groups():
    ret = {
        "ok": False,
        "msg": "",
        "data": [],
    }

    q = request.args.get("q") or ""
    if not q:
        ret["msg"] = "no query params given"
        return json.dumps(ret)

    groups = Group.search(q.split())
    groups_str = [x.name for x in groups]
    groups_str.sort()
    ret['data'] = groups_str
    ret['ok'] = True

    return json.dumps(ret)


@bp.route("/api/endpoints")
def api_endpoints():
    ret = {
        "ok": False,
        "msg": "",
        "data": [],
    }

    q = request.args.get("q") or ""
    raw_tag = request.args.get("tags") or ""
    tags = raw_tag and [x.strip() for x in raw_tag.split(",")] or []
    limit = int(request.args.get("limit") or 100)
    regex_query = request.args.get("regex_query") or "0"

    if not q and not tags:
        ret["msg"] = "no query params given"
        return json.dumps(ret)

    endpoints = []

    if tags and q:
        endpoint_ids = TagEndpoint.get_endpoint_ids(tags, limit=limit) or []
        endpoints = Endpoint.search_in_ids(q.split(), endpoint_ids)
    elif tags:
        endpoint_ids = TagEndpoint.get_endpoint_ids(tags, limit=limit) or []
        endpoints = Endpoint.gets(endpoint_ids)
    elif regex_query == "1":
        endpoints = Endpoint.search_regexp(q.split(), limit=limit)
    else:
        endpoints = Endpoint.search(q.split(), limit=limit)

    endpoints_str = [x.endpoint for x in endpoints]
    endpoints_str.sort()
    ret['data'] = endpoints_str
    ret['ok'] = True

    return json.dumps(ret)


@bp.route("/api/counters", methods=["POST"])
def api_get_counters():
    ret = {
        "ok": False,
        "msg": "",
        "data": [],
    }
    endpoints = request.form.get("endpoints") or ""
    endpoints = endpoints and json.loads(endpoints)
    q = request.form.get("q") or ""
    limit = int(request.form.get("limit") or 100)

    nethelp = request.form.get("nethelp") or ""
    if not (endpoints or q):
        ret['msg'] = "no endpoints or counter given"
        return json.dumps(ret)

    endpoint_objs = Endpoint.gets_by_endpoint(endpoints)
    endpoint_ids = [x.id for x in endpoint_objs]
    group_ids = []
    if not endpoint_ids:
        group_objs = Group.gets_by_group(endpoints)
        group_ids = [x.id for x in group_objs]
        grouphost_objs = GroupHost.search(group_ids)
        host_ids = [x.hostId for x in grouphost_objs]
        host_objs = Host.search(host_ids)
        host_names = [x.name for x in host_objs]
        endpoint_objs = Endpoint.gets_by_endpoint(host_names)
        endpoint_ids = [x.id for x in endpoint_objs]

        if not endpoint_ids:
            ret['msg'] = "no endpoints in graph"
            return json.dumps(ret)

    qs = q.split()
    if nethelp == "true":
        ecs = EndpointCounter.search_in_endpoint_ids(qs, endpoint_ids, limit=100)
    elif len(group_ids) > 0:
        limit = 5000
    if len(qs) > 0:
        ecs = EndpointCounter.search_in_endpoint_ids(qs, endpoint_ids, limit=limit)
    else:
        ecs = EndpointCounter.gets_by_endpoint_ids(endpoint_ids, limit=limit)

    if not ecs:
        ret["msg"] = "no counters in graph"
        return json.dumps(ret)

    counters_map = {}
    for x in ecs:
        counters_map[x.counter] = [x.counter, x.type_, x.step]
    sorted_counters = sorted(counters_map.keys())
    sorted_values = [counters_map[x] for x in sorted_counters]

    ret['data'] = sorted_values
    ret['ok'] = True

    return json.dumps(ret)

@bp.route("/api/tmpgraph", methods=["POST",])
def api_create_tmpgraph():
    d = request.data
    jdata = json.loads(d)
    endpoints = jdata.get("endpoints") or []
    counters = jdata.get("counters") or []
    id_ = TmpGraph.add(endpoints, counters)

    ret = {
        "ok": False,
        "id": id_,
    }
    if id_:
        ret['ok'] = True
        return json.dumps(ret)
    else:
        return json.dumps(ret)

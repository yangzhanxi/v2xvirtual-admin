import logging

from flask import Blueprint, session
from flask_jwt_extended import jwt_required
from flask_security import roles_accepted

from const import ADMIN_ROLE, APP_LOGGER
from services.network_management.network_mgmt_handler import (part_num_handler,
                                                              ports_handler)

LOG = logging.getLogger(APP_LOGGER)

net = Blueprint("network", __name__)


@net.get("/ports")
@jwt_required()
@roles_accepted(ADMIN_ROLE)
def get_licenses():
    """
    GET ports view.
    """
    session.permanent = True

    return ports_handler()
    # return mock_ports()


@net.get("/partnum")
@jwt_required()
@roles_accepted(ADMIN_ROLE)
def get_part_num():
    """
    GET part num view.
    """
    session.permanent = True

    return part_num_handler()
    # return mock_part_num()


def mock_ports():
    ret = [
        {
            "address": {
                "label": "IP Address", "value": "172.16.20.22"},
            "auto_negotiation": {
                "label": "Auto-Negotiation", "value": "true"},
            "auto_negotiation_role": {
                "label": "Auto-Negotiation Role", "value": "MASTER"},
            "duplex_mode": {
                "label": "Duplex Mode", "value": "FULL"},
            "gateway": {
                "label": "Gateway", "value": ""},
            "ip_version": {
                "label": "IP version", "value": "IPv4"},
            "link_status": {
                "label": "Link Status", "value": "UP"},
            "line_speed": {
                "label": "Line Speed", "value": "Speed"},
            "netmask": {
                "label": "Netmask", "value": "255.255.255.0"},
            "port_handel": {
                "label": "Port Handel", "value": "port1"},
            "port_name": {
                "label": "Port Name", "value": "slot1port1"}
        },
        {
            "address": {
                "label": "IP Address", "value": "172.16.21.22"},
            "auto_negotiation": {
                "label": "Auto-Negotiation", "value": "true"},
            "auto_negotiation_role": {
                "label": "Auto-Negotiation Role", "value": "MASTER"},
            "duplex_mode": {
                "label": "Duplex Mode", "value": "FULL"},
            "gateway": {
                "label": "Gateway", "value": ""},
            "ip_version": {
                "label": "IP version", "value": "IPv4"},
            "link_status": {
                "label": "Link Status", "value": "DOWN"},
            "line_speed": {
                "label": "Line Speed", "value": "Speed"},
            "netmask": {
                "label": "Netmask", "value": "255.255.255.0"},
            "port_handel": {
                "label": "Port Handel", "value": "port1"},
            "port_name": {
                "label": "Port Name", "value": "slot1port2"}
        },
        {
            "address": {
                "label": "IP Address", "value": "172.16.22.22"},
            "auto_negotiation": {
                "label": "Auto-Negotiation", "value": "true"},
            "auto_negotiation_role": {
                "label": "Auto-Negotiation Role", "value": "MASTER"},
            "duplex_mode": {
                "label": "Duplex Mode", "value": "FULL"},
            "gateway": {
                "label": "Gateway", "value": ""},
            "ip_version": {
                "label": "IP version", "value": "IPv4"},
            "link_status": {
                "label": "Link Status", "value": "DOWN"},
            "line_speed": {
                "label": "Line Speed", "value": "Speed"},
            "netmask": {
                "label": "Netmask", "value": "255.255.255.0"},
            "port_handel": {
                "label": "Port Handel", "value": "port1"},
            "port_name": {
                "label": "Port Name", "value": "slot1port3"}
        },
        {
            "address": {
                "label": "IP Address", "value": "172.16.23.22"},
            "auto_negotiation": {
                "label": "Auto-Negotiation", "value": "true"},
            "auto_negotiation_role": {
                "label": "Auto-Negotiation Role", "value": "MASTER"},
            "duplex_mode": {
                "label": "Duplex Mode", "value": "FULL"},
            "gateway": {
                "label": "Gateway", "value": ""},
            "ip_version": {
                "label": "IP version", "value": "IPv4"},
            "link_status": {
                "label": "Link Status", "value": "ERROR"},
            "line_speed": {
                "label": "Line Speed", "value": "Speed"},
            "netmask": {
                "label": "Netmask", "value": "255.255.255.0"},
            "port_handel": {
                "label": "Port Handel", "value": "port1"},
            "port_name": {
                "label": "Port Name", "value": "slot1port4"}
        }
    ]

    return ret


def mock_part_num():
    return {"part_num": "SPT-C50"}

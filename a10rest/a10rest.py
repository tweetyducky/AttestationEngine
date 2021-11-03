# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import os
import sys

from a10.asvr import elements, policies, attestation, claims, expectedvalues, results, types
from a10.structures import constants
from flask import Flask, request, send_from_directory, jsonify

from flask_swagger import swagger

print(sys.path)

a10rest = Flask(__name__)


#
# Home
#



@a10rest.route("/")
def hello():
    return "Hello from A10REST"




#
# Swagger - documentation for OpenAPI
#

@a10rest.route("/spec")
def spec():
    swag = swagger(a10rest)
    swag['info']['version'] = "1.0"
    swag['info']['description'] = "The A10 REST API Server"
    swag['info']['title'] = "A10REST"
    swag['title']= "A10REST"
    return jsonify(swag)



#
# ELEMENTS (ALL OF THEM)
#

@a10rest.route("/elements", methods=['GET'])
def getelements():
    """
    Gets a list of all elements
    ---
    get:
       responses:
         - 200:
            content:
                application/json:
                    schema: list itemid
    """
    es = [ x['itemid'] for x in elements.getElements() ]
    print("ES is ",es)
    return str(es), 200


@a10rest.route("/elements/types", methods=['GET'])
def getTypes():

    ts = str(types.getTypes())

    return ts, 200

#
# ELEMENT (SINGULAR)
#



@a10rest.route("/element/<itemid>", methods=['GET'])
def getelement(itemid):
    """
    Gets the details of a specific element
    ---
    get:
       parameters:
         - in: itemid
           schema: Item ID
       responses:
         - 404
         - 200:
            content:
                application/json:
                    schema: Element
    """
    elem = elements.getElement(itemid)

    if elem.rc() != constants.SUCCESS:
        return elem.msg(), 404
    else:
        return elem.msg(), 200


@a10rest.route("/element", methods=['POST'])
def addElement():
    content = request.json
    print("content", content)

    e = elements.addElement(content)

    if e[1] != constants.SUCCESS:
        return e[0], 400
    else:
        return e[0], 200


@a10rest.route("/element", methods=['DELETE'])
def deleteElement():
    itemid = request.args.get('itemid')
    print("itemid", itemid)
    e = elements.deleteElement(itemid)

    if e[1] != constants.SUCCESS:
        return e[0], 404
    else:
        return e[0], 200


@a10rest.route("/element", methods=['PUT'])
def updateElement():
    content = request.json
    print("content", content)

    e = elements.updateElement(content)

    if e[1] != constants.SUCCESS:
        return e[0], 400
    else:
        return e[0], 200





#
# POLICIES
#
@a10rest.route("/policies", methods=['GET'])
def getpolicies():

    ps = [ x['itemid'] for x in policies.getPolicies() ]
    print("ES is ",ps)
    return str(ps), 200

@a10rest.route("/policy/<itemid>", methods=['GET'])
def getpolicy(itemid):

    print("itemid", itemid)
    e = policies.getPolicy(itemid)

    if e.rc() != constants.SUCCESS:
        return e.msg(), 404
    else:
        return e.msg(), 200


@a10rest.route("/policy", methods=['POST'])
def addPolicy():
    content = request.json
    print("content", content)

    e = policies.addPolicy(content)

    if e.rc() != constants.SUCCESS:
        return e.msg(), 400
    else:
        return e.msg(), 200


@a10rest.route("/policy", methods=['DELETE'])
def deletePolicy():
    itemid = request.args.get('itemid')
    print("itemid", itemid)
    e = policies.deletePolicy(itemid)

    if e.rc() != constants.SUCCESS:
        return e.msg(), 404
    else:
        return e.msg(), 200


@a10rest.route("/policy", methods=['PUT'])
def updatePolicy():
    content = request.json
    print("content", content)

    e = policies.updatePolicy(content)

    if e.rc() != constants.SUCCESS:
        return e.msg(), 400
    else:
        return e.msg(), 200


#
# EXPECTED VALUES
#


@a10rest.route("/expectedvalue/<itemid>", methods=['GET'])
def getEV(itemid):
    print("itemid", itemid)
    e = expectedValues.getExpectedValue(itemid)

    if e.rc() != constants.SUCCESS:
        return e.msg(), 404
    else:
        return e.msg(), 200




@a10rest.route("/expectedvalue/<eid>/<pid>", methods=['GET'])
def getEVep(eid,pid):
    
    print(" eid",eid," pid",pid)
    e = expectedValues.getExpectedValueByElementPolicyIDs(typ,eid,pid)
    
    if e.rc() != constants.SUCCESS:
        return e.msg(),404
    else:
        return e.msg(),200


@a10rest.route("/expectedvalue", methods=['POST'])
def addEV():
    content = request.json
    print("content", content)

    e = expectedValues.addExpectedValue(content)

    if e.rc() != constants.SUCCESS:
        return e.msg(), 400
    else:
        return e.msg(), 200


@a10rest.route("/expectedvalue/<itemid>", methods=['DELETE'])
def deleteEV(itemid):
    print("itemid", itemid)
    e = expectedValues.deleteExpectedValue(itemid)

    if e.rc() != constants.SUCCESS:
        return e.msg(), 404
    else:
        return e.msg(), 200


@a10rest.route("/expectedvalue", methods=['PUT'])
def updateEV():
    content = request.json
    print("content", content)

    e = expectedValues.updateExpectedValue(content)

    if e.rc() != constants.SUCCESS:
        return e.msg(), 400
    else:
        return e.msg(), 200


#
# CLAIMS - decided not to allow writing claims for the moment as the ASVR libraires do this during attestation
#


@a10rest.route("/claim/<itemid>", methods=['GET'])
def getclaim(itemid):
    print("itemid", itemid)
    e = claims.getClaimByID(itemid)

    if e.rc() != constants.SUCCESS:
        return e.msg(), 404
    else:
        return e.msg(), 200


#
# RESULTS - decided not to allow writing claims for the moment as the ASVR libraires do this during attestation
#


@a10rest.route("/result/<itemid>", methods=['GET'])
def getresult(itemid):
    print("itemid", itemid)
    e = results.getResultByID(itemid)

    if e.rc() != constants.SUCCESS:
        return e.msg(), 404
    else:
        return e.msg(), 200


#
# ATTESTATION and VERIFICATION
#


@a10rest.route("/attest", methods=['POST'])
def attest():
    content = request.json
    print("content", content)
    eid = content["eid"]
    pid = content["pid"]
    cps = content["cps"]

    e = attestation.attest(eid, pid, cps)

    if e.rc() != constants.SUCCESS:
        return e.msg(), 400
    else:
        return e.msg(), 200


@a10rest.route("/verify", methods=['POST'])
def verify():
    content = request.json
    print("content", content)
    cid = content["cid"]
    rul = content["rule"]

    e = attestation.verify(cid, rul)

    if e.rc() != constants.SUCCESS:
        return e.msg(), 400
    else:
        return e.msg(), 200


#
# Main
#


def main(cert, key, config_filename='a10rest.conf'):
    a10rest.config.from_pyfile(config_filename)
    if cert and key:
        a10rest.run(debug=a10rest.config['FLASKDEBUG'], threaded=a10rest.config['FLASKTHREADED'],
                    host=a10rest.config['DEFAULTHOST'],
                    port=a10rest.config['DEFAULTPORT'], ssl_context=(cert, key))
    else:
        a10rest.run(debug=a10rest.config['FLASKDEBUG'], threaded=a10rest.config['FLASKTHREADED'],
                    host=a10rest.config['DEFAULTHOST'],
                    port=a10rest.config['DEFAULTPORT'])


if __name__ == '__main__':
    print("A10REST Starting")
    main('', '')

# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import sys,os
import logging, ConfigParser, thread, subprocess, inspect, pickle, json, socket, zipfile, shutil, urllib, re, time, hashlib, urllib, base64

os.chdir(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
sys.path.insert(0, os.getcwd())
sys.path.append(os.path.abspath('lib'))

import sleekxmpp
import logging
import logging.config

class ServiceTester(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.jid=jid
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # MUC
        self.register_plugin('xep_0060') # MUC
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0078') # Non-SASL Authentication
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0249') # Direct MUC invitation
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, signal):
      log=logging.getLogger("serviceTester")
      if signal['type'] in ('normal', 'chat'):
                line = signal['body'] 
                log.info('Received XMPP bus signal: "%s"', line)
                self.handleSignal(line, signal['from'])
                 
    def run(self):
        if self.connect(("172.21.160.51",5223),use_tls=False, use_ssl=True):
            self.channelJid = "default@conference.whale.nurc.nato.int"
            self.busResource = "admin@whale.nurc.nato.int"
            self.plugin['xep_0045'].joinMUC(self.channelJid, self.busResource, password="Crociera100!")

            self.add_event_handler('muc::%s::got_online' % self.channelJid, self.gotOnline)

            print("in the loop...")
            self.process(block=True)
        else:
            print("Unable to connect.")

    def gotOnline(self, presence):
        ''' If got online event fired:
                - if self gotOnline: configureChat
                - if service got online: invite
        
            @param msg: the got online msg
        '''
        if 'master' in str(presence['muc']['nick']):
            # Send XMPP invitation
            self.sendInvitation(presence['from'])

    def sendInvitation(self, servicejid):
        ''' send invitation to a service to register with the orchestrator
        
            @param jid: the jid which should be invited
        '''
        log=logging.getLogger("serviceTester")
        log.debug('Send Invitation to %s', servicejid)
        self.send_message(servicejid, mbody='topic=invite')
        pass

    def handleSignal(self, signal, origin):
        ''' Handle an incoming signal either via IPC BUS or XMPP
            @param signal: the message body
        '''
        
        signalArgs = None
        try:
            signalArgs = dict([tuple(each.strip().split('=')) for each in signal.split('&')])
        except:
            logging.error('Bus signal "%s" not supported (Error: %s)', signal, sys.exc_info()[0])
        
        # This is a list of supported bus signals that trigger an action  
        if signalArgs is not None:
            # Handle topic
            if signalArgs.has_key('topic'):
                if signalArgs['topic'] == 'register':
                    logging.info('Registering remote service "%s"' % signalArgs['service'])
                    logging.debug('Received a request for "%s"', signalArgs['service'])
                    self.invokeService(signalArgs['service'], origin)

                elif signalArgs['topic'] == 'progress':
                    logging.debug('received progress msg with value %s', signalArgs['message'])

                elif signalArgs['topic'] == 'log':
                    logging.debug('Received log msg with level %s msg=%s', signalArgs['level'],signalArgs['message'] )

                elif signalArgs['topic'] == 'completed':
                    msgbody='topic=finished' + '&id=' + self.pid
                    logging.debug( msgbody )
                    self.send_message(origin, mbody=msgbody)
                elif signalArgs['topic'] == 'error':
                    logging.debug( "**** error ****" )
                    logging.debug( msgbody )

                        
              
            else:
                logging.warn('Bus signal "%s" provides no topic', signal)

    def invokeService(self, service, origin):

        request = self.request_oaa_custom_riskmap()

        requestPickle = pickle.dumps(request)
        msgPickledURLEnc=urllib.quote(requestPickle)

        self.pid = hashlib.md5(str(time.time())).hexdigest()[-5:] + '_' + hashlib.md5('%s%s' % (service, urllib.quote(msgPickledURLEnc))).hexdigest()

        # Send Request to the Service
        msgbody='topic=request&service=' + service + '&id=' + self.pid + '&message=' + msgPickledURLEnc + '&baseURL=localhost'
        print msgbody
        self.send_message(origin, mbody=msgbody)

    def request_ok(self):
        request = {u'asset': [u'{\n    "Asset": {\n        "Pfa": 0.001, \n        "maxSpeed": 10, \n        "minSpeed": 2, \n        "maxHeading": 2.1, \n        "minHeading": -2.1, \n        "lat0": 10.0, \n        "cost": 1e-06, \n        "obsRange": 50000, \n        "heading0": 0, \n        "lon0": 62.0, \n        "type": "Frigate", \n        "id": 1, \n        "Pd": 0.6, \n        "name": "Ship 1"\n    }\n}',
            u'{\n    "Asset": {\n        "Pfa": 0.001, \n        "maxSpeed": 10, \n        "minSpeed": 2, \n        "maxHeading": 2.1, \n        "minHeading": -2.1, \n        "lat0": 10.0, \n        "cost": 1e-06, \n        "obsRange": 50000, \n        "heading0": 0, \n        "lon0": 60.0, \n        "type": "Frigate", \n        "id": 2, \n        "Pd": 0.6, \n        "name": "Ship 2"\n    }\n}',
            u'{\n    "Asset": {\n        "Pfa": 0.001, \n        "maxSpeed": 10, \n        "minSpeed": 2, \n        "maxHeading": 2.1, \n        "minHeading": -2.1, \n        "lat0": 5.0, \n        "cost": 1e-06, \n        "obsRange": 50000, \n        "heading0": 0, \n        "lon0": 58.0, \n        "type": "Frigate", \n        "id": 3, \n        "Pd": 0.6, \n        "name": "Ship 3"\n    }\n}',
            u'{\n    "Asset": {\n        "Pfa": 0.001, \n        "maxSpeed": 10, \n        "minSpeed": 2, \n        "maxHeading": 2.1, \n        "minHeading": -2.1, \n        "lat0": 5.0, \n        "cost": 1e-06, \n        "obsRange": 50000, \n        "heading0": 0, \n        "lon0": 58.0, \n        "type": "Frigate", \n        "id": 4, \n        "Pd": 0.6, \n        "name": "Ship 4"\n    }\n}'],
            'numberOfEvaluations': 600,
            'referenceDate': '20140901',
            'timeHorizon': 259200,
            'minlon' : 50.0,
            'maxlon' : 70.0,
            'minlat' : 0,
            'maxlat' : 20.0
            }
        return request

    def request_error(self):
        request = {u'asset': [
            u'{\n    "Asset": {\n        "Pfa": 1, \n        "maxSpeed": 1, \n        "minSpeed": 1, \n        "maxHeading": 1, \n        "minHeading": 1, \n        "lat0": 10.0, \n       "cost": 1, \n        "obsRange": 1, \n        "heading0": 1, \n        "lon0": 62.0, \n        "type": "Frigate", \n        "id": 1, \n        "Pd": 1, \n        "name": "Ship 1"\n    }\n}',
            u'{\n    "Asset": {\n        "Pfa": 1, \n        "maxSpeed": 1, \n        "minSpeed": 1, \n        "maxHeading": 1, \n        "minHeading": 1, \n        "lat0": 10.0, \n       "cost": 1, \n        "obsRange": 1, \n        "heading0": 1, \n        "lon0": 60.0, \n        "type": "Frigate", \n        "id": 2, \n        "Pd": 1, \n        "name": "Ship 2"\n    }\n}',
            u'{\n    "Asset": {\n        "Pfa": 1, \n        "maxSpeed": 1, \n        "minSpeed": 1, \n        "maxHeading": 1, \n        "minHeading": 1, \n        "lat0": 5.0, \n        "cost": 1, \n        "obsRange": 1, \n        "heading0": 1, \n        "lon0": 58.0, \n        "type": "Frigate", \n        "id": 3, \n        "Pd": 1, \n        "name": "Ship 3"\n    }\n}',
            u'{\n    "Asset": {\n        "Pfa": 1, \n        "maxSpeed": 1, \n        "minSpeed": 1, \n        "maxHeading": 1, \n        "minHeading": 1, \n        "lat0": 5.0, \n        "cost": 1, \n        "obsRange": 1, \n        "heading0": 1, \n        "lon0": 58.0, \n        "type": "Frigate", \n        "id": 4, \n        "Pd": 1, \n        "name": "Ship 4"\n    }\n}'],
            'numberOfEvaluations': 600,
            'referenceDate': '20140901',
            'timeHorizon': 259200,
            'minlon' : 50.0,
            'maxlon' : 70.0,
            'minlat' : 0,
            'maxlat' : 20.0
            }
        return request

    def request_riskmap(self):
        request = {
            'referenceDate' : '20150115',
            'minlon' : 50.0,
            'maxlon' : 70.0,
            'minlat' : 0,
            'maxlat' : 20.0,
            'baseWCSURL' : 'karapthos',
            'layerName' : 'testlayer',
            'outputFormat' : 'GeoTiff',
            'requestCRS' : '3426',
            'outputCRS' : '4326',
            'resX' :  200,
            'resY' :  200,
            'workdir' : 'd:\\tmp2\\'
            }

    def request_oaa_custom_riskmap(self):
        request = {
            'referenceDate' : '20150115',
            'numberOfEvaluations': 600,
            'timeHorizon': 259200,
            u'asset': [
                u'{\n    "Asset": {\n        "Pfa": 1, \n        "maxSpeed": 1, \n        "minSpeed": 1, \n        "maxHeading": 1, \n        "minHeading": 1, \n        "lat0": 10.0, \n       "cost": 1, \n        "obsRange": 1, \n        "heading0": 1, \n        "lon0": 62.0, \n        "type": "Frigate", \n        "id": 1, \n        "Pd": 1, \n        "name": "Ship 1"\n    }\n}',
                u'{\n    "Asset": {\n        "Pfa": 1, \n        "maxSpeed": 1, \n        "minSpeed": 1, \n        "maxHeading": 1, \n        "minHeading": 1, \n        "lat0": 10.0, \n       "cost": 1, \n        "obsRange": 1, \n        "heading0": 1, \n        "lon0": 60.0, \n        "type": "Frigate", \n        "id": 2, \n        "Pd": 1, \n        "name": "Ship 2"\n    }\n}',
                u'{\n    "Asset": {\n        "Pfa": 1, \n        "maxSpeed": 1, \n        "minSpeed": 1, \n        "maxHeading": 1, \n        "minHeading": 1, \n        "lat0": 5.0, \n        "cost": 1, \n        "obsRange": 1, \n        "heading0": 1, \n        "lon0": 58.0, \n        "type": "Frigate", \n        "id": 3, \n        "Pd": 1, \n        "name": "Ship 3"\n    }\n}',
                u'{\n    "Asset": {\n        "Pfa": 1, \n        "maxSpeed": 1, \n        "minSpeed": 1, \n        "maxHeading": 1, \n        "minHeading": 1, \n        "lat0": 5.0, \n        "cost": 1, \n        "obsRange": 1, \n        "heading0": 1, \n        "lon0": 58.0, \n        "type": "Frigate", \n        "id": 4, \n        "Pd": 1, \n        "name": "Ship 4"\n    }\n}'
            ],
            'minlon' : 50.0,
            'maxlon' : 70.0,
            'minlat' : 0,
            'maxlat' : 20.0,
            'owsBaseURL' : 'http://karpathos-dev/geoserver/wcs',
            'owsService' : 'WCS',
            'owsVersion' : '1.0.0',
            'requestCRS' : 'EPSG:4326',
            'timeResolution' : 3,
            'owsResourceIdentifier' : 'TDA:PAGM'
        }

        return request

if __name__ == '__main__':
    logging.config.fileConfig("logger_serviceTester.properties")
    log=logging.getLogger("serviceTester")
    log.debug("start tester")
    
    xmpp = ServiceTester("admin@whale.nurc.nato.int","Crociera100!")
    
    xmpp.run()

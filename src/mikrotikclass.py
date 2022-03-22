#Mikrotik Class
#2022
#Angelo.poggi@opti9tech.com

import sys
from common.creds import MIKROTIK_PASSWORD,MIKROTIK_USERNAME
from ssclass import smart
import routeros_api
import datetime
import smartsheet



class mtinit:
    def __init__(self,client,firewall):
        self.begin_time =datetime.datetime.now()
        self.ssinit = smart()
        self.sheetmap = self.ssinit.sheetMap(client)
        self.MIKTOIK_USERNAME = MIKROTIK_USERNAME
        self.MIKROTIK_PASSWORD = MIKROTIK_PASSWORD
        self.client = client
        self.firewall = firewall
        self.api = self.mt_connect_plain(firewall)
    def mt_connect_plain(self,firewall):
        '''Logins to the MT and inits the smartsheet stuff'''

        self.connection = routeros_api.RouterOsApiPool(
            firewall,
            username=MIKROTIK_USERNAME,
            password=MIKROTIK_PASSWORD,
            port=8728,
            plaintext_login=True
        )
        try:
            self.api = self.connection.get_api()
        except Exception as e:
            print(e)
            sys.exit(1)

        return self.api

    def dumpIPs(self):
        ''''Dumps IPs from fireewall into SSheet'''
        columnMap = self.ssinit.column_mapper(self.ssSDKinit, self.sheetMap[0])
        ipaddressData = self.api.get_resource('/ip/address').get()
        print("Dumping Interfaces and IP Addresses")
        for item in ipaddressData:
            row = smartsheet.models.Row()
            row.to_top = True
            row.cells.append({
                'column_id': columnMap[0]['id'],
                'value':     item.get('interface', '')
            })
            row.cells.append({
                'column_id': columnMap[1]['id'],
                'value':     item.get('address', '')
            })
            row.cells.append({
                'column_id': columnMap[2]['id'],
                'value':     item.get('comment', '')
            })
            row.cells.append({
                'column_id': columnMap[3]['id'],
                'value':     item.get('disabled', '')
            })
            self.self.ssSDKinit.Sheets.add_rows(
                self.sheetMap[0]['id'],
                [row])

    def dumproutes(self):
        '''Dumps the routing table'''
        columnMap = self.ssinit.column_mapper(self.ssSDKinit, self.self.sheetMap[1])
        routeData = self.api.get_resource('/ip/route').get()
        print("Dumping Routes")
        for item in routeData:
            row = smartsheet.models.Row()
            row.to_top = True
            row.cells.append({
                'column_id': columnMap[0]['id'],
                'value':     item.get('dst-address', '')
            })
            row.cells.append({
                'column_id': columnMap[1]['id'],
                'value':     item.get('pref-src', '')
            })
            row.cells.append({
                'column_id': columnMap[2]['id'],
                'value':     item.get('distance', '')
            })
            row.cells.append({
                'column_id': columnMap[3]['id'],
                'value':     item.get('comment', '')
            })
            row.cells.append({
                'column_id': columnMap[4]['id'],
                'value':     item.get('disabled', '')
            })
            self.ssSDKinit.Sheets.add_rows(
                self.sheetMap[1]['id'],
                [row])

    def dumpfilters(self):
        '''dumps the firewall filters'''
        filterData = self.api.get_resource('/ip/firewall/filter').get()
        columnMap = self.ssinit.column_mapper(self.ssSDKinit, self.sheetMap[2])
        print("Dumping Filter Rules")
        for item in filterData:
            row = smartsheet.models.Row()
            row.to_top = True
            row.cells.append({
                'column_id': columnMap[0]['id'],
                'value':     item.get('chain', '')
            })
            row.cells.append({
                'column_id': columnMap[1]['id'],
                'value':     item.get('action', '')
            })
            row.cells.append({
                'column_id': columnMap[2]['id'],
                'value':     item.get('protocol', '')
            })
            if 'src-address' in item.keys():
                row.cells.append({
                    'column_id': columnMap[3]['id'],
                    'value':     item.get('src-address', '')
                })
            elif 'src-address-list' in item.keys():
                row.cells.append({
                    'column_id': columnMap[3]['id'],
                    'value':     item.get('src-address-list', '')
                })
            if 'dst-address' in item.keys():
                row.cells.append({
                    'column_id': columnMap[4]['id'],
                    'value':     item.get('dst-address', '')
                })
            elif 'dst-address-list' in item.keys():
                row.cells.append({
                    'column_id': columnMap[4]['id'],
                    'value':     item.get('dst-address-list', '')
                })
            row.cells.append({
                'column_id': columnMap[5]['id'],
                'value':     item.get('src-port', '')
            })
            row.cells.append({
                'column_id': columnMap[6]['id'],
                'value':     item.get('dst-port', '')
            })
            row.cells.append({
                'column_id': columnMap[7]['id'],
                'value':     item.get('in-interface', '')
            })
            row.cells.append({
                'column_id': columnMap[8]['id'],
                'value':     item.get('out-interface', '')
            })
            row.cells.append({
                'column_id': columnMap[9]['id'],
                'value':     item.get('comment', '')
            })
            row.cells.append({
                'column_id': columnMap[10]['id'],
                'value':     item.get('disabled', '')
            })
            self.ssSDKinit.Sheets.add_rows(
                self.sheetMap[2]['id'],
                [row])

    def dumpNats(self):
        '''dumps all NAT rules'''
        natData = self.api.get_resource('/ip/firewall/nat').get()
        columnMap = self.ssinit.column_mapper(self.ssSDKinit, self.sheetMap[3])
        print("Dumping NAT Rules")
        for item in natData:
            row = smartsheet.models.Row()
            row.to_top = True
            row.cells.append({
                'column_id': columnMap[0]['id'],
                'value':     item.get('chain', '')
            })
            row.cells.append({
                'column_id': columnMap[1]['id'],
                'value':     item.get('action', '')
            })
            row.cells.append({
                'column_id': columnMap[2]['id'],
                'value':     item.get('src-address', '')
            })
            row.cells.append({
                'column_id': columnMap[4]['id'],
                'value':     item.get('dst-address', '')
            })
            row.cells.append({
                'column_id': columnMap[5]['id'],
                'value':     item.get('to-address', '')
            })
            row.cells.append({
                'column_id': columnMap[6]['id'],
                'value':     item.get('protocol', '')
            })
            row.cells.append({
                'column_id': columnMap[7]['id'],
                'value':     item.get('out-interface', '')
            })
            row.cells.append({
                'column_id': columnMap[8]['id'],
                'value':     item.get('comment', '')
            })
            row.cells.append({
                'column_id': columnMap[9]['id'],
                'value':     item.get('disabled', '')
            })
            self.ssSDKinit.Sheets.add_rows(
                self.sheetMap[3]['id'],
                [row])

    def dumpAdrLists(self):
        '''dumps all address lists'''
        addresslistData = self.api.get_resource('/ip/firewall/address-list').get
        columnMap = self.ssinit.column_mapper(self.ssSDKinit, self.sheetMap[4])
        print("Dumping Address lists")
        for item in addresslistData:
            row = smartsheet.models.Row()
            row.to_top = True
            row.cells.append({
                'column_id': columnMap[0]['id'],
                'value':     item.get('list', '')
            })
            row.cells.append({
                'column_id': columnMap[1]['id'],
                'value':     item.get('address', '')
            })
            row.cells.append({
                'column_id': columnMap[2]['id'],
                'value':     item.get('comment', '')
            })
            row.cells.append({
                'column_id': columnMap[4]['id'],
                'value':     item.get('disabled', '')
            })
            self.ssSDKinit.Sheets.add_rows(
                self.sheetMap[4]['id'],
                [row])

    def dumpipsecPh1(self):
        '''Dumps IPSEC phase 1'''
        phase1Data = self.api.get_resource('/ip/ipsec/peer').get()
        columnMap = self.ssinit.column_mapper(self.ssSDKinit, self.sheetMap[5])
        print("Dumping IPsec Phase 1")
        for item in phase1Data:
            row = smartsheet.models.Row()
            row.to_top = True
            row.cells.append({
                'column_id': columnMap[0]['id'],
                'value':     item.get('name', '')
            })
            row.cells.append({
                'column_id': columnMap[1]['id'],
                'value':     item.get('address', '')
            })
            row.cells.append({
                'column_id': columnMap[2]['id'],
                'value':     item.get('local-address', '')
            })
            row.cells.append({
                'column_id': columnMap[4]['id'],
                'value':     item.get('profile', '')
            })
            self.ssSDKinit.Sheets.add_rows(
                self.sheetMap[5]['id'],
                [row])
    def dumpipsecPh1Profile(self):
        '''dumps IPSEC phase 1 profiles'''
        phase1ProfileData = self.api.get_resource('/ip/ipsec/profile').get()
        columnMap = self.ssinit.column_mapper(self.ssSDKinit, self.sheetMap[6])
        print("Dumping IPsec Phase 1 Profiles")
        for item in phase1ProfileData:
            row = smartsheet.models.Row()
            row.to_top = True
            row.cells.append({
                'column_id': columnMap[0]['id'],
                'value':     item.get('name', '')
            })
            row.cells.append({
                'column_id': columnMap[1]['id'],
                'value':     item.get('hash-algorithm', '')
            })
            row.cells.append({
                'column_id': columnMap[2]['id'],
                'value':     item.get('enc-algorithm', '')
            })
            row.cells.append({
                'column_id': columnMap[3]['id'],
                'value':     item.get('dh-group', '')
            })
            row.cells.append({
                'column_id': columnMap[4]['id'],
                'value':     item.get('lifetime', '')
            })
            row.cells.append({
                'column_id': columnMap[5]['id'],
                'value':     item.get('nat-traversal', '')
            })
            self.ssSDKinit.Sheets.add_rows(
                self.sheetMap[6]['id'],
                [row])


    def dumpIpsecPh2(self):
        '''Dumps IPSEC phase 2'''
        phase2Data = self.api.get_resource('/ip/ipsec/policy').get()
        columnMap = self.ssinit.column_mapper(self.ssSDKinit, self.sheetMap[7])
        print("Dumping IPsec phase 2")
        for item in phase2Data:
            if 'default' in item.keys():
                continue
            else:
                row = smartsheet.models.Row()
                row.to_top = True
                row.cells.append({
                    'column_id': columnMap[0]['id'],
                    'value':     item.get('peer', '')
                })
                row.cells.append({
                    'column_id': columnMap[1]['id'],
                    'value':     item.get('src-address', '')
                })
                row.cells.append({
                    'column_id': columnMap[2]['id'],
                    'value':     item.get('dst-address', '')
                })
                row.cells.append({
                    'column_id': columnMap[3]['id'],
                    'value':     item.get('sa-src-address', '')
                })
                row.cells.append({
                    'column_id': columnMap[4]['id'],
                    'value':     item.get('sa-dst-address', '')
                })
                row.cells.append({
                    'column_id': columnMap[5]['id'],
                    'value':     item.get('comment', '')
                })
                row.cells.append({
                    'column_id': columnMap[6]['id'],
                    'value':     item.get('policy', '')
                })
                row.cells.append({
                    'column_id': columnMap[7]['id'],
                    'value':     item.get('disabled', '')
                })
                self.ssSDKinit.Sheets.add_rows(
                    self.sheetMap[7]['id'],
                    [row])

    def dumpAll(self):
        self.dumpIPs()
        self.dumproutes()
        self.dumpfilters()
        self.dumpNats()
        self.dumpAdrLists()
        self.dumpipsecPh1()
        self.dumpipsecPh1Profile()
        self.dumpIpsecPh2()
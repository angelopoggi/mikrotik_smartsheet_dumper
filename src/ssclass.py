#Mikrotik Audit Tool
#2022
#Angelo.poggi@opti9tech.com

import smartsheet
from common.creds import (
SMARTSHEET_ACCESS_TOKEN,
WORKSPACE_ID,
TEMPLATE_ID
)
import json

class smart:
    def __init__(self):
        self.SMARTSHEET_ACCESS_TOKEN = SMARTSHEET_ACCESS_TOKEN
        self.WORKSPACE_ID = WORKSPACE_ID
        self.TEMPLATE_ID = TEMPLATE_ID
        self.ssSDKinit = smartsheet.Smartsheet(SMARTSHEET_ACCESS_TOKEN)
    def ss_init(self,clientName, firewall):
        '''Initializes smartsheet and creates the folders and sheets required if not there'''
        if clientName.upper().startswith('CID'):
            pass
        else:
            print('Invalid client name, please ensure it follows this convention; "CID<NUMBER>"')
            exit()
        try:
            smartsheet_client = smartsheet.Smartsheet(SMARTSHEET_ACCESS_TOKEN)
        except Exception as e:
            raise (f'unable to connect to smartsheet. Ensure you have the proper access levels! \n {e} ')
        workspaceResponse = json.loads(smartsheet_client.Workspaces.get_workspace(WORKSPACE_ID).to_json())
        if 'folders' not in workspaceResponse:
            print("no folders in workspace, creating first client folder")
            smartsheet_client.Workspaces.create_folder_in_workspace(WORKSPACE_ID, clientName.upper())
            workspaceResponse = json.loads(smartsheet_client.Workspaces.get_workspace(WORKSPACE_ID).to_json())
        clientList = []
        for item in workspaceResponse['folders']:
            clientList.append(item['name'])
        if clientName.upper() in clientList:
            for item in workspaceResponse['folders']:
                if item['name'] == clientName.upper():
                    clientFolderID = item['id']
        else:
            print('New Client; Creating folder.')
            folderResponse = json.loads(
                smartsheet_client.Workspaces.create_folder_in_workspace(WORKSPACE_ID, clientName.upper()).to_json())
            clientFolderID = folderResponse['data']['id']
        subFolderResponse = json.loads(smartsheet_client.Folders.list_folders(clientFolderID).to_json())
        if 'data' not in subFolderResponse:
            print('no firewall folders for this client; creating new folder & sheets')
            newFirewallFolder = json.loads(
                smartsheet_client.Folders.create_folder_in_folder(clientFolderID, firewall.lower()).to_json())
            subFolderID = newFirewallFolder['data']['id']
            smartsheet_client.Folders.copy_folder(TEMPLATE_ID,
                                                  smartsheet.models.ContainerDestination({
                                                      'destination_id':   subFolderID,
                                                      'destination_type': 'folder',
                                                      'new_name':         'Audit Dashboard Resources'
                                                  }))
        else:
            folderMap = {}
            for i, item in enumerate(subFolderResponse['data']):
                folderMap[i] = ({
                    'Name': item['name'],
                    'id':   item['id']
                })
            for i, item in folderMap.items():
                if firewall.lower() == item['Name']:
                    print("found old firewall folder")
                    subFolderID = item['id']
                else:
                    print("Creating new folder for firewall")
                    smartsheet_client.Folders.create_folder_in_folder(clientFolderID, firewall.lower())
                    smartsheet_client.Folders.copy_folder(TEMPLATE_ID,
                                                          smartsheet.models.ContainerDestination({
                                                              'destination_id':   subFolderID,
                                                              'destination_type': 'folder',
                                                              'new_name':         f'{firewall.lower()} - Audit Dashboard Resources'
                                                          }))
        sheetResponse = json.loads(smartsheet_client.Folders.get_folder(subFolderID).to_json())
        if 'sheets' not in sheetResponse:
            self.create_sheet(subFolderID)
        else:
            print('Old sheets found; purging and creating new ones.')
            for item in sheetResponse['sheets']:
                smartsheet_client.Sheets.delete_sheet(item['id'])
            self.create_sheet(subFolderID)
        return subFolderID

    def column_mapper(self,smartsheet_client, sheetMap):
        '''Creates a map of the column for a given sheet'''
        self.columnMap = {}
        sheetResponse = json.loads(smartsheet_client.Sheets.get_sheet(sheetMap['id']).to_json())
        for i, item in enumerate(sheetResponse['columns']):
            self.columnMap[i] = ({
                'title': item['title'],
                'id':    item['id']
            })
        return self.columnMap

    def sheet_mapper(self, clientID):
        '''Creates a map of all the sheets, their names and IDs'''
        self.sheetMap = {}
        folderResponse = json.loads(self.ssSDKinit.Folders.get_folder(clientID).to_json())
        for i, item in enumerate(folderResponse['sheets']):
            self.sheetMap[i] = ({
                'Name': item['name'],
                'id':   item['id']
            })
        return self.sheetMap

    def create_sheet(self, clientFolerID):
        '''Creates all the actual sheets'''
        try:
            smartsheet_client = smartsheet.Smartsheet(SMARTSHEET_ACCESS_TOKEN)
        except Exception as e:
            raise (f'unable to connect to smartsheet. Ensure you have the proper access levels! \n {e} ')
        interfaceSheet = smartsheet.models.Sheet({
            'name':     'Interfaces & IP Address',
            'columns':  [{
                'title':   'Interface',
                'type':    'TEXT_NUMBER',
                'primary': True
            },
                {
                    'title': 'Address',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Comment',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Disabled',
                    'type':  'TEXT_NUMBER'
                }
            ],
            "textWrap": ["on"]
        })
        routeSheet = smartsheet.models.Sheet({
            'name':     'Routes',
            'columns':  [{
                'title':   'Dst. Address',
                'type':    'TEXT_NUMBER',
                'primary': True
            },
                {
                    'title': 'Pref. Source',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Distance',
                    'type':  'TEXT_NUMBER',
                },
                {
                    'title': 'Comment',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Disabled',
                    'type':  'TEXT_NUMBER'
                }
            ],
            "textWrap": ["on"]
        })
        filterSheet = smartsheet.models.Sheet({
            'name':     'Filter Rules',
            'columns':  [{
                'title':   'Chain',
                'type':    'TEXT_NUMBER',
                'primary': True
            },
                {
                    'title': 'Action',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Protocol',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Src. Address / Address List',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Dst. Address / Address List',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Src. Port',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Dst. Port',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'In Inteface',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Out Interface',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Comment',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Disabled',
                    'type':  'TEXT_NUMBER'
                }
            ],
            "textWrap": ["on"]
        })
        natSheet = smartsheet.models.Sheet({
            'name':     'NAT Rules',
            'columns':  [{
                'title':   'Chain',
                'type':    'TEXT_NUMBER',
                'primary': True
            },
                {
                    'title': 'Action',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Src. Address',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Dst. Address',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'To Address',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Protocol',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'To Ports',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Out Interface',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Comment',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Disabled',
                    'type':  'TEXT_NUMBER'
                }
            ],
            "textWrap": ["on"]
        })
        addresslistSheet = smartsheet.models.Sheet({
            'name':     'Address Lists',
            'columns':  [{
                'title':   'List Name',
                'type':    'TEXT_NUMBER',
                'primary': True
            },
                {
                    'title': 'IP Address',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Comment',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Date Created',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Disabled',
                    'type':  'TEXT_NUMBER'
                }
            ],
            "textWrap": ["on"]
        })
        ipsecPhase1Sheet = smartsheet.models.Sheet({
            'name':     'IPsec Phase 1',
            'columns':  [{
                'title':   'Name',
                'type':    'TEXT_NUMBER',
                'primary': True
            },
                {
                    'title': 'Peer Address',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Local Address',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Exchange Mode',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Encryption Profile',
                    'type':  'TEXT_NUMBER'
                },

            ],
            "textWrap": ["on"]
        })
        ipsecPhase1ProfileSheet = smartsheet.models.Sheet({
            'name':     'Phase 1 Profiles',
            'columns':  [{
                'title':   'Name',
                'type':    'TEXT_NUMBER',
                'primary': True
            },
                {
                    'title': 'Hash algorithm',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Encryption Algorithm',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'DH-Group',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Lifetime',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'NAT Traversal',
                    'type':  'TEXT_NUMBER'
                },
            ],
            "textWrap": ["on"]
        })
        ipsecPhase2Sheet = smartsheet.models.Sheet({
            'name':     'IPsec Phase 2',
            'columns':  [{
                'title':   'Peer',
                'type':    'TEXT_NUMBER',
                'primary': True
            },
                {
                    'title': 'Src. Address',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Dst. Address',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'SA-Src. Address',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'SA-Dst. Address',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Comment',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Policy',
                    'type':  'TEXT_NUMBER'
                },
                {
                    'title': 'Disabled',
                    'type':  'TEXT_NUMBER'
                },
            ],
            "textWrap": ["on"]
        })
        smartsheet_client.Folders.create_sheet_in_folder(clientFolerID, interfaceSheet)
        smartsheet_client.Folders.create_sheet_in_folder(clientFolerID, routeSheet)
        smartsheet_client.Folders.create_sheet_in_folder(clientFolerID, filterSheet)
        smartsheet_client.Folders.create_sheet_in_folder(clientFolerID, natSheet)
        smartsheet_client.Folders.create_sheet_in_folder(clientFolerID, addresslistSheet)
        smartsheet_client.Folders.create_sheet_in_folder(clientFolerID, ipsecPhase1Sheet)
        smartsheet_client.Folders.create_sheet_in_folder(clientFolerID, ipsecPhase1ProfileSheet)
        smartsheet_client.Folders.create_sheet_in_folder(clientFolerID, ipsecPhase2Sheet)

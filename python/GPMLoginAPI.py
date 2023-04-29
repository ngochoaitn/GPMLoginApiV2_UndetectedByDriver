import requests
class GPMLoginAPI(object):
    API_START_PATH = "/v2/start"
    API_STOP_PATH = "/v2/stop"
    API_CREATE_PATH = "/v2/create"
    API_UPDATE_PROXY_PATH = "/v2/update-proxy"
    API_UPDATE_NOTE_PATH = "/v2/update-note"
    API_PROFILE_LIST_PATH = "/v2/profiles"
    API_DELETE_PATH = "/v2/delete"

    _apiUrl = ''
    def __init__(self, apiUrl: str):
        self._apiUrl = apiUrl

    def GetProfiles(self):
        try:
            url = f"{self._apiUrl}{self.API_PROFILE_LIST_PATH}"
            print(url)
            resp = requests.get(url)
            return resp.json()
        except:
            print('error GetProfiles()')
            return None

    def Create(self, name: str, group : str = 'All', proxy: str = '', isNoiseCanvas: bool = False, fakeFont : bool = True, turnOnWebRTC : bool = True): #, saveType : int = 1):
        """
        Create a new profile
        :param int saveType: 1 => Local, 2 => Cloud
        """
        try:
            # Make api url
            url = f"{self._apiUrl}{self.API_CREATE_PATH}?name={name}&group={group}&proxy={proxy}"
            url += f"&canvas={'on' if isNoiseCanvas else 'off'}"
            url += f"&font={'on' if fakeFont else 'off'}"
            url += f"&webrtc={'on' if turnOnWebRTC else 'off'}"
            # url += f"&save_type={saveType}"
            # Call api
            resp = requests.get(url)
            return resp.json()
        except Exception as e:
            print(e)
            return None

    def UpdateProxy(self, profileId: str, proxy: str = ''):
        try:
            # Make api url
            url = f"{self._apiUrl}{self.API_UPDATE_PROXY_PATH}?id={profileId}&proxy={proxy}"
            # Call api
            resp = requests.get(url)
            return resp.text.lower() == "true"
        except Exception as e:
            print(e)
            return False

    def UpdateNote(self, profileId: str, note: str):
        try:
            # Make api url
            url = f"{self._apiUrl}{self.API_UPDATE_NOTE_PATH}?id={profileId}&note={note}"
            # Call api
            resp = requests.get(url)
            return resp.text.lower() == "true"
        except Exception as e:
            print(e)
            return False

    def Start(self, profileId: str, remoteDebugPort: int = 0, addinationArgs: str = ''):
        try:
            # Make api url
            url = f"{self._apiUrl}{self.API_START_PATH}?profile_id={profileId}"
            if(remoteDebugPort > 0):
                url += f"&remote_debug_port={remoteDebugPort}"
            if(addinationArgs != ''):
                url += f"&addination_args={addinationArgs}"
            
            # call api
            resp = requests.get(url)
            return resp.json()
        except Exception as e:
            print(e)
            return None

    def Stop(self, profileId: str):
        url = f"{self._apiUrl}{self.API_STOP_PATH}?profile_id={profileId}"
        requests.get(url)

    def Delete(self, profileId: str, mode: int = 2):
        url = f"{self._apiUrl}{self.API_DELETE_PATH}?profile_id={profileId}&mode={mode}"
        requests.get(url)
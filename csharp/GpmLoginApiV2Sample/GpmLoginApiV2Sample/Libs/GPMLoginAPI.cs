using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace GpmLoginApiV2Sample.Libs
{
    public class GPMLoginAPI
    {
        private string _apiUrl;

        private const string API_START_PATH = "/v2/start";
        private const string API_STOP_PATH = "/v2/stop";
        private const string API_CREATE_PATH = "/v2/create";
        private const string API_UPDATE_PROXY_PATH = "/v2/update-proxy";
        private const string API_UPDATE_NOTE_PATH = "/v2/update-note";
        private const string API_PROFILE_LIST_PATH = "/v2/profiles";
        private const string API_DELETE_PATH = "/v2/delete";

        /// <summary>
        /// Init with API_URL (get on GPM-LOGIN app)
        /// </summary>
        /// <param name="apiUrl">Eg: 127.0.0.1:57172</param>
        public GPMLoginAPI(string apiUrl)
        {
            if(apiUrl.EndsWith("/"))
                apiUrl = apiUrl.Substring(0, apiUrl.Length - 1);
            _apiUrl = apiUrl;
        }

        /// <summary>
        /// Start a profile by ID
        /// </summary>
        /// <param name="profileId"></param>
        /// <param name="remoteDebugPort"></param>
        /// <param name="addinationArgs"></param>
        /// <returns>View API document</returns>
        public JObject Start(string profileId, uint? remoteDebugPort = null, string addinationArgs = "")
        {
            // Make api url
            string url = _apiUrl + API_START_PATH + $"?profile_id={profileId}";
            if (remoteDebugPort != null) url += $"&remote_debug_port={remoteDebugPort}";
            if (!string.IsNullOrEmpty(addinationArgs)) url += $"&addination_args={addinationArgs}";

            // Call api
            string resp = httpRequest(url);
            return resp != null ? JObject.Parse(resp) : null;
        }

        public void Stop(string profileId)
        {
            string url = _apiUrl + API_STOP_PATH + $"?profile_id={profileId}";
            httpRequest(url);
        }

        /// <summary>
        /// Create profile on GPMLogin
        /// </summary>
        /// <param name="name"></param>
        /// <param name="group"></param>
        /// <param name="proxy"></param>
        /// <param name="isNoiseCanvas"></param>
        /// <param name="fakeFont">Default on</param>
        /// <param name="turnOnWebRTC">Default on</param>
        /// <param name="saveType">1 => Local, 2 => Cloud</param>
        /// <returns>View in API document</returns>
        public JObject Create(string name, string group="All", string proxy = "", bool isNoiseCanvas = false, bool fakeFont = true, bool turnOnWebRTC = true)//, int saveType = 1)
        {
            // Make api url
            string url = _apiUrl + API_CREATE_PATH + $"?name={name}&group={group}&proxy={proxy}";
            url += $"&canvas={(isNoiseCanvas ? "on" : "off")}";
            url += $"&font={(fakeFont ? "on" : "off")}";
            url += $"&webrtc={(turnOnWebRTC ? "on" : "off")}";
            //url += $"&save_type={saveType}";

            // Call api
            string resp = httpRequest(url);
            return resp != null ? JObject.Parse(resp) : null;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="proxy">Empty => Without proxy; Http Proxy => IP:Port OR IP:Port:User:Pass | Socks5 Proxy => socks5://IP:Port OR socks5://IP:Port:User:Pass</param>
        /// <returns></returns>
        public bool UpdateProxy(string porofileId, string proxy = "")
        {
            // Make api url
            string url = _apiUrl + API_UPDATE_PROXY_PATH + $"?id={porofileId}&proxy={proxy}";
           
            // Call api
            string resp = httpRequest(url);
            return resp?.ToLower() == "true";
        }

        public bool UpdateNote(string porofileId, string note)
        {
            // Make api url
            string url = _apiUrl + API_UPDATE_NOTE_PATH + $"?id={porofileId}&note={note}";

            // Call api
            string resp = httpRequest(url);
            return resp?.ToLower() == "true";
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="profileId"></param>
        /// <param name="mode">1 - Chỉ xóa trên app, 2 - Xóa cả trên app lẫn folder profile (Mặc định: 2)</param>
        public void Delete(string profileId, int mode = 2)
        {
            // Make api url
            string url = _apiUrl + API_DELETE_PATH + $"?profile_id={profileId}&mode={mode}";

            // Call api
            httpRequest(url);
        }

        public List<JObject> GetProfiles()
        {
            // Make api url
            string url = _apiUrl + API_PROFILE_LIST_PATH;

            // Call api
            string resp = httpRequest(url);
            return resp != null ? JsonConvert.DeserializeObject<List<JObject>>(resp) : null;
        }

        #region Helpers
        private string httpRequest(string url)
        {
            try
            {
                HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
                using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
                {
                    using (Stream stream = response.GetResponseStream())
                    {
                        using (StreamReader reader = new StreamReader(stream))
                        {
                            return reader.ReadToEnd();
                        }
                    }
                }
            }
            catch
            {
                return null;
            }
        }
        #endregion
    }
}

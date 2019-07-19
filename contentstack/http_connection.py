class HTTPConnection:

    def __init__(self, url: str, query: dict, headers: dict):

        if url is not None and query is not None and headers is not None:
            if len(url) > 0 and len(query) > 0 and len(headers) > 0:
                self.url = url
                self.query = query
                self.headers = headers
            else:
                raise TypeError('Arguments can not be empty')
        else:
            raise TypeError('Invalid Arguments')

    def get_result(self, url: str, query: dict, headers: dict) -> tuple:

        import requests
        from urllib import parse
        from requests import Response
        from contentstack.stack import SyncResult

        if url is not None and len(url) > 0:
            self.url = url
        if query is not None and len(query) > 0:
            self.query = query
        if headers is not None and len(headers) > 0:
            self.headers = headers

        # Adding user agent to headers
        self.headers.update(self.__user_agents())
        # Encoding query to string
        payload = parse.urlencode(query=self.query, encoding='UTF-8')

        try:

            # requesting for url, payload and headers
            response: Response = requests.get(self.url, params=payload, headers=self.headers)
            # if response.status_code = 200
            if response.ok:

                # Decode byte response to json
                result = response.json()
                # If result contains stack, return json response
                if 'stack' in result:
                    return result['stack']
                # If result contains entry, return Entry
                if 'entry' in result:
                    dict_entry = result['entry']
                    return self.__parse_entries(dict_entry)
                # If result contains entries, return list[Entry]
                if 'entries' in result:
                    entry_list = result['entries']
                    return self.__parse_entries(entry_list)
                # If result contains asset, return Asset
                if 'asset' in result:
                    dict_asset = result['asset']
                    return self.__parse_assets(dict_asset)
                # If result contains assets, return list[Asset]
                if 'assets' in result:
                    asset_list = result['assets']
                    return self.__parse_assets(asset_list)
                # If result contains content_type, return content_type json
                if 'content_type' in result:
                    return result['content_type']
                # If result contains items, return SyncResult json
                if 'items' in result:
                    sync_result = SyncResult().configure(result)
                    return sync_result

            else:
                # Decode byte response to json
                return response.json()

        except requests.RequestException as err:
            raise ConnectionError(err)

    @staticmethod
    def __parse_entries(result):
        from contentstack import Entry
        entries: list[Entry] = []
        entry = Entry()

        if result is not None and len(result) > 0:
            if isinstance(result, dict):
                return entry.configure(result)
            if isinstance(result, list):
                for entry_obj in result:
                    each_entry = Entry().configure(entry_obj)
                    entries.append(each_entry)
                return entries

    @staticmethod
    def __parse_assets(result):
        from contentstack import Asset
        assets: list[Asset] = []
        asset = Asset()

        if result is not None and len(result) > 0:
            if isinstance(result, dict):
                return asset.configure(result)
            if isinstance(result, list):
                for asset_obj in result:
                    itr_asset = asset.configure(asset_obj)
                    assets.append(itr_asset)
                return assets

    @staticmethod
    def __user_agents() -> dict:

        import contentstack
        import platform

        """
        Contentstack-User-Agent.
        
        """
        header = {'sdk': dict(name=contentstack.__package__, version=contentstack.__version__)}
        os_name = platform.system()

        if os_name == 'Darwin':
            os_name = 'macOS'

        elif not os_name or os_name == 'Java':
            os_name = None

        elif os_name and os_name not in ['macOS', 'Windows']:
            os_name = 'Linux'

        header['os'] = {
            'name': os_name,
            'version': platform.release()
        }
        local_headers = {'X-User-Agent': str(header), "Content-Type": 'application/json'}
        return local_headers

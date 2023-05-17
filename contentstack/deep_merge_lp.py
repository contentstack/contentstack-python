class DeepMergeMixin:

    def __init__(self, entry_response, lp_response):
        self.entry_response = entry_response
        self.lp_response = lp_response

        for lp_obj in self.lp_response:
            uid = lp_obj.get("uid")
            matching_objs = [entry_obj for entry_obj in entry_response if entry_obj.get("uid") == uid]
            if matching_objs:
                for matching_obj in matching_objs:
                    self._deep_merge(lp_obj, matching_obj)

    def _deep_merge(self, source, destination):
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                self._deep_merge(value, node)
            else:
                destination[key] = value
        return destination

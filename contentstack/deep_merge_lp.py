class DeepMergeMixin:

    def __init__(self, entry_response, lp_response):
        if not isinstance(entry_response, list) or not isinstance(lp_response, list):
            raise TypeError("Both entry_response and lp_response must be lists of dictionaries")

        self.entry_response = entry_response
        self.lp_response = lp_response
        self.merged_response = self._merge_entries(entry_response, lp_response)

    def _merge_entries(self, entry_list, lp_list):
        """Merge each LP entry into the corresponding entry response based on UID"""
        merged_entries = {entry["uid"]: entry.copy() for entry in entry_list}  # Convert to dict for easy lookup

        for lp_obj in lp_list:
            uid = lp_obj.get("uid")
            if uid in merged_entries:
                self._deep_merge(lp_obj, merged_entries[uid])
            else:
                merged_entries[uid] = lp_obj  # If LP object does not exist in entry_response, add it

        return list(merged_entries.values())  # Convert back to a list

    def _deep_merge(self, source, destination):
        if not isinstance(destination, dict) or not isinstance(source, dict):
            return source  # Return source if it's not a dict
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                self._deep_merge(value, node)
            else:
                destination[key] = value
        return destination

    def to_dict(self):
        return self.merged_response

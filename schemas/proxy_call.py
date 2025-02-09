import re
from marshmallow import validate, pre_load, fields
from plugins.shared_orch.app_objects import ma
from tools import VaultClient, session_project
from pylon.core.tools import log


class ProxyCallSchema(ma.Schema):
    method = fields.Str(validate=[
        validate.OneOf(['get', 'post', 'delete', 'put', 'patch'])
    ], required=True)
    url = fields.Url(required=True)
    payload = fields.Dict()


    @pre_load
    def unsecret_fields(self, data, **kwargs):
        url = data.get('url')
        if not url:
            return data
        
        secret_regex = r"{{\s*secret\.[\w]+\s*}}"
        secrets = re.findall(secret_regex, url)
        client = VaultClient.from_project(session_project.get())
        for secret in secrets:
            value = client.unsecret(secret)
            url = re.sub(secret, value, url)

        data['url'] = url
        return data



proxy_call_schema = ProxyCallSchema()






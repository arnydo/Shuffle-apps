import json
import ldap3
import asyncio
from ldap3 import Server, Connection, AUTO_BIND_NO_TLS, SUBTREE, BASE, ALL_ATTRIBUTES, ObjectDef, AttrDef, Reader, Entry, Attribute, OperationalAttribute
from walkoff_app_sdk.app_base import AppBase


class ADQuery(AppBase):
    __version__ = "1.0.0"
    app_name = "AD-Query"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    # Write your data inside this function
    async def search_samaccountname(self, domainName, serverName, userName, password, samaccountname, search_base):

        user = '{}\\{}'.format(domainName, userName)

        conn = Connection(Server(serverName, port=3269, use_ssl=True), auto_bind=AUTO_BIND_NO_TLS, user=user, password=password)

        print(conn,
            search_base,
            sep='\n')

        conn.search(
            search_base=search_base,
            search_filter=f'(samAccountName={samaccountname})',
            attributes=ALL_ATTRIBUTES
        )

        return json.loads(conn.response_to_json())['entries'][0]

if __name__ == "__main__":
    asyncio.run(ADQuery.run(), debug=True)

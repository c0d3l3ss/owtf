from zapv2 import ZAPv2
from framework.dependency_management.dependency_resolver import BaseComponent


class ZAP_API(BaseComponent):

    COMPONENT_NAME = "zap_api"

    def __init__(self, core):
        self.register_in_service_locator()
        self.Core = core
        self.config = self.Core.Config
        self.transaction = self.Core.DB.Transaction
        zap_proxy_address = "http://" + self.config.FrameworkConfigGet(
            "ZAP_PROXY_ADDR") + ":" + self.config.FrameworkConfigGet("ZAP_PROXY_PORT")
        self.zap = ZAPv2(proxies={'http': zap_proxy_address,
                                  'https': zap_proxy_address})  # the values are hard-coded just for the test purpose, will be taken from config later


def ForwardRequest(self, target_id, transaction_id):
    request = self.transaction.GetByIDAsDict(int(transaction_id), target_id=int(target_id))['raw_request']
    self.zap.core.send_request(request)


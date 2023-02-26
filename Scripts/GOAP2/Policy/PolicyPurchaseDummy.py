from GOAP2.Task.TaskAlias import TaskAlias
from Notification import Notification

class PolicyPurchaseDummy(TaskAlias):

    def _onParams(self, params):
        self.Product = params["Product"]

    def pay(self):
        prod_params = self.Product

        if _DEVELOPMENT:
            Trace.msg("DUMMY pay - prod_params={}".format(prod_params))
            Notification.notify(Notificator.onPaySuccess, prod_params.id)

    def _onGenerate(self, source):
        source.addFunction(self.pay)
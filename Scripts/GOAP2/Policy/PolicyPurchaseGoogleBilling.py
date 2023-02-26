from GOAP2.Systems.SystemGoogleServices import SystemGoogleServices
from GOAP2.Task.TaskAlias import TaskAlias

class PolicyPurchaseGoogleBilling(TaskAlias):

    def _onParams(self, params):
        self.Product = params["Product"]

    def pay(self):
        prod_id = self.Product.id
        SystemGoogleServices.buy(prod_id)

    def hasAccess(self):
        return _PLUGINS.get("GooglePlayBilling", False) is True

    def _onGenerate(self, source):
        if self.hasAccess() is True:
            source.addFunction(self.pay)
        else:
            source.addTask("PolicyPurchaseDummy", Product=self.Product)
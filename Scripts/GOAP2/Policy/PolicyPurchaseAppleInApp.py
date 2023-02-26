from GOAP2.Systems.SystemAppleServices import SystemAppleServices
from GOAP2.Task.TaskAlias import TaskAlias

class PolicyPurchaseAppleInApp(TaskAlias):

    def _onParams(self, params):
        self.Product = params["Product"]

    def pay(self):
        prod_id = self.Product.id
        SystemAppleServices.pay(prod_id)

    def hasAccess(self):
        return SystemAppleServices.canUserMakePurchases()

    def _onGenerate(self, source):
        if self.hasAccess() is True:
            source.addFunction(self.pay)
        else:
            source.addTask("PolicyPurchaseDummy", Product=self.Product)
from Foundation.Task.Task import Task

class TaskFacebookPostMessage(Task):

    def _onParams(self, params):
        super(TaskFacebookPostMessage, self)._onParams(params)
        self.data = params.get('data', {})
        pass

    def _onRun(self):
        super(TaskFacebookPostMessage, self)._onRun()
        Facebook.send_post_message(self.data)
        return True
        pass
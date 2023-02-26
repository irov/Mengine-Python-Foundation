from GOAP2.Task.MixinObjectTemplate import MixinMovie2
from GOAP2.Task.MixinTime import MixinTime
from GOAP2.Task.TaskAlias import TaskAlias

class AliasMovie2AlphaTo(MixinMovie2, MixinTime, TaskAlias):
    Skiped = True
    MixinTime_Validate_TimeZero = False

    def _onParams(self, params):
        super(AliasMovie2AlphaTo, self)._onParams(params)

        self.alpha_from = params.get("From", None)
        self.alpha_to = params.get("To")
        self.easing = params.get("Easing", "easyLinear")
        self.layers_list = params.get("LayersAlphaToList", None)

        layers_only = params.get("bLayersOnly", None)

        self.b_layer_list_not_empty = self.layers_list is not None and isinstance(self.layers_list, list) and len(self.layers_list) > 0

        # if bLayersOnly not explicitly set, set True if LayersAlphaToList is not empty else False
        if layers_only is None:
            self.b_layers_only = self.b_layer_list_not_empty
        else:
            self.b_layers_only = bool(layers_only)

        # if LayersAlphaToList not empty, force easing to easyLinear for synchronizing with TaskMovie2LayerAlphaTo
        if self.b_layer_list_not_empty:
            self.easing = "easyLinear"  # const

    def _onInitialize(self):
        super(AliasMovie2AlphaTo, self)._onInitialize()

    def __setLayersExtraOpacity(self, opacity):
        if self.layers_list is None or not isinstance(self.layers_list, list):
            return

        self.Movie2.setMultipleLayersExtraOpacity(self.layers_list, opacity)

    def _onGenerate(self, source):
        if not self.Movie2.isActive():
            return

        entity_node = self.Movie2.getEntityNode()
        if self.time == 0.0 or entity_node.isActivate() is False:
            if entity_node.isActivate() is False and _DEVELOPMENT is True:
                Trace.log("Task", 0, "AliasMovie2AlphaTo: {!r} node is not active - alpha task interrupted".format(entity_node.getName()))
            if not self.b_layers_only:
                self.Movie2.setParam("Alpha", self.alpha_to)
            self.__setLayersExtraOpacity(self.alpha_to)
            return

        with source.addParallelTask(2) as (parallel_movie, parallel_layers):
            if self.b_layer_list_not_empty:
                for layer, parallel_layer in parallel_layers.addParallelTaskList(self.layers_list):
                    parallel_layer.addTask("TaskMovie2LayerAlphaTo", To=self.alpha_to, From=self.alpha_from, Time=self.time, Layer=layer, Movie2=self.Movie2)

            if not self.b_layers_only:
                movie_en_alpha_to_param = dict(Node=entity_node, To=self.alpha_to, From=self.alpha_from, Time=self.time, Easing=self.easing)
                parallel_movie.addTask("TaskNodeAlphaTo", **movie_en_alpha_to_param)
                source.addFunction(self.Movie2.setAlpha, self.alpha_to)
from GOAP2.Task.TaskAlias import TaskAlias

class AliasMakeMovieAndPlayOnce(TaskAlias):
    def _onParams(self, params):
        super(AliasMakeMovieAndPlayOnce, self)._onParams(params)
        self.Parent = params.get("Parent")
        self.MovieGroupName = params.get("MovieGroupName")
        self.MovieName = params.get("MovieName")
        self.Position = params.get("Position")
        self.Loop = params.get("Loop", False)
        self.Time = params.get("Time")
        self.Duration = params.get("Duration")
        self.Scheduler = params.get("Scheduler")
        self.Important = params.get("Important", True)
        pass

    def _onGenerate(self, source):
        Movie = Utils.makeMovieNode(self.MovieGroupName, self.MovieName, Enable=True, Loop=self.Loop, Position=self.Position, Important=self.Important)

        if Movie is None:
            return
            pass

        self.Parent.addChild(Movie)

        if self.Duration is None:
            source.addTask("TaskAnimatablePlay", Animatable=Movie, Time=self.Time, Destroy=True)
            pass
        else:
            with source.addFork() as source_animatable_fork:
                source_animatable_fork.addTask("TaskAnimatablePlay", Animatable=Movie, Time=self.Time, Destroy=True)
                pass

            source.addDelay(self.Duration, self.Scheduler)
            pass
        pass
    pass
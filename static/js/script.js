var test;
$(function() {
    $("#sortable").sortable({
        revert: true
    });
    $("ul, li").disableSelection();

    function Task(title, isDone, ownerViewModel) {
        this.title = ko.observable(title);
        this.isDone = ko.observable(isDone);
        this.ownerViewModel = ownerViewModel;
        this.remove = function() {
            console.log("Deleted task");
            ownerViewModel.removeTask(this);
        };
    }

    function TaskList(title, id, ownerViewModel) {
        this.title = ko.observable(title);
        this.id = id;
        this.tasks = ko.observableArray([]);
        this.remove = function() {
            var taskLists = ownerViewModel.taskLists;
            taskLists.remove(this);
        };
        var self = this;
        this.add = function(title, isDone) {
            self.tasks.push(new Task(title, isDone, self))
        };
        this.removeTask = function(task) {
            self.tasks.remove(task);
        }
    }

    function TaskListsViewModel() {
        this.taskLists = ko.observableArray([]);
        var self = this;

        $.getJSON('/taskLists', function(data) {
            $.map(data, function(taskList) {
                var tempTaskList = new TaskList(taskList.title, taskList.id, self);
                $.map(taskList.tasks, function(task) {
                    tempTaskList.add(task.title, task.isDone);
                });
                self.taskLists.push(tempTaskList);
            })
        });
    }

    ko.applyBindings(new TaskListsViewModel());
});
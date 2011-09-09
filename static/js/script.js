var test;
$(function() {
	$( "#sortable" ).sortable({
	        revert: true
	    });
	    $( "ul, li" ).disableSelection();
	
	function task(title, isDone, ownerViewModel) {
        this.title = ko.observable(title);
        this.isDone = ko.observable(isDone);
        this.remove = function() { ownerViewModel.tasks.remove(this) }
    }

    function taskListViewModel() {
        this.tasks = ko.observableArray([]);
        this.newTaskText = ko.observable();
        this.addTask = function() {
            this.tasks.push(new task(this.newTaskText(), false, this));
            this.newTaskText("");    
        }
        this.incompleteTasks = ko.dependentObservable(function() {
            return ko.utils.arrayFilter(this.tasks(), function(task) { return !task.isDone(); });
        }, this);
        self = this;
        $.getJSON('/tasks', function(data){
            $.map(data, function(item){
                self.tasks.push(new task(item.name, item.isDone, self));
            })
        });
    }

    ko.applyBindings(new taskListViewModel());
});
var test;
$(function() {
	$( "#sortable" ).sortable({
    revert: true
  });
  $("ul, li").disableSelection();
	
	function Task(title, isDone, ownerViewModel) {
    this.title = ko.observable(title);
    this.isDone = ko.observable(isDone);
    this.remove = function() {
      jQuery.each(ownerViewModel.taskLists(),function(index, taskList){
        taskList.tasks.remove(this);
      });
    };
  }

  function TaskList(title, id, tasks, ownerViewModel) {
    this.title = ko.observable(title);
    this.id = id;
    this.tasks = ko.observableArray(tasks);
    this.remove = function() {
      var taskLists = ownerViewModel.taskLists;
      taskLists.remove(this);
    };
  }

  function TaskListsViewModel(){
    this.taskLists = ko.observableArray([]);
    var self = this;
    $.getJSON('/taskLists', function(data){
      $.map(data, function(taskList){
        var myTasks = [];
        $.map(taskList.tasks, function(task){
          myTasks.push(new Task(task.title, task.isDone, self));
        });
        self.taskLists.push(new TaskList(taskList.title, taskList.id, myTasks, self));
      })
    });
  }

  ko.applyBindings(new TaskListsViewModel());
});















//$(function() {
//	$( "#sortable" ).sortable({
//    revert: true
//  });
//  $( "ul, li" ).disableSelection();
//
//	function task(title, isDone, ownerViewModel) {
//    this.title = ko.observable(title);
//    this.isDone = ko.observable(isDone);
//    this.remove = function() { ownerViewModel.tasks.remove(this) };
//  }
//
//  function taskListViewModel() {
//    this.tasks = ko.observableArray([]);
//    this.newTaskText = ko.observable();
//    this.addTask = function() {
//      this.tasks.push(new task(this.newTaskText(), false, this));
//      this.newTaskText("");
//    };
//    this.incompleteTasks = ko.dependentObservable(function() {
//      return ko.utils.arrayFilter(this.tasks(), function(task) { return !task.isDone(); });
//    }, this);
//    self = this;
//    $.getJSON('/tasks', function(data){
//      $.map(data, function(item){
//          self.tasks.push(new task(item.name, item.isDone, self));
//      })
//    });
//  }
//
//  ko.applyBindings(new taskListViewModel());
//});
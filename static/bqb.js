$(document).ready(function() {
	var ROOT = $(location).attr('href');
	ROOT = ROOT.substr(0, ROOT.lastIndexOf("/"));
	
	var Question = Backbone.Model.extend({
		url: ROOT + "/getQuestion",
    });
	
	var Player = Backbone.Model.extend({
		url: ROOT + "/isLoggedIn",
    });
	
	var handleError = function(xhr) {
	    alert("An error has occurred. Email vokuheila@gmail.com and tell him about it.");
	};
	
	var HighscoreView = Backbone.View.extend({
		el: $("div#highscores"),
		initialize: function() {
		    _.bindAll(this, "render", "fetchtable");
		    this.fetchtable();
		},
		fetchtable : function() {
			var self = this;
    		Backbone.ajax({
        		type : "GET",
        		url : "list",
        		data: {} ,
                success: function(data) {
        			self.render(data.results);
                },
                error: function(xhr, status, error) {
    	    		handleError(xhr);
                }
        	});
		},
	    render: function(highscores) {
		    var table = $("<table>", {class : "highscores"});
		    var header1 = $("<th>").text("Username");
		    var header2 = $("<th>").text("Highscore");
		    table.append($("<tr>").append(header1).append(header2));
			for (var index = 0; index < highscores.length; index++) {
			    var row = $("<tr>");
			    row.append($("<td>").text(highscores[index].username))
			    .append($("<td>").text(highscores[index].highscore));
			    table.append(row);
		    }
			$("div#highscores").empty().append(table);
		}
		
	});
	
	var MainView = Backbone.View.extend({
		el: $("div#content"),
    	initialize: function() {
		    _.bindAll(this, "checkLogin",  "login", "guest", "renderTopbarLoggedIn", "renderTopbarLoggedOut", "refreshTopbar");
		    //see if a user is logged in
    		this.checkLogin();
        },
        events: {
            "click a#loginbutton": "login",
            "click a#guestbutton": "guest"
        },
        checkLogin: function() {
    		var self = this;
    		var player = new Player();
    		player.fetch({
    	        success : function(data) {
        	    	self.username = player.get("username");
        	    	self.highscore = player.get("highscore");
        	    	if (self.username == "Guest") {
        	    		self.highscore = "Not available";
        	    	}
            	    if (self.username) {
            	    	self.renderTemplate("topbar.html", self.renderTopbarLoggedIn);
            	    	self.renderTemplate("introduction.html", self.renderMain);
            	    }
            	    else {
            	    	self.renderTemplate("topbar.html", self.renderTopbarLoggedOut);
            	    	self.renderTemplate("login.html", self.renderMain);
            	    }
    	    	},
        	    error: function(xhr, status, error) {
    	    		handleError(xhr);
                }
    	    });
        },
        refreshTopbar: function() {
        	var player = new Player();
        	var self = this;
    		player.fetch({
    	        success : function(data) {
        	    	self.username = player.get("username");
        	    	self.highscore = player.get("highscore");
        	    	if (self.username == "Guest") {
        	    		self.highscore = "Not available";
        	    	}
            	    if (self.username) {
            	    	self.renderTemplate("topbar.html", self.renderTopbarLoggedIn);
            	    }
            	    else {
            	    	self.renderTemplate("topbar.html", self.renderTopbarLoggedOut);
            	    }
    	    	},
        	    error: function(xhr, status, error) {
    	    		handleError(xhr);
                }
    	    });
        },
        renderTopbarLoggedOut : function(content) {
        	$("div#top-bar").html(content);
    		$("a#profile").text("Not logged in");
    	    $("a#logout").text("");
        },
        renderTopbarLoggedIn : function(content) {
        	$("div#top-bar").html(content);
        	if (this.username) {
        	    $("a#profile").text(this.username + " Highscore: " + this.highscore);
        	    $("a#logout").text("Log out");
        	}
        },
        renderMain : function(content) {
        	$("div#content").html(content);
        },
        renderTemplate : function(filename, callback) {
    		Backbone.ajax({
        		url : "getTemplate",
        		data: { filename: filename} ,
                success: function(data) {
                    callback(data);
                },
                error: function(xhr, status, error) {
    	    		handleError(xhr);
                }
        	});
    	},
        login : function() {
        	var username = $("input#login_username").val();
        	var password = $("input#login_password").val();
        	self = this;
        	Backbone.ajax({
        		type : "POST",
        		url : "login",
        		data: { username: username, password:password} ,
                success: function(data) {
        			self.checkLogin();
                },
                error: function(xhr, status, error) {
    	    		handleError(xhr);
                }
        	});
        },
        guest : function() {
        	self = this;
        	Backbone.ajax({
        		type : "POST",
        		url : "login",
        		data: { username: "Guest", password:"guestpassword"} ,
                success: function(data) {
        			self.checkLogin();
                },
                error: function(xhr, status, error) {
    	    		handleError(xhr);
                }
        	});
        }
	});
	
	var QuestionView = Backbone.View.extend({
		el: $("div#content"),
        initialize: function(){
        	_.bindAll(this, "checkAnswer",  "nextQuestion", "startTimer", "stopTimer", "updateTimer", "endGame");
		    this.question = new Question();
		    this.score = 0;
        },
        events: {
            "click a#start": "nextQuestion",
            "click a.answer": "checkAnswer"
        },
        startTimer: function() {
        	this.time = 700;
        	this.timer = setInterval(this.updateTimer, 10);
        },
        updateTimer : function() {
        	if (this.time == 0) {
        	    this.stopTimer();
        	    $("#prompt").text("Time is up! Your score is " + this.score);
        	    this.endGame();
        	    return;
        	}
            this.time -= 1;
            
            var seconds = Math.floor(this.time / 100);
            var milli = this.time % 100;
            if (milli < 10) {
                milli = "0" + milli;
            }
            $("#timer").text("0" + seconds + ":" + milli + "  Score: " + this.score);
            
            if (this.time < 200) {
            	$("#timer").css("color", "red");
            }
        },
        stopTimer : function() {
            clearInterval(this.timer);
        },
        endGame : function() {
        	this.stopTimer();
        	if (view.username != "Guest" && this.score > view.highscore) {
        		$("#prompt").append("<br/><br/>NEW PERSONAL HIGH SCORE!");
        		$("#answers").empty().append("Sending score.. Please wait.");
        		var self = this;
        		Backbone.ajax({
            		type : "POST",
            		url : "updateHighscore",
            		data: { username: view.username, highscore:self.score} ,
                    success: function(data) {
            			view.refreshTopbar();
            			highscoreView.fetchtable();
            			self.showStart();
            			this.score = 0;
                    },
                    error: function(xhr, status, error) {
        	    		handleError(xhr);
                    }
            	});
        	}
        	else {
        	    $("a.answer").remove();
        	    this.showStart();
    	        this.score = 0;
        	}
        },
        checkAnswer : function(ev) {
        	var answer = $(ev.currentTarget).attr("id");
        	var correct = $.inArray(answer, this.question.get("correct")) == 0;
        	
        	if (correct) {
        		var score = Math.ceil(this.time / 100);
        		this.showCorrectExample(this.question.get("correctExample"));
        		$("a.answer").remove();
        		this.score += score;
        		this.updateTimer();
        		this.stopTimer();
        		this.nextQuestion();
        	}
        	else {
        	    this.showJustification(this.question.get("justifications"));
        	    this.endGame();
        	}
        	
        },
        showStart : function() {
        	$("#answers").empty().append($("<a>", {class:"large success button", id:"start"}).text("Start!"));
        },
        showLoading : function() {
        	$("#start").attr("class", "large disabled button").text("Loading..");
        },
        showCorrectExample : function(ex) {
        	if (ex instanceof Array) {
        		if (ex.length < 2) {
        			$("#prompt").text("Correct!");
        		    return;
        		}
            	var msg = ex[0];
            	var path = ex[1];
            	$("#prompt").text(msg);
                for (var i = 0; i < path.length; i++) {
                    $("td#" + path[i]).attr("class", "highlighted");
                }
            }
            else {
            	$("#prompt").text(ex);
            }
        },
        showJustification : function(ju) {
            if (ju instanceof Array) {
            	var msg = ju[0];
            	var path = ju[1];
            	$("#prompt").text(msg + " Your score is " + this.score);
                for (var i = 0; i < path.length; i++) {
                    $("td#" + path[i]).attr("class", "highlighted");
                }
            }
            else {
            	$("#prompt").text(ju + " Your score is " + this.score);
            }
        },
        nextQuestion : function() {
        	self = this;
        	this.showLoading();
        	this.question.fetch({
                success: function(data) {
                    self.render();
                    self.startTimer();
                },
                error: function(xhr, status, error) {
    	    		handleError(xhr); 
                }
        	});
        },
        render : function() {
        	var q = this.question;
        	
        	$(this.el).empty();
        	
        	var table = $("<table>", {id : "board"});
        	var letters = this.question.get("board").letters;
        	for (var row=0;row<4;row++) {
        		var r = $("<tr>");
        		for (var col=0;col<4;col++) {
        			var index = row*4 + col;
        			r.append($("<td>", {id : index, class: "normal"}).text(letters[index]));
        		}
        		table.append(r);
        	}
        	
        	//construct timer
        	var timerdiv = $("<div>", {id : "timer", class : "row"});
        	
        	//construct prompt 
        	var prompt = $("<div>", {id : "prompt"}).append(q.get("prompt"));
        	
        	//construct answers
        	var answers = $("<div>", {id : "answers", class : "row"});
        	var column = $("<div>", {class : "columns"});
        	
        	for (var i =0; i<q.get("answers").length; i++) {
        		var text = q.get("answers")[i];
        	    var answer = $("<a>", {class : "large success button answer", id : text}).text(text);
        	    column.append(answer);
        	}
        	answers.append(column);
        	
        	$(this.el).append(table);
        	$(this.el).append(prompt);
        	$(this.el).append(timerdiv);
        	$(this.el).append(answers);
        }
    });
	
    var view = new MainView();
    var questionView = new QuestionView();
    var highscoreView = new HighscoreView();
});
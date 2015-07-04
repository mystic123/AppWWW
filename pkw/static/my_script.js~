$(document).ready(function() {
	var csrftoken = $.cookie("csrftoken");

	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
							if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
								xhr.setRequestHeader("X-CSRFToken", csrftoken);
							}
						}
	});

	(function($) {
		$.fn.invis = function() {
			return this.each(function() {
				$(this).addClass("invis");
			});
		};
		$.fn.visible = function() {
			return this.each(function() {
				$(this).removeClass("invis");
			});
		};
	}(jQuery));

	$("#dist-panel").hide();
	$("#county-panel").hide();
	$("#comm-panel").hide();
	$("#loading-box").hide();
	var voiv = '';
	var dist = '';
	var county = '';
	$("table").on({
		mouseenter: function() {
							if ($(this).find(".save-button").hasClass("invis")) {
								$(this).find(".edit-button").visible();
							}
						},
		mouseleave: function() {
							$(this).find(".edit-button").invis();
						}
	}, "tr.comm-entry");


	var makeTransparent = function() {
		$(this).addClass("half-transparent");
	}

	var unTransparent = function() {
		$(this).removeClass("half-transparent");
	}

	$("table").on({
		mouseenter: unTransparent,
		mouseleave: makeTransparent,
		mouseover: function() {
			$(this).addClass("mouse-over");
		}
	}, ".comm-button");

	$("table").on({
		mouseenter: unTransparent,
		mouseleave: makeTransparent,
		click: function() {
			$(this).parent().parent().remove();
		}
	}, ".close-button");

	$("table").on({
		input: function() {
					 $(this).val($(this).val().replace(/[\D]/g,""));
					 if ($(this).val() != "0") {
						 $(this).val($(this).val().replace(/^0/,""));	
					 }
				 }
	}, ".input");

	var commHTML = function(nr, name, recv_votes, allowed_vote, id, updates) {
		return $("<tr class=\"comm-entry\">" + "<td>" + nr + ". " + name + "</td>" +
				"<td class=\"recv_votes\"><input type=\"tel\" maxlength=\"12\" class=\"input\"><span class=\"text\">" + recv_votes + "</span></td>" +
				"<td class=\"allowed_vote\"><input type=\"tel\" maxlength=\"12\" class=\"input\"><span class=\"text\">" + allowed_vote + "</span></td>" +
				"<td class=\"buttons nowrap\">" +
				"<span class=\"glyphicon glyphicon-ok half-transparent comm-button save-button\" aria-hidden=\"true\"></span>" +
				"<span class=\"glyphicon glyphicon-remove half-transparent comm-button cancel-button\" aria-hidden=\"true\"></span>" +
				"<span class=\"glyphicon glyphicon-pencil half-transparent comm-button edit-button\" aria-hidden=\"true\"></span>" +
				"</td>" +
				"<td class=\"comm_id hidden\">" + id + "</td>" +
				"<td class=\"comm_updates hidden\">" + updates + "</td></tr>");
	}

	var updateSuccess = function(sender,data) {
		var row = sender.parent().parent();
		recv_input_val = row.find(".recv_votes > input").val();
		allowed_input_val = row.find(".allowed_vote > input").val();
		row.find("td.recv_votes > input").hide();
		row.find("td.allowed_vote > input").hide();
		row.find("td.recv_votes > span.text").text(recv_input_val).show();
		row.find("td.allowed_vote > span.text").text(allowed_input_val).show();
		row.find("td.comm_updates").text(data['updates']);
		sender.parent().find(".edit-button").visible();
		sender.parent().find(".save-button").invis();
		sender.parent().find(".cancel-button").invis();
		var html = $("<tr class=\"comm-entry alert-success\"><td colspan=\"3\">" +
				"Pomyślnie wprowadzono dane.</td><td>" +
				"<span class=\"glyphicon glyphicon-remove half-transparent close-button\" aria-hidden=\"true\"></span></td>");
		$(html).insertAfter(row);
		$("#loading-box").hide();
	}

	var updateError = function(sender,data) {
		var row = sender.parent().parent();
		editComm(sender);
		var html = $("<tr class=\"comm-entry alert-danger\"><td colspan=\"3\">" +
				"Dane zostały zmienione od ostatniego odczytu.</td><td>" +
				"<span class=\"glyphicon glyphicon-remove half-transparent close-button\" aria-hidden=\"true\"></span></td>");
		$(html).insertAfter(sender.parent().parent());
		("#loading-box").hide();
	}

	$("#selection").on("mouseover", ".list-group-item", function(event) {
		$(event.target).addClass("active");
	});

	$("#selection").on("mouseout", ".list-group-item", function(event) {
		if ($(event.target).prop('checked') != true)
		$(event.target).removeClass("active");
	});

	var editComm = function(sender) {
		$("#loading-box").show();
		var row = sender.parent().parent();
		var comm_id = row.find("td.comm_id").text();
		$.ajax({
			url: "req/votes/" + comm_id + "/",
			type: "GET",

			success: function(json) {
				row.find("td.recv_votes > input").val(json['recv_votes']).show();
				row.find("td.allowed_vote > input").val(json['allowed_vote']).show();
				row.find("td.recv_votes > span.text").text(json['recv_votes']).hide();
				row.find("td.allowed_vote > span.text").text(json['allowed_vote']).hide();
				row.find("td.comm_updates").text(json['updates']);
				sender.parent().find(".edit-button").invis();
				sender.parent().find(".save-button").visible();
				sender.parent().find(".cancel-button").visible();
			},

			error: function(xhr, errmsg, err) {
					 }
		});
		$("#loading-box").hide();
	}

	$("#comm-panel").on("click", ".edit-button", function(event) {
		editComm($(this));
	});

	var sendData = function(sender, comm_id, recv_votes, allowed_vote,updates) {
		var postData = {};
		postData["recv_votes"] = recv_votes;
		postData["allowed_vote"] = allowed_vote;
		postData["updates"] = updates;
		$.ajax({
			url: "/req/save/" + comm_id + "/",
			type: "POST",
			data: postData, 
			success: function(data) {
				if (data["success"]) {
					updateSuccess(sender,data);
				}
				else if (data["locked"]) {
					setTimeout(sendData, 500, sender, comm_id, recv_votes, allowed_vote, updates);
				}
				else {
					updateError(sender,data);
				}
			},
			error: function(xhr, errmsg, err) {}
		});
	}

	$("#comm-panel").on("click", ".save-button", function(event) {
		$("#loading-box").show();
		var comm_id = $(this).parent().parent().find("td.comm_id").text();
		var sender = $(this);
		var row = sender.parent().parent();
		var recv_votes = row.find("td.recv_votes > input").val();
		var allowed_vote = row.find("td.allowed_vote > input").val();
		var updates = row.find("td.comm_updates").text();
		sendData($(this), comm_id, recv_votes, allowed_vote, updates);
	});


	$("#comm-panel").on("click", ".cancel-button", function(event) {
		var sender = $(this);
		var row = sender.parent().parent();
		recv_input_val = row.find(".recv_votes > input").val();
		allowed_input_val = row.find(".allowed_vote > input").val();
		row.find("td.recv_votes > input").hide();
		row.find("td.allowed_vote > input").hide();
		row.find("td.recv_votes > span.text").show();
		row.find("td.allowed_vote > span.text").show();
		sender.parent().find(".edit-button").visible();
		sender.parent().find(".save-button").invis();
		sender.parent().find(".cancel-button").invis();
	});

	$.getJSON("req/", function(data) {
		var items = [];
		$.each(data, function(i) {
			items.push("<li class=\"list-group-item voiv\">" + data[i]['name'] + "</li>");
		});
		$("#voiv-list").append(items);
	});

	$("#voiv-list").on("click", ".voiv", function(event) {
		var voivs = $("#voiv-list").find("li");
		if (voiv == '') {
			$.getJSON("req/" + $(this).text() + "/", function(data) {
				voiv = $(event.target).text();
				$(event.target).addClass("active");
				$(event.target).prop("checked", true);
				voivs.each(function(i, elem) {
					if (elem != event.target) {
						$(elem).hide(300);
					}
				});
				var items = [];
				$.each(data, function(i) {
					items.push("<li class=\"list-group-item dist\">" + data[i]['dist']['name'] + "</li>");
				});
				$("#dist-list").append(items);
				$("#dist-panel").show(300);
			});
		}
		else {
			$("#dist-panel").hide();
			$("#county-panel").hide();
			$("#comm-panel").hide();
			$("#dist-list").empty();
			$("#county-list").empty();
			$("#comm-list > tbody").empty();
			voiv = '';
			dist = '';
			county = '';
			voivs.each(function(i, elem) {
				$(elem).show(300);
				$(elem).removeClass("active");
			});
			$(event.target).prop("checked", false);
		}
	});

	var showCommissions = function(data) {
		var items = [];
		$.each(data, function(i) {
			items.push(commHTML(data[i]['comm']['nr'],
					data[i]['comm']['name'],
					data[i]['comm']['recv_votes'],
					data[i]['comm']['allowed_vote'],
					data[i]['comm']['id'],
					data[i]['comm']['updates']
					));
		});
		$("#comm-list > tbody").append(items);
		$("#comm-panel").show(300);
		var inputs = $("#comm-panel").find("input");
		$.each(inputs, function(i) {
			$(inputs[i]).hide();
		});
		var buttons = $("#comm-panel").find(".comm-button");
		$.each(buttons, function(i) {
			$(buttons[i]).invis();
		});
	}

	$("#dist-list").on("click", ".dist", function(event) {
		var dists = $("#dist-list").find("li");
		if (dist == '') {
			$(event.target).prop("checked", true);
			var etext = $(event.target).text();
			dist = etext;
			$(event.target).addClass("active");
			dists.each(function(i, elem) {
				if (elem != event.target) {
					$(elem).hide(300);
				}
			});
			$.getJSON("req/" + voiv + "/" + dist + "/", function(data) {
				var items = [];
				if (etext == "Zagranica" || etext.indexOf(", m.") > -1 || etext.indexOf("Statki") > -1) {
					showCommissions(data);
				}
				else {
					$.each(data, function(i) {
						items.push("<li class=\"list-group-item county\">" + data[i]['dist']['name'] + "</li>");
					});
					$("#county-list").append(items);
					$("#county-panel").show(300);
				}
			});
		}
		else {
			$("#county-panel").hide();
			$("#comm-panel").hide();
			$("#county-list").empty();
			$("#comm-list > tbody").empty();
			dist = '';
			county = '';
			dists.each(function(i, elem) {
				$(elem).show(300);
				$(elem).removeClass("active");
			});
			$(event.target).prop("checked", false);
		}
	});

	$("#county-list").on("click", ".county", function(event) {
		var countys = $("#county-list").find("li");
		if (county == '') {
			$(event.target).prop("checked", true);
			county = $(event.target).text();
			$(event.target).addClass("active");
			countys.each(function(i, elem) {
				if (elem != event.target) {
					$(elem).hide(300);
				}
			});
			$.getJSON("req/" + voiv + "/" + dist + "/" + county + "/", function(data) {
				showCommissions(data);
			});
		}
		else {
			$("#comm-panel").hide();
			$("#comm-list > tbody").empty();
			county = '';
			countys.each(function(i, elem) {
				$(elem).show(300);
				$(elem).removeClass("active");
			});
			$(event.target).prop("checked", false);
		}
	});
});


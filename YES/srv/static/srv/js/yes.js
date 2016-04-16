/**
 * makes a callback function which ...
 * will unroll an element and bring back the currently unrolled element
 * into the list of compressed elements
 * @param v the element to enrol
 **/
function unrollFunction(v){
    return function(){
	var unrolled=$("#unrolled div").first();
	$("#compressed").prepend(unrolled);
	// hide parts which are only for compressed displays
	$("#unrolled").append(v);
	initCompressed();
	var i = v.find("iframe").first();
	if (i){
	    // reload the iframe's content; this seems to be important for
	    // video broadcast
	    var src = i.attr('src');
	    i.attr('src','');
	    i.attr('src',src);
	}
    };
}

function removeUnrollStuff(sel){
    sel.find(".unrollButton").remove(); 
    sel.find(".unrollEnd").remove(); 
}

/**
 * Prepares the Compressed div
 **/
function initCompressed(){
    var compressed=$("#compressed");
    compressed.sortable();
    compressed.disableSelection();
    var views = compressed.find("div.view");
    for (var i=0;i < views.length; i++){
	var v = $(views[i]);
	removeUnrollStuff(v); //don't keep old buttons
	var b=$("<button>", {
	    "class": "unrollButton seeCompressed",
	}).text("<").click(unrollFunction(v));
	v.prepend(b);
	v.append($("<br>",{"class": "unrollEnd seeCompressed",}));
    }
}

$(function() { //will be called when the document is ready
    var views=$(".view");
    for (var i=0; i < views.length; i++){
	if (i==0){
	    $("#unrolled").append($(views[i]));
	} else {
	    $("#compressed").append($(views[i]));
	}
    }
    initCompressed();
    // init datepickers
    $(".datepicker").datepicker({format: "dd/mm/yyyy",});
});

/**
 * variables globales
 */
document.success="Success";
document.failure="Failure";

/**
 * affiche un message dans une division fugitive, qui apparaît deux secondes
 * puis disparaît.
 * @param s le message à afficher
 * @param option valeur telle que Success, Failure.
 */
function message(s, option){
    var msg=$("#message");
    var closeBtn=$("<div>")
	.text("×")
	.on('click', function(){
	    msg.clearQueue();
	    msg.css({
		display:"none",
	    });
	})
	.css({
	    background: "rgba(255, 255, 255, 0.5)",
	    "border-radius": "4px",
	    color: "#888",
	    display: "inline-block",
	    position: "relative",
	    right: "-0.5ex",
	    top: "-1ex",
	    cursor: "pointer",
	});
    msg.html(s);
    msg.append(closeBtn);
    msg.removeClass();
    msg.addClass(option);
    msg.fadeIn( 300 ).delay(5000 ).fadeOut( 2000 );
}

/**
 * disable reservation entries based on the database's contents
 * @param resa a list of tuples [begin,duration, username]
 * @param user the login name of the currently logged user
 **/
function updateResa(resa, user){
    // reset all timeslots
    var timeslots=$(".timeslot");
    timeslots.css({background: "yellow"})
    timeslots.find("input").prop({
	'disabled': false,
	'checked' :false,
    });
    for (var i=0; i < timeslots.length; i++){
	var span=$(timeslots[i]);
	var txt=span.text();
	span.attr('title', txt+gettext("... free"));
    }
    // manage reserved timeslots
    for (var i=0; i < resa.length; i++){
	var minute=resa[i][0];
	var span=$("#resa input:checkbox[name=t"+minute+"]").first().parent();
	var txt=span.text();
	span.attr("title", txt + " " + gettext("reserved by") + " " + resa[i][2]);
	if (user==resa[i][2]){
	    // same user; the reservation can be undone
	    span.css({background: "lightgreen"});
	    span.find("input").prop({
		'checked' : true,
	    });
	} else {
	    // different user, the reservation cannot be undone
	    span.css({background: "red"});
	    span.find("input").prop({
		'disabled': true,
		'checked' : true,
	    });
	}
    }
}

/**
 * callback function when the wanted date changes for reservations
 **/
function wantedDateChange(){
    window.wantedDate=$("#wantedDate").val();
    $.get("/srv/reservationsByDate",{wantedDate: window.wantedDate})
	.done(
	    function (data){
		// alert(JSON.stringify(data));
		var resa=data["resa"];
		var user=data["name"];
		updateResa(resa, user);
	    }
	)
	.fail(
	    function(){
		alert(gettext("wantedDate failed"));
	    }
	);
}

/**
 * callback function for submitted reservations
 * @param username login name for the user which makes the reservation
 **/
function submitResa(username){
    var timeslots=[];
    var checked=$("#resa input:checked")
    for (var i=0; i < checked.length; i++){
	timeslots.push($(checked[i]).attr("name"))
    }
    if (username.length==0){
	alert(gettext("You are not logged; reservations are not possible"));
	return;
    }
    $.get("/srv/makeResa",{
	name      : username,
	wantedDate: $("#wantedDate").val(),
	timeslots : timeslots.join(","),
    }).done(
	function (data){
	    var resa=data["resa"];
	    var user=data["name"];
	    updateResa(resa, user);
	    // alert(JSON.stringify(data));
	}
    ).fail(
	function(){
	    alert(gettext("failed makeResa"));
	}
    );
}

/**
 * callback function for toggling a reservation
 * @param username login name for the user which makes the reservation
 * @param checkbox the input[type=checkbox] element which calls back
 **/
function toggleResa(username, checkbox){
    if (username.length==0){
	alert(gettext("You are not logged; reservations are not possible"));
	return;
    }
    $.get("/srv/toggleResa",{
	name      : username,
	wantedDate: $("#wantedDate").val(),
	minute: $(checkbox).attr("name"),
	checked: $(checkbox).prop("checked"),
    }).done(
	function (data){
	    var resa=data["resa"];
	    var user=data["name"];
	    updateResa(resa, user);
	    // alert(JSON.stringify(data));
	}
    ).fail(
	function(){
	    alert(gettext("failed makeResa"));
	}
    );
}

/**
 * changes the attributes of an element into a list of parameters for
 * a HTTP GET query
 * @param name the name of an element
 * @ return a string for a GET query
 **/
function elParams(name){
    var element=$("[name='"+name+"']")[0];
    var result=[];
    for (var i=0; i < element.attributes.length; i++){
	var name=element.attributes[i].name;
	var value=element.attributes[i].value;
	if (name.substring(0,2) != "on"){
	    // do not take in account onchange or onclick attributes!
	    result.push(name+"="+element.attributes[i].value);
	}
    }
    return result.join("&");
}

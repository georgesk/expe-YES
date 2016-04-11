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
	v.find(".seeCompressed").hide()
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
    var views = compressed.find("div");
    // show parts which are only for compressed displays
    views.find(".seeCompressed").hide()
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
 **/
function updateResa(resa){
    // reset all timeslots
    $(".timeslot").css({background: "yellow"})
    $(".timeslot input").prop('disabled',false);
    // disable reserved timeslots
    for (var i=0; i < resa.length; i++){
	var minute=resa[i][0];
	var span=$("#resa input:checkbox[name=t"+minute+"]").first().parent();
	var txt=span.text();
	span.css({background: "red"});
	span.attr("title", txt + " reserved by " + resa[i][2]);
	span.find("input").prop({
	    'disabled': true,
	    'checked' :false,
	});
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
		updateResa(resa);
	    }
	)
	.fail(
	    function(){
		alert("wantedDate failed");
	    }
	);
}

/**
 * callback function for submitted reservations
 **/
function submitResa(){
    var timeslots=[];
    var checked=$("#resa input:checked")
    for (var i=0; i < checked.length; i++){
	timeslots.push($(checked[i]).attr("name"))
    }
    var username=$("#username").val();
    if (username.length==0){
	alert("You are not logged; reservations are not possible");
	return;
    }
    $.get("/srv/makeResa",{
	name      : username,
	wantedDate: $("#wantedDate").val(),
	timeslots : timeslots.join(","),
    }).done(
	function (data){
	    var resa=data["resa"];
	    updateResa(resa);
	    // alert(JSON.stringify(data));
	}
    ).fail(
	function(){
	    alert("failed makeResa");
	}
    );
}

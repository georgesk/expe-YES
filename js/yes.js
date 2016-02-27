/**
 * makes a callback function which ...
 * will unroll an element and bring back the currently unrolled element
 * into the list of compressed elements
 * @param v the element to enrol
 **/
function unrollFunction(v){
    return function(){
	console.log(v);
	var unrolled=$("#unrolled div").first();
	$("#compressed").prepend(unrolled);
	removeUnrollStuff(v);
	$("#unrolled").append(v);
	initCompressed();
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
    for (var i=0;i < views.length; i++){
	var v = $(views[i]);
	removeUnrollStuff(v); //don't keep old buttons
	var b=$("<button>", {
	    "class": "unrollButton",
	}).text("<").click(unrollFunction(v));
	v.prepend(b);
	v.append($("<br>",{"class": "unrollEnd",}));
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
});


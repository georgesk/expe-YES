$(function() { //will be called when the document is ready
    var views=$(".view");
    for (var i=0; i < views.length; i++){
	if (i==0){
	    $("#unrolled").append($(views[i]));
	} else {
	    $("#compressed").append($(views[i]));
	}
    }
});

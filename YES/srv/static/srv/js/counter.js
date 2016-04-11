window.n=0;

function decrN(){
    window.n-=1;
    $("#s").text(window.n);
    window.setTimeout(decrN,1000);
}

$(function (){ // to be launched when the page is loaded
    window.n=parseInt($("#s").text());
    window.setTimeout(decrN,1000);
})


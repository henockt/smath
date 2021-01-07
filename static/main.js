$(function() {
    $("#output").html("{{ message }}");
    initialize();
});

var app;
// initialize Vue
function initialize() {
    app = new Vue({
        el: "#output",
        data: {
            message: "Enter expression"
        }
    })
}


// make API call
function calc() {
    app.message = "Evaluating..."
    var expression = encodeURIComponent($("#exp").val());
    fetch(window.location.href + "api?q=" + expression)
      .then(response => response.json())
      .then(data => app.message = data['result']);
}

// map enter key to calc()
function handle(e) {
    if(e.keyCode === 13)
        calc();   
}


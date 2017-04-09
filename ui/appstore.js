(function(){
    $(function(){
        var timer = null;
        var showLoading = function(){
            $('#results').html('<div id="loader" class="mdl-spinner mdl-js-spinner is-active"></div>');
        };
        var removeLoading = function(){
            $('#results').html('');
        };
        var doSearch = function(){
            var value = $('#q').val();

            $('#results .item').remove();
            if(value == ""){
                return;
            }

            showLoading();
            $.getJSON(APP_API + "?q=" + value, function(response){
                removeLoading();
                var results = $('#results');
                var template = _.template($('#result-template').html());
                for(var i = 0; i < response.apps.length; i++){
                    var app = response.apps[i];
                    var html = template({'app': app.apple});
                    results.append(html);
                }
            });
        };
        $('#q').keypress(function(e){
            clearTimeout(timer);

            if(e.keyCode == 13){
                doSearch();
                return;
            }

            timer = setTimeout(doSearch, 300);
        });

    });
})();
function parseText(text){
    var result = text.indexOf(".");
    var exclamation = text.indexOf('!');
    if(exclamation < result){
        result = exclamation;
    }
    if(result == -1){
        return 100;
    }

    return text.substring(0, result);
}
function formatScore(number){
    return Math.round(number * 10) / 10;
}
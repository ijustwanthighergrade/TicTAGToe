// * 常用的function
// location to index
function ReturnToIndex(){
    location.href = "/";
}

// control menu
function ControlMenu(){
    $("[data-btn='menu']").on("click", function(){
        if ($("[data-block='menu']")[0].style.display == "none"){
            $("[data-block='menu']")[0].style.display = 'block';
        } else {
            $("[data-block='menu']")[0].style.display = 'none';
        }
    });
}

// call ajax
function AjaxRequest(url,params,successFunc,errorFunc) {
    url = url || '';
    params = params || {};
    successFunc = successFunc || function(){}
    errorFunc = errorFunc || function(){}

    $.ajax({
        type: "post",
        url: url,
        data: params,
        dataType: "json",
        success: successFunc,
        error: errorFunc
    });
}

// click tag start search
function ClickTagStartSearch() {
    $("[data-btn='searchTag']").on("click", function() {
        if ($("[data-input='keyword']")[0].value != "") {
            location.href = '/searchres?keyword=' + $("[data-input='keyword']")[0].value;
        } else {
            return;
        }
    });
    
}
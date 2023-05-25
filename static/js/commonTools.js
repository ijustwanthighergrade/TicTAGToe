// * 常用的function
// location to index
function ReturnToIndex(){
    location.href = "/";
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
function ClickTagStartSearch(tagName) {
    location.href = '/?keyword=' + tagName;
}
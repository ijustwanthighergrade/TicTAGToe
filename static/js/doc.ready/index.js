$(function(){
    // 
    AjaxRequest('/testajax',{'test':'666'},
    function(data){
        console.log(data);
    });
})
$(function(){
    ControlMenu();

    // * test
    CreateSocialPostItem('../static/img/test.jpeg','123','','2023-05-31','測試內容','20','3',['水果','蘋果','大麻'],['../static/img/test.jpeg','../static/img/search.png','../static/img/menu.png'])
    CreateSocialPostItem('../static/img/test.jpeg','123','','2023-05-31','測試內容','20','3',['水果','蘋果','大麻'],['../static/img/test.jpeg','../static/img/test.jpeg'])
    
    // ! create knowledge map example
    CreateKnowledgeMap([{ key: 1,category:"people", text: "xxx",type:"people" },{ key: 2,category:"tag", text: "xxx",type:"tag"},{ key: 3,category:"place", text: "xxx",type:"place" },{ key: 4,category:"obj", text: "xxx",type:"obj" },{ key: 5,category:"tag", text: "hashtag",type:"tag"}],[{ from: 1, to: 2},{ from: 3, to: 2},{ from: 4, to: 2},{ from: 3, to: 5}]);
    
    $("[data-close-block-ui]").on("click", function(){
        $("[data-block-ui='" + this.dataset.closeBlockUi + "']")[0].style.display = "none";
    });
    
    // click social button
    $("[data-social-btn='facebook']").on("click", function(){
        if($("[data-input='keyword']")[0].value == ''){
            alert('請先在搜尋欄輸入想查詢的Hashtag！');
            return;
        } else {
            AjaxRequest('/search_FB',{'keyword': $("[data-input='keyword']")[0].value},
            function(data){
                // remove original data
                RemoveAllSocialPost();
    
                for (var i = 0; i < data['post_item'].length; i++) {
                    // create social post
                    CreateSocialPostItem(data['post_item'][i]['post_image'],data['post_item'][i]['post_name'],data['post_item'][i]['post_club'],data['post_item'][i]['post_time'],data['post_item'][i]['post_text'],data['post_item'][i]['post_likes'],data['post_item'][i]['post_comments'],data['post_item'][i]['post_hashtag'],data['post_item'][i]['post_picture']);
                }
            });
        }
    });

    $("[data-social-btn='instagram']").on("click", function(){
        alert('該功能尚未開啟');
        return;
        // if($("[data-input='keyword']")[0].value == ''){
        //     alert('請先在搜尋欄輸入想查詢的Hashtag！');
        //     return;
        // } else {
            
        // }
    });

    $("[data-social-btn='twitter']").on("click", function(){
        alert('該功能尚未開啟');
        return;
        // if($("[data-input='keyword']")[0].value == ''){
        //     alert('請先在搜尋欄輸入想查詢的Hashtag！');
        //     return;
        // } else {
            
        // }
    });

    $("[data-social-btn='tictagtoe']").on("click", function(){
        alert('該功能尚未開啟');
        return;
        // if($("[data-input='keyword']")[0].value == ''){
        //     alert('請先在搜尋欄輸入想查詢的Hashtag！');
        //     return;
        // } else {
            
        // }
    });
})
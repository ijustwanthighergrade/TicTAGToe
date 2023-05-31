$(function(){
    ControlMenu();
    
    // ! create knowledge map example
    CreateKnowledgeMap([{ key: 1,category:"people", text: "xxx",type:"people" },{ key: 2,category:"tag", text: "xxx",type:"tag"}],[{ from: 1, to: 2}]);
    
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
        if($("[data-input='keyword']")[0].value == ''){
            alert('請先在搜尋欄輸入想查詢的Hashtag！');
            return;
        } else {
            
        }
    });

    $("[data-social-btn='twitter']").on("click", function(){
        if($("[data-input='keyword']")[0].value == ''){
            alert('請先在搜尋欄輸入想查詢的Hashtag！');
            return;
        } else {
            
        }
    });

    $("[data-social-btn='tictagtoe']").on("click", function(){
        if($("[data-input='keyword']")[0].value == ''){
            alert('請先在搜尋欄輸入想查詢的Hashtag！');
            return;
        } else {
            
        }
    });
})
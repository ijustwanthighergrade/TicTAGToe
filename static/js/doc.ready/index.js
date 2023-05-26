$(function(){
    // ajax example
    $("[data-btn='search']").on("click",function(){
        AjaxRequest('/search',{'keyword': $("[data-input='keyword']")[0].value},
        function(data){
            // console.log(data);
            console.log(data['post_item']);
            console.log(data['hashtag_detail']);

            // 取得容器元素
            var container = $('[data-container="socialPost"]');

            // 迭代 post_item 陣列
            for (var i = 0; i < data['post_item'].length; i++) {
                var item = data['post_item'][i];
                
                // 建立 post-card 元素
                var postCard = $('<div>').addClass('post-card');
                
                // 建立 circle-image 元素
                var circleImage = $('<div>').addClass('circle-image');
                
                // 建立圖片元素
                var image = $('<img>').attr('src', item['post_image']).attr('alt', '圖片');
                
                // 將圖片元素加入 circle-image 元素
                circleImage.append(image);
                
                // 建立發文者名稱元素
                var postTitle1 = $('<p>').addClass('post-title').text('發文者: ' + item['post_name']);
                
                // 建立社團元素
                var postTitle2 = $('<p>').addClass('post-title').text('社團: ' + item['post_club']);
                
                // 建立發文時間元素
                var postTime = $('<p>').addClass('post-time').text('發文時間: ' + item['post_time']);
                
                // 建立發文內容元素
                var postContent = $('<p>').addClass('post-content').text('發文內容: ' + item['post_text']);

                // 建立發文圖片元素
                var postPicture = $('<p>').addClass('post-time');
                
                // 迭代發文圖片陣列
                for (var j = 0; j < item['post_picture'].length; j++) {
                    var picture = $('<img>').attr('src', item['post_picture'][j]).addClass('content_pic').attr('alt', '圖片');
                    
                    // 將發文圖片元素加入發文內容元素
                    postPicture.append(picture);
                }
                
                // 加入發文影片內容
                postContent.text(postContent.text() + item['post_video']);

                var postHashtags = null

                if (item['post_hashtag'].length > 0) {
                    // 建立發文 Hashtag 元素
                    postHashtags = $('<p>').addClass('post-hashtags').text('發文hashtag內容: ');
                    
                    // 迭代發文 Hashtag 陣列
                    for (var k = 0; k < item['post_hashtag'].length; k++) {
                        var hashtag = $('<span>').addClass('post-hashtag').text(item['post_hashtag'][k]);
                        
                        // 將發文 Hashtag 元素加入發文 Hashtag 內容元素
                        postHashtags.append(hashtag);
                    }
                }

                // 建立貼文讚數元素
                var postLikes = item["post_likes"];
                var postLikesElement = $('<p>').addClass('post-time').text('貼文讚數: ' + postLikes);

                // 建立貼文留言數元素
                var postComments = item["post_comments"];
                var postCommentsElement = $('<p>').addClass('post-time').text('貼文留言數: ' + postComments);

                
                // 將子元素加入 post-card 元素
                postCard.append(circleImage);
                postCard.append(postTitle1);
                postCard.append(postTitle2);
                postCard.append(postTime);
                postCard.append(postContent);
                postCard.append(postPicture);
                
                // 如果沒有標hashtag，就不會顯示hashtag的div區塊元素
                if (postHashtags != null) {
                    postCard.append(postHashtags);
                }

                postCard.append(postLikesElement);
                postCard.append(postCommentsElement);

                // 將 post-card 元素加入容器元素
                container.append(postCard);


            }
        });
    })
    
    // click social button
    $("[data-social-btn='facebook']").on("click", function(){
        AjaxRequest('/search',{'keyword': $("[data-input='keyword']")[0].value},
        function(data){
            // remove original data
            RemoveAllSocialPost();

            for (var i = 0; i < data['post_item'].length; i++) {
                // create social post
                CreateSocialPostItem(data['post_item'][i]['post_image'],data['post_item'][i]['post_name'],data['post_item'][i]['post_club'],data['post_item'][i]['post_time'],data['post_item'][i]['post_text'],data['post_item'][i]['post_likes'],data['post_item'][i]['post_comments'],data['post_item'][i]['post_hashtag'],data['post_item'][i]['post_picture']);
            }
        });
        
    });

    $("[data-social-btn='instagram']").on("click", function(){

    });

    $("[data-social-btn='twitter']").on("click", function(){

    });

    $("[data-social-btn='tictagtoe']").on("click", function(){

    });
})
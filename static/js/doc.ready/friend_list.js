$(function(){
    // control menu
    ControlMenu();

    // header search bar
    ClickTagStartSearch();

    // send friend request
    SendFriendRequest();

    // change friend or member relationship
    ChangeFriendRelationship();

    GetFriendList();

    // 尋找好友按鈕
    $("[data-search-friend]").on("click",function(){
        GetFriendList('/getmemlist');
    });


})
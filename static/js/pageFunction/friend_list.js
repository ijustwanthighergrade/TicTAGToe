// 發送好友請求
function SendFriendRequest(friend) {
    $("[data-btn='']").off("click");

    $("[data-btn='']").on("click", function(){
        
        AjaxRequest('/addfriend',{'memId':friend},
        function(data){
            data['res'] == 'fail' ? alert(data['msg']) : alert('好友邀請已成功送出！');
        });

    });
}

// 改變好友(會員)間狀態(關係)
function ChangeFriendRelationship(friend, status) {
    $("[data-btn='']").off("click");

    $("[data-btn='']").on("click", function(){
        
        AjaxRequest('/changefriendstatus',{'memId':friend,'status':status},
        function(data){

            data['res'] == 'fail' ? alert(data['msg']) : alert(friendStatus[status]);

        });

    });
}
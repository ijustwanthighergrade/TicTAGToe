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

// 取得好友列表
function GetFriendList(url){
    url = url || '/getfriendlist';

    AjaxRequest(url,{'memName':$("[data-name='memName']")[0].value},function(data){
        console.log(data);
        var n = $("[data-mem-list]").length;

        for (let i = 0; i < n; i++) {
            $("[data-mem-list]")[0].remove();
        }
        for (let i = 0; i < data['data'].length; i++) {
            var memContainer = CreateMemListElement(data['data'][i][0],data['data'][i][1],data['data'][i][2],url);

            url == '/getfriendlist' ? $("[data-block='friendList']")[0].appendChild(memContainer) : $("[data-block='searchFriend']")[0].appendChild(memContainer);
            
            linkMem();
        }
    });
}

// 跳轉到會員頁面
function linkMem(){
    $("[data-mem-link]").off("click");

    $("[data-mem-link]").on("click",function(){
        location.href = '/individual?mem=' + this.dataset.memLink;
    });
}

// 發送好友邀請
function SendFriendRequest() {
    
}

// 刪除好友
function DelFriend() {
    $("[data-del-friend]").off("click");

    $("[data-del-friend]").on("click",function(){
        AjaxRequest('/deletefriend',{'memId':this.dataset.delFriend},function(data){
            location.reload();
        });
    });
}

// create好友列表區塊element
function CreateMemListElement(memId,memName,imgSrc,type) {
    var memContainer = document.createElement('div');
    var contentContainer = document.createElement('div');
    var imgContainer = document.createElement('div');
    var img = document.createElement('img');
    var nameContainer = document.createElement('div');
    var nameSpan = document.createElement('span');
    var btnContainer = document.createElement('div');
    var btn = document.createElement('button');
    var btnSvg = document.createElement('svg');
    var btnPath = document.createElement('path');

    memContainer.dataset.memList = '';
    memContainer.className = 'container-fluid fs-1 my-5';
    contentContainer.className = 'row align-items-center';
    imgContainer.className = 'col-6 text-center';
    img.src = imgSrc;
    img.className = 'mx-auto d-block';
    img.style.height = '250px';
    img.style.width = '250px';
    img.style.border = '5px solid #97CBFF';
    img.style.borderRadius = '25%';
    nameContainer.className = 'col-3 text-center';
    nameContainer.style.fontSize = '65px';
    nameSpan.textContent = memName;
    nameSpan.dataset.memLink = memId;
    // nameSpan.href = '/individual?mem=' + memId;
    btnContainer.className = 'col-3 text-center';
    btn.className = 'btn btn-light border-0 bg-transparent';
    btn.style.cursor = 'point';
    if (type == '/getfriendlist') {
        btn.textContent = '刪除';
        btn.dataset.delFriend = memId;
    } else {
        btn.textContent = '添加';
        btn.dataset.addFriend = memId;
    }
    // type == '/getfriendlist' ? btn.textContent = '刪除' : btn.textContent = '添加';
    btn.style.fontSize = '40px';
    // btnSvg.setAttribute('xmlns','http://www.w3.org/2000/svg');
    // btnSvg.setAttribute('width','70');
    // btnSvg.setAttribute('height','70');
    // btnSvg.setAttribute('fill','#97CBFF');
    // btnSvg.setAttribute('class','bi bi-x-square-fill');
    // btnSvg.setAttribute('viewBox','0 0 16 16');
    // btnPath.setAttribute('d','M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm3.354 4.646L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 1 1 .708-.708z');

    memContainer.appendChild(contentContainer);
    contentContainer.appendChild(imgContainer);
    contentContainer.appendChild(nameContainer);
    contentContainer.appendChild(btnContainer);
    imgContainer.appendChild(img);
    nameContainer.appendChild(nameSpan);
    // btnContainer.appendChild(btn);
    // btn.appendChild(btnSvg);
    // btnSvg.appendChild(btnPath);
    return memContainer;
}
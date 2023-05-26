// todo create social post
function CreateSocialPostItem(posterImgSrc,posterName,postClub,time,content,likeCount,CommentCount,hashtag=[],postImg=[]) {
    // create element
    let postContainer = document.createElement('div');
    let posterImgContainer = document.createElement('div');
    let posterImg = document.createElement('img');
    let poster = document.createElement('p');
    let club = document.createElement('p');
    let postTIme = document.createElement('p');
    let postContent = document.createElement('p');
    let postImgContainer = document.createElement('p');
    let postHashtagContainer = document.createElement('p');
    let like = document.createElement('p');
    let comment = document.createElement('p');

    postContainer.dataset.post = '';

    // poster img
    posterImgContainer.className = 'circle-image';
    posterImg.src = posterImgSrc;
    posterImgContainer.appendChild(posterImg);

    // post's poster
    poster.className = 'post-title';
    poster.textContent = '發文者：' + posterName;

    // post club
    club.className = 'post-title';
    club.textContent = '社團：' + postClub;

    // post time
    postTIme.className = 'post-time';
    postTIme.textContent = '發文時間：' + time;

    // postContent
    postContent.className = 'post-content';
    postContent.textContent = '發文內容：' + content;

    // post img
    for (let i = 0; i < postImg.length; i++) {
        var postImgElement = document.createElement('img');

        postImgElement.src = postImg[i];
        postImgElement.className = '';
        postImgElement.alt = '圖片';
        postImgContainer.appendChild(postImgElement);
    }

    // hashtag
    for (let i = 0; i < hashtag.length; i++) {
        var hashtagElement = document.createElement('a');
        hashtagElement.textContent = hashtag[i];
        hashtagElement.className = 'post-hashtag';
        hashtagElement.href = '127.0.0.1:8080?keyword=' + hashtag[i];

        postHashtagContainer.appendChild(hashtagElement);
    }

    // like count
    like.className = 'post-time';
    like.textContent = '讚：' + likeCount;

    // comment count
    comment.className = 'post-time';
    comment.textContent = '留言：' + CommentCount;

    postContainer.appendChild(posterImgContainer);
    postContainer.appendChild(poster);
    postContainer.appendChild(club);
    postContainer.appendChild(postTIme);
    postContainer.appendChild(postContent);
    postContainer.appendChild(postImgContainer);
    postContainer.appendChild(postHashtagContainer);
    postContainer.appendChild(like);
    postContainer.appendChild(comment);
    $("[data-container='socialPost']")[0].appendChild(postContainer);
}

// Remove all social post
function RemoveAllSocialPost() {
    let postCount = $("[data-post]").length;

    for (let i = 0; i < postCount; i++) {
        $("[data-post]")[0].remove();
    }
}
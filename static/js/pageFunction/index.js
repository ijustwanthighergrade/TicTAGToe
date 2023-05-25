// todo create social post
function CreateSocialPostItem(posterImgSrc,posterName,postImg=[]) {
    // create element
    let postContainer = document.createElement('div');
    let posterImgContainer = document.createElement('div');
    let posterImg = document.createElement('img');
    let poster = document.createElement('p');
    let club = document.createElement('p');
    let postTIme = document.createElement('p');
    let postContent = document.createElement('p');
    let postImgContainer = document.createElement('p');

    // poster img
    posterImgContainer.className = 'circle-image';
    posterImg.src = posterImgSrc;
    posterImgContainer.appendChild(posterImg);

    // post's poster
    poster.className = 'post-title';
    poster.textContent = '發文者：' + posterName;

    // post img
    for (let i = 0; i < postImg.length; i++) {
        var postImgElement = document.createElement('img');

        postImgElement.src = postImg[i];
        postImgElement.className = '';
        postImgElement.alt = '圖片';
        postImgContainer.appendChild(postImgElement);
    }



}

// Remove all social post
function RemoveAllSocialPost() {
    
}
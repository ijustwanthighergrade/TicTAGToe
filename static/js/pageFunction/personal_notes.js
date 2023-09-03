function saveChanges() {
    var postId = document.getElementById('postId').value;
    var location = document.getElementById('location').value;
    var tags = document.getElementById('tags').value;
    var content = document.getElementById('content').value;

    if (location === "" || tags === "" || content === "") {
        window.alert("欄位請勿為空!!");
    }
    else {
        let url = `/update/note`;
        let headers = {
            "Content-Type": "application/json"
        };
        let body = {
            "postId": postId,
            "location": location,
            "tags": tags,
            "content": content
        };

        fetch(url, {method: 'POST', headers:headers, body: JSON.stringify(body)})
        .then(function(res) {
            return res.json();
        })
        .then(function(result) {
            var result = result.result;
            window.alert(result);
        })
        .catch(function(err) {
            console.log(err);
        });
    }
}

function deletePost() {
    var postId = document.getElementById('postId').value;
    let url = `/delete/note`;
    let headers = {
        "Content-Type": "application/json"
    };
    let body = {
        "postId": postId
    };

    fetch(url, {method: 'POST', headers: headers, body: JSON.stringify(body)})
    .then(function(res) {
        return res.json();
    })
    .then(function(result) {
        var result = result.result;
        window.alert(result);
        window.location.href = "/individual";
    })
    .catch(function(err) {
        console.log(err);
    });
}
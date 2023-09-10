// Save changes
function saveChanges1() {
    var name = document.getElementById('name').value;
    var id = document.getElementById('id').value;
    var email = document.getElementById('email').value;

    if (name === "" || id === "" || email === "") {
        window.alert("欄位請勿為空!!");
    }
    else {
        let url = `/update_info`;
        let headers = {
            "Content-Type": "application/json"
        };
        let body = {
            "name": name,
            "id": id,
            "email": email
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
}

function saveChanges2() {
    window.alert("Update successful");
    window.location.href = "/individual";
}

// Cancel changes
function cancelChanges() {
    let url = `/update_cancel`;
    let headers = {
        "Content-Type": "application/json"
    };
    fetch(url, {method: 'GET', headers: headers})
    .then(function(res) {
        return res.json();
    })
    .then(function(result) {
        var name = document.getElementById('name');
        var id = document.getElementById('id');
        var email = document.getElementById('email');
        name.value = result.name;
        id.value = result.id;
        email.value = result.email;
    })
    .catch(function(err) {
        console.log(err);
    });
}

// Add hashtag
function addContainer1() {
    var tagContainer = document.getElementById('addTag');
    var addContainer = document.getElementById('addContainer1');

    if (tagContainer.value === "") {
        window.alert("請輸入hashtag!!");
    }
    else {
        let url = `/add_tag`;
        let headers = {
            "Content-Type": "application/json"
        };
        let body = {
            "tag": tagContainer.value
        };
        console.log(body);

        fetch(url, {method: 'POST', headers: headers, body: JSON.stringify(body)})
        .then(function(res) {
            return res.json()
        })
        .then(function(result) {
            var result = result.result;
        })
        .catch(function(err) {
            console.log(err);
        });

        const newContainer = document.createElement('div');
        newContainer.className = 'container-fluid mt-5';
        newContainer.innerHTML = `
            <div class="row">
                <div class="col-1"></div>
                <div class="col-7 text-center fs-1">
                    <input type="text" readonly class="form-control-plaintext" id="${tagContainer.value}" value="${tagContainer.value}">
                </div>
                <div class="col-4 text-center fs-1">
                    <button class="btn btn-light border-0 bg-transparent" onclick="deleteContainer1('${tagContainer.value}')">
                        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="#97CBFF" class="bi bi-x-square-fill" viewBox="0 0 16 16">
                            <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm3.354 4.646L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 1 1 .708-.708z"/>
                        </svg>
                    </button>
                </div>
            </div>
        `;
        addContainer.appendChild(newContainer);
        tagContainer.value = "";
    }
}

// Delete hashatg
function deleteContainer1(tag) {
    var container = document.getElementById(tag);
    let url = `/delete_tag`;
    let headers = {
        "Content-Type": "application/json"
    };
    let body = {
        "tag": container.value
    };

    fetch(url, {method: 'POST', headers: headers, body: JSON.stringify(body)})
    .then(function(res) {
        return res.json()
    })
    .then(function(result) {
        var result = result.result;
    })
    .catch(function(err) {
        console.log(err);
    });

    if (container) {
        container.closest('.container-fluid').remove();
    }
}

//Add socail link
function addContainer2() {
    var linkContainer = document.getElementById('addLink');
    var addContainer = document.getElementById('addContainer2');

    if (linkContainer.value === "") {
        window.alert("請輸入社群連結!!");
    }
    else {
        let url = `/add_link`;
        let headers = {
            "Content-Type": "application/json"
        };
        let body = {
            "link": linkContainer.value
        };
        console.log(body);

        fetch(url, {method: 'POST', headers: headers, body: JSON.stringify(body)})
        .then(function(res) {
            return res.json()
        })
        .then(function(result) {
            var result = result.result;
        })
        .catch(function(err) {
            console.log(err);
        });

        const newContainer = document.createElement('div');
        newContainer.className = 'container-fluid mt-5';
        newContainer.innerHTML = `
        <div class="row">
            <div class="col-1"></div>
            <div class="col-7 text-center fs-1">
                <input id="addLink" type="text" readonly class="form-control-plaintext" id="${linkContainer.value}" value="${linkContainer.value}">
            </div>
            <div class="col-4 text-center fs-1">
                <button class="btn btn-light border-0 bg-transparent" onclick="deleteContainer2('${linkContainer.value}')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="#97CBFF" class="bi bi-x-square-fill" viewBox="0 0 16 16">
                        <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm3.354 4.646L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 1 1 .708-.708z"/>
                    </svg>
                </button>
            </div>
        </div>
        `;
        addContainer.appendChild(newContainer);
        linkContainer.value = "";
    }
}

// Delete socail link
function deleteContainer2(link) {
    var container = document.getElementById(link);
    let url = `/delete_link`;
    let headers = {
        "Content-Type": "application/json"
    }
    let body = {
        "link": container.value
    };

    fetch(url, {method: 'POST', headers: headers, body: JSON.stringify(body)})
    .then(function(res) {
        return res.json()
    })
    .then(function(result) {
        var result = result.result;
    })
    .catch(function(err) {
        console.log(err);
    })

    if (container) {
        container.closest('.container-fluid').remove();
    }
}
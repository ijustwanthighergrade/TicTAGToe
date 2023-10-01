function add_member() {
    var email = document.getElementById('email_register').value;
    var password = document.getElementById('password_register').value;
    var password_confirm = document.getElementById('password_confirm').value;
    var name = document.getElementById('name').value;
    var id = document.getElementById('ID').value;
    var fileInput = document.getElementById('picture');
    var picture = fileInput.files[0];
    console.log(picture);

    if (email === "" || password === "" || name === "" || id === "") {
        window.alert("欄位請勿為空!!");
    }
    else {
        if (password !== password_confirm) {
            window.alert("密碼不一致!!");
            window.location.href = "/login";
        }
        else {
            let url = `/add/member`;
            let headers = {
                "Content-Type": "application/json"
            };
            let body = {
                "email": email,
                "password": password,
                "name": name,
                "id": id, 
                "picture": picture
            };

            fetch(url, {method: 'POST', headers: headers, body: JSON.stringify(body)})
            .then(function(res) {
                return res.json();  
            })
            .then(function(result) {
                var result = result.result;
                window.alert(result);
                // window.location.href = "/login";
            })
            .catch(function(err) {
                console.log(err);
            });
        }
    }
}
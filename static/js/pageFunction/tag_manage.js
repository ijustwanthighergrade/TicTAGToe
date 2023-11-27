document.getElementById('newtag_btn').addEventListener('click', function () {
    // Get the input value
    var inputValue = document.getElementById('new_tag').value;
    var selectValue = document.getElementById('tag_type').value;
    var color, tagCategory;
  
    // Check if the input value is not empty
    if (inputValue.trim() !== '') {
        if (selectValue === '4') {
          color = '#97CBFF';
          tagCategory = 'public';
        }
        else {
          color = '#f5aad3';
          tagCategory = 'private';
        }
  
        // Create a new span element
        var newSpan = document.createElement('span');
  
        // Set the id and text content of the new span
        newSpan.id = inputValue;
        newSpan.textContent = '#' + inputValue;
        newSpan.setAttribute('data-hashtag-type', tagCategory);
        newSpan.setAttribute('data-hashtag-status', 'new');
        newSpan.style.color = color;
  
        // Append the new span to the hashtag_list div
        document.getElementById('hashtag_list').appendChild(newSpan);
  
        // Add a non-breaking space after the new span
        document.getElementById('hashtag_list').appendChild(document.createTextNode('\u00A0'));
  
        // Clear the input field
        document.getElementById('new_tag').value = '';
    }
    else {
      alert('欄位請勿為空值!!');
      return;
    }
});

// TODO Add new tag
document.getElementById('confirm_submit').addEventListener('click', async function (event) {
    event.stopPropagation();
    let spanArray;
    let publicTagArray = [];
    let privateTagArray = [];
    let tagArray = [];
    let tagObj;
    
    var hashtagListDiv = document.getElementById('hashtag_list');
    // Get all span elements inside the div
    var spanElements = hashtagListDiv.getElementsByTagName('span');
    // Convert the HTMLCollection to an array
    spanArray = Array.from(spanElements);

    spanArray.forEach(function(span) {
        if (span.dataset.hashtagStatus === "public") {
            publicTagArray.push(span);
        }
        else {
            privateTagArray.push(span);
        }
    });

    if (spanArray.length > 0) {
        spanArray.forEach(function(span) {
            tagObj = {
                "tag_name": span.getAttribute('id'),
                "tag_type": span.dataset.hashtagStatus
            };
            tagArray.push(tagObj);
        });
        

        let addTagUrl = `/add_tag`;
        let headers = {
            "Content-Type": "application/json"
        };
        let addTagBody = {
            "tag": tagArray,
        };

        fetch(addTagUrl, {method: 'POST', headers: headers, body: JSON.stringify(addTagBody)})
        .then(res => {
        return res.json();
        })
        .then(result => {
        if (result.result === 'Add failed') {
            alert('Add failed!!');
            return;
        }
        })
        .catch(error => {
        console.log("Error: ", error);
        });
    }
    else {
        alert('已新增hashtag欄位請勿為空!!');
        return;
    }
});

document.getElementById('clean_content').addEventListener('click', function () {
    // Reload the page
    window.location.reload();
});
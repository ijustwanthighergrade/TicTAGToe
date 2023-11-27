document.addEventListener("DOMContentLoaded", function () {
  (function() {
    let public_hashtag_url = `/public/hashtags`;
    let private_hashtag_url = `/private/hashtags`;
    let headers = {
        "Content-Type": "application/json"
    };
  
    const fetch_public_hashtags = async () => {
      try {
        const res = await fetch(public_hashtag_url, {method: 'GET', headers: headers});
        const result = await res.json();
        return result;
      } catch(error) {
        console.log('Error', error);
      }
    };
  
    const fetch_private_hashtags = async () => {
      try {
        const res = await fetch(private_hashtag_url, {method: 'GET', headers: headers});
        const result = await res.json();
        return result;
      } catch(error) {
        console.log('Error', error);
      }
    };
    
    function autocomplete(inp, arr) {
        /*the autocomplete function takes two arguments,
        the text field element and an array of possible autocompleted values:*/
        var currentFocus;
        /*execute a function when someone writes in the text field:*/
        inp.addEventListener("input", function(e) {
            var a, b, i, val = this.value;
            /*close any already open lists of autocompleted values*/
            closeAllLists();
            if (!val) { return false;}
            currentFocus = -1;
            /*create a DIV element that will contain the items (values):*/
            a = document.createElement("DIV");
            a.setAttribute("id", this.id + "autocomplete-list");
            a.setAttribute("class", "autocomplete-items");
            /*append the DIV element as a child of the autocomplete container:*/
            this.parentNode.appendChild(a);
            /*for each item in the array...*/
            for (i = 0; i < arr.length; i++) {
              /*check if the item starts with the same letters as the text field value:*/
              if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                    b.addEventListener("click", function(e) {
                    /*insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;
                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                a.appendChild(b);
              }
            }
        });
        /*execute a function presses a key on the keyboard:*/
        inp.addEventListener("keydown", function(e) {
            var x = document.getElementById(this.id + "autocomplete-list");
            if (x) x = x.getElementsByTagName("div");
            if (e.keyCode == 40) {
              /*If the arrow DOWN key is pressed,
              increase the currentFocus variable:*/
              currentFocus++;
              /*and and make the current item more visible:*/
              addActive(x);
            } else if (e.keyCode == 38) { //up
              /*If the arrow UP key is pressed,
              decrease the currentFocus variable:*/
              currentFocus--;
              /*and and make the current item more visible:*/
              addActive(x);
            } else if (e.keyCode == 13) {
              /*If the ENTER key is pressed, prevent the form from being submitted,*/
              e.preventDefault();
              if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
              }
            }
        });
        function addActive(x) {
          /*a function to classify an item as "active":*/
          if (!x) return false;
          /*start by removing the "active" class on all items:*/
          removeActive(x);
          if (currentFocus >= x.length) currentFocus = 0;
          if (currentFocus < 0) currentFocus = (x.length - 1);
          /*add class "autocomplete-active":*/
          x[currentFocus].classList.add("autocomplete-active");
        }
        function removeActive(x) {
          /*a function to remove the "active" class from all autocomplete items:*/
          for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
          }
        }
        function closeAllLists(elmnt) {
          /*close all autocomplete lists in the document,
          except the one passed as an argument:*/
          var x = document.getElementsByClassName("autocomplete-items");
          for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
            x[i].parentNode.removeChild(x[i]);
          }
        }
      }
      /*execute a function when someone clicks in the document:*/
      document.addEventListener("click", function (e) {
          closeAllLists(e.target);
      });
    }
  
    fetch_public_hashtags().then(public_hashtags => {
      console.log(public_hashtags.result);
      autocomplete(document.getElementById('public_tag'), public_hashtags.result);
      fetch_private_hashtags().then(private_hashtags => {
        console.log(private_hashtags.result);
        autocomplete(document.getElementById('private_tag'), private_hashtags.result);
      });
    });
  })();
});

document.getElementById('public_btn').addEventListener('click', function () {
  // Get the input value
  var inputValue = document.getElementById('public_tag').value;

  // Check if the input value is not empty
  if (inputValue.trim() !== '') {
      const checkExistPublic = async (inputValue) => {
        let url = `/check/public/hashtag`;
        let headers = {
          "Content-Type": "application/json"
        };
        let body = {
          'tag_name': inputValue
        };
      
        const res = await fetch(url, {method: 'POST', headers: headers, body: JSON.stringify(body)})
        const result = await res.json()
        console.log(result.result);
        if (result.result === 'This hashtag does not exist') {
          alert('並沒有這個公開的hashtag!!');
          return;
        }
        else {
          // Create a new span element
          var newSpan = document.createElement('span');

          // Set the id and text content of the new span
          newSpan.id = inputValue;
          newSpan.textContent = '#' + inputValue;
          newSpan.setAttribute('data-hashtag-type', 'public');
          newSpan.setAttribute('data-hashtag-status', 'old');
          newSpan.style.color = '#97CBFF';

          // Append the new span to the hashtag_list div
          document.getElementById('hashtag_list').appendChild(newSpan);

          // Add a non-breaking space after the new span
          document.getElementById('hashtag_list').appendChild(document.createTextNode('\u00A0'));

          // Clear the input field
          document.getElementById('public_tag').value = '';
        }
      }

      checkExistPublic(inputValue);
  }
  else {
    alert('欄位請勿為空值!!');
    return;
  }
});

document.getElementById('private_btn').addEventListener('click', function () {
  // Get the input value
  var inputValue = document.getElementById('private_tag').value;

  // Check if the input value is not empty
  if (inputValue.trim() !== '') {
    const checkExistPrivate = async (inputValue) => {
      let url = `/check/private/hashtag`;
      let headers = {
        "Content-Type": "application/json"
      };
      let body = {
        'tag_name': inputValue
      };
    
      const res = await fetch(url, {method: 'POST', headers: headers, body: JSON.stringify(body)})
      const result = await res.json()
      console.log(result.result);
      if (result.result === 'This hashtag does not exist') {
        alert('並沒有這個私人的hashtag!!');
        return;
      }
      else {
        // Create a new span element
        var newSpan = document.createElement('span');

        // Set the id and text content of the new span
        newSpan.id = inputValue;
        newSpan.textContent = '#' + inputValue;
        newSpan.setAttribute('data-hashtag-type', 'private');
        newSpan.setAttribute('data-hashtag-status', 'old');
        newSpan.style.color = '#f5aad3';

        // Append the new span to the hashtag_list div
        document.getElementById('hashtag_list').appendChild(newSpan);

        // Add a non-breaking space after the new span
        document.getElementById('hashtag_list').appendChild(document.createTextNode('\u00A0'));

        // Clear the input field
        document.getElementById('private_tag').value = '';
      }
    }

    checkExistPrivate(inputValue);

  }
  else {
    alert('欄位請勿為空值!!');
    return;
  }
});

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

document.getElementById('confirm_submit').addEventListener('click', async function (event) {
      event.stopPropagation();
      let title = document.getElementById('title').value;
      let location = document.getElementById('location').value;
      let member = document.getElementById('member').value;
      let content = document.getElementById('content').value;
      var tagContent = [];
      let spanArray;
      let oldTagArray = [];
      let newTagArray = [];
      let dataId;

      if (title !== '' && content !== '' ) {
        // Get the reference to the parent div
        var hashtagListDiv = document.getElementById('hashtag_list');

        // Get all span elements inside the div
        var spanElements = hashtagListDiv.getElementsByTagName('span');

        // Convert the HTMLCollection to an array
        spanArray = Array.from(spanElements);
          // console.log('content: ', span.textContent);
          // console.log('id: ', span.getAttribute('id')); 
          // console.log('hashtagType: ', span.dataset.hashtagType); 
          // console.log('hashtagStatus: ', span.dataset.hashtagStatus); 
        // });

        for (let i = 0; i < $("[data-hashtag-type]").length; i++) {
            tagContent.push($("[data-hashtag-type]")[i].textContent.split('#')[1]);
        }

        console.log("tagContent: ", tagContent);

        let AddNoteUrl = `/add/note`;
        let headers = {
          "Content-Type": "application/json"
        };
        let AddNoteBody = {
          "title": title,
          "location": location,
          "member": member,
          "content": content,
          "tag": tagContent
        }

        try {
            const res = await fetch(AddNoteUrl, { method: 'POST', headers: headers, body: JSON.stringify(AddNoteBody) });
            const result = await res.json();
            if (result.result === 'Add failed') {
                alert('Add failed!!');
                return;
            } else {
                dataId = result.postId;
                alert('Add successful!!');
                window.location.href = "/individual";
            }
        } catch (error) {
            console.log("Error: ", error);
        }
      }
      else {
        alert('標題和內容欄位請勿為空!!');
        return;
      }
});

document.getElementById('clean_content').addEventListener('click', function () {
  // Reload the page
  window.location.reload();
});
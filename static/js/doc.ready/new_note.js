$(function(){
    // control menu
    ControlMenu();

    // header search bar
    ClickTagStartSearch();

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
})
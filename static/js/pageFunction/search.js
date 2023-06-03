// create social post
function CreateSocialPostItem(posterImgSrc,posterName,postClub,time,content,likeCount,CommentCount,hashtag=[],postImg=[]) {
    // create element
    let postContainer = document.createElement('div');
    let posterImgContainer = document.createElement('div');
    let posterImg = document.createElement('img');
    let poster = document.createElement('p');
    let club = document.createElement('p');
    let postTIme = document.createElement('p');
    let postContent = document.createElement('p');
    let postImgContainer = document.createElement('div');
    let postHashtagContainer = document.createElement('p');
    let like = document.createElement('p');
    let comment = document.createElement('p');

    postContainer.dataset.post = '';
    postContainer.className = 'post-card';

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
    postImgContainer.className = 'slideshow ';
    for (let i = 0; i < postImg.length; i++) {
        var postImgElement = document.createElement('div');
        var img = document.createElement('img');

        // postImgElement.style.backgroundImage = postImg[i];
        img.src = postImg[i];
        img.alt = '圖片';
        postImgElement.className = 'slide';
        
        postImgElement.appendChild(img);
        postImgContainer.appendChild(postImgElement);
    }

    // hashtag
    for (let i = 0; i < hashtag.length; i++) {
        var hashtagElement = document.createElement('a');
        hashtagElement.textContent = hashtag[i];
        hashtagElement.className = 'post-hashtag';
        hashtagElement.href = '/searchres?keyword=' + hashtag[i];

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

// create knowledge map
/*
    * example 
    * nodeData =[{ key: 1,category:"tag", text: "xxx",type:"tag" },{ key: 2, text: "xxx xxx" }...]
    * linkData = [{ from: nodeData key, to: nodeData key,},{ from: nodeData key, to: nodeData key}...]
*/
function CreateKnowledgeMap(nodeData,linkData) {
    var $ = go.GraphObject.make;  // for conciseness in defining templates
    myDiagram =
    $(go.Diagram, "knowledgeMap",  // must name or refer to the DIV HTML element
        {
        initialAutoScale: go.Diagram.Uniform,  // an initial automatic zoom-to-fit
        contentAlignment: go.Spot.Center,  // align document to the center of the viewport
        layout:
        $(go.ForceDirectedLayout,  // automatically spread nodes apart
            { maxIterations: 200, defaultSpringLength: 30, defaultElectricalCharge: 100 })
        });
    // define each Node's appearance
        myDiagram.nodeTemplate =
        $(go.Node, "Auto",  // the whole node panel
            { locationSpot: go.Spot.Center },
            // define the node's outer shape, which will surround the TextBlock
        $(go.Shape, "Rectangle",
            { fill: $(go.Brush, "Linear", { 0: "rgb(254, 201, 0)", 1: "rgb(254, 162, 0)" }), stroke: "black" }),
        $(go.TextBlock,
            { font: "bold 10pt helvetica, bold arial, sans-serif", margin: 4 },
        new go.Binding("text", "text"))
        );
 // replace the default Link template in the linkTemplateMap
    myDiagram.nodeTemplateMap.add("tag",
        $(go.Node, "Auto",  // the whole node panel
            { locationSpot: go.Spot.Center },
            // define the node's outer shape, which will surround the TextBlock
        $(go.Shape, "Rectangle",
            { fill: $(go.Brush, "Linear", { 0: "#97CBFF", 1: "#97CBFF" }), stroke: "black" }),
        $(go.TextBlock,
            { font: "bold 10pt helvetica, bold arial, sans-serif", margin: 4 },
        new go.Binding("text", "text"))
        )
    );

    myDiagram.nodeTemplateMap.add("people",
        $(go.Node, "Auto",
            $(go.Panel, "Vertical",
                // $(go.Shape, "Circle",{ fill: "lightgreen", stroke: "black", strokeWidth: 1, width: 40, height: 40 }),
                $(go.Picture,{ source: "../static/img/icon.png", width: 30, height: 30 })
            )
            //,
            // $(go.TextBlock,{ margin: 8, font: "12px sans-serif" },
            //     new go.Binding("text", "text")
            // )
        )
    );

    myDiagram.nodeTemplateMap.add("place",
        $(go.Node, "Auto",
            $(go.Panel, "Vertical",
                // $(go.Shape, "Circle",{ fill: "lightgreen", stroke: "black", strokeWidth: 1, width: 40, height: 40 }),
                $(go.Picture,{ source: "../static/img/address.png", width: 30, height: 30 })
            )
            //,
            // $(go.TextBlock,{ margin: 8, font: "12px sans-serif" },
            //     new go.Binding("text", "text")
            // )
        )
    );

    myDiagram.nodeTemplateMap.add("obj",
        $(go.Node, "Auto",
            $(go.Panel, "Vertical",
                // $(go.Shape, "Circle",{ fill: "lightgreen", stroke: "black", strokeWidth: 1, width: 40, height: 40 }),
                $(go.Picture,{ source: "../static/img/bookmark.png", width: 30, height: 30 })
            )
            //,
            // $(go.TextBlock,{ margin: 8, font: "12px sans-serif" },
            //     new go.Binding("text", "text")
            // )
        )
    );


    myDiagram.linkTemplate =
    $(go.Link,  // the whole link panel
    $(go.Shape, { stroke: "black" }),// the link shape
    // $(go.Shape,{ toArrow: "standard", stroke: null }), // the arrowhead
    $(go.Panel, "Auto",
    $(go.TextBlock,  // the label text
    {
        textAlign: "center",
        font: "10pt helvetica, arial, sans-serif",
        stroke: "#555555",
        margin: 4
    },
    //  new go.Binding("text", "text"))
     new go.Binding())
     )
   );
 // create the model for the concept map
//  var nodeDataArray = [
//   { key: 1,category:"icon", text: "Concept Maps",type:"tag" },
//   { key: 2, text: "Organized Knowledge" },
//   { key: 3, text: "Context Dependent" },
//   { key: 4, text: "Concepts" },
//  ];
    var nodeDataArray = nodeData;
//  var linkDataArray = [
//   { from: 1, to: 2, text: "represent" },
//   { from: 2, to: 3, text: "is" },
//   { from: 2, to: 4, text: "is" }
//  ];
    var linkDataArray = linkData;
    myDiagram.model = new go.GraphLinksModel(nodeDataArray, linkDataArray);
    myDiagram.addDiagramListener("ObjectSingleClicked", function(e) {
    var part = e.subject.part;
    if (part instanceof go.Node) {
        var node = part;
        // alert("Node clicked: " + node.data.type);
        switch (node.data.type) {
            case 'tag':
                // search this tag
                location.href = '/searchres?keyword=' + node.data.text;
                break;

            case 'people':
                // todo 到個人頁面
                // location.href = '/...?a=';
                alert('該功能尚未開啟，未來將會導向至個人頁面');
                break;

            case 'post':
                // todo 到貼文頁面
                // location.href = '/...?a=';
                alert('該功能尚未開啟，未來將會導向至個人頁面');
                break;

            case 'place':
                // todo open block ui and show info
                SetBlockUiContent('地點描述：' + node.data.text);
                break;

            case 'obj':
                // todo open block ui and show info

                SetBlockUiContent('物品描述：' + node.data.text);
                break;
        
            default:
                break;
        }

        return;
    }
 });
}

function AddImgInBlockUi() {
    
}

function SetBlockUiContent(content,addNewEle=false) {
    $("[data-input='blockUiContent']")[0].textContent = content;
    
    $("[data-block-ui='knowledgeMap']")[0].style.display = '';
}
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

// create knowledge map
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
    myDiagram.nodeTemplateMap.add("icon",
        $(go.Node, "Auto",
            $(go.Panel, "Vertical",
                $(go.Shape, "Circle",{ fill: "lightgreen", stroke: "black", strokeWidth: 1, width: 40, height: 40 }),
                $(go.Picture,{ source: "icon.png", width: 30, height: 30 })
            ),
            $(go.TextBlock,{ margin: 8, font: "12px sans-serif" },
                new go.Binding("text", "text")
            )
        )
    );
    myDiagram.linkTemplate =
    $(go.Link,  // the whole link panel
    $(go.Shape, { stroke: "black" }),// the link shape
    $(go.Shape,{ toArrow: "standard", stroke: null }), // the arrowhead
    $(go.Panel, "Auto",
    $(go.Shape,  // the label background, which becomes transparent around the edges
        {fill: $(go.Brush, "Radial", { 0: "rgb(240, 240, 240)", 0.3: "rgb(240, 240, 240)", 1: "rgba(240, 240, 240, 0)" }),
        stroke: null
        }
    ),
   $(go.TextBlock,  // the label text
    {
        textAlign: "center",
        font: "10pt helvetica, arial, sans-serif",
        stroke: "#555555",
        margin: 4
    },
     new go.Binding("text", "text"))
     )
   );
 // create the model for the concept map
//  var nodeDataArray = [
//   { key: 1,category:"icon", text: "Concept Maps",type:"tag" },
//   { key: 2, text: "Organized Knowledge" },
//   { key: 3, text: "Context Dependent" },
//   { key: 4, text: "Concepts" },
//   { key: 5, text: "Propositions" },
//   { key: 6, text: "Associated Feelings or Affect" },
//   { key: 7, text: "Perceived Regularities" },
//   { key: 8, text: "Labeled" },
//   { key: 9, text: "Hierarchically Structured" },
//   { key: 10, text: "Effective Teaching" },
//   { key: 11, text: "Crosslinks" },
//   { key: 12, text: "Effective Learning" },
//   { key: 13, text: "Events (Happenings)" },
//   { key: 14, text: "Objects (Things)" },
//   { key: 15, text: "Symbols" },
//   { key: 16, text: "Words" },
//   { key: 17, text: "Creativity" },
//   { key: 18, text: "Interrelationships" },
//   { key: 19, text: "Infants" },
//   { key: 20, text: "Different Map Segments" }
//  ];
    var nodeDataArray = nodeData;
//  var linkDataArray = [
//   { from: 1, to: 2, text: "represent" },
//   { from: 2, to: 3, text: "is" },
//   { from: 2, to: 4, text: "is" },
//   { from: 2, to: 5, text: "is" },
//   { from: 2, to: 6, text: "includes" },
//   { from: 2, to: 10, text: "necessary\nfor" },
//   { from: 2, to: 12, text: "necessary\nfor" },
//   { from: 4, to: 5, text: "combine\nto form" },
//   { from: 4, to: 6, text: "include" },
//   { from: 4, to: 7, text: "are" },
//   { from: 4, to: 8, text: "are" },
//   { from: 4, to: 9, text: "are" },
//   { from: 5, to: 9, text: "are" },
//   { from: 5, to: 11, text: "may be" },
//   { from: 7, to: 13, text: "in" },
//   { from: 7, to: 14, text: "in" },
//   { from: 7, to: 19, text: "begin\nwith" },
//   { from: 8, to: 15, text: "with" },
//   { from: 8, to: 16, text: "with" },
//   { from: 9, to: 17, text: "aids" },
//   { from: 11, to: 18, text: "show" },
//   { from: 12, to: 19, text: "begins\nwith" },
//   { from: 17, to: 18, text: "needed\nto see" },
//   { from: 18, to: 20, text: "between" }
//  ];
    var linkDataArray = linkData;
    myDiagram.model = new go.GraphLinksModel(nodeDataArray, linkDataArray);
    myDiagram.addDiagramListener("ObjectSingleClicked", function(e) {
    var part = e.subject.part;
    if (part instanceof go.Node) {
        var node = part;
        alert("Node clicked: " + node.data.type);
    }
 });
}
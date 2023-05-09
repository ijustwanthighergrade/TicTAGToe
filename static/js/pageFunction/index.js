function SetTagCloud(tag){
    //取得d3顏色
    var fill = d3.scaleOrdinal(d3.schemeCategory10);

    //文字雲/關鍵字，及字型大小（這邊只放三個）
    var data = [
        // {text: "加里山", size: 21},
        // {text: "文字雲", size: 18},
        // {text: "翠湖 螢火蟲", size: 17}
    ];
    
    for (let i = 0; i < tag.length; i++) {
        data.push({text: tag[i], size:Math.random() * 2});
    }

    //取得呈現處的寬、高
    var w = parseInt(d3.select("#tag").style("width"), 50);
    var h = parseInt(d3.select("#tag").style("height"), 50);

    d3.layout.cloud().size([w, h])
            .words(data)
            .padding(2)
            .rotate(function () {
                return ~~(Math.random() * 2) * 90;
            })
            .rotate(function () {
                return 0;
            })
            .fontSize(function (d) {
                return d.size;
            })
            .on("end", draw)
            .start();
}

function DrawTagCloud(words) {
    // d3.select("#tag").append("svg")
    d3.select("[data-container='tagCloud']").append("svg")
        .attr("width", w)
        .attr("height", h)
        .append("g")
        .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")")
        .selectAll("text")
        .data(words)
        .enter().append("text")
        .style("font-size", function (d) {
            return d.size + "px";
        })
        .style("font-family", "Microsoft JhengHei")
        .style("cursor", 'pointer')
        .style("fill", function (d, i) {
            return fill(i);
        })
        .attr("text-anchor", "middle")
        .attr("transform", function (d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function (d) {
            return d.text;
        })
        .on("click", function (d) {
            window.open("https://www.google.com/search?q=" + d.text, '_blank');
        });
}
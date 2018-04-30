$(document).ready(function(){
    // global value which will use later
    var traPerc;
    var traMotion;
    var traColor;
    var traAudio;
    var traArray;
    var starPerc;
    var starMotion;
    var starColor;
    var starAudio;
    var starArray;
    var musPerc;
    var musMotion;
    var musColor;
    var musAudio;
    var musArray;
    var movPerc;
    var movMotion; 
    var movColor;
    var movAudio;
    var movArray;
    var intPerc;
    var intMotion;
    var intColor;
    var intAudio;
    var intArray;
    var floPerc;
    var floMotion;
    var floColor;
    var floAudio;
    var floArray;
    var spoPerc;
    var spoMotion;
    var spoColor;
    var spoAudio;
    var spoArray;
    var motionPerc;
    var audioPerc;
    var colorPerc;
    var timeArray = []
    count = 0;
    for(var i = 0; i < 601;i++){
        var str = ""
        if(count <10) {
            str +="0:0" + count
        } else {
            str +="0:" + count
        }
        timeArray.push(str)
        if(i%30 == 0) {
            count++;
        }
    }
    
    $("#searchbutton").click(function(){                             
        // sort match rate, and put top match in datbase video section
        var input = $("#searchInput").val();
        xmlhttp=new XMLHttpRequest()
        xmlhttp.open("GET", input + ".json", false);
        xmlhttp.send();
        xmlDoc=xmlhttp.responseText;
        obj=JSON.parse(xmlDoc);
        // read traffic video data from JSON
        motionPerc = obj.data.motion
        colorPerc = obj.data.color
        audioPerc = obj.data.audio
        traPerc = obj.data.traffic.matchPerc
        traMotion = obj.data.traffic.motion
        traColor = obj.data.traffic.color
        traAudio = obj.data.traffic.audio
        traArray = obj.data.traffic.array
                             
        // read starcraft data
        starPerc = obj.data.starcraft.matchPerc
        starMotion = obj.data.starcraft.motion
        starColor = obj.data.starcraft.color
        starAudio = obj.data.starcraft.audio
        starArray = obj.data.starcraft.array
                             

        // read musicvideo data
        musPerc = obj.data.musicvideo.matchPerc
        musMotion = obj.data.musicvideo.motion
        musColor = obj.data.musicvideo.color
        musAudio = obj.data.musicvideo.audio
        musArray = obj.data.musicvideo.array
                             
                             
        // read movie data
        movPerc = obj.data.movie.matchPerc
        movMotion = obj.data.movie.motion
        movColor = obj.data.movie.color
        movAudio = obj.data.movie.audio
        movArray = obj.data.movie.array

                             
        // read interview data
        intPerc = obj.data.interview.matchPerc
        intMotion = obj.data.interview.motion
        intColor = obj.data.interview.color
        intAudio = obj.data.interview.audio
        intArray = obj.data.interview.array
                             
        // read flowers data
        floPerc = obj.data.flowers.matchPerc
        floMotion = obj.data.flowers.motion
        floColor = obj.data.flowers.color
        floAudio = obj.data.flowers.audio
        floArray = obj.data.flowers.array
                             
        // read sports data
        spoPerc = obj.data.sports.matchPerc
        spoMotion = obj.data.sports.motion
        spoColor = obj.data.sports.color
        spoAudio = obj.data.sports.audio
        spoArray = obj.data.sports.array
        
        var finalArray = [spoPerc,floPerc,intPerc,movPerc,musPerc,starPerc,traPerc]
        finalArray.sort().reverse()
        var selectString = ""
        var videoString = ""
        for (var i = 0; i < finalArray.length; i++) {
            if(finalArray[i] == traPerc) {
                selectString += "<option value=\"tra\">traffic(" + (traPerc * 100).toFixed(0)+"%)</option>"
                if(i == 0){
                    $('#botSection video source').attr('src', "traffic.mp4");
                    $("#botSection video")[0].load();
                    drawGraph(traArray,timeArray);
                }
            } else if(finalArray[i] == starPerc) {
                selectString += "<option value=\"star\">starcraft(" + (starPerc * 100).toFixed(0)+"%)</option>"
                if(i == 0){
                    $('#botSection video source').attr('src', "starcraft.mp4");
                    $("#botSection video")[0].load();
                    drawGraph(starArray,timeArray);
                }
            } else if(finalArray[i] == musPerc) {
                selectString += "<option value=\"mus\">musicvideo(" + (musPerc * 100).toFixed(0)+"%)</option>"
                if(i == 0){
                    $('#botSection video source').attr('src', "musicvideo.mp4");
                    $("#botSection video")[0].load();
                    drawGraph(musArray,timeArray);
                }
            } else if(finalArray[i] == movPerc) {
                selectString += "<option value=\"mov\">movie(" + (movPerc * 100).toFixed(0) * 100+"%)</option>" 
                if(i == 0){
                    $('#botSection video source').attr('src', "movie.mp4");
                    $("#botSection video")[0].load();
                    drawGraph(movArray,timeArray);
                }
            } else if(finalArray[i] == intPerc) {
                selectString += "<option value=\"int\">interview(" + (intPerc * 100).toFixed(0)+ "%)</option>"
                if(i == 0){
                    $('#botSection video source').attr('src', "interview.mp4");
                    $("#botSection video")[0].load();
                    drawGraph(intArray,timeArray);
                }
            } else if(finalArray[i] == floPerc) {
                 selectString += "<option value=\"flo\">flowers(" + (floPerc * 100).toFixed(0)+"%)</option>"
                 if(i == 0){
                    $('#botSection video source').attr('src', "flowers.mp4");
                    $("#botSection video")[0].load();
                     drawGraph(floArray,timeArray);
                 }
            } else {
                // this is sports
                selectString += "<option value=\"spo\">sports(" + (spoPerc * 100).toFixed(0)+"%)</option>"
                if(i == 0){
                    $('#botSection video source').attr('src', "sports.mp4");
                    $("#botSection video")[0].load();
                    drawGraph(spoArray,timeArray);
                 }
            }
        }
        $('#botParts video source').attr('src', input+".mp4");
        $("#botParts video")[0].load();
        // add table statistic to table content
        var tableContent = "<tr><th>Video Type</th><th>Motion Change(" + (motionPerc * 100).toFixed(0) + "%)</th><th>Color Change(" + (colorPerc * 100).toFixed(0) + "%)</th><th>Sound Change(" + (audioPerc * 100).toFixed(0) + "%)</th><th>Total Percentage</th></tr>"
        tableContent += "<tr><td>Traffic</td><td>" + (traMotion * 100).toFixed(0) +"%</td><td>"+ (traColor*100).toFixed(0) + "%</td><td>"+ (traAudio*100).toFixed(0) + "%</td><td>"+ (traPerc*100).toFixed(0) + "%</td></tr>"
        tableContent += "<tr><td>Starcraft</td><td>" + (starMotion * 100).toFixed(0) +"%</td><td>"+ (starColor*100).toFixed(0) + "%</td><td>"+ (starAudio*100).toFixed(0)  + "%</td><td>"+ (starPerc*100).toFixed(0) + "%</td></tr>"
        tableContent += "<tr><td>MusicVideo</td><td>" + (musMotion * 100).toFixed(0) +"%</td><td>"+ (musColor*100).toFixed(0) + "%</td><td>"+ (musAudio*100).toFixed(0) + "%</td><td>"+ (musPerc*100).toFixed(0) + "%</td></tr>"
        tableContent += "<tr><td>Movie</td><td>" + (movMotion * 100).toFixed(0) +"%</td><td>"+ (movColor*100).toFixed(0) + "%</td><td>"+ (movAudio*100).toFixed(0) + "%</td><td>"+ (movPerc*100).toFixed(0) + "%</td></tr>"
        tableContent += "<tr><td>interview</td><td>" + (intMotion * 100).toFixed(0) +"%</td><td>"+ (intColor*100).toFixed(0) + "%</td><td>"+ (intAudio*100).toFixed(0)  + "%</td><td>"+ (intPerc*100).toFixed(0) + "%</td></tr>"
        tableContent += "<tr><td>Flowers</td><td>" + (floMotion * 100).toFixed(0) +"%</td><td>"+ (floColor*100).toFixed(0) + "%</td><td>"+ (floAudio*100).toFixed(0)  + "%</td><td>"+ (floPerc*100).toFixed(0) + "%</td></tr>"
        tableContent += "<tr><td>Sports</td><td>" + (spoMotion * 100).toFixed(0) +"%</td><td>"+ (spoColor*100).toFixed(0) + "%</td><td>"+ (spoAudio*100).toFixed(0) + "%</td><td>"+ (spoPerc*100).toFixed(0) + "%</td></tr>"
         $('table').html(tableContent);
        $("#selectResult").html(selectString);
        $("#content").show()
    });
    $("#numTableBut").click(function(){
        $("#statsTable").show()
        $("#content").hide()
    });
    
    // select change controller, need to change the graph as well.graph has not draw yet.
    $('select').on('change', function() {
        if(this.value == "flo"){
            $('#botSection video source').attr('src', "flowers.mp4");
            $("#botSection video")[0].load();
            drawGraph(floArray,timeArray);
        } else if(this.value == "spo"){
            $('#botSection video source').attr('src', "sports.mp4");
            $("#botSection video")[0].load();
            drawGraph(spoArray,timeArray);
        } else if(this.value == "int"){
            $('#botSection video source').attr('src', "interview.mp4");
            $("#botSection video")[0].load();
            drawGraph(intArray,timeArray);
        } else if(this.value == "mus"){
            $('#botSection video source').attr('src', "musicvideo.mp4");
            $("#botSection video")[0].load();
            drawGraph(musArray,timeArray);
        } else if(this.value == "star"){
            $('#botSection video source').attr('src', "starcraft.mp4");
            $("#botSection video")[0].load();
            drawGraph(starArray,timeArray);
        } else if(this.value == "tra"){
            $('#botSection video source').attr('src', "traffic.mp4");
            $("#botSection video")[0].load();
            drawGraph(traArray,timeArray);
        } else {
            //movie has been select
            $('#botSection video source').attr('src', "movie.mp4");
            $("#botSection video")[0].load();
            drawGraph(movArray,timeArray);
        }
    })
    $("#gobackbut").click(function(){
        $("#statsTable").hide()
        $("#content").show()
    });
});
function drawGraph(data, array){
    chart = Highcharts.chart('container', {
            title: {
                text: ''
            },
            xAxis: {
                categories: array,
                tickInterval:30
            },
            yAxis:{
                 title:{
                    text:''
                },
                min: 0
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },

            series: [{
                type: 'area',
                data: data
            }]
        });
    chart.series[0].setData(data,true);
}

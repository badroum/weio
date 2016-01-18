/**
 * Wifi SockJS object, Web socket for scaning and changing wifi parameters
 */
var updaterSocket;

var weioNeedsUpdate = false;

var weioUpdaterTimeTillReload = 0; // counter till 100%
var updaterTimerInterval;

var estimatedInstallTime = 0;

var updaterChart;

var connectedToInternet = false;
/**
 * Global configuration
 */
var confFile;
var http_prefix = "http://";

$(document).ready(function() {

    /** Get global configuration */
    $.getJSON('config.json', function(data) {
                      confFile = data;

            if (confFile.https == "YES") {
                http_prefix = "https://";
            }
            else {
                http_prefix = "http://";
            }

            /**
            * Wifi SockJS object, Web socket for scaning and changing wifi parameters
            */
            updaterSocket = new SockJS(http_prefix + location.host + '/updater');


            //////////////////////////////////////////////////////////////////////////////////////////////////// SOCK JS WIFI

            /*
            * On opening of wifi web socket ask server to scan wifi networks
            */
            updaterSocket.onopen = function() {
                console.log('Updater Web socket is opened');
                //updateCheck();
            };

            /*
            * Wifi web socket parser, what we got from server
            */
            updaterSocket.onmessage = function(e) {
                //console.log('Received: ' + e.data);

                // JSON data is parsed into object
                data = JSON.parse(e.data);
                console.log(data);

                if ("requested" in data) {
                    // this is instruction that was echoed from server + data as response
                    instruction = data.requested;

                    if (instruction in callbacksUpdater)
                        callbacksUpdater[instruction](data);
                } else if ("serverPush" in data) {
                        // this is instruction that was echoed from server + data as response
                        instruction = data.serverPush;
                        if (instruction in callbacksUpdater)
                            callbacksUpdater[instruction](data);
                }
            };

            updaterSocket.onclose = function() {
                console.log('Updater Web socket is closed');
            };

    }); /** getJSON */

    updaterChart = new Chart(document.getElementById("updateProgressChart").getContext("2d"));

});


/**
 * Update check. Asks server to compare it's own version with distant one
 */
function updateCheck() {
    $("#needsUpdateStatus").html("<i class='icon-spinner'></i> Checking updates...");
    var rq = { "request": "checkVersion"};
    updaterSocket.send(JSON.stringify(rq));
}

function updateProgressBar(data) {
    updaterTimerInterval = setInterval(function(){countTimeTillReload()},1000);
}

function countTimeTillReload(data) {
    // normal update needs 35 secs to be done
    delayTime = 100.0/estimatedInstallTime;
    weioUpdaterTimeTillReload+=delayTime;

    var updateData = [
                   // Chart
                   {
                   value: weioUpdaterTimeTillReload,
                   color :"#0088cc"
                   },
                   {
                   value : 100.0-weioUpdaterTimeTillReload,
                   color:"#666"
                   }
                   ];


    updaterChart.Doughnut(updateData, defs);

    if (Math.round(weioUpdaterTimeTillReload)<100) {
        $("#progressStatus").html("Installing WeIO " + String(Math.round(weioUpdaterTimeTillReload)) + "%");
    } else {
        $("#progressStatus").html("Finished, please reload this page");
        clearInterval(updaterTimerInterval);
        $("#reloadMeButton").show();
    }
}

function reloadMe() {
    var randomNumber = Math.random();
    // prevent loading from cache
    var url = http_prefix + location.host + "/?"+randomNumber;
    //location.reload();
    window.location.href = url;
}

function reinstallFw() {

    if (connectedToInternet) {
        var rq = { "request": "reinstallFw"};
        updaterSocket.send(JSON.stringify(rq));
        console.log("reinstall rq sent to server");
        $("#updaterMessage").html("WeIO is downloading firmware right now. Please don't touch a thing. Once finished downloading, application will be closed and installation process will start. Be patient because this procedure can take up to 5 minutes");
        $("#reloadMeButton").hide();
        $("#updateWeioProcedure").modal("show");
    } else {
        $("#noInternet").modal("show");
    }

}

function downloadProgressFw(data) {
    var percent = parseInt(data.data);

    var updateData = [
                   // Chart
                   {
                   value: percent,
                   color :"#0088cc"
                   },
                   {
                   value : 100.0-percent,
                   color:"#666"
                   }
                   ];

    updaterChart.Doughnut(updateData, defs);
    $("#progressStatus").html("Downloading WeIO " + String(percent) + "%");
}

function reinstallFwCounter() {
    console.log("go to black!");
}

function noInternet() {
    connectedToInternet = false;
    //$("#noInternet").modal("show");
}

//CALLBACKS////////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * Define callbacks here and request keys
 * Each key is binded to coresponding function
 */
 // XXX need a modal view for errorDownloading
var callbacksUpdater = {
    "checkVersion": checkVersion,
    "updateProgress" : updateProgressBar,
    "readyToReinstallFw" : reinstallFwCounter,
    "downloadingFw": downloadProgressFw,
    "noInternetConnection": noInternet
};

var modalIsPopulated = false;
function checkVersion(data) {

    console.log("Local version is : " + data.localVersion);
    console.log("WeIO repository version is : " + data.distantVersion);
    console.log("WeIO needs un update : " + data.needsUpdate);

    modalIsPopulated = true;
    connectedToInternet = true;
    if (data.needsUpdate=="YES") {
        console.log("WeIO install duration in s will be : " + data.install_duration);
        needsUpdate = true;
        $("#needsUpdateStatus").html("WeIO update is available!");

        $("#updateButton").html("Update WeIO");

        // XXX Where is this message displayed ?
        txt = "";
        txt+="Your current version is " + data.localVersion + " and the latest available is " + data.distantVersion;
        txt+="<br>";
        txt+="<h4> What's new in " + data.distantVersion + " version " + data.description + "</h4>";
        txt+="<br>";
        txt+="<p>" + data.whatsnew + "</p>";
        txt+="<br>";
        txt+="Click on Update WeIO to start updating process";

        $("#updateWeioData").html(txt);
        weioNeedsUpdate = true;
        estimatedInstallTime = data.install_duration;

    } else {
        needsUpdate = false;
        $("#needsUpdateStatus").html("WeIO version is up to date");
        $("#updateButton").html("OK");
        $("#updateWeioData").html("Your current version " + data.localVersion + " is up to date!");
        weioNeedsUpdate = false;
    }

};

function bringUpdater(){
    if (modalIsPopulated && weioNeedsUpdate) {
        $("#reinstallFw").modal("show");
    }
}


var defs = {
    //Boolean - Whether we should show a stroke on each segment
    segmentShowStroke : true,

    //String - The colour of each segment stroke
    segmentStrokeColor : "#fff",

    //Number - The width of each segment stroke
    segmentStrokeWidth : 2,

    //The percentage of the chart that we cut out of the middle.
    percentageInnerCutout : 70,

    //Boolean - Whether we should animate the chart
    animation : false,

    //Number - Amount of animation steps
    animationSteps : 100,

    //String - Animation easing effect
    animationEasing : "easeOutBounce",

    //Boolean - Whether we animate the rotation of the Doughnut
    animateRotate : true,

    //Boolean - Whether we animate scaling the Doughnut from the centre
    animateScale : false,

    //Function - Will fire on animation completion.
    onAnimationComplete : null
};

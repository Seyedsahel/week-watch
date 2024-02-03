chrome.tabs.onCreated.addListener(function(tab) {
  var url = tab.url;
  var serverUrl = "https://getinfo.iran.liara.run/record/";
  var localUrl = "http://localhost:8000/record/";

  var xhr = new XMLHttpRequest();
  xhr.open("POST", localUrl, true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

  var payload = "link=" + encodeURIComponent(url);
  payload += "&email=TahaM8000@gmail.com";
  payload += "&action=create";

  xhr.send(payload);
});


chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    var url = tab.url;
    var serverUrl = "https://getinfo.iran.liara.run/record/";
    var localUrl = "http://localhost:8000/record/";

    var xhr = new XMLHttpRequest();
    xhr.open("POST", localUrl, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    var params = new URLSearchParams();
    params.append("link", url);
    params.append("email", "TahaM8000@gmail.com");
    params.append("action", "updated");
    
    params.append("changeInfo", changeInfo);
    params.append("tabId", tabId);

    xhr.send(params);
});
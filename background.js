var currentURL = window.location.href;

function sendLinkToWebsite(link) {
  var url = 'https://example.comhttps://djangoworker.pythonanywhere.com/polls/giveme//your-endpoint'; // آدرس وبسایت و نقطه پایانی را در این قسمت قرار دهید
  var data = {
    link: link
  };

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(function(response) {
    // پاسخ دریافتی از وبسایت
    console.log('پاسخ دریافتی:', response);
  })
  .catch(function(error) {
    // خطا در ارسال درخواست
    console.error('خطا:', error);
  });
}

sendLinkToWebsite(currentURL);
var currentURL = window.location.href;

async function sendLinkToWebsite(link) {
  try {
    const csrfToken = await getCSRFToken();
    const url = 'http://127.0.0.1:8000/giveme/';
    const data = {
      link: link
    };

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(data)
    });

    console.log('CSRF Token:', csrfToken);
    console.log('پاسخ دریافتی:', response);
  } catch (error) {
    console.error('خطا:', error);
  }
}

async function getCSRFToken() {
  try {
    const response = await fetch('http://localhost:8000/csrf/', {
      method: 'GET',
    });
    const data = await response.json();
    const csrfToken = data.csrf_token;
    return csrfToken;
  } catch (error) {
    console.error('خطا در دریافت CSRF Token:', error);
  }
}

sendLinkToWebsite(currentURL);
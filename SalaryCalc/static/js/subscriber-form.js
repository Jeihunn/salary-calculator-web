let subscribeForm = document.getElementById("subscribe-form");

subscribeForm.addEventListener("submit", async function (event) {
  event.preventDefault();
  let email = document.getElementById("subscribe-email").value;

  try {
    const response = await fetch(`${location.origin}/api/subscriber/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": subscribeForm.csrfmiddlewaretoken.value,
      },
      body: JSON.stringify({
        email: email,
      }),
    });

    if (response.ok) {
      subscribeForm.innerHTML = `<h5 class="text-white">Əla! Artıq bizə abunə oldunuz.</h4>`;
    } else {
      const data = await response.json();
      let errorList = subscribeForm.querySelector(".errorlist");

      let html = "";
      for (let [key, value] of Object.entries(data)) {
        html += `<li class="error">${value}</li>`;
      }
      errorList.innerHTML = html;
    }
  } catch (error) {
    console.error("Error:", error);
  }
});
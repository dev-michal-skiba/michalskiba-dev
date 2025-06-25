function clearLoggingError() {
  document.getElementById("wpt-login-error").innerText = "";
}

function setLoggingError() {
  document.getElementById("wpt-login-error").innerText = "Wrong credentials";
}

function submit(event) {
  event.preventDefault();
  login();
}

function login() {
  clearLoggingError();
  const username = document.getElementById("wpt-username").value;
  const password = document.getElementById("wpt-password").value;
  window.setButtonLoading("wpt-login-button", "wpt-login-button-text");
  window
    .callApi({
      method: "POST",
      path: "/demo/auth/login",
      body: {
        username: username,
        password: password,
      },
      credentials: "include",
    })
    .then((response) => {
      if (response.status === 200) {
        localStorage.setItem("wptIsLoggedIn", "true");
        localStorage.setItem("wptUsername", username);
        loadPage();
      } else {
        setLoggingError();
        window.unsetButtonLoading(
          "wpt-login-button",
          "wpt-login-button-text",
          "Log In",
        );
      }
    })
    .catch(() => {
      setLoggingError();
      window.unsetButtonLoading(
        "wpt-login-button",
        "wpt-login-button-text",
        "Log In",
      );
    });
}

function logout() {
  window.setButtonLoading("wpt-logout-button", "wpt-logout-button-text");
  window
    .callApi({
      method: "POST",
      path: "/demo/auth/logout",
      credentials: "include",
    })
    .then((response) => {
      if (response.status === 200) {
        localStorage.setItem("wptIsLoggedIn", "false");
        localStorage.removeItem("wptUsername");
        loadPage();
      }
    })
    .catch(() => {
      window.unsetButtonLoading(
        "wpt-logout-button",
        "wpt-logout-button-text",
        "logout",
      );
    });
}

function clearLogoutButton() {
  const button = document.getElementById("wpt-logout-button");
  if (button) {
    button.parentNode.removeChild(button);
  }
}

function displayLogoutButton() {
  let button = document.createElement("button");
  button.id = "wpt-logout-button";
  button.className = "nav-link link-button secondary-color";
  let span = document.createElement("span");
  span.id = "wpt-logout-button-text";
  span.innerText = "logout";
  button.appendChild(span);
  button.addEventListener("click", logout);
  document.getElementById("wpt-logout-container").appendChild(button);
}

function displayPressApplication(pressApplication) {
  let container = document.getElementById("wpt-press-container");
  let header = document.createElement("h2");
  header.innerText = "Accreditation info";
  container.append(header);
  if (pressApplication.accreditation_code) {
    let status = document.createElement("p");
    let statusText = document.createTextNode("Status: ");
    let statusSpan = document.createElement("span");
    statusSpan.className = "success";
    statusSpan.innerText = "Accepted";
    status.appendChild(statusText);
    status.appendChild(statusSpan);
    container.append(status);

    let accreditation_code = document.createElement("p");
    let codeText = document.createTextNode("Accreditation code: ");
    let codeBold = document.createElement("b");
    codeBold.innerText = pressApplication.accreditation_code;
    accreditation_code.appendChild(codeText);
    accreditation_code.appendChild(codeBold);
    container.append(accreditation_code);
  } else {
    let status = document.createElement("p");
    let statusText = document.createTextNode("Status: ");
    let statusSpan = document.createElement("span");
    statusSpan.className = "warning";
    statusSpan.innerText = "Waiting for approval";
    status.appendChild(statusText);
    status.appendChild(statusSpan);
    container.append(status);
  }
  let organization = document.createElement("p");
  organization.innerText = "Organization: " + pressApplication.organization;
  container.append(organization);
}

function displayPressApplicationPage(pressApplication) {
  clearPage();
  displayLogoutButton();
  displayPressApplication(pressApplication);
}

function displayLoginPage() {
  clearPage();
  let container = document.getElementById("wpt-press-container");
  if (!container) {
    return;
  }

  let formWrapper = document.createElement("div");
  formWrapper.className = "row";
  
  let formCol = document.createElement("div");
  formCol.className = "col-12";

  let h2 = document.createElement("h2");
  h2.innerText = "Log in to WPT press portal";
  formCol.appendChild(h2);
  
  let form = document.createElement("form");
  form.id = "wpt-login-form";

  let row_1 = document.createElement("div");
  row_1.className = "row mt-5";
  let col_1 = document.createElement("div");
  col_1.className = "col-4";
  let div_1 = document.createElement("div");
  div_1.className = "mb-3";
  let input_1 = document.createElement("input");
  input_1.type = "text";
  input_1.className = "form-control";
  input_1.id = "wpt-username";
  input_1.name = "username";
  input_1.placeholder = "Username";
  div_1.appendChild(input_1);
  col_1.appendChild(div_1);
  row_1.appendChild(col_1);
  
  let row_2 = document.createElement("div");
  row_2.className = "row";
  let col_2 = document.createElement("div");
  col_2.className = "col-4";
  let div_2 = document.createElement("div");
  div_2.className = "mb-3";
  let input_2 = document.createElement("input");
  input_2.type = "password";
  input_2.className = "form-control";
  input_2.id = "wpt-password";
  input_2.name = "password";
  input_2.placeholder = "Password";
  div_2.appendChild(input_2);
  col_2.appendChild(div_2);
  row_2.appendChild(col_2);
  
  let row_error = document.createElement("div");
  row_error.className = "row";
  let col_error = document.createElement("div");
  col_error.className = "col-12";
  let p_error = document.createElement("p");
  p_error.id = "wpt-login-error";
  p_error.className = "error";
  col_error.appendChild(p_error);
  row_error.appendChild(col_error);
  
  let row_3 = document.createElement("div");
  row_3.className = "row";
  let col_3 = document.createElement("div");
  col_3.className = "col-4";
  let button_3 = document.createElement("button");
  button_3.type = "submit";
  button_3.className = "btn primary-button";
  button_3.id = "wpt-login-button";
  let span_3 = document.createElement("span");
  span_3.id = "wpt-login-button-text";
  span_3.innerText = "Log In";
  button_3.appendChild(span_3);
  col_3.appendChild(button_3);
  row_3.appendChild(col_3);
  
  form.appendChild(row_1);
  form.appendChild(row_2);
  form.appendChild(row_error);
  form.appendChild(row_3);
  form.addEventListener("submit", submit);

  // Assemble the centered structure
  formCol.appendChild(form);
  formWrapper.appendChild(formCol);
  container.appendChild(formWrapper);
}

function clearPage() {
  window.unsetContainerLoading("wpt-press-container");
  clearLogoutButton();
  const container = document.getElementById("wpt-press-container");
  if (container) {
    container.innerText = "";
  }
}

function loadPage() {
  clearPage();
  window.setContainerLoading("wpt-press-container");
  let queryParams = {};
  if (localStorage.getItem("wptIsLoggedIn") === "true") {
    if (!window.getIsSecureVersionOn()) {
      const username = localStorage.getItem("wptUsername");
      queryParams["username"] = username;
    }
    window
      .callApi({
        method: "GET",
        path: "/demo/web-parameter-tampering/press-application",
        queryParams: queryParams,
        credentials: "include",
      })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => displayPressApplicationPage(data))
      .catch(() => displayLoginPage());
  } else {
    displayLoginPage();
  }
}

window.onload = function () {
  document.getElementById("version-switch").checked =
    window.getIsSecureVersionOn();
  loadPage();
};

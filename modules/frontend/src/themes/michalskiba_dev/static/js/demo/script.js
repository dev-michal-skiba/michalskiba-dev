function setIsSecureVersionOn(value) {
  localStorage.setItem("is_secure_version_on", value);
}

function getIsSecureVersionOn() {
  const is_secure_version_on = localStorage.getItem("is_secure_version_on");
  if (is_secure_version_on == null) {
    setIsSecureVersionOn("true");
    return true;
  }
  return is_secure_version_on.toLowerCase() !== "false";
}

function versionSwitchClick() {
  let is_secure_version_on = getIsSecureVersionOn();
  setIsSecureVersionOn(!is_secure_version_on);
  window.location.reload();
}

function customEncodeURI(value) {
  return encodeURIComponent(value).replace(/-/g, "%2D");
}

function getQueryParamsString(queryParams) {
  queryParams["is_secure_version_on"] = getIsSecureVersionOn();
  const queryParamsString = Object.entries(queryParams)
    .map(([key, value]) => `${key}=${customEncodeURI(value)}`)
    .join("&");
  if (queryParamsString.length > 0) {
    return "?" + queryParamsString;
  }
  return "";
}

async function callApi({
  method,
  path,
  queryParams = {},
  body = null,
  credentials = "same-origin",
} = {}) {
  if (body != null) {
    body = JSON.stringify(body);
  }
  const options = {
    method: method,
    headers: {
      "Content-Type": "application/json",
      "x-api-key": localStorage.getItem("apiKey") || "",
    },
    body,
    credentials,
  };
  return await fetch(
    "/api" + path + getQueryParamsString(queryParams),
    options,
  );
}

function setLoading(buttonId, spanId) {
  const button = document.getElementById(buttonId);
  if (!button.dataset.originalWidth) {
    button.dataset.originalWidth = button.offsetWidth + "px";
  }
  button.disabled = true;
  button.style.width = button.dataset.originalWidth;
  const span = document.getElementById(spanId);
  const spinner = document.createElement("span");
  spinner.className = "spinner-border spinner-border-sm";
  spinner.setAttribute("role", "status");
  spinner.setAttribute("aria-hidden", "true");
  span.textContent = "";
  span.appendChild(spinner);
}

function unsetLoading(buttonId, spanId, originalText) {
  const button = document.getElementById(buttonId);
  button.disabled = false;
  button.style.width = "";
  const span = document.getElementById(spanId);
  span.innerText = originalText;
}

window.versionSwitchClick = versionSwitchClick;
window.getIsSecureVersionOn = getIsSecureVersionOn;
window.callApi = callApi;
window.setLoading = setLoading;
window.unsetLoading = unsetLoading;

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
    queryParams['is_secure_version_on'] = getIsSecureVersionOn();
    const queryParamsString = Object.entries(queryParams).map(([key, value]) => `${key}=${customEncodeURI(value)}`).join('&');
    if (queryParamsString.length > 0) {
        return '?' + queryParamsString;
    }
    return '';
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
            'Content-Type': 'application/json',
        },
        body,
        credentials,
    };

    return await fetch(
        window.HUGO_API_URL + path + getQueryParamsString(queryParams),
        options,
    );
}

window.versionSwitchClick = versionSwitchClick;
window.getIsSecureVersionOn = getIsSecureVersionOn;
window.callApi = callApi;

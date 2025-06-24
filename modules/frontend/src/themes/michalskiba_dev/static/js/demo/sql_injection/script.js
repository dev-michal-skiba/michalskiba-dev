function setAddressSearchPhrase(value) {
  localStorage.setItem("sql_injection_address_search_phrase", value);
}

function getAddressSearchPhrase() {
  const addressSearchPhrase = localStorage.getItem(
    "sql_injection_address_search_phrase",
  );
  if (addressSearchPhrase == null) {
    setAddressSearchPhrase("");
    return "";
  }
  return addressSearchPhrase;
}

function renderParcelStores(parcelStores) {
  if (parcelStores.length === 0) {
    setNoResults();
    return;
  }
  const parentContainer = document.getElementById("parent-container");
  const container = document.createElement("div");
  parcelStores.forEach((store) => {
    const tile = document.createElement("div");
    tile.classList.add("sql-injection-parcel-store-tile");
    const nameParagraph = document.createElement("p");
    const nameB = document.createElement("b");
    nameB.innerText = "Name: ";
    nameParagraph.appendChild(nameB);
    nameParagraph.appendChild(document.createTextNode(store.name));

    const addressParagraph = document.createElement("p");
    const addressB = document.createElement("b");
    addressB.innerText = "Address: ";
    addressParagraph.appendChild(addressB);
    addressParagraph.appendChild(document.createTextNode(store.address));

    const openingHoursParagraph = document.createElement("p");
    const hoursB = document.createElement("b");
    hoursB.innerText = "Opening hours: ";
    openingHoursParagraph.appendChild(hoursB);
    openingHoursParagraph.appendChild(
      document.createTextNode(store.opening_hours),
    );
    tile.appendChild(nameParagraph);
    tile.appendChild(addressParagraph);
    tile.appendChild(openingHoursParagraph);
    container.appendChild(tile);
  });
  parentContainer.innerText = "";
  parentContainer.appendChild(container);
}

function clearParentContainer() {
  const parentContainer = document.getElementById("parent-container");
  parentContainer.innerText = "";
}

function setNoResults() {
  const parentContainer = document.getElementById("parent-container");
  parentContainer.innerText = "No parcel stores found";
}

function setClearLoading() {
  window.setButtonLoading("clear-button", "clear-button-text");
  clearParentContainer();
}

function setSearchLoading() {
  window.setButtonLoading("submit-button", "submit-button-text");
  clearParentContainer();
}

function sqliUnsetLoading() {
  window.unsetButtonLoading("submit-button", "submit-button-text", "Search");
  window.unsetButtonLoading("clear-button", "clear-button-text", "Clear");
}

function submitForm(isClear = false) {
  if (isClear) {
    setClearLoading();
  } else {
    setSearchLoading();
  }
  window
    .callApi({
      method: "GET",
      path: "/demo/sql-injection/parcel-stores",
      queryParams: {
        address_search_phrase: getAddressSearchPhrase(),
      },
    })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      renderParcelStores(data.parcel_stores);
      sqliUnsetLoading();
    })
    .catch((error) => {
      console.debug(error);
      sqliUnsetLoading();
      setNoResults();
    });
}

// Add listener to store info in local storage about search text
document
  .getElementById("address-search-phrase")
  .addEventListener("change", (event) => {
    setAddressSearchPhrase(event.target.value);
  });

// Add listener to clear info in local storage about search text
document.getElementById("clear-button").addEventListener("click", () => {
  setAddressSearchPhrase("");
  document.getElementById("address-search-phrase").value = "";
  submitForm(true);
});

// Add listener to correctly submit form
document
  .getElementById("parcel-store-search-form")
  .addEventListener("submit", (event) => {
    event.preventDefault();
    submitForm();
  });

// Add listener to call API for parcel stores
document.getElementById("submit-button").addEventListener("click", function () {
  submitForm();
});

window.onload = function () {
  document.getElementById("version-switch").checked =
    window.getIsSecureVersionOn();
  document.getElementById("address-search-phrase").value =
    getAddressSearchPhrase();
  submitForm();
};

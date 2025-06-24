function getValidatedEmail() {
  const email = document.getElementById("email").value;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (emailRegex.test(email)) {
    return email;
  }
  return null;
}

function clearError() {
  document.getElementById("error-message").innerText = "";
}

function showError(message) {
  document.getElementById("error-message").innerText = message;
}

function updateModalAndShow(email, resetLink) {
  const modalEmail = document.getElementById("email-email");
  modalEmail.innerText = email;

  const modalLink = document.getElementById("reset-link");
  modalLink.href = resetLink;

  const emailModal = new bootstrap.Modal(
    document.getElementById("email-modal"),
  );
  emailModal.show();
}

function submitForm() {
  clearError();
  const email = getValidatedEmail();
  if (email === null) {
    showError("Please enter a valid email address");
    return;
  }
  window.setLoading(
    "submit-password-reset-initiate-button",
    "submit-password-reset-initiate-button-text",
  );
  window
    .callApi({
      method: "POST",
      path: "/demo/host-header-injection/password-reset/initiate",
      body: { email },
    })
    .then((response) => response.json())
    .then((data) => {
      updateModalAndShow(email, data.reset_link);
      window.unsetLoading(
        "submit-password-reset-initiate-button",
        "submit-password-reset-initiate-button-text",
        "Reset Password",
      );
    });
}

function submitNewPassword() {
  clearError();
  const token = new URLSearchParams(window.location.search).get("token");
  const password = document.getElementById("new-password").value;
  if (!password) {
    showError("Please enter a new password");
    return;
  }
  window.setLoading(
    "submit-password-reset-button",
    "submit-password-reset-button-text",
  );
  window
    .callApi({
      method: "POST",
      path: "/demo/host-header-injection/password-reset/complete",
      body: { token, password },
    })
    .then((response) => {
      if (response.status !== 204) {
        throw new Error("Failed to reset password, please try again.");
      }
      window.location.href =
        "/demo/host-header-injection/password-reset/success";
    })
    .catch((error) => {
      showError(error.message);
      window.unsetLoading(
        "submit-password-reset-button",
        "submit-password-reset-button-text",
        "Reset Password",
      );
    });
}

window.onload = function () {
  document.getElementById("version-switch").checked =
    window.getIsSecureVersionOn();

  const passwordResetInitiateForm = document.getElementById(
    "password-reset-initiate-form",
  );
  if (passwordResetInitiateForm) {
    passwordResetInitiateForm.addEventListener("submit", (event) => {
      event.preventDefault();
      submitForm();
    });
  }

  const submitPasswordResetInitiateButton = document.getElementById(
    "submit-password-reset-initiate-button",
  );
  if (submitPasswordResetInitiateButton) {
    submitPasswordResetInitiateButton.addEventListener("click", submitForm);
  }

  const passwordResetForm = document.getElementById("password-reset-form");
  if (passwordResetForm) {
    passwordResetForm.addEventListener("submit", (event) => {
      event.preventDefault();
      submitForm();
    });
  }

  const submitPasswordResetButton = document.getElementById(
    "submit-password-reset-button",
  );
  if (submitPasswordResetButton) {
    submitPasswordResetButton.addEventListener("click", submitNewPassword);
  }
};

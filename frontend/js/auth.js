// REGISTER
const registerForm = document.getElementById("registerForm");

if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(registerForm));

    const res = await apiRequest("/user/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (res.ok) {
      alert("Başarılı kayıt");
      window.location.href = "register.html";
    } else {
      alert("Kayıt hatası");
    }
  });
}

// LOGIN
const loginForm = document.getElementById("loginForm");

if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(loginForm);

    const res = await apiRequest("/user/login", {
      method: "POST",
      body: formData, 
    });

    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("token", data.access_token);
      window.location.href = "index.html";
    } else {
      alert("Yanlış giriş veya şifre");
    }
  });
}
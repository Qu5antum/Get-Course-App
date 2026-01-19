document.getElementById("courseForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");
    if (!token) {
        alert("Oturum açmanız gerekiyor!");
        return;
    }

    const formData = new FormData(e.target);

    const title = formData.get("title");
    const description = formData.get("description");
    const imageUrl = formData.get("image_url");

    const messageDiv = document.getElementById("message");

    try {
        const params = new URLSearchParams({
            title,
            description
        });

        if (imageUrl) {
            params.append("image_url", imageUrl);
        }

        const res = await fetch(
            `http://127.0.0.1:8000/new_course/courses?${params.toString()}`,
            {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await res.json();

        if (res.ok) {
            messageDiv.style.color = "green";
            messageDiv.innerText = "Kurs başarıyla oluşturuldu.";
            e.target.reset();
        } else {
            messageDiv.style.color = "red";
            messageDiv.innerText = data.detail || "Kurs oluşturulurken hata oluştu.";
        }

    } catch (err) {
        console.error(err);
        messageDiv.style.color = "red";
        messageDiv.innerText = "Sunucu bağlantı hatası";
    }
});

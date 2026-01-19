const API_URL = "http://127.0.0.1:8000";
const token = localStorage.getItem("token");

const coursesEl = document.getElementById("courses");
const errorEl = document.getElementById("error");

if (!token) {
    errorEl.innerText = "Giriş yapmadınız.";
    throw new Error("No token");
}

async function loadMyCourses() {
    try {
        const res = await fetch(`${API_URL}/courses/user_courses`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!res.ok) {
            const err = await res.json();
            errorEl.innerText = err.detail || "Kurslar yüklenirken hata oluştu.";
            return;
        }

        const courses = await res.json();

        if (courses.length === 0) {
            coursesEl.innerHTML = "<p>Henüz hiçbir kursa kayıtlı değilsiniz.</p>";
            return;
        }

        coursesEl.innerHTML = "";

        for (const course of courses) {
            const progress = await loadProgress(course.id);

            const card = document.createElement("div");
            card.className = "course-card";

            card.innerHTML = `
                <h2>${course.title}</h2>
                <p>${course.description || ""}</p>

                <div class="progress-bar">
                    <div class="progress" style="width: ${progress.percent}%"></div>
                </div>
                <span class="progress-text">
                    Kurs ilerlemesi: ${progress.percent}%
                </span>

                <button onclick="openCourse(${course.id})">
                    Kursa git
                </button>
            `;

            coursesEl.appendChild(card);
        }

    } catch (err) {
        console.error(err);
        errorEl.innerText = "Sunucu bağlantı hatası";
    }
}

async function loadProgress(courseId) {
    try {
        const res = await fetch(
            `${API_URL}/course/${courseId}/complete`,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!res.ok) return { percent: 0 };

        return await res.json(); 
        // ожидаем: { percent: 65 } или аналог

    } catch {
        return { percent: 0 };
    }
}

function openCourse(courseId) {
    window.location.href = `enroll.html?id=${courseId}`;
}

loadMyCourses();

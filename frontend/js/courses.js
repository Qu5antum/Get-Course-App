const API_URL = "http://127.0.0.1:8000";

function handleSearch() {
    const value = document.getElementById("searchInput").value;
    loadCourses(value);
}

async function loadCourses(title = "") {
    try {
        const response = await fetch(
            `${API_URL}/courses/search?title=${encodeURIComponent(title)}`
        );

        if (!response.ok) {
            throw new Error("Kurslar yüklenirken hata oluştu");
        }

        const courses = await response.json();

        const container = document.getElementById("courses");
        container.innerHTML = "";

        if (courses.length === 0) {
            container.innerHTML = "<p>Hiçbir kurs bulunamadı</p>";
            return;
        }

        courses.forEach(course => {
            const card = document.createElement("div");
            card.className = "course-card";

            card.innerHTML = `
                <div class="course-title">${course.title}</div>
                <div class="course-author">${course.author_name}</div>

                <div class="course-footer">
                    <span>📘 ${course.lessons_count} dersler</span>
                    <button class="btn" onclick="openCourse(${course.id})">
                        Kursa kaydol
                    </button>
                </div>
            `;

            container.appendChild(card);
        });

    } catch (error) {
        console.error(error);
        document.getElementById("courses").innerHTML =
            "<p>Kurslar yüklenirken hata oluştu</p>";
    }
}

function openCourse(courseId) {
    // переход на страницу курса с id в query-параметре
    console.log("Open course:", courseId);
    window.location.href = `enroll.html?id=${courseId}`;
}


loadCourses();

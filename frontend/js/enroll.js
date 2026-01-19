const API_URL = "http://127.0.0.1:8000";

const params = new URLSearchParams(window.location.search);
const courseId = params.get("id");

const titleEl = document.getElementById("courseTitle");
const descEl = document.getElementById("courseDescription");
const sectionsEl = document.getElementById("sections");
const errorEl = document.getElementById("error");

const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY4ODM2NjE5fQ.tDHKL2JGX0JIBAhn2vovKpVXD6iiST9fftXjqA4r_lE"

if (!courseId) {
    errorEl.innerText = "Kurs ID belirtilmemiş.";
    throw new Error("courseId missing");
}

async function loadCourse() {
    if (!token) {
        errorEl.innerText = "Giriş yapmadınız.";
        return;
    }

    try {
        const response = await fetch(`${API_URL}/courses/${courseId}`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const error = await response.json();
            errorEl.innerText = error.detail || "Kurs yüklenirken hata oluştu.";
            return;
        }

        const course = await response.json();

        errorEl.innerText = "";
        titleEl.innerText = course.title;
        descEl.innerText = course.description;

        renderSections(course.sections);

    } catch (err) {
        console.error(err);
        errorEl.innerText = "Sunucu bağlantı hatası";
    }
}



function renderSections(sections) {
    sectionsEl.innerHTML = "";

    if (!sections || sections.length === 0) {
        sectionsEl.innerHTML = "<p>Kursun henüz hiçbir bölümü yok.</p>";
        return;
    }

    sections.forEach(section => {
        const sectionDiv = document.createElement("div");
        sectionDiv.className = "section";

        sectionDiv.innerHTML = `
            <h2>${section.title}</h2>
            <ul class="lessons"></ul>
        `;
        sectionsEl.appendChild(sectionDiv);
    });
}


function goBack() {
    window.history.back();
}

loadCourse();


function loadStudentDetails(studentId) {
    fetch(`/students/${studentId}`)
        .then(res => res.json())
        .then(data => {
            let content = `
                <h4>${data.name}</h4>
                <p><strong>Email :</strong> ${data.email}</p>
                <p><strong>Crédits :</strong> ${data.credits}</p>
                
            <h5 class="mt-4">Abonnements</h5>
            <ul class="list-group mb-3">
                ${data.subscriptions
                    .sort((a, b) => new Date(a.start) - new Date(b.start))
                    .map(sub => `
                        <li class="list-group-item ${sub.active ? '' : 'text-muted'}">
                            ${sub.start} → ${sub.end} — ${sub.weekly_limit} cours/semaine
                            ${sub.active
                                ? '<span class="badge bg-success ms-2">Actif</span>'
                                : '<span class="badge bg-secondary ms-2">Non Actif</span>'}
                        </li>
                    `).join('')}
            </ul>


                <h5 class="mt-4">Cours par état</h5>
            `;

            for (let state in data.registrations) {
                content += `<h6 class="mt-3">${state}</h6><ul class="list-group">`;
                for (let reg of data.registrations[state]) {
                    content += `<li class="list-group-item">
                        ${reg.course_name} — ${reg.date} avec ${reg.teacher}
                    </li>`;
                }
                content += `</ul>`;
            }

            content += `
                <div class="mt-5">
                    <h5>Ajouter un pack de crédits</h5>
                    <div class="d-flex gap-2">
                        <button class="btn btn-outline-success credit-btn" data-value="10" data-id="${studentId}">+10 crédits</button>
                        <button class="btn btn-outline-success credit-btn" data-value="20" data-id="${studentId}">+20 crédits</button>
                        <button class="btn btn-outline-success credit-btn" data-value="40" data-id="${studentId}">+40 crédits</button>
                    </div>

                    <h5 class="mt-4">Ajouter un abonnement</h5>
                  <form id="subscriptionForm" class="row g-3 align-items-end" data-id="${studentId}">
                    <div class="col-md-3">
                        <label class="form-label">Début</label>
                        <input type="date" class="form-control" name="start_date" required>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">Durée (mois)</label>
                        <input type="number" class="form-control" name="months" min="1" value="1" required>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">Cours / semaine</label>
                        <select name="weekly_limit" class="form-select" required>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                        </select>
                    </div>
                    <div class="col-md-3 d-grid">
                        <button type="submit" class="btn btn-outline-success">Ajouter</button>
                    </div>
                </form>

                </div>
            `;

            document.getElementById("studentModalContent").innerHTML = content;

            const modalEl = document.getElementById("studentModal");
            const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
            if (!modalEl.classList.contains("show")) {
                modal.show();
            }
        });
}

// Clic sur "Voir détails"
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('view-details-btn')) {
        const studentId = e.target.dataset.studentId;
        loadStudentDetails(studentId);
    }
});

// Ajouter crédits
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('credit-btn')) {
        const value = e.target.dataset.value;
        const studentId = e.target.dataset.id;

        fetch(`/students/${studentId}/add_credits`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({amount: value})
        })
        .then(res => res.json())
        .then(() => {
            loadStudentDetails(studentId);
        });
    }
});

// Ajouter abonnement
document.addEventListener('submit', function (e) {
    if (e.target.id === "subscriptionForm") {
        e.preventDefault();
        const form = e.target;
        const studentId = form.dataset.id;

        const data = {
            start_date: form.start_date.value,
            months: form.months.value,
            weekly_limit: form.weekly_limit.value
        };

        fetch(`/students/${studentId}/add_subscription`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(() => {
            loadStudentDetails(studentId);
        });
    }
});

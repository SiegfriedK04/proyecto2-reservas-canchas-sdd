(() => {
    const app = document.getElementById("booking-app");
    if (!app) return;

    const grid = document.getElementById("calendar-grid");
    const monthLabel = document.getElementById("month-label");
    const dateLabel = document.getElementById("selected-date-label");
    const slotGrid = document.getElementById("slot-grid");
    const slotState = document.getElementById("slot-state");
    const summaryDate = document.getElementById("summary-date");
    const summaryTime = document.getElementById("summary-time");
    const feedback = document.getElementById("booking-feedback");
    const confirmButton = document.getElementById("confirm-booking");
    const previousButton = document.getElementById("previous-month");
    const nextButton = document.getElementById("next-month");

    const months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
    const longDate = new Intl.DateTimeFormat("es-PA", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
    const shortTime = new Intl.DateTimeFormat("es-PA", { hour: "numeric", minute: "2-digit", hour12: true });
    const today = startOfDay(new Date());
    let selectedDate = parseLocalDate(app.dataset.initialDate);
    let currentMonth = new Date(selectedDate.getFullYear(), selectedDate.getMonth(), 1);
    let selectedSlot = null;

    function startOfDay(value) {
        return new Date(value.getFullYear(), value.getMonth(), value.getDate());
    }

    function parseLocalDate(value) {
        const [year, month, day] = value.split("-").map(Number);
        return new Date(year, month - 1, day);
    }

    function dateKey(value) {
        const year = value.getFullYear();
        const month = String(value.getMonth() + 1).padStart(2, "0");
        const day = String(value.getDate()).padStart(2, "0");
        return `${year}-${month}-${day}`;
    }

    function sameDay(first, second) {
        return dateKey(first) === dateKey(second);
    }

    function setFeedback(message = "", type = "") {
        feedback.textContent = message;
        feedback.className = "booking-feedback";
        if (message) feedback.classList.add("visible", type);
    }

    function renderCalendar() {
        grid.innerHTML = "";
        monthLabel.textContent = `${months[currentMonth.getMonth()]} ${currentMonth.getFullYear()}`;
        const firstWeekday = currentMonth.getDay();
        const daysInMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 0).getDate();
        const previousMonthDays = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), 0).getDate();

        for (let index = 0; index < 42; index += 1) {
            const dayNumber = index - firstWeekday + 1;
            let value;
            let otherMonth = false;
            if (dayNumber < 1) {
                value = new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1, previousMonthDays + dayNumber);
                otherMonth = true;
            } else if (dayNumber > daysInMonth) {
                value = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, dayNumber - daysInMonth);
                otherMonth = true;
            } else {
                value = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), dayNumber);
            }

            const button = document.createElement("button");
            button.type = "button";
            button.className = "calendar-day";
            button.textContent = String(value.getDate());
            button.setAttribute("role", "gridcell");
            button.setAttribute("aria-label", longDate.format(value));
            if (otherMonth) button.classList.add("other-month");
            if (value < today) button.disabled = true;
            else button.classList.add("available");
            if (sameDay(value, selectedDate)) button.classList.add("selected");
            button.addEventListener("click", () => selectDate(value));
            grid.appendChild(button);
        }

        previousButton.disabled = currentMonth.getFullYear() === today.getFullYear() && currentMonth.getMonth() === today.getMonth();
    }

    function selectDate(value) {
        selectedDate = startOfDay(value);
        currentMonth = new Date(value.getFullYear(), value.getMonth(), 1);
        selectedSlot = null;
        setFeedback();
        summaryDate.textContent = capitalize(longDate.format(selectedDate));
        summaryTime.textContent = "Sin seleccionar";
        if (confirmButton) confirmButton.disabled = true;
        renderCalendar();
        loadSlots();
    }

    function capitalize(value) {
        return value.charAt(0).toUpperCase() + value.slice(1);
    }

    async function loadSlots() {
        slotGrid.innerHTML = "";
        slotState.hidden = false;
        slotState.className = "slot-state loading";
        slotState.textContent = "Consultando disponibilidad…";
        dateLabel.textContent = capitalize(longDate.format(selectedDate));
        try {
            const response = await fetch(`${app.dataset.availabilityUrl}?date=${dateKey(selectedDate)}`, { headers: { Accept: "application/json" } });
            const payload = await response.json();
            if (!response.ok) throw new Error(payload.error || "No fue posible consultar los horarios.");
            slotState.className = "slot-state";
            const occupied = payload.occupied_slots || [];
            const schedule = [
                ...payload.slots.map((slot) => ({ ...slot, available: true })),
                ...occupied.map((slot) => ({ ...slot, available: false })),
            ].sort((first, second) => new Date(first.start) - new Date(second.start));
            if (!schedule.length) {
                slotState.textContent = "No quedan horarios disponibles para este día.";
                return;
            }
            if (payload.slots.length) slotState.hidden = true;
            else slotState.textContent = "Todos los horarios de este día están ocupados. Prueba con otra fecha.";
            schedule.forEach((slot) => {
                const button = document.createElement("button");
                button.type = "button";
                button.className = "slot-button";
                button.textContent = slot.label;
                if (slot.available) {
                    button.setAttribute("aria-pressed", "false");
                    button.addEventListener("click", () => selectSlot(slot, button));
                } else {
                    button.disabled = true;
                    button.classList.add("slot-occupied");
                    button.setAttribute("aria-label", `${slot.label}, ocupado`);
                    const tag = document.createElement("small");
                    tag.textContent = "Ocupado";
                    button.appendChild(tag);
                }
                slotGrid.appendChild(button);
            });
        } catch (error) {
            slotState.className = "slot-state";
            slotState.textContent = error.message;
        }
    }

    function selectSlot(slot, button) {
        selectedSlot = slot;
        slotGrid.querySelectorAll(".slot-button:not(.slot-occupied)").forEach((item) => {
            item.classList.remove("selected");
            item.setAttribute("aria-pressed", "false");
        });
        button.classList.add("selected");
        button.setAttribute("aria-pressed", "true");
        const start = new Date(slot.start);
        const end = new Date(slot.end);
        summaryTime.textContent = `${shortTime.format(start)} - ${shortTime.format(end)}`;
        if (confirmButton) confirmButton.disabled = false;
        setFeedback();
    }

    function csrfToken() {
        const cookie = document.cookie.split(";").map((item) => item.trim()).find((item) => item.startsWith("csrftoken="));
        return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
    }

    async function confirmBooking() {
        if (!selectedSlot || !confirmButton) return;
        confirmButton.disabled = true;
        confirmButton.textContent = "Confirmando…";
        setFeedback();
        try {
            const response = await fetch(app.dataset.bookingUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken(), Accept: "application/json" },
                body: JSON.stringify({ court_id: Number(app.dataset.courtId), starts_at: selectedSlot.start, ends_at: selectedSlot.end }),
            });
            const payload = await response.json();
            if (!response.ok) {
                const alternatives = (payload.alternatives || []).map((item) => item.label).join(", ");
                const suffix = alternatives ? ` Alternativas: ${alternatives}.` : "";
                throw new Error(`${payload.error || "No fue posible confirmar."}${suffix}`);
            }
            setFeedback("Reserva confirmada. Abriendo tu agenda…", "success");
            window.setTimeout(() => { window.location.href = app.dataset.myBookingsUrl; }, 700);
        } catch (error) {
            setFeedback(error.message, "error");
            confirmButton.disabled = false;
            confirmButton.textContent = "Confirmar reserva";
            loadSlots();
        }
    }

    previousButton.addEventListener("click", () => {
        currentMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1, 1);
        renderCalendar();
    });
    nextButton.addEventListener("click", () => {
        currentMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 1);
        renderCalendar();
    });
    if (confirmButton) confirmButton.addEventListener("click", confirmBooking);

    selectDate(selectedDate);
})();


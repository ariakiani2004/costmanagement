// دکمهٔ نمایش رمز فقط وقتی جاوااسکریپت فعال است اضافه می‌شود.
for (const input of document.querySelectorAll(".field input[type='password']")) {
    const row = document.createElement("div");
    row.className = "password-row";
    input.before(row);
    row.append(input);

    const button = document.createElement("button");
    button.type = "button";
    button.className = "password-toggle";
    button.textContent = "نمایش";
    button.setAttribute("aria-controls", input.id);
    button.addEventListener("click", () => {
        const hidden = input.type === "password";
        input.type = hidden ? "text" : "password";
        button.textContent = hidden ? "پنهان کردن" : "نمایش";
    });
    row.append(button);
}

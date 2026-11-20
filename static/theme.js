// با کلید مشترک، پنل مدیریت جنگو هم انتخاب مرورگر را می‌خواند.
const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");
let themeChoice = "auto";
try {
    themeChoice = localStorage.getItem("theme") || "auto";
} catch {
    // تغییر حالت بدون ذخیره‌سازی هم در صفحهٔ فعلی کار می‌کند.
}

function applyTheme() {
    const dark = themeChoice === "dark" || (themeChoice !== "light" && systemTheme.matches);
    document.documentElement.dataset.theme = dark ? "dark" : "light";
    const button = document.querySelector("[data-theme-toggle]");
    if (button) {
        button.setAttribute("aria-pressed", String(dark));
    }
}

applyTheme();
systemTheme.addEventListener("change", applyTheme);
window.addEventListener("storage", (event) => {
    if (event.key === "theme" || event.key === null) {
        themeChoice = event.newValue || "auto";
        applyTheme();
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("[data-theme-toggle]");
    if (!button) return;

    applyTheme();
    button.hidden = false;
    button.addEventListener("click", () => {
        themeChoice = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
        try {
            localStorage.setItem("theme", themeChoice);
        } catch {
            // وقتی مرورگر ذخیره‌سازی را بسته، انتخاب موقت است.
        }
        applyTheme();
    });
});

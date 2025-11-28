document.addEventListener("DOMContentLoaded", () => {
    const title = document.querySelector("h1");
    const nav = document.querySelector("nav");
    const mainContent = document.querySelector("main");
    const aside = document.querySelector("aside");

    title.textContent = "Belajar Javascript Dasar - Interaksi Pertama!";
    title.addEventListener("click", () => {
        nav.classList.toggle("show-nav");
    });

    document.addEventListener("keydown", (event) => {
        if(event.key === "d")
            documen.body.classList.toggle("dark");
    });

    let count = 0;
    mainContent.addEventListener("click", () => {
        count++;
        aside.textContent = `kamu klik konten ini sebanyak ${count} kali`;
    })

    document.addEventListener('keydown', (event) => {
    if (event.key.toLowerCase() === 'f') {
        document.querySelector('nav').classList.toggle('nav-besar');
    }
    });


});
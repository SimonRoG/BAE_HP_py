document.addEventListener("DOMContentLoaded", function () {
    var videoBackground = document.getElementById("video-background");

    if (document.body.id === "home-page") {
        videoBackground.addEventListener('canplay', function () {
            setupPageTransition();
            videoBackground.addEventListener('canplaythrough', function () {
                videoBackground.play();
            });
        });
    } else {
        setupPageTransition();
    }

    window.addEventListener("scroll", function () {
        if (window.scrollY >= 800) {
            videoBackground.pause();
        } else {
            videoBackground.play();
        }
    });

    window.addEventListener('load', () => {
        const $recaptcha = document.querySelector('#g-recaptcha-response');
        if ($recaptcha) {
            $recaptcha.setAttribute('required', 'required');
        }
    })
});

function openCloseMobileMenu() {
    if (document.getElementById("dropdown").style.display === "none") {
        document.getElementById("dropdown").style.display = "block";
        setTimeout(() => { document.getElementById("dropdown").style.opacity = 1; }, 50);
        var img = document.getElementById("menu-button-img");
        img.src = "/static/Icons/close.svg";
    } else {
        document.getElementById("dropdown").style.opacity = 0;
        setTimeout(() => {
            document.getElementById("dropdown").style.display = "none";
        }, 100);
        var img = document.getElementById("menu-button-img");
        img.src = "/static/Icons/menu.svg";
    }
}

function popup(img) {
    window.open(
        img,
        'window',
        'toolbar=no, location=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=1090px, height=550px, top=25px left=120px'
    );
}

function filterApply() {
    let ort = document.getElementById('ort').value;
    let anstellung = document.getElementById('anstellung').value;
    let taetigkeit = document.getElementById('taetigkeit').value;
    let stellenanzeigen = Array.from(document.getElementsByClassName('stellenanzeige'));

    stellenanzeigen.forEach(stellenanzeige => {
        stellenanzeige.style.display = 'none';
        if (stellenanzeige.classList.contains(ort) &&
            stellenanzeige.classList.contains(anstellung) &&
            stellenanzeige.classList.contains(taetigkeit)) {
            stellenanzeige.style.display = 'grid';
        }
    });
}

function show_more() {
    const projekteArr = document.getElementsByClassName('projekt');
    const showLessButton = document.getElementsByClassName('showless')[0];
    const showMoreButton = document.getElementsByClassName('showmore')[0];
    for (let i = 0; i < projekteArr.length; i++) {
        if (projekteArr[i].style.display === "none") {
            for (let j = i; j < i + 6 && j < projekteArr.length; j++) {
                projekteArr[j].style.display = "block";
                if (j === projekteArr.length - 1)
                    showMoreButton.style.display = "none";
            }
            showLessButton.style.display = "block";
            break;
        }
    }
}

function show_less() {
    const projekteArr = document.getElementsByClassName('projekt');
    const showLessButton = document.getElementsByClassName('showless')[0];
    const showMoreButton = document.getElementsByClassName('showmore')[0];
    for (let i = projekteArr.length - 1; i >= 0; i--) {
        if (projekteArr[i].style.display === "block") {
            for (let j = i; j >= i - (i % 6); j--) {
                projekteArr[j].style.display = "none";
                if (j === 6)
                    showLessButton.style.display = "none";
            }
            showMoreButton.style.display = "block";
            break;
        }
    }
}

function accept_cookie(value) {
    fetch('/set_cookie_consent/' + value, {
        method: 'POST'
    }).then(function () {
        document.getElementById('cookie-banner').style.display = 'none';
    }).then(function () {
        const lang = document.documentElement.lang;
        fetch('/set_language/' + lang, { method: 'POST' });
    });
}

function set_language(lang) {
    fetch('/set_language/' + lang, { method: 'POST' });
}

function destroy(button) {
    const div = button.parentElement;
    div.remove();
}

function scrollPrev() {
    const scroll = document.getElementById("scroll");
    let width = window.getComputedStyle(scroll).width;
    scroll.scrollBy({ left: -(parseFloat(width) + 20) });
}

function scrollNext() {
    const scroll = document.getElementById("scroll");
    let width = window.getComputedStyle(scroll).width;
    scroll.scrollBy({ left: parseFloat(width) + 20 });
}

function scrollToS(Standort, button) {
    document.getElementById(Standort).scrollIntoView({ block: 'center' });
    document.querySelectorAll('.standortbtn').forEach(btn => btn.classList.remove('selected'));
    button.classList.add('selected');
}
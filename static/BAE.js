document.addEventListener("DOMContentLoaded", function () {
    var loadingPage = document.getElementById("loadingPage");
    var loadingLogoContainer = document.getElementById("loadingLogoContainer");
    var startPage = document.getElementById("startPage");
    var videoContainer = document.querySelector(".Hauptseite");
    var videoBackground = document.getElementById("video-background");
    var loadingSpinner = document.getElementById("loadingSpinner");

    function showLogoAndText() {
        if (loadingLogoContainer) {
            loadingLogoContainer.style.opacity = 1;
        }

        setTimeout(function () {
            if (loadingSpinner) {
                loadingSpinner.style.display = "block";
            }
            if (document.body) {
                document.body.classList.remove("loading");
            }
        }, 50);
    }

    showLogoAndText();

    function setupPageTransition() {
        if (loadingSpinner) {
            loadingSpinner.style.display = "none";
        }
        if (loadingPage) {
            loadingPage.style.display = "none";
        }
        if (startPage) {
            startPage.style.display = "none";
        }
        if (videoContainer) {
            videoContainer.style.display = "block";
        }
    }

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

function closeMobileMenu() {
    document.getElementById("mobileMenu").classList.remove('down');
    setTimeout(() => {
        document.getElementById("mobileMenu").style.display = "none";
    }, 700);
}

function openMobileMenu() {
    document.getElementById("mobileMenu").style.display = "block";
    setTimeout(() => {
        document.getElementById("mobileMenu").classList.add('down');
    }, 50);
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
            stellenanzeige.style.display = 'block';
        }
    });
}

function displaySelected() {
    const seiten = document.getElementsByClassName('seite');
    const projekteArr = document.getElementsByClassName('projekt')
    let index;
    for (let i = 0; i < seiten.length; i++)
        if (seiten[i].classList.contains('selected'))
            index = i;

    for (let i = 0; i < projekteArr.length; i++)
        if (i >= index * 10 && i < (index + 1) * 10)
            projekteArr[i].style.display = 'flex';
        else
            projekteArr[i].style.display = 'none';
    window.scrollTo(0, 0);
}

function navigate(index) {
    const seiten = document.getElementsByClassName('seite');
    for (let i = 0; i < seiten.length; i++)
        if (seiten[i].classList.contains('selected'))
            seiten[i].classList.remove('selected');

    const seite = document.getElementById('seite' + index);
    seite.classList.add('selected');
    displaySelected();

}

function prev() {
    const seiten = document.getElementsByClassName('seite');
    for (let i = 0; i < seiten.length; i++)
        if (seiten[i].classList.contains('selected') && i != 0) {
            seiten[i].classList.remove('selected');
            seiten[i - 1].classList.add('selected');
            displaySelected();
            return;
        }
}

function next() {
    const seiten = document.getElementsByClassName('seite');
    for (let i = 0; i < seiten.length; i++)
        if (seiten[i].classList.contains('selected') && i != seiten.length - 1) {
            seiten[i].classList.remove('selected');
            seiten[i + 1].classList.add('selected');
            displaySelected();
            return;
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
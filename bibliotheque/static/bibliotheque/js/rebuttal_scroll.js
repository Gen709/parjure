//https://alvarotrigo.com/blog/css-animations-scroll/
//https://www.joshwcomeau.com/animation/css-transitions/

//https://css-tricks.com/lets-make-one-of-those-fancy-scrolling-animations-used-on-apple-product-pages/

//https://codepen.io/jacob_124/pen/dyydWbB

//https://scroll-out.github.io



function reveal() {
    var menuBottom = document.querySelector(".navbar").getBoundingClientRect().bottom;
    var reveals = document.querySelectorAll(".reveal");
    var l = 91;

    for (var i = 0; i < reveals.length; i++) {
        var windowHeight = window.innerHeight;
        var elementTop = reveals[i].getBoundingClientRect().top;
        var elementBottom = reveals[i].getBoundingClientRect().bottom;
        var elementVisible = 650;

        if(elementTop == l){
            l = l + elementBottom
        };

        if (elementTop < windowHeight - elementVisible) {
            reveals[i].classList.add("active");
            console.log(l, elementTop);
//            console.log('element', i,
//                        'element top',elementTop,
//                        'window height',windowHeight,
//                        'active treshold',windowHeight - elementVisible,
//                        "menu", menuBottom)
        } else {
            reveals[i].classList.remove("active");
//            reveals[i].classList.remove("fixed");
        };
    };
};

window.addEventListener("scroll", reveal);
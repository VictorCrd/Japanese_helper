function set_img_src(speed_of_speach) {
    image = document.getElementById('speed_img');
    if (speed_of_speach < 0.25) {
        image.src = "../static/img/rabbit.jpg";
    } else if (speed_of_speach < 0.5) {
        image.src = "../static/img/inu.jpg";
    } else {
        image.src = "../static/img/turtle.jpg";
    }
}
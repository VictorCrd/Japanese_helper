function set_img_src(speed_of_speach) {
    image = document.getElementById('speed_img');
    if (speed_of_speach < 0.25) {
        image.src = "../static/img/rabbitjpg.jpg";
    } else if (speed_of_speach < 0.5) {
        image.src = "../static/img/inu.png";
    } else {
        image.src = "../static/img/turtlejpg.jpg";
    }
}
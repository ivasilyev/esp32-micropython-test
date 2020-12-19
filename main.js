const ANIMATIONS = ['random_blink', 'cycle2', 'bounce2'];

function validateFormOnSubmit() {
    request_current_state();
    let validations = [];
    let animation = document.getElementById('animation_dropdown').value;
    validations.push(validate_animation(animation, 'animation_dropdown'));

    let colors = {};

    const _arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
    _arr.forEach((n) => {
        let id = `color_${n}`;
        let color = document.getElementById(id);
        if (color !== null) {
            color = color.value;
            validations.push(validateColor(color));
            colors[id] = color;
        }
    });

    if (validations.every((x) => {
        return x
    })) {
        let out = {
            colors: colors,
            animation: animation
        };
        console.log(out);
        localStorage.setItem('animation_data', JSON.stringify(out));
        send_get_query(out);
    }
}

function send_post_query(json) {
    let xhr = new XMLHttpRequest();
    let url = "/";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            json = JSON.parse(xhr.responseText);
        }
    };
    let data = JSON.stringify(json);
    xhr.send(data);
}

function send_get_query(json) {
    let xhr = new XMLHttpRequest();
    let url = "url?data=" + encodeURIComponent(JSON.stringify(json));
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log('send_get_query', xhr.responseText)
            //json = JSON.parse(xhr.responseText);

        }
    };
    xhr.send();
}

function request_current_state() {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/state', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            //let json = JSON.parse(xhr.responseText);
            //console.log(json);
            console.log('request_current_state', xhr.responseText)
        }
    };
    xhr.send();
}

function draw_error(element_id, error_description) {
    document.getElementById(element_id).innerHTML = error_description;
}

function validateColor(hex) {
    return (hex.startsWith('#') && hex.length === 7);
}

function validate_animation(animation_name, element_id) {
    if (!ANIMATIONS.includes(animation_name)) {
        alert('Please choose an animation!');
        draw_error(element_id, 'Please choose an animation!');
        return false;
    }
    return true;
}

class App {
    constructor() {
        this.animation_data = JSON.parse(localStorage.getItem('animation_data'));
    }
}
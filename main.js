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
            let state = JSON.parse(xhr.responseText);
            console.log('send_get_query', state);
            app.setState(state)
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
            let state = JSON.parse(xhr.responseText);
            console.log('request_current_state', state);
            app.setState(state)
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
        //draw_error(element_id, 'Please choose an animation!');
        return false;
    }
    return true;
}

class App {
    DEFAULT_STATE = {animation: "", color_transitions: 10, always_lit: false,
                      colors: {color_0: "#f5647f", color_1: "#7cc4e4"}};
    DEFAULT_COLOR = '#000000';

    constructor() {
        this.state = {};
        this.animation_data = JSON.parse(localStorage.getItem('animation_data'));
        request_current_state();
        if (Object.keys(this.state).length === 0) {
            this.setState(this.DEFAULT_STATE);
        }
    }

    render() {
        let a = this.state.animation;
        if (a.length > 0) {
            document.getElementById('animation_dropdown').value = a;
        }
        Object.keys(this.state.colors).forEach((k) => {
            document.getElementById(k).value = this.state.colors[k];
        });
    }

    setState(state) {
        if (Object.keys(state).length > 0) {
            this.state = state;
            this.render();
        }
    }
    
    makeColorPicker(number) {
        const div = document.getElementById('color_selector');
        div.insertAdjacentHTML('beforeend',
            `<span id="color_picker_${number}"><label for="color_${number}">Color ${number + 1}</label><input type="color" id="color_${number}" name="${number}" value=${this.DEFAULT_COLOR}></span>`);
        this.state.colors[`color_${number}`] = this.DEFAULT_COLOR;
    }
    
    removeColorPicker(number) {
        const span = document.getElementById(`color_picker_${number}`);
        span.remove();
        delete this.state.colors[`color_${number}`];
    }

    getLatestColorNumber() {
        return Object.keys(this.state.colors).map((x) => {
            return (parseInt(x.match('_([0-9]+)$')[1]))
        }).slice(-1)[0];
    }

    pushColorPicker() {
        this.makeColorPicker(this.getLatestColorNumber() + 1);
    }

    popColorPicker() {
        this.removeColorPicker(this.getLatestColorNumber() + 1);
    }
}

const app = new App();
const form = document.querySelector('form');
if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
    });
}
document.getElementById('button__push_color').addEventListener(
    'click', function(e) {
        app.pushColorPicker();
    });

function make_color_field(number) {
    const div = document.getElementById('color_selector');
    div.insertAdjacentHTML('beforeend',
        `<span id="color_picker_${number}"><label for="color_${number}">Color ${number}</label><input type="color" id="color_${number}" name="${number}" value="#000000"></span>`);
}

function remove_color_field(number) {
    const span = document.getElementById(`color_picker_${number}`);
    span.remove();
}
document.getElementById('button__push_color')